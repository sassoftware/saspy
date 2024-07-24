#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import http.client as hc
import base64
import json
import os
import ssl
import sys
import urllib
import warnings
import io
import ssl
import atexit

import secrets
import hashlib
import base64

import tempfile as tf
from time import sleep
from threading import Thread

from saspy.sasexceptions import (SASHTTPauthenticateError,
                                 SASHTTPconnectionError,
                                 SASHTTPsubmissionError,
                                 SASDFNamesToLongError,
                                 SASIOConnectionTerminated
                                )

import logging
logger = logging.getLogger('saspy')

try:
   import pandas as pd
   import numpy  as np
   from warnings import simplefilter
   simplefilter(action="ignore", category=pd.errors.PerformanceWarning) #Ignore the following warning:
   # PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times,
   # which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead.
   # To get a de-fragmented frame, use `newframe = frame.copy()`
   #   df[[col[0] for col in static_columns]] = tuple([col[1] for col in static_columns])
except ImportError:
   pass

import shutil
import datetime
try:
   import pyarrow         as pa
   import pyarrow.compute as pc
   import pyarrow.parquet as pq
except ImportError:
   pa = None
   pass

class SASconfigHTTP:
   '''
   This object is not intended to be used directly. Instantiate a SASsession object instead
   '''
   def __init__(self, session, **kwargs):
      self._kernel   = kwargs.get('kernel', None)
      SAScfg         = session._sb.sascfg.SAScfg
      self.name      = session._sb.sascfg.name
      cfg            = getattr(SAScfg, self.name)

      self._token    = cfg.get('authtoken', None)
      self._refresh  = cfg.get('refreshtoken', None)
      self.url       = cfg.get('url', '')
      self.proxy     = cfg.get('proxy', None)
      self.serverid  = cfg.get('serverid', None)
      self.ip        = cfg.get('ip', '')
      self.port      = cfg.get('port', None)
      self.ctxname   = cfg.get('context', '')
      self.ctx       = {}
      self.options   = cfg.get('options', [])
      self.ssl       = cfg.get('ssl', True)
      self.cafile    = cfg.get('cafile', None)
      self.verify    = cfg.get('verify', None)
      self.timeout   = cfg.get('timeout', None)
      user           = cfg.get('user', '')
      pw             = cfg.get('pw', '')
      client_id      = cfg.get('client_id', None)
      client_secret  = cfg.get('client_secret', '')
      authcode       = cfg.get('authcode', None)
      jwt            = cfg.get('jwt', None)
      self.encoding  = cfg.get('encoding', '')
      self.authkey   = cfg.get('authkey', '')
      self._prompt   = session._sb.sascfg._prompt
      self.lrecl     = cfg.get('lrecl', None)
      self.inactive  = cfg.get('inactive', 120)
      puser          = cfg.get('proxy_user', '')
      ppw            = cfg.get('proxy_pw', '')
      pauthkey       = cfg.get('proxy_authkey', '')
      self.pkce      = cfg.get('pkce', None)

      try:
         self.outopts = getattr(SAScfg, "SAS_output_options")
         self.output  = self.outopts.get('output', 'html5')
      except:
         self.output  = 'html5'

      if self.output.lower() not in ['html', 'html5']:
         logger.warning("Invalid value specified for SAS_output_options. Using the default of HTML5")
         self.output  = 'html5'

      # GET Config options
      try:
         self.cfgopts = getattr(SAScfg, "SAS_config_options")
      except:
         self.cfgopts = {}

      lock = self.cfgopts.get('lock_down', True)
      # in lock down mode, don't allow runtime overrides of option values from the config file.

      self.verbose = self.cfgopts.get('verbose', True)
      self.verbose = kwargs.get('verbose', self.verbose)

      inproxy = kwargs.get('proxy', None)
      if inproxy is not None:
         if lock and len(self.proxy):
            logger.warning("Parameter 'proxy' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.proxy = inproxy

      inurl = kwargs.get('url', None)
      if inurl is not None:
         if lock and len(self.url):
            logger.warning("Parameter 'url' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.url = inurl

      insid = kwargs.get('serverid', None)
      if insid is not None:
         if lock and self.serverid:
            print("Parameter 'serverid' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.serverid = insid

      inip = kwargs.get('ip', None)
      if inip is not None:
         if lock and len(self.ip):
            logger.warning("Parameter 'ip' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.ip = inip

      inport = kwargs.get('port', None)
      if inport is not None:
         if lock and self.port:
            logger.warning("Parameter 'port' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.port = int(inport)

      inctxname = kwargs.get('context', None)
      if inctxname is not None:
         if lock and len(self.ctxname):
            logger.warning("Parameter 'context' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.ctxname = inctxname

      inoptions = kwargs.get('options', None)
      if inoptions is not None:
         if lock and len(self.options):
           logger.warning("Parameter 'options' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.options = inoptions

      intout = kwargs.get('timeout', None)
      if intout is not None:
         if lock and self.timeout:
            logger.warning("Parameter 'timeout' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.timeout = intout

      inencoding = kwargs.get('encoding', 'NoOverride')
      if inencoding != 'NoOverride':
         if lock and len(self.encoding):
            logger.warning("Parameter 'encoding' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.encoding = inencoding
      if not self.encoding or self.encoding != 'utf_8':
         self.encoding = 'utf_8'

      inautht = kwargs.get('authtoken', None)
      if inautht is not None:
         self._token = inautht

      inrefresh = kwargs.get('refreshtoken', None)
      if inrefresh is not None:
         self._refresh = inrefresh

      injwt = kwargs.get('jwt', None)
      if injwt is not None:
         jwt = injwt

      inauthc = kwargs.get('authcode', None)
      if inauthc is not None:
         authcode = inauthc

      incis = kwargs.get('client_secret', None)
      if incis is not None:
         if lock and client_secret:
            logger.warning("Parameter 'client_secret' passed to SAS_session was ignored due to configuration restriction.")
         else:
            client_secret = incis

      incid = kwargs.get('client_id', None)
      if incid is not None:
         if lock and client_id:
            logger.warning("Parameter 'client_id' passed to SAS_session was ignored due to configuration restriction.")
         else:
            client_id = incid
      if client_id is None:
         use_authcode = False
      else:
         use_authcode = True

      inlrecl = kwargs.get('lrecl', None)
      if inlrecl is not None:
         if lock and self.lrecl:
            logger.warning("Parameter 'lrecl' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.lrecl = inlrecl
      if not self.lrecl:
         self.lrecl = 1048576

      inito = kwargs.get('inactive', None)
      if inito is not None:
         if lock and self.inactive:
            logger.warning("Parameter 'inactive' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.inactive = inito

      inak = kwargs.get('authkey', '')
      if len(inak) > 0:
         if lock and len(self.authkey):
            logger.warning("Parameter 'authkey' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.authkey = inak

      inpak = kwargs.get('proxy_authkey', '')
      if len(inpak) > 0:
         if lock and len(pauthkey):
            logger.warning("Parameter 'proxy_authkey' passed to SAS_session was ignored due to configuration restriction.")
         else:
            pauthkey = inpak

      inpuser = kwargs.get('proxy_user', '')
      if len(inpuser) > 0:
         if lock and len(puser):
            logger.warning("Parameter 'proxy_user' passed to SAS_session was ignored due to configuration restriction.")
         else:
            puser = inpuser

      inppw = kwargs.get('proxy_pw', '')
      if len(inppw) > 0:
         if lock and len(ppw):
            logger.warning("Parameter 'proxy_pw' passed to SAS_session was ignored due to configuration restriction.")
         else:
            ppw = inppw

      inssl = kwargs.get('ssl', None)
      if inssl is not None:
         if lock and self.ssl:
            logger.warning("Parameter 'ssl' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.ssl = bool(inssl)

      incaf = kwargs.get('cafile', None)
      if incaf is not None:
         if lock and self.cafile:
            logger.warning("Parameter 'cafile' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.cafile = incaf

      inver = kwargs.get('verify', None)
      if inver is not None:
         if lock and self.verify:
            logger.warning("Parameter 'verify' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.verify = bool(inver)

      inpkce = kwargs.get('pkce', None)
      if inpkce is not None:
         if lock and self.pkce:
            logger.warning("Parameter 'pkce' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.pkce = inpkce
      if self.pkce is None:
         self.pkce = True

      if len(self.url) > 0:
         http = self.url.split('://')
         hp   = http[1].split(':')
         if http[0].lower() in ['http', 'https']:
            self.ip   = hp[0]
            self.port = int(hp[1]) if len(hp) > 1 else self.port
            self.ssl  = True if 's' in http[0].lower() else False
         else:
            logger.warning("Parameter 'url' not in recognized format. Expeting 'http[s]://host[:port]'. Ignoring parameter.")

      while len(self.ip) == 0:
         if not lock:
            self.ip = self._prompt("Please enter the host (ip address) you are trying to connect to: ")
            if self.ip is None:
               self._token = None
               raise RuntimeError("No IP address provided.")
         else:
            logger.fatal("In lockdown mode and missing ip adress in the config named: "+cfgname )
            raise RuntimeError("No IP address provided.")

      if not self.port:
         if self.ssl:
            self.port = 443
         else:
            self.port = 80

      cv = None
      if not self._token and not authcode and not jwt and not self.serverid:
         found = False
         if self.authkey:
            if os.name == 'nt':
               pwf = os.path.expanduser('~')+os.sep+'_authinfo'
            else:
               pwf = os.path.expanduser('~')+os.sep+'.authinfo'
            try:
               fid = open(pwf, mode='r')
               for line in fid:
                  if line.startswith(self.authkey):
                     user = line.partition(' user')[2].lstrip().partition(' ')[0].partition('\n')[0]
                     pw   = line.partition(' password')[2].lstrip().partition(' ')[0].partition('\n')[0]
                     found = True
                     break
               fid.close()
            except OSError as e:
               logger.warning('Error trying to read authinfo file:'+pwf+'\n'+str(e))
               pass
            except:
               pass

            if not found:
               logger.warning('Did not find key '+self.authkey+' in authinfo file:'+pwf+'\n')

         inuser = kwargs.get('user', '')
         if len(inuser) > 0:
            if lock and len(user):
               logger.warning("Parameter 'user' passed to SAS_session was ignored due to configuration restriction.")
            else:
               user = inuser

         inpw = kwargs.get('pw', '')
         if len(inpw) > 0:
            if lock and len(pw):
               logger.warning("Parameter 'pw' passed to SAS_session was ignored due to configuration restriction.")
            else:
               pw = inpw

         if use_authcode and not user:
            code_pw = 'authcode'
         else:
            code_pw = ''
            if not user:
               msg  = "To connect to Viya you need either an authcode or a userid/pw. Neither were provided.\n"
               msg += "Please enter which one you want to enter next. Type one of these now: [default=authcode | userid]: "
               while code_pw.lower() not in ['userid','authcode']:
                  code_pw = self._prompt(msg)
                  if code_pw == '':
                     code_pw = 'authcode'
                  if code_pw is None:
                     self._token = None
                     raise RuntimeError("Neither authcode nor userid provided.")

         if code_pw.lower() == 'authcode':
            ci    = 'SASPy' if client_id is None else client_id
            if self.pkce:
               cv    = secrets.token_urlsafe(32)
               cvh   = hashlib.sha256(cv.encode('ascii')).digest()
               cvhe  = base64.urlsafe_b64encode(cvh)
               cc    = cvhe.decode('ascii')[:-1]
               purl = "/SASLogon/oauth/authorize?client_id={}&response_type=code&code_challenge_method=S256&code_challenge={}".format(ci, cc)
            else:
               purl = "/SASLogon/oauth/authorize?client_id={}&response_type=code".format(ci)

            if len(self.url) > 0:
               purl = self.url+purl
            else:
               purl = "http{}://{}:{}{}".format('s' if self.ssl else '', self.ip, str(self.port), purl)
            if self.pkce:
               msg  = "The PKCE required url to authenticate with is {}\n".format(purl)
            else:
               msg  = "The default url to authenticate with would be {}\n".format(purl)
            msg += "Please enter authcode: "
            authcode = self._prompt(msg)
            if authcode is None:
               self._token = None
               raise RuntimeError("No authcode provided.")
         else:
            while len(user) == 0:
               user = self._prompt("Please enter userid: ")
               if user is None:
                  self._token = None
                  raise RuntimeError("No userid provided.")

            while len(pw) == 0:
               pw = self._prompt("Please enter password: ", pw = True)
               if pw is None:
                  self._token = None
                  raise RuntimeError("No password provided.")

      if self.proxy is not None:
         http = self.proxy.split('://')
         if http[0].lower() in ['http', 'https']:
            hp = http[1].split(':')
         else:
            hp = http[0].split(':')

         self.pip   = self.ip
         self.ip    = hp[0]
         self.pport = self.port
         self.port  = int(hp[1]) if len(hp) > 1 else self.port

         if pauthkey or puser:
            if not puser:
               found = False
               if os.name == 'nt':
                  pwf = os.path.expanduser('~')+os.sep+'_authinfo'
               else:
                  pwf = os.path.expanduser('~')+os.sep+'.authinfo'
               try:
                  fid = open(pwf, mode='r')
                  for line in fid:
                     ls = line.split()
                     if len(ls) == 5 and ls[0] == self.sascfg.authkey and ls[1] == 'user' and ls[3] == 'password':
                        user  = ls[2]
                        pw    = ls[4]
                        found = True
                        break
                  fid.close()
               except OSError as e:
                  logger.warning('Error trying to read authinfo file:'+pwf+'\n'+str(e))
                  pass
               except:
                  pass

               if not found:
                  logger.warning('Did not find key '+self.authkey+' in authinfo file:'+pwf+'\n')

            while len(puser) == 0:
               puser = self._prompt("Please enter proxy_userid: ")
               if puser is None:
                  self._token = None
                  raise RuntimeError("No proxy_userid provided.")

            while len(ppw) == 0:
               ppw = self._prompt("Please enter proxy_password: ", pw = True)
               if ppw is None:
                  self._token = None
                  raise RuntimeError("No proxy_password provided.")
      else:
         self.pip = None

      # get Connections
      if self.ssl:
         sslctx = ssl.create_default_context(cafile=self.cafile)
         if   self.verify is None:
            # handle having self signed certificate default on Viya w/out copies on client; still ssl, just not verifiable
            try:
               self.REFConn  = hc.HTTPSConnection(self.ip, self.port, timeout=self.timeout, context=sslctx)
               self.REFConn.connect();  self.REFConn.close()
               self.HTTPConn = hc.HTTPSConnection(self.ip, self.port, timeout=self.timeout, context=sslctx)
               self.HTTPConn.connect(); self.HTTPConn.close()
            except ssl.SSLError as e:
               logger.warning("SSL certificate verification failed, creating an unverified SSL connection. Error was:"+str(e))
               self.REFConn  = hc.HTTPSConnection(self.ip, self.port, timeout=self.timeout, context=ssl._create_unverified_context())
               self.HTTPConn = hc.HTTPSConnection(self.ip, self.port, timeout=self.timeout, context=ssl._create_unverified_context())
               logger.warning("You can set 'verify=False' to get rid of this message ")
         elif self.verify:
            try:
               self.REFConn  = hc.HTTPSConnection(self.ip, self.port, timeout=self.timeout, context=sslctx)
               self.REFConn.connect();  self.REFConn.close()
               self.HTTPConn = hc.HTTPSConnection(self.ip, self.port, timeout=self.timeout, context=sslctx)
               self.HTTPConn.connect(); self.HTTPConn.close()
            except ssl.SSLError as e:
               logger.error("SSL certificate verification failed and verify was True; no connection established.\nError was:"+str(e))
               raise SASHTTPconnectionError(msg="SSL certificate verification failed and verify was True; no connection established.")
         else:
            self.REFConn  = hc.HTTPSConnection(self.ip, self.port, timeout=self.timeout, context=ssl._create_unverified_context())
            self.HTTPConn = hc.HTTPSConnection(self.ip, self.port, timeout=self.timeout, context=ssl._create_unverified_context())
      else:
         self.REFConn  = hc.HTTPConnection(self.ip, self.port, timeout=self.timeout)
         self.HTTPConn = hc.HTTPConnection(self.ip, self.port, timeout=self.timeout)

      if self.pip:
         if puser and ppw:
            uuser  = urllib.parse.quote(puser)
            upw    = urllib.parse.quote(ppw)
            auth   = "Basic "+base64.encodebytes((uuser+":"+upw).encode(self.encoding)).splitlines()[0].decode(self.encoding)
            header = {"Proxy-Authorization":auth}
         else:
            header = None
         self.REFConn.set_tunnel( self.pip, self.pport, header)
         self.HTTPConn.set_tunnel(self.pip, self.pport, header)

      # get AuthToken
      if not self._token:
         js = self._authenticate(user, pw, authcode, client_id, client_secret, jwt, cv)
         self._token   = js.get('access_token',  None)
         self._refresh = js.get('refresh_token', None)

      if not self._token:
         logger.error("Could not acquire an Authentication Token")
         raise SASHTTPconnectionError(msg="Could not acquire an Authentication Token. No connection established.")

      # GET Contexts
      contexts = self._get_contexts()
      if contexts == None:
         self._token = None
         raise SASHTTPconnectionError(msg="No Contexts found on Compute Service at ip="+self.ip)

      if not self.serverid:
         ctxnames = []
         for i in range(len(contexts)):
            ctxnames.append(contexts[i].get('name'))

         if len(ctxnames) == 0:
            self._token = None
            raise SASHTTPconnectionError(msg="No Contexts found on Compute Service at ip="+self.ip)

         if len(self.ctxname) == 0:
            if len(ctxnames) == 1:
               self.ctxname = ctxnames[0]
               logger.info("Using SAS Context: " + self.ctxname)
            else:
               try:
                  ctxname = self._prompt("Please enter the SAS Context you wish to run. Available contexts are: " +
                                         str(ctxnames)+" ")
                  if ctxname is None:
                     self._token = None
                     raise RuntimeError("No SAS Context provided.")
                  else:
                     self.ctxname = ctxname
               except:
                  raise SASHTTPconnectionError(msg=
                     "SAS Context specified '"+self.ctxname+"' was not found. Prompting failed. Available contexts were: " +
                      str(ctxnames)+" ")

         while self.ctxname not in ctxnames:
            if not lock:
               '''    this was original code before compute was production. users can't create these on the fly.
               createctx = self._prompt(
                   "SAS Context specified was not found. Do you want to create a new context named "+self.ctxname+" [Yes|No]?")
               if createctx.upper() in ('YES', 'Y'):
                  contexts = self._create_context(user)
               else:
               '''
               try:
                  ctxname = self._prompt(
                      "SAS Context specified was not found. Please enter the SAS Context you wish to run. Available contexts are: " +
                       str(ctxnames)+" ")
                  if ctxname is None:
                     self._token = None
                     raise SASHTTPconnectionError(msg=
                         "SAS Context specified '"+self.ctxname+"' was not found. Prompting failed. Available contexts were: " +
                          str(ctxnames)+" ")
                  else:
                     self.ctxname = ctxname
               except:
                  raise SASHTTPconnectionError(msg=
                      "SAS Context specified '"+self.ctxname+"' was not found. Prompting failed. Available contexts were: " +
                       str(ctxnames)+" ")
            else:
               msg  = "SAS Context specified in the SASconfig ("+self.ctxname+") was not found on this server, and because "
               msg += "the SASconfig is in lockdown mode, there is no prompting for other contexts. No connection established."
               logger.error(msg)
               self._token = None
               raise RuntimeError("No SAS Context provided.")

         for i in range(len(contexts)):
            if contexts[i].get('name') == self.ctxname:
               self.ctx = contexts[i]
               break

         if self.ctx == {}:
            raise SASHTTPconnectionError(msg="No context information returned for context {}\n{}".format(self.ctxname, contexts))
      else:
         self.ctx     = contexts
         self.ctxname = self.serverid

         return

   def _authenticate(self, user, pw, authcode, client_id, client_secret, jwt, cv):

      if self.serverid:
         return {'access_token':'tom'}

      if client_id is None:
         client_id = 'SASPy'
         ci = False
      else:
         ci = True

      if   authcode:
         uauthcode      = urllib.parse.quote(authcode)
         uclient_id     = urllib.parse.quote(client_id)
         uclient_secret = urllib.parse.quote(client_secret)
         headers        = {"Accept":"application/vnd.sas.compute.session+json","Content-Type":"application/x-www-form-urlencoded"}
         if self.pkce:
            if not cv:
               msg  = "A PKCE URL is configured to be used to acquire an authcode with is system, but a non-PKCE authcode was passed in.\n"
               msg += "Failure in GET AuthToken."
               raise SASHTTPauthenticateError(msg)
            d1          = ("grant_type=authorization_code&code="+uauthcode+"&code_verifier="+cv+
                          "&client_id="+uclient_id+"&client_secret="+uclient_secret).encode(self.encoding)
         else:
            d1          = ("grant_type=authorization_code&code="+uauthcode+
                          "&client_id="+uclient_id+"&client_secret="+uclient_secret).encode(self.encoding)
      elif jwt:
         if client_id == 'SASPy':
            msg  = "BEING DEPRECATED - Viya has decided to remove this authentication mechanism for SASPy; when using the SASPy client_id."
            msg += "To still use `jwt` you have to define your own client in Viya and provide that via `'client_id` along with `client_secret` and the jwt."
            logger.warning(msg)
         ujwt           = urllib.parse.quote(jwt)
         d1             = "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion="+ujwt
         client         = "Basic "+base64.encodebytes((client_id+":"+client_secret).encode(self.encoding)).splitlines()[0].decode(self.encoding)
         headers        = {"Accept":"application/vnd.sas.compute.session+json", "Content-Type":"application/x-www-form-urlencoded",
                           "Authorization":client}
      else:
         if not ci:
            client_id   = "sas.tkmtrb"
         uuser          = urllib.parse.quote(user)
         upw            = urllib.parse.quote(pw)
         d1             = ("grant_type=password&username="+uuser+"&password="+upw).encode(self.encoding)
         client         = "Basic "+base64.encodebytes((client_id+":").encode(self.encoding)).splitlines()[0].decode(self.encoding)
         headers        = {"Accept":"application/vnd.sas.compute.session+json","Content-Type":"application/x-www-form-urlencoded",
                           "Authorization":client}

      # POST AuthToken
      conn = self.HTTPConn; conn.connect()
      try:
         conn.request('POST', "/SASLogon/oauth/token", body=d1, headers=headers)
         req = conn.getresponse()
      except:
         #print("Failure in GET AuthToken. Could not connect to the logon service. Exception info:\n"+str(sys.exc_info()))
         msg="Failure in GET AuthToken. Could not connect to the logon service. Exception info:\n"+str(sys.exc_info())
         raise SASHTTPauthenticateError(msg)
         #return None

      status = req.status
      resp = req.read()
      conn.close()

      if status > 299:
         #print("Failure in GET AuthToken. Status="+str(status)+"\nResponse="+resp.decode(self.encoding))
         msg="Failure in GET AuthToken. Status="+str(status)+"\nResponse="+str(resp)
         raise SASHTTPauthenticateError(msg)
         #return None

      js = json.loads(resp.decode(self.encoding))
      return js

   def _get_contexts(self):
      # GET Contexts
      conn = self.HTTPConn; conn.connect()

      if not self.serverid:
         headers={"Accept":"application/vnd.sas.collection+json",
                  "Accept-Item":"application/vnd.sas.compute.context.summary+json",
                  "Authorization":"Bearer "+self._token}
         conn.request('GET', "/compute/contexts?limit=999999", headers=headers)
      else:
         headers={"Accept":"*/*",
                  "Accept-Item":"application/vnd.sas.compute.context.summary+json",
                  "Authorization":"Bearer "+self._token}
         conn.request('GET', "/compute/servers/"+self.serverid, headers=headers)

      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      if status > 299:
         if not self.serverid:
            fmsg = "Failure in GET Contexts. Status="+str(status)+"\nResponse="+resp.decode(self.encoding)
         else:
            fmsg = "Failure in GET Server. Status="+str(status)+"\nResponse="+resp.decode(self.encoding)
         raise SASHTTPconnectionError(msg=fmsg)

      js = json.loads(resp.decode(self.encoding))
      if not self.serverid:
         contexts = js.get('items')
      else:
         contexts = js

      return contexts

   def _create_context(self, user):
      # GET Contexts
      conn = self.HTTPConn; conn.connect()
      d1  = '{"name": "SASPy","version": 1,"description": "SASPy Context","attributes": {"sessionInactiveTimeout": 60 },'
      d1 += '"launchContext": {"contextName": "'+self.ctxname+'"},"launchType": "service","authorizedUsers": ["'+user+'"]}'

      headers={"Accept":"application/vnd.sas.compute.context+json",
               "Content-Type":"application/vnd.sas.compute.context.request+json",
               "Authorization":"Bearer "+self._token}
      conn.request('POST', "/compute/contexts", body=d1, headers=headers)
      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      if status > 299:
         logger.error("Failure in POST Context. Status="+str(status)+"\nResponse="+resp.decode(self.encoding))
         return None

      contexts = self._get_contexts()
      return contexts


class SASsessionHTTP():
   '''
   The SASsession object is the main object to instantiate and provides access to the rest of the functionality.
   cfgname   - value in SAS_config_names List of the sascfg.py file
   kernel    - None - internal use when running the SAS_kernel notebook
   user      - userid to use to connect to Compute Service
   pw        - pw for the userid being used to connect to Compute Service
   ip        - overrides IP      Dict entry of cfgname in sascfg.py file
   port      - overrides Port    Dict entry of cfgname in sascfg.py file
   context   - overrides Context Dict entry of cfgname in sascfg.py file
   options   - overrides Options Dict entry of cfgname in sascfg.py file
   encoding  - This is the python encoding value that matches the SAS session encoding of the Compute Server you are connecting to
   '''
   #def __init__(self, cfgname: str ='', kernel: '<SAS_kernel object>' =None, user: str ='', pw: str ='',
   #                   ip: str ='', port: int ='', context: str ='', options: list =[]) -> '<SASsession object>':
   def __init__(self, **kwargs):
      self.pid        = None
      self._session   = None
      self._sb        = kwargs.get('sb', None)
      self._log       = "\nNo SAS session established, something must have failed trying to connect\n"
      self.sascfg     = SASconfigHTTP(self, **kwargs)

      if self.sascfg._token:
         self._startsas()
      else:
         None

   def __del__(self):
      if self._session:
         self._endsas()
      self._sb.SASpid = None
      return

   def _startsas(self):
      if self.pid:
         return self.pid

      if len(self.sascfg.options):
         options = '[';
         for opt in self.sascfg.options:
            options += '"'+opt+'", '
         options = (options.rpartition(','))[0]+']'
      else:
         options = '[]'

      # POST Session
      uri = None
      for ld in self.sascfg.ctx.get('links'):
         if ld.get('method') == 'POST' and ld.get('rel') == 'createSession':
            uri = ld.get('uri')
            break

      if not uri:
         raise SASHTTPconnectionError(msg=
         "POST uri not found in context info. You may not have permission to use this context.\n{}".format(self.sascfg.ctx))

      conn = self.sascfg.HTTPConn; conn.connect()
      d1  = '{"name":"'+self.sascfg.ctxname+'", "description":"saspy session", "version":1, "environment":{"options":'+options+'}'
      d1 += ',"attributes": {"sessionInactiveTimeout": '+str(int(float(self.sascfg.inactive)*60))+'}}'
      headers={"Accept":"application/vnd.sas.compute.session+json","Content-Type":"application/vnd.sas.compute.session.request+json",
               "Authorization":"Bearer "+self.sascfg._token}

      try:
         conn.request('POST', uri, body=d1, headers=headers)
         req = conn.getresponse()
      except:
         #print("Could not acquire a SAS Session for context: "+self.sascfg.ctxname)
         raise SASHTTPconnectionError(msg="Could not acquire a SAS Session for context: "+self.sascfg.ctxname+". Exception info:\n"+str(sys.exc_info()))
         #return None

      status = req.status
      resp = req.read()
      conn.close()

      if status > 299:
         #print("Failure in POST Session \n"+resp.decode(self.sascfg.encoding))
         #print("Could not acquire a SAS Session for context: "+self.sascfg.ctxname)
         msg="Could not acquire a SAS Session for context: "+self.sascfg.ctxname+". Exception info:\nStatus="+str(status)+"\nResponse="+str(resp)
         raise SASHTTPconnectionError(msg)
         #return None

      self._session = json.loads(resp.decode(self.sascfg.encoding))

      if self._session == None:
         logger.error("Could not acquire a SAS Session for context: "+self.sascfg.ctxname)
         return None

      #GET Session uri's once
      for ld in self._session.get('links'):
         if   ld.get('method') == 'GET'     and ld.get('rel') == 'log':
            self._uri_log   = ld.get('uri')
         elif ld.get('method') == 'GET'     and ld.get('rel') == 'listing':
            self._uri_lst   = ld.get('uri')
         elif ld.get('method') == 'GET'     and ld.get('rel') == 'results':
            self._uri_ods   = ld.get('uri')
         elif ld.get('method') == 'GET'     and ld.get('rel') == 'state':
            self._uri_state = ld.get('uri')
         elif ld.get('method') == 'POST'    and ld.get('rel') == 'execute':
            self._uri_exe   = ld.get('uri')
         elif ld.get('method') == 'PUT'     and ld.get('rel') == 'cancel':
            self._uri_can   = ld.get('uri')
         elif ld.get('method') == 'DELETE'  and ld.get('rel') == 'delete':
            self._uri_del   = ld.get('uri')
         elif ld.get('method') == 'GET'     and ld.get('rel') == 'files':
            self._uri_files = ld.get('uri')

      self.pid = self._session.get('id')

      self._log = self._getlog().replace(chr(12), chr(10))

      # POST Job - Lets see if the server really came up, cuz you can't tell from what happend so far
      conn = self.sascfg.HTTPConn; conn.connect()
      jcode = json.dumps('\n')
      d1 = '{"code":['+jcode+']}'
      headers={"Accept":"application/json","Content-Type":"application/vnd.sas.compute.job.request+json",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', self._uri_exe, body=d1, headers=headers)
      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      try:
         jobid = json.loads(resp.decode(self.sascfg.encoding))
      except:
         jobid = None

      if not jobid or status > 299:
         logger.error("Compute server had issues starting:\n")
         for key in jobid:
            logger.error(key+"="+str(jobid.get(key)))
         return None

      self._sb.SESSION_ID = self.pid
      ll = self.submit("options svgtitle='svgtitle'; options validvarname=any validmemname=extend pagesize=max nosyntaxcheck; ods graphics on;", "text")
      if self.sascfg.verbose:
         logger.info("SAS server started using Context "+self.sascfg.ctxname+" with SESSION_ID="+self.pid)

      self._refthd = Thread(target=self._refresh_thread, args=())
      self._refthd.daemon = True
      self._refthd.start()

      atexit.register(self._endsas)

      return self.pid

   def _endsas(self):
      rc = 0
      if self._session:
         # DELETE Session
         conn = self.sascfg.HTTPConn; conn.connect()
         headers={"Accept":"application/json","Authorization":"Bearer "+self.sascfg._token}
         conn.request('DELETE', self._uri_del, headers=headers)
         req = conn.getresponse()
         resp = req.read()
         conn.close()

         self._refthd.join(1)

         if self.sascfg.verbose:
            logger.info("SAS server terminated for SESSION_ID="+self._session.get('id'))
         self._session   = None
         self.pid        = None
         self._sb.SASpid = None
      return rc

   def _refresh_thread(self):
      while True:
         sleep(3000)
         if self.pid is None:
            return
         self._refresh_token()

   def _refresh_token(self):
      if not self.sascfg._refresh:
         return
      d1      = ("grant_type=refresh_token&refresh_token="+self.sascfg._refresh).encode(self.sascfg.encoding)
      client  = "Basic "+base64.encodebytes(("SASPy:").encode(self.sascfg.encoding)).splitlines()[0].decode(self.sascfg.encoding)
      headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization":client}

      # POST AuthToken
      conn = self.sascfg.REFConn; conn.connect()
      try:
         conn.request('POST', "/SASLogon/oauth/token", body=d1, headers=headers)
         req = conn.getresponse()
      except:
         #print("Failure in REFRESH AuthToken. Could not connect to the logon service. Exception info:\n"+str(sys.exc_info()))
         msg="Failure in REFRESH AuthToken. Could not connect to the logon service. Exception info:\n"+str(sys.exc_info())
         raise SASHTTPauthenticateError(msg)
         #return None

      status = req.status
      resp   = req.read()
      conn.close()

      if status > 299:
         #print("Failure in REFRESH AuthToken. Status="+str(status)+"\nResponse="+resp.decode(self.sascfg.encoding))
         msg="Failure in REFRESH AuthToken. Status="+str(status)+"\nResponse="+str(resp)
         raise SASHTTPauthenticateError(msg)
         #return None

      js                   = json.loads(resp.decode(self.sascfg.encoding))
      self.sascfg._token   = js.get('access_token')
      self.sascfg._refresh = js.get('refresh_token')
      return

   def _getlog(self, jobid=None, loglines=False):
      start = 0
      logr = ''
      logl = []

      # GET Log
      if jobid:
         for ld in jobid.get('links'):
            if ld.get('method') == 'GET' and ld.get('rel') == 'log':
               uri = ld.get('uri')
               break
      else:
         uri   = self._uri_log

      while True:
         # GET Log
         conn = self.sascfg.HTTPConn; conn.connect()
         headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
         conn.request('GET', uri+"?start="+str(start)+"&limit="+str(start+1000), headers=headers)
         req = conn.getresponse()
         status = req.status
         resp = req.read()
         conn.close()

         try:
            js    = json.loads(resp.decode(self.sascfg.encoding))
            log   = js.get('items')
            lines = len(log)
         except:
            lines = None

         if not lines:
            break
         start += lines

         logl += log

      for line in logl:
          logr += line.get('line')+'\n'

      if jobid != None:
         logr       = logr.replace(chr(12), chr(10))
         self._log += logr

      if logr.count('\nERROR:') > 0:
         warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
         self._sb.check_error_log = True

      if not loglines:
         del(logl)
         return logr
      else:
         return (logr, logl)

   def _getlst(self, jobid=None):
      htm = ''
      i   = 0

      # GET the list of results
      if jobid:
         for ld in jobid.get('links'):
            if ld.get('method') == 'GET' and ld.get('rel') == 'results':
               uri = ld.get('uri')+"?includeTypes=ODS"
               break
      else:
         uri = self._uri_lst

      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      conn.request('GET', uri, headers=headers)
      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      try:
         js = json.loads(resp.decode(self.sascfg.encoding))
         results = js.get('items')
         if not results:
            results = []
      except:
         results = []

      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      while i < len(results):
         # GET an ODS Result
         if results[i].get('type') == 'ODS'         and \
            results[i].get('name').endswith('.htm') and \
            len(results[i].get('links')) > 0:
               conn.request('GET', results[i].get('links')[0].get('href'), headers=headers)
               req = conn.getresponse()
               status = req.status
               resp = req.read()
               htm += resp.decode(self.sascfg.encoding)
         i += 1
      conn.close()

      lstd = htm.replace(chr(12), chr(10)).replace('<body class="c body">',
                                                   '<body class="l body">').replace("font-size: x-small;",
                                                                                    "font-size:  normal;")
      return lstd

   def _getlsttxt(self, jobid=None):
      start = 0
      lstr = ''

      # GET Log
      if jobid:
         for ld in jobid.get('links'):
            if ld.get('method') == 'GET' and ld.get('rel') == 'listing':
               uri = ld.get('uri')
               break
      else:
         uri   = self._uri_lst

      while True:
         conn = self.sascfg.HTTPConn; conn.connect()
         headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
         conn.request('GET', uri+"?start="+str(start)+"&limit="+str(start+1000), headers=headers)
         req = conn.getresponse()
         status = req.status
         resp = req.read()
         conn.close()

         try:
            js    = json.loads(resp.decode(self.sascfg.encoding))
            lst   = js.get('items')
            lines = len(lst)
         except:
            lines = None

         if not lines:
            break
         start += lines

         for line in lst:
             lstr += line.get('line')+'\n'

      return lstr.replace(chr(12), chr(10))

   def _asubmit(self, code, results="html"):
      odsopen  = json.dumps("ods listing close;ods "+self.sascfg.output+" (id=saspy_internal) options(bitmap_mode='inline') device=svg style="+self._sb.HTML_Style+"; ods graphics on / outputfmt=png;\n")
      odsclose = json.dumps("ods "+self.sascfg.output+" (id=saspy_internal) close;ods listing;\n")

      jcode = json.dumps(code)
      if results.upper() != "HTML":
         d1 = '{"code":['+jcode+']}'
      else:
         d1 = '{"code":['+odsopen+','+jcode+','+odsclose+']}'

      # POST Job
      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"application/json","Content-Type":"application/vnd.sas.compute.job.request+json",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', self._uri_exe, body=d1, headers=headers)
      req = conn.getresponse()
      resp = req.read()
      conn.close()

      jobid = json.loads(resp.decode(self.sascfg.encoding))

      return jobid

   def _jobstate(self, jobid):

      uri = None
      for ld in jobid.get('links'):
         if ld.get('method') == 'GET' and ld.get('rel') == 'state':
            uri = ld.get('uri')
            break

      if not uri:
         print("No job found")
         return None

      conn    = self.sascfg.HTTPConn;
      headers = {"Accept":"text/plain", "Authorization":"Bearer "+self.sascfg._token}
      conn.connect()
      conn.request('GET', uri, headers=headers)
      req = conn.getresponse()
      resp = req.read()
      conn.close()

      return resp


   def submit(self, code: str, results: str ="html", prompt: dict = None, **kwargs) -> dict:
      '''
      code    - the SAS statements you want to execute
      results - format of results, HTML is default, TEXT is the alternative
      prompt  - dict of names:flags to prompt for; create marco variables (used in submitted code), then keep or delete
                The keys are the names of the macro variables and the boolean flag is to either hide what you type and delete
                the macros, or show what you type and keep the macros (they will still be available later)
                for example (what you type for pw will not be displayed, user and dsname will):

                results = sas.submit(
                   """
                   libname tera teradata server=teracop1 user=&user pw=&pw;
                   proc print data=tera.&dsname (obs=10); run;
                   """ ,
                   prompt = {'user': False, 'pw': True, 'dsname': False}
                   )

      Returns - a Dict containing two keys:values, [LOG, LST]. LOG is text and LST is 'results' (HTML or TEXT)

      NOTE: to view HTML results in the ipykernel, issue: from IPython.display import HTML  and use HTML() instead of print()
      i.e,: results = sas.submit("data a; x=1; run; proc print;run')
            print(results['LOG'])
            HTML(results['LST'])
      '''
      prompt  = prompt if prompt is not None else {}
      printto = kwargs.pop('undo', False)
      cancel  = kwargs.pop('cancel', False)
      lines   = kwargs.pop('loglines', False)

      odsopen  = json.dumps("ods listing close;ods "+self.sascfg.output+" (id=saspy_internal) options(bitmap_mode='inline') device=svg style="+self._sb.HTML_Style+"; ods graphics on / outputfmt=png;\n")
      odsclose = json.dumps("ods "+self.sascfg.output+" (id=saspy_internal) close;ods listing;\n")
      ods      = True;

      if self._session == None:
         #return dict(LOG="No SAS process attached. SAS process has terminated unexpectedly.", LST='')
         logger.fatal("No SAS process attached. SAS process has terminated unexpectedly.")
         raise SASIOConnectionTerminated(Exception)

      if len(prompt):
         pcodeiv = ''
         pcodei  = 'options nosource nonotes;\n'
         pcodeo  = 'options nosource nonotes;\n'
         for key in prompt:
            gotit = False
            while not gotit:
               var = self.sascfg._prompt('Please enter value for macro variable '+key+' ', pw=prompt[key])
               if var is None:
                  raise RuntimeError("No value for prompted macro variable provided.")
               if len(var) > 0:
                  gotit = True
               else:
                  print("Sorry, didn't get a value for that variable.")
            if prompt[key]:
               pcodei  += '%let '+key+'='+var+';\n'
            else:
               pcodeiv += '%let '+key+'='+var+';\n'
            if prompt[key]:
               pcodeo += '%symdel '+key+';\n'
         pcodei += 'options source notes;\n'
         pcodeo += 'options source notes;\n'
         jcode = json.dumps(pcodei+pcodeiv+code+'\n'+pcodeo)
      else:
         jcode = json.dumps(code)

      if results.upper() != "HTML":
         ods = False
         d1 = '{"code":['+jcode+']}'
      else:
         d1 = '{"code":['+odsopen+','+jcode+','+odsclose+']}'

      # POST Job
      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"application/json","Content-Type":"application/vnd.sas.compute.job.request+json",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', self._uri_exe, body=d1, headers=headers)
      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      try:
         jobid = json.loads(resp.decode(self.sascfg.encoding))
      except:
         raise SASHTTPsubmissionError(msg="Problem parsing response from Compute Service.\n   Status="+str(status)+"\n   Response="+str(resp))

      if not jobid or status > 299:
         raise SASHTTPsubmissionError(msg="Problem submitting job to Compute Service.\n   Status code="+str(jobid.get('httpStatusCode'))+"\n   Message="+jobid.get('message'))

      uri = None
      can = None
      for ld in jobid.get('links'):
         if ld.get('method') == 'GET' and ld.get('rel') == 'state':
            uri = ld.get('uri')
         if ld.get('method') == 'PUT' and ld.get('rel') == 'cancel':
            can = ld.get('uri')
         if uri and can:
            break

      Etag = req.getheader("Etag")

      conn    = self.sascfg.HTTPConn;
      headers = {"Accept":"text/plain", "Authorization":"Bearer "+self.sascfg._token}
      done    = False

      delay   = kwargs.get('GETstatusDelay'  , 0)
      excpcnt = kwargs.get('GETstatusFailcnt', 5)

      while not done:
         try:
            while True:
               # GET Status for JOB
               conn.connect()
               conn.request('GET', uri, headers=headers)
               req = conn.getresponse()
               resp = req.read()
               Etag = req.getheader("Etag")
               conn.close()
               if resp not in [b'running', b'pending']:
                  done = True
                  break
               sleep(delay)

         except (KeyboardInterrupt, SystemExit):
            conn.close()
            print('Exception caught!')
            if cancel:
               msg = "Please enter (C) to Cancel submitted code or (Q) to Quit waiting for results or (W) continue to Wait."
            else:
               msg = "CANCEL is only supported for the submit*() methods. Please enter (Q) to Quit waiting for results or (W) to continue to Wait."

            response = self.sascfg._prompt(msg)

            while True:
               if cancel and response is None or response.upper() == 'C':
                  # GET Status for JOB
                  canheaders = {"Accept":"text/plain", "Authorization":"Bearer "+self.sascfg._token, "If-Match":Etag}
                  conn.connect()
                  conn.request('PUT', can, headers=canheaders)
                  req = conn.getresponse()
                  resp = req.read()
                  conn.close()
                  print('Canceled submitted statements\n')
                  break
               if response is None or response.upper() == 'Q':
                  return dict(LOG='', LST='')
               if response.upper() == 'W':
                  break
               response = self.sascfg._prompt(msg)

         except hc.RemoteDisconnected as Dis:
            conn.close()
            print('RemoteDisconnected Exception caught!\n'+str(Dis))
            excpcnt -= 1
            if excpcnt < 0:
               raise

      logs = self._getlog(jobid, lines)

      if not lines:
         logd = logs
      else:
         logd, logl = logs

      if ods:
         lstd = self._getlst(jobid)
      else:
         lstd = self._getlsttxt(jobid)

      trip = lstd.rpartition("/*]]>*/")
      if len(trip[1]) > 0 and len(trip[2]) < 200:
         lstd = ''

      self._sb._lastlog = logd

      # issue 294
      if printto:
         conn = self.sascfg.HTTPConn; conn.connect()
         jcode = json.dumps('proc printto;run;\n')
         d1 = '{"code":['+jcode+']}'
         headers={"Accept":"application/json","Content-Type":"application/vnd.sas.compute.job.request+json",
                  "Authorization":"Bearer "+self.sascfg._token}
         conn.request('POST', self._uri_exe, body=d1, headers=headers)
         req = conn.getresponse()
         status = req.status
         resp = req.read()
         conn.close()

      if lines:
         logd = list(logl)
         del(logl)

      return dict(LOG=logd, LST=lstd)

   def saslog(self):
      '''
      this method is used to get the current, full contents of the SASLOG
      '''
      return self._log

   def exist(self, table: str, libref: str ="") -> bool:
      '''
      table  - the name of the SAS Data Set
      libref - the libref for the Data Set, defaults to WORK, or USER if assigned

      Returns True it the Data Set exists and False if it does not
      '''
      #can't have an empty libref, so check for user or work
      sd = table.strip().replace("'", "''")
      if not libref:
         # HEAD Libref USER
         conn = self.sascfg.HTTPConn; conn.connect()
         headers={"Accept":"*/*", "Authorization":"Bearer "+self.sascfg._token}
         conn.request('HEAD', "/compute/sessions/"+self.pid+"/data/USER", headers=headers)
         req = conn.getresponse()
         status = req.status
         conn.close()

         if status == 200:
            libref = 'USER'
         else:
            libref = 'WORK'

      code  = 'data _null_; e = exist("'
      code += libref+"."
      code += "'"+sd+"'n"+'"'+");\n"
      code += 'v = exist("'
      code += libref+"."
      code += "'"+sd+"'n"+'"'+", 'VIEW');\n if e or v then e = 1;\n"
      code += "te='TABLE_EXISTS='; put te e;run;\n"

      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("TABLE_EXISTS= ")
      l2 = l2[2].partition("\n")
      exists = int(l2[0])

      return bool(exists)

      """
      # HEAD Data Table
      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"*/*", "Authorization":"Bearer "+self.sascfg._token}
      conn.request('HEAD', "/compute/sessions/"+self.pid+"/data/"+libref+"/"+table, headers=headers)
      req = conn.getresponse()
      status = req.status
      conn.close()

      if status == 200:
         exists = True
      else:
         exists = False

      return exists
      """

   def upload(self, localfile: str, remotefile: str, overwrite: bool = True, permission: str = '', **kwargs):
      """
      This method uploads a local file to the SAS servers file system.
      localfile  - path to the local file to upload
      remotefile - path to remote file to create or overwrite
      overwrite  - overwrite the output file if it exists?
      permission - permissions to set on the new file. See SAS Filename Statement Doc for syntax
      """
      valid = self._sb.file_info(remotefile, quiet = True)

      # check for non-exist, dir or existing file
      if valid is None:
         remf  = remotefile
         exist = False
      else:
         if valid == {}:
            remf = remotefile + self._sb.hostsep + localfile.rpartition(os.sep)[2]
            valid = self._sb.file_info(remf, quiet = True)
            if valid is None:
               exist = False
            else:
               if valid == {}:
                  return {'Success' : False,
                          'LOG'     : "File "+str(remf)+" is an existing directory. Upload was stopped."}
               else:
                  exist = True
                  if overwrite == False:
                     return {'Success' : False,
                             'LOG'     : "File "+str(remf)+" exists and overwrite was set to False. Upload was stopped."}
         else:
            remf  = remotefile
            exist = True
            if overwrite == False:
               return {'Success' : False,
                       'LOG'     : "File "+str(remotefile)+" exists and overwrite was set to False. Upload was stopped."}

      try:
         fd = open(localfile, 'rb')
      except OSError as e:
         return {'Success' : False,
                 'LOG'     : "File "+str(localfile)+" could not be opened. Error was: "+str(e)}

      fsize = os.path.getsize(localfile)

      if fsize > 0:
         code = "filename _sp_updn '"+remf+"' recfm=N permission='"+permission+"';"
         ll = self.submit(code, 'text')
         logf = ll['LOG']

         # See if that worked cuz the next call will abend SAS if not; if lockdown/WatchDog ...
         conn = self.sascfg.HTTPConn; conn.connect()
         headers={"Accept":"application/vnd.sas.compute.fileref+json;application/json",
                  "Authorization":"Bearer "+self.sascfg._token}
         conn.request('HEAD', self._uri_files+"/_sp_updn", headers=headers)
         req = conn.getresponse()
         status = req.status
         resp = req.read()
         conn.close()

         if status > 299:
            fd.close()
            return {'Success' : False,
                    'LOG'     : logf}

         # GET Etag
         conn = self.sascfg.HTTPConn; conn.connect()
         headers={"Accept":"application/vnd.sas.compute.fileref+json;application/json",
                  "Authorization":"Bearer "+self.sascfg._token}
         conn.request('GET', self._uri_files+"/_sp_updn", headers=headers)
         req = conn.getresponse()
         status = req.status
         resp = req.read()
         conn.close()

         Etag = req.getheader("Etag")

         # PUT data
         conn = self.sascfg.HTTPConn; conn.connect()
         headers={"Accept":"*/*","Content-Type":"application/octet-stream",
                  "Transfer-Encoding" : "chunked",
                  "Authorization":"Bearer "+self.sascfg._token}

         conn.connect()
         conn.putrequest('PUT', self._uri_files+"/_sp_updn/content")
         conn.putheader("Accept","*/*")
         conn.putheader("Content-Type","application/octet-stream")
         conn.putheader("If-Match",Etag)
         conn.putheader("Transfer-Encoding","chunked")
         conn.putheader("Authorization","Bearer "+self.sascfg._token)
         conn.endheaders()

         blksz = int(kwargs.get('blocksize', 50000))
         while True:
            buf = fd.read1(blksz)
            if len(buf) == 0:
               conn.send(b"0\r\n\r\n")
               break
            try:
               lenstr = "%s\r\n" % hex(len(buf))[2:]
               conn.send(lenstr.encode())
               conn.send(buf)
               conn.send(b"\r\n")
            except Exception as e:
               req    = conn.getresponse()
               status = req.status
               resp   = req.read()
               conn.close()
               fd.close()
               logger.error("Caught an exception in upload.\nException="+str(e)+"\nStatus="+str(status)+
                            "\nResponse="+str(resp.decode())+"\nLOG=\n"+logf)
               raise e

         req    = conn.getresponse()
         status = req.status
         resp   = req.read()
         conn.close()
         fd.close()

         ll = self.submit("filename _sp_updn;", 'text')
         logf += ll['LOG']

         if status > 299:
            return {'Success' : False,
                    'LOG'     : "Failure in upload. Status="+str(status)+"\nResponse="+str(resp.decode())+
                                "\n\n"+logf}
      else:
         logf = ''
         code = """
            filename _sp_updn '"""+remf+"""' recfm=F encoding=binary lrecl=1 permission='"""+permission+"""';
            data _null_;
            fid = fopen('_sp_updn', 'O');
            if fid then
               rc = fclose(fid);
            run;
            filename _sp_updn;
            """
         ll = self.submit(code, 'text')
         logf += ll['LOG']
         fd.close()

      valid2  = self._sb.file_info(remf, quiet = True)

      if valid2 is not None:
         if exist:
            success = False
            for key in valid.keys():
               if valid[key] != valid2[key]:
                  success = True
                  break
         else:
            success = True
      else:
         success = False

      return {'Success' : success,
              'LOG'     : logf}

   def download(self, localfile: str, remotefile: str, overwrite: bool = True, **kwargs):
      """
      This method downloads a remote file from the SAS servers file system.
      localfile  - path to the local file to create or overwrite
      remotefile - path to remote file tp dpwnload
      overwrite  - overwrite the output file if it exists?
      """
      valid = self._sb.file_info(remotefile, quiet = True)

      if valid is None:
         return {'Success' : False,
                 'LOG'     : "File "+str(remotefile)+" does not exist."}

      if valid == {}:
         return {'Success' : False,
                 'LOG'     : "File "+str(remotefile)+" is a directory."}

      if os.path.isdir(localfile):
         locf = localfile + os.sep + remotefile.rpartition(self._sb.hostsep)[2]
      else:
         locf = localfile

      try:
         fd = open(locf, 'wb')
         fd.write(b'write can fail even if open worked, as it turns out')
         fd.close()
         fd = open(locf, 'wb')
      except OSError as e:
         return {'Success' : False,
                 'LOG'     : "File "+str(locf)+" could not be opened or written to. Error was: "+str(e)}

      code = "filename _sp_updn '"+remotefile+"' recfm=F encoding=binary lrecl=4096;"

      ll = self.submit(code, "text")
      logf  = ll['LOG']

      # GET data
      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"*/*","Content-Type":"application/octet-stream",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('GET', self._uri_files+"/_sp_updn/content", headers=headers)
      req = conn.getresponse()
      status = req.status

      if status > 299:
         ret = {'Success' : False,
                'LOG'     : "Failure in download. Status="+str(status)+"\nReason="+str(req.reason)}
      else:
         while not req.isclosed():
            fd.write(req.read(1024*1024))
         fd.flush()
         ret = None

      fd.close()
      conn.close()

      ll = self.submit("filename _sp_updn;", 'text')
      logf += ll['LOG']

      if ret is None:
         ret = {'Success' : True,
                'LOG'     : logf}

      return ret

   def _getbytelenF(self, x):
      return len(x.encode(self.sascfg.encoding))

   def _getbytelenR(self, x):
      return len(x.encode(self.sascfg.encoding, errors='replace'))

   def dataframe2sasdata(self, df: '<Pandas Data Frame object>', table: str ='a',
                         libref: str ="", keep_outer_quotes: bool=False,
                                          embedded_newlines: bool=True,
                         LF: str = '\x01', CR: str = '\x02',
                         colsep: str = '\x03', colrep: str = ' ',
                         datetimes: dict={}, outfmts: dict={}, labels: dict={},
                         outdsopts: dict={}, encode_errors = None, char_lengths = None,
                         **kwargs):
      '''
      This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      keep_outer_quotes - for character columns, have SAS keep any outer quotes instead of stripping them off.
      embedded_newlines - if any char columns have embedded CR or LF, set this to True to get them imported into the SAS data set
      LF - if embedded_newlines=True, the chacter to use for LF when transferring the data; defaults to '\x01'
      CR - if embedded_newlines=True, the chacter to use for CR when transferring the data; defaults to '\x02'
      colsep - the column seperator character used for streaming the delimmited data to SAS defaults to '\x03'
      datetimes - dict with column names as keys and values of 'date' or 'time' to create SAS date or times instead of datetimes
      outfmts - dict with column names and SAS formats to assign to the new SAS data set
      labels  - dict with column names and SAS Labels to assign to the new SAS data set
      outdsopts - a dictionary containing output data set options for the table being created
      encode_errors - 'fail' or 'replace' - default is to 'fail', other choice is to 'replace' invalid chars with the replacement char \
                      'ignore' will not  transcode n Python, so you get whatever happens with your data and SAS
      char_lengths - How to determine (and declare) lengths for CHAR variables in the output SAS data set
      '''
      input   = ""
      xlate   = ""
      card    = ""
      format  = ""
      length  = ""
      label   = ""
      dts     = []
      ncols   = len(df.columns)
      lf      = "'"+'%02x' % ord(LF.encode(self.sascfg.encoding))+"'x"
      cr      = "'"+'%02x' % ord(CR.encode(self.sascfg.encoding))+"'x "
      delim   = "'"+'%02x' % ord(colsep.encode(self.sascfg.encoding))+"'x "

      dts_upper = {k.upper():v for k,v in datetimes.items()}
      dts_keys  = dts_upper.keys()
      fmt_upper = {k.upper():v for k,v in outfmts.items()}
      fmt_keys  = fmt_upper.keys()
      lab_upper = {k.upper():v for k,v in labels.items()}
      lab_keys  = lab_upper.keys()

      if encode_errors is None:
         encode_errors = 'fail'

      CnotB = kwargs.pop('CnotB', None)

      if char_lengths is None:
         return -1

      chr_upper = {k.upper():v for k,v in char_lengths.items()}

      if type(df.index) != pd.RangeIndex:
         warnings.warn("Note that Indexes are not transferred over as columns. Only actual columns are transferred")

      longname = False
      for name in df.columns:
         colname = str(name).replace("'", "''")
         if len(colname.encode(self.sascfg.encoding)) > 32:
            warnings.warn("Column '{}' in DataFrame is too long for SAS. Rename to 32 bytes or less".format(colname),
                     RuntimeWarning)
            longname = True
         col_up  = str(name).upper()
         input  += "input '"+colname+"'n "
         if col_up in lab_keys:
            label += "label '"+colname+"'n ="+lab_upper[col_up]+";\n"
         if col_up in fmt_keys:
            format += "'"+colname+"'n "+fmt_upper[col_up]+" "

         if df.dtypes[name].kind in ('O','S','U','V'):
            try:
               length += " '"+colname+"'n $"+str(chr_upper[col_up])
            except KeyError as e:
               logger.error("Dictionary provided as char_lengths is missing column: "+colname)
               raise e
            if keep_outer_quotes:
               input  += "~ "
            dts.append('C')
            if embedded_newlines:
               xlate += " '"+colname+"'n = translate('"+colname+"'n, '0A'x, "+lf+");\n"
               xlate += " '"+colname+"'n = translate('"+colname+"'n, '0D'x, "+cr+");\n"
         else:
            if df.dtypes[name].kind in ('M'):
               length += " '"+colname+"'n 8"
               input  += ":B8601DT26.6 "
               if col_up not in dts_keys:
                  if col_up not in fmt_keys:
                     format += "'"+colname+"'n E8601DT26.6 "
               else:
                  if dts_upper[col_up].lower() == 'date':
                     if col_up not in fmt_keys:
                        format += "'"+colname+"'n E8601DA. "
                     xlate  += " '"+colname+"'n = datepart('"+colname+"'n);\n"
                  else:
                     if dts_upper[col_up].lower() == 'time':
                        if col_up not in fmt_keys:
                           format += "'"+colname+"'n E8601TM. "
                        xlate  += " '"+colname+"'n = timepart('"+colname+"'n);\n"
                     else:
                        logger.warning("invalid value for datetimes for column "+colname+". Using default.")
                        if col_up not in fmt_keys:
                           format += "'"+colname+"'n E8601DT26.6 "
               dts.append('D')
            else:
               length += " '"+colname+"'n 8"
               if df.dtypes[name] == 'bool':
                  dts.append('B')
               else:
                  dts.append('N')
         input += ";\n"

      if longname:
         raise SASDFNamesToLongError(Exception)

      code = "data "
      if len(libref):
         code += libref+"."
      code += "'"+table.strip().replace("'", "''")+"'n"

      if len(outdsopts):
         code += '('
         for key in outdsopts:
            code += key+'='+str(outdsopts[key]) + ' '
         code += ");\n"
      else:
         code += ";\n"

      if len(length):
         code += "length "+length+";\n"
      if len(format):
         code += "format "+format+";\n"
      code += label
      code += "infile datalines delimiter="+delim+" STOPOVER;\n"
      code += "input @;\nif _infile_ = '' then delete;\nelse do;\n"
      code +=  input+xlate+";\n"
      code += "end;\n"
      code += "datalines4;"
      jobid = self._asubmit(code, "text")
      self._log += self._getlog(jobid)

      blksz = int(kwargs.get('blocksize', 1000000))
      noencode = self._sb.sascei == 'utf-8' or encode_errors == 'ignore'
      row_num = 0
      code = ""
      for row in df.itertuples(index=False):
         row_num += 1
         card  = ""
         for col in range(ncols):
            var = 'nan' if row[col] is None else str(row[col])

            if   dts[col] == 'N' and var == 'nan':
               var = '.'
            elif dts[col] == 'C':
               if  var == 'nan' or len(var) == 0:
                  var = ' '+colsep
               elif len(var) == var.count(' '):
                  var += colsep
               else:
                  if var.startswith(';;;;'):
                     var = ' '+var
                  var = var.replace(colsep, colrep)
            elif dts[col] == 'B':
               var = str(int(row[col]))
            elif dts[col] == 'D':
               if var in ['nan', 'NaT', 'NaN']:
                  var = '.'
               else:
                  var = str(row[col].to_datetime64())[:26]

            if embedded_newlines:
               var = var.replace(LF, colrep).replace(CR, colrep)
               var = var.replace('\n', LF).replace('\r', CR)

            card += var+"\n"

         code += card

         if len(code) > blksz:
            if not noencode:
               if encode_errors == 'fail':
                  if CnotB:
                     try:
                        chk = code.encode(self.sascfg.encoding)
                     except Exception as e:
                        self._asubmit(";;;;\n;;;;", "text")
                        ll = self.submit("run;", 'text')
                        logger.error("Transcoding error encountered. Data transfer stopped on or before row "+str(row_num))
                        logger.error("DataFrame contains characters that can't be transcoded into the SAS session encoding.\n"+str(e))
                        return row_num
               else:
                  code = code.encode(self.sascfg.encoding, errors='replace').decode(self.sascfg.encoding)

            jobid = self._asubmit(code, "text")
            self._log += self._getlog(jobid)
            code = ""

      if not noencode and len(code) > 0:
         if encode_errors == 'fail':
            if CnotB:
               try:
                  code = code.encode(self.sascfg.encoding).decode(self.sascfg.encoding)
               except Exception as e:
                  self._asubmit(";;;;\n;;;;", "text")
                  ll = self.submit("run;", 'text')
                  logger.error("Transcoding error encountered. Data transfer stopped on or before row "+str(row_num))
                  logger.error("DataFrame contains characters that can't be transcoded into the SAS session encoding.\n"+str(e))
                  return row_num
         else:
            code = code.encode(self.sascfg.encoding, errors='replace').decode(self.sascfg.encoding)

      jobid = self._asubmit(code+";;;;\n;;;;", "text")
      self._log += self._getlog(jobid)
      ll = self.submit("quit;", 'text')
      return None

   def sasdata2dataframe(self, table: str, libref: str ='', dsopts: dict = None,
                         rowsep: str = '\x01', colsep: str = '\x02',
                         rowrep: str = ' ',    colrep: str = ' ',
                         **kwargs) -> '<Pandas Data Frame object>':
      '''
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table   - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref  - the libref for the SAS Data Set.
      dsopts  - data set options for the input SAS Data Set
      rowsep  - the row seperator character to use; defaults to '\x01'
      colsep  - the column seperator character to use; defaults to '\x02'
      rowrep  - the char to convert to for any embedded rowsep chars, defaults to  ' '
      colrep  - the char to convert to for any embedded colsep chars, defaults to  ' '
      '''
      dsopts = dsopts if dsopts is not None else {}

      method = kwargs.pop('method', None)
      if   method and method.lower() == 'csv':
         return self.sasdata2dataframeCSV(table, libref, dsopts, **kwargs)
      #elif method and method.lower() == 'disk':
      else:
         return self.sasdata2dataframeDISK(table, libref, dsopts, rowsep, colsep,
                                           rowrep, colrep, **kwargs)


   def sasdata2dataframeCSV(self, table: str, libref: str ='', dsopts: dict =None, opts: dict = None,
                            **kwargs) -> '<Pandas Data Frame object>':
      '''
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table    - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref   - the libref for the SAS Data Set.
      dsopts   - data set options for the input SAS Data Set
      opts     - a dictionary containing any of the following Proc Export options(delimiter, putnames)
      tempfile - DEPRECATED
      tempkeep - DEPRECATED

      These two options are for advanced usage. They override how saspy imports data. For more info
      see https://sassoftware.github.io/saspy/advanced-topics.html#advanced-sd2df-and-df2sd-techniques

      dtype   - this is the parameter to Pandas read_csv, overriding what saspy generates and uses
      my_fmts - bool: if True, overrides the formats saspy would use, using those on the data set or in dsopts=
      '''
      tmp = kwargs.pop('tempfile', None)
      tmp = kwargs.pop('tempkeep', None)

      tsmax = kwargs.pop('tsmax', None)
      tsmin = kwargs.pop('tsmin', None)
      tscode = ''

      dsopts = dsopts if dsopts is not None else {}
      opts   = opts   if   opts is not None else {}

      if libref:
         tabname = libref+".'"+table.strip().replace("'", "''")+"'n "
      else:
         tabname = "'"+table.strip().replace("'", "''")+"'n "

      code  = "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";run;\n"

      ll = self.submit(code, "text")

      ##GET Data Table Info
      #conn = self.sascfg.HTTPConn; conn.connect()
      #headers={"Accept":"application/vnd.sas.compute.data.table+json", "Authorization":"Bearer "+self.sascfg._token}
      #conn.request('GET', "/compute/sessions/"+self.pid+"/data/work/sasdata2dataframe", headers=headers)
      #req = conn.getresponse()
      #status = req.status
      #conn.close()

      #resp = req.read()
      #js = json.loads(resp.decode(self.sascfg.encoding))

      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      conn.request('GET', "/compute/sessions/"+self.pid+"/data/work/sasdata2dataframe/columns?start=0&limit=9999999", headers=headers)
      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      try:
         js = json.loads(resp.decode(self.sascfg.encoding))

         varlist = []
         vartype = []
         nvars = js.get('count')
         lst = js.get('items')
         for i in range(len(lst)):
            varlist.append(lst[i].get('name'))
            vartype.append(lst[i].get('type'))

         dvarlist = list(varlist)
         for i in range(len(varlist)):
            varlist[i] = varlist[i].replace("'", "''")
      except Exception as e:
         logger.error("Invalid output produced durring sasdata2dataframe step. Step failed.\
         \nPrinting the error: {}\nPrinting the SASLOG as diagnostic\n{}\
         \nPrinting the Status and Response as diagnostic\n{}\n{}".format(str(e), ll['LOG'], str(status), str(resp)))
         return None

      topts = dict(dsopts)
      topts.pop('firstobs', None)
      topts.pop('obs', None)

      code  = "data work._n_u_l_l_;output;run;\n"
      code += "data _null_; set work._n_u_l_l_ "+tabname+self._sb._dsopts(topts)+";put 'FMT_CATS=';\n"

      for i in range(nvars):
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "stop;\nrun;\nproc delete data=work._n_u_l_l_;run;"

      ll = self.submit(code, "text")

      try:
         l2 = ll['LOG'].rpartition("FMT_CATS=")
         l2 = l2[2].partition("\n")
         varcat = l2[2].split("\n", nvars)
         del varcat[nvars]
      except Exception as e:
         logger.error("Invalid output produced durring sasdata2dataframe step. Step failed.\
         \nPrinting the error: {}\nPrinting the SASLOG as diagnostic\n{}".format(str(e), ll['LOG']))
         return None

      code  = "proc delete data=work.sasdata2dataframe(memtype=view);run;\n"
      code += "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";\nformat "

      idx_col = kwargs.pop('index_col', False)
      eng     = kwargs.pop('engine',    'c')
      my_fmts = kwargs.pop('my_fmts',   False)
      k_dts   = kwargs.pop('dtype',     None)
      if k_dts is None and my_fmts:
         logger.warning("my_fmts option only valid when dtype= is specified. Ignoring and using necessary formatting for data transfer.")
         my_fmts = False

      if not my_fmts:
         for i in range(nvars):
            if vartype[i] == 'FLOAT':
               code += "'"+varlist[i]+"'n "
               if varcat[i] in self._sb.sas_date_fmts:
                  code += 'E8601DA10. '
                  if tsmax:
                     tscode += "if {} GE 110405 then {} = datepart('{}'dt);\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmax)
                     if tsmin:
                        tscode += "else if {} LE -103099 then {} = datepart('{}'dt);\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
                  elif tsmin:
                     tscode += "if {} LE -103099 then {} = datepart('{}'dt);\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
               else:
                  if varcat[i] in self._sb.sas_time_fmts:
                     code += 'E8601TM15.6 '
                  else:
                     if varcat[i] in self._sb.sas_datetime_fmts:
                        code += 'E8601DT26.6 '
                        if tsmax:
                           tscode += "if {} GE  9538991236.85477 then {} = '{}'dt;\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmax)
                           if tsmin:
                              tscode += "else if {} LE -8907752836.85477 then {} = '{}'dt;\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
                        elif tsmin:
                           tscode += "if {} LE -8907752836.85477 then {} = '{}'dt;\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
                     else:
                        code += 'best32. '
      code += ";run;\n"
      ll = self.submit(code, "text")

      if k_dts is None:
         dts = {}
         for i in range(nvars):
            if vartype[i] == 'FLOAT':
               if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  dts[dvarlist[i]] = 'float'
               else:
                  dts[dvarlist[i]] = 'str'
            else:
               dts[dvarlist[i]] = 'str'
      else:
         dts = k_dts

      code  = "filename _tomodsx '"+self._sb.workpath+"_tomodsx' lrecl="+str(self.sascfg.lrecl)+" recfm=v  encoding='utf-8';\n"
      code += "proc export data=work.sasdata2dataframe outfile=_tomodsx dbms=csv replace;\n"
      code += self._sb._expopts(opts)+" run;\n"
      code += "proc delete data=work.sasdata2dataframe(memtype=view);run;\n"
      code += "filename _tomodsx;"

      ll = self.submit(code, 'text')
      logf  = ll['LOG']

      code = "filename _sp_updn '"+self._sb.workpath+"_tomodsx' recfm=F encoding=binary lrecl=4096;"

      ll = self.submit(code, "text")
      logf += ll['LOG']

      # GET data
      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"*/*","Content-Type":"application/octet-stream",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('GET', self._uri_files+"/_sp_updn/content", headers=headers)
      req = conn.getresponse()
      status = req.status

      sockout = _read_sock(req=req)

      df = pd.read_csv(sockout, index_col=idx_col, encoding='utf8', engine=eng, dtype=dts, **kwargs)

      conn.close()

      if k_dts is None:  # don't override these if user provided their own dtypes
         for i in range(nvars):
            if vartype[i] == 'FLOAT':
               if varcat[i] in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  df[dvarlist[i]] = pd.to_datetime(df[dvarlist[i]], errors='coerce')

      code = "data _null_; rc = fdelete('_sp_updn'); run;\nfilename _sp_updn;"

      ll = self.submit(code, 'text')
      logf += ll['LOG']

      return df

   def sasdata2dataframeDISK(self, table: str, libref: str ='', dsopts: dict = None,
                             rowsep: str = '\x01', colsep: str = '\x02',
                             rowrep: str = ' ',    colrep: str = ' ', **kwargs) -> '<Pandas Data Frame object>':
      '''
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table    - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref   - the libref for the SAS Data Set.
      dsopts   - data set options for the input SAS Data Set
      rowsep   - the row seperator character to use; defaults to '\x01'
      colsep   - the column seperator character to use; defaults to '\x02'
      rowrep  - the char to convert to for any embedded rowsep chars, defaults to  ' '
      colrep  - the char to convert to for any embedded colsep chars, defaults to  ' '
      tempfile - DEPRECATED
      tempkeep - DEPRECATED

      These two options are for advanced usage. They override how saspy imports data. For more info
      see https://sassoftware.github.io/saspy/advanced-topics.html#advanced-sd2df-and-df2sd-techniques

      dtype   - this is the parameter to Pandas read_csv, overriding what saspy generates and uses
      my_fmts - bool: if True, overrides the formats saspy would use, using those on the data set or in dsopts=
      '''
      tmp = kwargs.pop('tempfile', None)
      tmp = kwargs.pop('tempkeep', None)

      tsmax = kwargs.pop('tsmax', None)
      tsmin = kwargs.pop('tsmin', None)
      tscode = ''

      errors = kwargs.pop('errors', 'strict')
      dsopts = dsopts if dsopts is not None else {}

      if libref:
         tabname = libref+".'"+table.strip().replace("'", "''")+"'n "
      else:
         tabname = "'"+table.strip().replace("'", "''")+"'n "

      code  = "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";run;\n"
      code += "data _null_; file LOG; d = open('work.sasdata2dataframe');\n"
      code += "lrecl = attrn(d, 'LRECL');\n"
      code += "lr='LRECL=';\n"
      code += "put lr lrecl;\n"
      code += "run;"

      ll = self.submit(code, "text")

      try:
         l2 = ll['LOG'].rpartition("LRECL= ")
         l2 = l2[2].partition("\n")
         lrecl = int(l2[0])
      except Exception as e:
         logger.error("Invalid output produced durring sasdata2dataframe step. Step failed.\
         \nPrinting the error: {}\nPrinting the SASLOG as diagnostic\n{}".format(str(e), ll['LOG']))
         return None

      ##GET Data Table Info
      #conn = self.sascfg.HTTPConn; conn.connect()
      #headers={"Accept":"application/vnd.sas.compute.data.table+json", "Authorization":"Bearer "+self.sascfg._token}
      #conn.request('GET', "/compute/sessions/"+self.pid+"/data/work/sasdata2dataframe", headers=headers)
      #req = conn.getresponse()
      #status = req.status
      #conn.close()

      #resp = req.read()
      #js = json.loads(resp.decode(self.sascfg.encoding))

      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      conn.request('GET', "/compute/sessions/"+self.pid+"/data/work/sasdata2dataframe/columns?start=0&limit=9999999", headers=headers)
      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      try:
         js = json.loads(resp.decode(self.sascfg.encoding))

         varlist = []
         vartype = []
         nvars = js.get('count')
         lst = js.get('items')
         for i in range(len(lst)):
            varlist.append(lst[i].get('name'))
            vartype.append(lst[i].get('type'))

         dvarlist = list(varlist)
         for i in range(len(varlist)):
            varlist[i] = varlist[i].replace("'", "''")
      except Exception as e:
         logger.error("Invalid output produced durring sasdata2dataframe step. Step failed.\
         \nPrinting the error: {}\nPrinting the SASLOG as diagnostic\n{}\
         \nPrinting the Status and Response as diagnostic\n{}\n{}".format(str(e), ll['LOG'], str(status), str(resp)))
         return None

      topts = dict(dsopts)
      topts.pop('firstobs', None)
      topts.pop('obs', None)

      code  = "proc delete data=work.sasdata2dataframe(memtype=view);run;"
      code += "data work._n_u_l_l_;output;run;\n"
      code += "data _null_; set work._n_u_l_l_ "+tabname+self._sb._dsopts(topts)+";put 'FMT_CATS=';\n"

      for i in range(nvars):
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "stop;\nrun;\nproc delete data=work._n_u_l_l_;run;"

      ll = self.submit(code, "text")

      try:
         l2 = ll['LOG'].rpartition("FMT_CATS=")
         l2 = l2[2].partition("\n")
         varcat = l2[2].split("\n", nvars)
         del varcat[nvars]
      except Exception as e:
         logger.error("Invalid output produced durring sasdata2dataframe step. Step failed.\
         \nPrinting the error: {}\nPrinting the SASLOG as diagnostic\n{}".format(str(e), ll['LOG']))
         return None

      rdelim = "'"+'%02x' % ord(rowsep.encode(self.sascfg.encoding))+"'x"
      cdelim = "'"+'%02x' % ord(colsep.encode(self.sascfg.encoding))+"'x "

      idx_col = kwargs.pop('index_col', False)
      eng     = kwargs.pop('engine',    'c')
      my_fmts = kwargs.pop('my_fmts',   False)
      k_dts   = kwargs.pop('dtype',     None)
      if k_dts is None and my_fmts:
         logger.warning("my_fmts option only valid when dtype= is specified. Ignoring and using necessary formatting for data transfer.")
         my_fmts = False

      code  = "filename _tomodsx '"+self._sb.workpath+"_tomodsx' recfm=v termstr=NL encoding='utf-8';\n"
      code += "data _null_; set "+tabname+self._sb._dsopts(dsopts)+";\n"

      if not my_fmts:
         for i in range(nvars):
            if vartype[i] == 'FLOAT':
               code += "format '"+varlist[i]+"'n "
               if varcat[i] in self._sb.sas_date_fmts:
                  code += 'E8601DA10.'
                  if tsmax:
                     tscode += "if {} GE 110405 then {} = datepart('{}'dt);\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmax)
                     if tsmin:
                        tscode += "else if {} LE -103099 then {} = datepart('{}'dt);\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
                  elif tsmin:
                     tscode += "if {} LE -103099 then {} = datepart('{}'dt);\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
               else:
                  if varcat[i] in self._sb.sas_time_fmts:
                     code += 'E8601TM15.6'
                  else:
                     if varcat[i] in self._sb.sas_datetime_fmts:
                        code += 'E8601DT26.6'
                        if tsmax:
                           tscode += "if {} GE  9538991236.85477 then {} = '{}'dt;\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmax)
                           if tsmin:
                              tscode += "else if {} LE -8907752836.85477 then {} = '{}'dt;\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
                        elif tsmin:
                           tscode += "if {} LE -8907752836.85477 then {} = '{}'dt;\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
                     else:
                        code += 'best32.'
               code += '; '
               if i % 10 == 9:
                  code +='\n'

      lreclx = max(self.sascfg.lrecl, (lrecl + nvars + 1))

      miss  = {}
      code += "\nfile _tomodsx lrecl="+str(lreclx)+" dlm="+cdelim+" recfm=v termstr=NL encoding='utf-8';\n"
      for i in range(nvars):
         if vartype[i] != 'FLOAT':
            code += "'"+varlist[i]+"'n = translate('"
            code +=     varlist[i]+"'n, '{}'x, '{}'x); ".format(   \
                        '%02x%02x' %                               \
                        (ord(rowrep.encode(self.sascfg.encoding)), \
                         ord(colrep.encode(self.sascfg.encoding))),
                        '%02x%02x' %                               \
                        (ord(rowsep.encode(self.sascfg.encoding)), \
                         ord(colsep.encode(self.sascfg.encoding))))
            miss[dvarlist[i]] = ' '
         else:
            code += "if missing('"+varlist[i]+"'n) then '"+varlist[i]+"'n = .; "
            miss[dvarlist[i]] = '.'
         if i % 10 == 9:
            code +='\n'
      code += "\nput "
      for i in range(nvars):
         code += " '"+varlist[i]+"'n "
         if i % 10 == 9:
            code +='\n'
      code += rdelim+";\nrun;\nfilename _tomodsx;"

      ll = self.submit(code, "text")

      if k_dts is None:
         dts = {}
         for i in range(nvars):
            if vartype[i] == 'FLOAT':
               if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  dts[dvarlist[i]] = 'float'
               else:
                  dts[dvarlist[i]] = 'str'
            else:
               dts[dvarlist[i]] = 'str'
      else:
         dts = k_dts

      quoting = kwargs.pop('quoting', 3)

      code = "filename _sp_updn '"+self._sb.workpath+"_tomodsx' recfm=F encoding=binary lrecl=4096;"

      ll = self.submit(code, "text")
      logf  = ll['LOG']

      # GET data
      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"*/*","Content-Type":"application/octet-stream",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('GET', self._uri_files+"/_sp_updn/content", headers=headers)
      req = conn.getresponse()
      status = req.status


      sockout = _read_sock(req=req, method='DISK', rsep=(colsep+rowsep+'\n').encode(), rowsep=rowsep.encode(), errors=errors)

      df = pd.read_csv(sockout, index_col=idx_col, engine=eng, header=None, names=dvarlist,
                       sep=colsep, lineterminator=rowsep, dtype=dts, na_values=miss, keep_default_na=False,
                       encoding='utf-8', quoting=quoting, **kwargs)

      conn.close()

      if k_dts is None:  # don't override these if user provided their own dtypes
         for i in range(nvars):
            if vartype[i] == 'FLOAT':
               if varcat[i] in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  df[dvarlist[i]] = pd.to_datetime(df[dvarlist[i]], errors='coerce')

      code = "data _null_; rc = fdelete('_sp_updn'); run;\nfilename _sp_updn;"

      ll = self.submit(code, 'text')
      logf += ll['LOG']

      return df

   def sasdata2parquet(self,
                       parquet_file_path: str,
                       table: str,
                       libref: str ='',
                       dsopts: dict = None,
                       pa_parquet_kwargs = None,
                       pa_pandas_kwargs  = None,
                       partitioned = False,
                       partition_size_mb = 128,
                       chunk_size_mb = 4,
                       coerce_timestamp_errors=True,
                       static_columns:list = None,
                       rowsep: str = '\x01',
                       colsep: str = '\x02',
                       rowrep: str = ' ',
                       colrep: str = ' ',
                       **kwargs) -> None:
      """
      This method exports the SAS Data Set to a Parquet file
      parquet_file_path       - path of the parquet file to create
      table                   - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref                  - the libref for the SAS Data Set.
      dsopts                  - data set options for the input SAS Data Set
      pa_parquet_kwargs       - Additional parameters to pass to pyarrow.parquet.ParquetWriter (default is {"compression": 'snappy', "flavor": "spark", "write_statistics": False}).
      pa_pandas_kwargs        - Additional parameters to pass to pyarrow.Table.from_pandas (default is {}).
      partitioned             - Boolean indicating whether the parquet file should be written in partitions (default is False).
      partition_size_mb       - The size in MB of each partition in memory (default is 128).
      chunk_size_mb           - The chunk size in MB at which the stream is processed (default is 4).
      coerce_timestamp_errors - Whether to coerce errors when converting timestamps (default is True).
      static_columns          - List of tuples (name, value) representing static columns that will be added to the parquet file (default is None).
      rowsep                  - the row seperator character to use; defaults to '\x01'
      colsep                  - the column seperator character to use; defaults to '\x02'
      rowrep                  - the char to convert to for any embedded rowsep chars, defaults to  ' '
      colrep                  - the char to convert to for any embedded colsep chars, defaults to  ' '

      These two options are for advanced usage. They override how saspy imports data. For more info
      see https://sassoftware.github.io/saspy/advanced-topics.html#advanced-sd2df-and-df2sd-techniques

      dtype                   - this is the parameter to Pandas read_csv, overriding what saspy generates and uses
      my_fmts                 - bool: if True, overrides the formats saspy would use, using those on the data set or in dsopts=
      """
      if not pa:
         logger.error("pyarrow was not imported. This method can't be used without it.")
         return None

      parquet_kwargs = pa_parquet_kwargs if pa_parquet_kwargs is not None else {"compression": 'snappy',
                                                                                "flavor":"spark",
                                                                                "write_statistics":False
                                                                                }
      pandas_kwargs  = pa_pandas_kwargs if pa_pandas_kwargs  is not None  else {}

      try:
         compression = parquet_kwargs["compression"]
      except KeyError:
         raise KeyError("The pa_parquet_kwargs dict needs to contain at least the parameter 'compression'. Default value is 'snappy'")

      tsmax = kwargs.pop('tsmax', None)
      tsmin = kwargs.pop('tsmin', None)
      tscode = ''

      errors = kwargs.pop('errors', 'strict')
      dsopts = dsopts if dsopts is not None else {}

      if libref:
         tabname = libref+".'"+table.strip().replace("'", "''")+"'n "
      else:
         tabname = "'"+table.strip().replace("'", "''")+"'n "

      code  = "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";run;\n"
      code += "data _null_; file LOG; d = open('work.sasdata2dataframe');\n"
      code += "lrecl = attrn(d, 'LRECL');\n"
      code += "lr='LRECL=';\n"
      code += "put lr lrecl;\n"
      code += "run;"

      ll = self.submit(code, "text")

      try:
         l2 = ll['LOG'].rpartition("LRECL= ")
         l2 = l2[2].partition("\n")
         lrecl = int(l2[0])
      except Exception as e:
         logger.error("Invalid output produced durring sasdata2dataframe step. Step failed.\
         \nPrinting the error: {}\nPrinting the SASLOG as diagnostic\n{}".format(str(e), ll['LOG']))
         return None

      ##GET Data Table Info
      #conn = self.sascfg.HTTPConn; conn.connect()
      #headers={"Accept":"application/vnd.sas.compute.data.table+json", "Authorization":"Bearer "+self.sascfg._token}
      #conn.request('GET', "/compute/sessions/"+self.pid+"/data/work/sasdata2dataframe", headers=headers)
      #req = conn.getresponse()
      #status = req.status
      #conn.close()

      #resp = req.read()
      #js = json.loads(resp.decode(self.sascfg.encoding))

      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      conn.request('GET', "/compute/sessions/"+self.pid+"/data/work/sasdata2dataframe/columns?start=0&limit=9999999", headers=headers)
      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      try:
         js = json.loads(resp.decode(self.sascfg.encoding))

         varlist = []
         vartype = []
         nvars = js.get('count')
         lst = js.get('items')
         for i in range(len(lst)):
            varlist.append(lst[i].get('name'))
            vartype.append(lst[i].get('type'))

         dvarlist = list(varlist)
         for i in range(len(varlist)):
            varlist[i] = varlist[i].replace("'", "''")
      except Exception as e:
         logger.error("Invalid output produced durring sasdata2dataframe step. Step failed.\
         \nPrinting the error: {}\nPrinting the SASLOG as diagnostic\n{}\
         \nPrinting the Status and Response as diagnostic\n{}\n{}".format(str(e), ll['LOG'], str(status), str(resp)))
         return None

      topts = dict(dsopts)
      topts.pop('firstobs', None)
      topts.pop('obs', None)

      code  = "proc delete data=work.sasdata2dataframe(memtype=view);run;"
      code += "data work._n_u_l_l_;output;run;\n"
      code += "data _null_; set work._n_u_l_l_ "+tabname+self._sb._dsopts(topts)+";put 'FMT_CATS=';\n"

      for i in range(nvars):
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "stop;\nrun;\nproc delete data=work._n_u_l_l_;run;"

      ll = self.submit(code, "text")

      try:
         l2 = ll['LOG'].rpartition("FMT_CATS=")
         l2 = l2[2].partition("\n")
         varcat = l2[2].split("\n", nvars)
         del varcat[nvars]
      except Exception as e:
         logger.error("Invalid output produced durring sasdata2dataframe step. Step failed.\
         \nPrinting the error: {}\nPrinting the SASLOG as diagnostic\n{}".format(str(e), ll['LOG']))
         return None

      rdelim = "'"+'%02x' % ord(rowsep.encode(self.sascfg.encoding))+"'x"
      cdelim = "'"+'%02x' % ord(colsep.encode(self.sascfg.encoding))+"'x "

      idx_col = kwargs.pop('index_col', False)
      eng     = kwargs.pop('engine',    'c')
      my_fmts = kwargs.pop('my_fmts',   False)
      k_dts   = kwargs.pop('dtype',     None)
      if k_dts is None and my_fmts:
         logger.warning("my_fmts option only valid when dtype= is specified. Ignoring and using necessary formatting for data transfer.")
         my_fmts = False

      code  = "filename _tomodsx '"+self._sb.workpath+"_tomodsx' recfm=v termstr=NL encoding='utf-8';\n"
      code += "data _null_; set "+tabname+self._sb._dsopts(dsopts)+";\n"

      if not my_fmts:
         for i in range(nvars):
            if vartype[i] == 'FLOAT':
               code += "format '"+varlist[i]+"'n "
               if varcat[i] in self._sb.sas_date_fmts:
                  code += 'E8601DA10.'
                  if tsmax:
                     tscode += "if {} GE 110405 then {} = datepart('{}'dt);\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmax)
                     if tsmin:
                        tscode += "else if {} LE -103099 then {} = datepart('{}'dt);\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
                  elif tsmin:
                     tscode += "if {} LE -103099 then {} = datepart('{}'dt);\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
               else:
                  if varcat[i] in self._sb.sas_time_fmts:
                     code += 'E8601TM15.6'
                  else:
                     if varcat[i] in self._sb.sas_datetime_fmts:
                        code += 'E8601DT26.6'
                        if tsmax:
                           tscode += "if {} GE  9538991236.85477 then {} = '{}'dt;\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmax)
                           if tsmin:
                              tscode += "else if {} LE -8907752836.85477 then {} = '{}'dt;\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
                        elif tsmin:
                           tscode += "if {} LE -8907752836.85477 then {} = '{}'dt;\n".format("'"+varlist[i]+"'n", "'"+varlist[i]+"'n",tsmin)
                     else:
                        code += 'best32.'
               code += '; '
               if i % 10 == 9:
                  code +='\n'

      lreclx = max(self.sascfg.lrecl, (lrecl + nvars + 1))

      miss  = {}
      code += "\nfile _tomodsx lrecl="+str(lreclx)+" dlm="+cdelim+" recfm=v termstr=NL encoding='utf-8';\n"
      for i in range(nvars):
         if vartype[i] != 'FLOAT':
            code += "'"+varlist[i]+"'n = translate('"
            code +=     varlist[i]+"'n, '{}'x, '{}'x); ".format(   \
                        '%02x%02x' %                               \
                        (ord(rowrep.encode(self.sascfg.encoding)), \
                         ord(colrep.encode(self.sascfg.encoding))),
                        '%02x%02x' %                               \
                        (ord(rowsep.encode(self.sascfg.encoding)), \
                         ord(colsep.encode(self.sascfg.encoding))))
            miss[dvarlist[i]] = ' '
         else:
            code += "if missing('"+varlist[i]+"'n) then '"+varlist[i]+"'n = .; "
            miss[dvarlist[i]] = '.'
         if i % 10 == 9:
            code +='\n'
      code += "\nput "
      for i in range(nvars):
         code += " '"+varlist[i]+"'n "
         if i % 10 == 9:
            code +='\n'
      code += rdelim+";\nrun;\nfilename _tomodsx;"

      ll = self.submit(code, "text")

      if k_dts is None:
         dts = {}
         for i in range(nvars):
            if vartype[i] == 'FLOAT':
               if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  dts[dvarlist[i]] = 'float'
               else:
                  dts[dvarlist[i]] = 'str'
            else:
               dts[dvarlist[i]] = 'str'
      else:
         dts = k_dts

      quoting = kwargs.pop('quoting', 3)

      code = "filename _sp_updn '"+self._sb.workpath+"_tomodsx' recfm=F encoding=binary lrecl=4096;"

      ll = self.submit(code, "text")
      logf  = ll['LOG']

      # GET data
      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"*/*","Content-Type":"application/octet-stream",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('GET', self._uri_files+"/_sp_updn/content", headers=headers)
      req = conn.getresponse()
      status = req.status

      #Define timestamp conversion functions
      def dt_string_to_float64(pd_series: pd.Series, coerce_timestamp_errors: bool) -> pd.Series:
         """
         This function converts a pandas Series of datetime strings to a Series of float64,
         handling NaN values and optionally coercing errors to NaN.
         """

         if coerce_timestamp_errors:
            # define conversion with error handling
            def convert(date_str):
               try:
                     return np.datetime64(date_str, 'ms').astype(np.float64)
               except ValueError:
                     return np.nan
            # vectorize for pandas
            vectorized_convert = np.vectorize(convert, otypes=[np.float64])
         else:
            # define conversion without error handling
            convert = lambda date_str: np.datetime64(date_str, 'ms').astype(np.float64)
            # vectorize for pandas
            vectorized_convert = np.vectorize(convert, otypes=[np.float64])

         result = vectorized_convert(pd_series)

         return pd.Series(result, index=pd_series.index)

      def dt_string_to_int64(pd_series: pd.Series, coerce_timestamp_errors: bool) -> pd.Series:
         """
         This function converts a pandas Series of datetime strings to a Series of Int64,
         handling NaN values and optionally coercing errors to NaN.
         """
         float64_series = dt_string_to_float64(pd_series, coerce_timestamp_errors)
         return float64_series.astype('Int64')

      ##### DEFINE SCHEMA #####

      def dts_to_pyarrow_schema(dtype_dict):
         # Define a mapping from string type names to pyarrow data types
         type_mapping = {
            'str': pa.string(),
            'float': pa.float64(),
            'int': pa.int64(),
            'bool': pa.bool_(),
            'date': pa.date32(),
            'timestamp': pa.timestamp('ms'),
            # python types
            str: pa.string(),
            float: pa.float64(),
            int: pa.int64(),
            bool: pa.bool_(),
            datetime.date: pa.timestamp('ms'),
            datetime.datetime: pa.timestamp('ms'),
            np.datetime64: pa.timestamp('ms')
         }

         # Create a list of pyarrow fields from the dictionary
         fields = []
         i=0
         for column_name, dtype in dtype_dict.items():
            pa_type = type_mapping.get(dtype)
            if pa_type is None:
               logging.warning(f"Unknown data type '{dtype} of column {column_name}. Will try cast to string")
               pa_type = pa.string()
         # account for timestamp columns
            if vartype[i] == 'N':
               if varcat[i] in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  pa_type = pa.timestamp('ms')
            fields.append(pa.field(column_name, pa_type))
            i+=1
         #add static columns to schema, if given
         if static_columns:
            for column_name, value in static_columns:
               py_type = type_mapping.get(type(value))
               if py_type is None:
                  logging.warning(f"Unknown data type '{dtype} of column {column_name}. Will try cast to string")
                  pa_type = pa.string()
               fields.append(pa.field(column_name, py_type))
         # Create a pyarrow schema from the list of fields
         schema = pa.schema(fields)
         return schema
      # derive parque schema if not defined by user.
      if "schema" not in parquet_kwargs or parquet_kwargs["schema"] is None:
         custom_schema = False
         parquet_kwargs["schema"] = dts_to_pyarrow_schema(dts)
      else:
         custom_schema = True
      pandas_kwargs["schema"] = parquet_kwargs["schema"]

      ##### START STERAM #####
      parquet_writer = None
      partition = 1
      loop = 1
      chunk_size = chunk_size_mb*1024*1024 #convert to bytes
      data_read = 0
      rows_read = 0

      try:
         sockout = _read_sock(req=req, method='DISK', rsep=(colsep+rowsep+'\n').encode(), rowsep=rowsep.encode(), errors=errors)
         logging.info("Socket ready, waiting for results...")

         # determine how many chunks should be written into one partition.
         chunks_in_partition = int(partition_size_mb/chunk_size_mb)
         if chunks_in_partition == 0:
            raise ValueError("Partition size needs to be larger than chunk size")
         while True:
            # 4 MB seems to be the most efficient chunk size, but could vary

            chunk = sockout.read(chunk_size)
            #check if query yields any results
            if loop == 1:
               logging.info("Stream ready")
            if loop == 1 and chunk == '':
               logging.warning("Query returned no rows.")
               return
            # create directory if partitioned
            elif loop == 1 and partitioned:
               os.makedirs(parquet_file_path)

            if chunk == '':
               logging.info("Done")
               break
            # for spark, it is better if large files are split over multiple partitions,
            # so that all worker nodes can be used to read the data
            if partitioned:
               #batch chunks into one partition
               if loop % chunks_in_partition == 0:
                  logging.info("Closing partition "+str(partition).zfill(5))
                  partition += 1
                  parquet_writer.close()
                  parquet_writer = None
               path = f"{parquet_file_path}/{str(partition).zfill(5)}.{compression}.parquet"
            else:
               path = parquet_file_path

            try:
               df = pd.read_csv(io.StringIO(chunk), index_col=idx_col, engine=eng, header=None, names=dvarlist,
                                sep=colsep, lineterminator=rowsep, dtype=dts, na_values=miss, keep_default_na=False,
                                encoding='utf-8', quoting=quoting, **kwargs)

               for col in df.columns:
                  if df[col].isnull().all():
                     df[col] = df[col].astype(dts[col])
                     df[col] = np.nan

               rows_read += len(df)
               if static_columns:
                  df[[col[0] for col in static_columns]] = tuple([col[1] for col in static_columns])

               if k_dts is None:  # don't override these if user provided their own dtypes
                  for i in range(nvars):
                     if vartype[i] == 'N':
                        if varcat[i] in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:

                           if coerce_timestamp_errors:
                              df[dvarlist[i]] = dt_string_to_int64(df[dvarlist[i]],coerce_timestamp_errors)
                           else:
                              try:
                                 df[dvarlist[i]] = dt_string_to_int64(df[dvarlist[i]],coerce_timestamp_errors)
                              except ValueError:
                                 raise ValueError(f"""The column {dvarlist[i]} contains an unparseable timestamp.
   Consider setting a different pd_timestamp_format or set coerce_timestamp_errors = True and they will be cast as Null""")

               pa_table = pa.Table.from_pandas(df,**pandas_kwargs)

               if not custom_schema:
                  #cast the int64 columns to timestamp
                  for i in range(nvars):
                     if vartype[i] == 'N':
                        if varcat[i] in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                           # Cast the integer column to the timestamp type using pyarrow.compute.cast
                           casted_column = pc.cast(pa_table[dvarlist[i]], pa.timestamp('ms'))
                           # Replace int64 with timestamp column
                           pa_table = pa_table.set_column(pa_table.column_names.index(dvarlist[i]), dvarlist[i], casted_column)

            except Exception as e:
            #### If parsing a chunk fails, the csv chunk is written to disk and the expression to read the csv using pandas is printed
               failed_path= os.path.abspath(path+"_failed")
               logging.error(f"Parsing chunk #{loop} failed, see {failed_path}/failedchunk.csv")
               if os.path.isdir(failed_path):
                  shutil.rmtree(failed_path)
               os.makedirs(failed_path)
               with open(f"{failed_path}/failedchunk.csv", "w",encoding='utf-8') as log:
                  log.write(chunk)
               logging.error(f"""
                              #Read the chunk using:
                              import pandas as pd
                              df = pd.read_csv(
                                 '{failed_path}/failedchunk.csv',
                                 index_col={idx_col},
                                 engine='{eng}',
                                 header=None,
                                 names={dvarlist},
                                 sep={colsep!r},
                                 lineterminator={rowsep!r},
                                 dtype={dts},
                                 na_values={miss},
                                 encoding='utf-8',
                                 quoting={quoting},
                                 **{kwargs}
                              )"""
               )
               raise e

            if not parquet_writer:
               if "schema" not in parquet_kwargs or parquet_kwargs["schema"] is None:
                  parquet_kwargs["schema"] = pa_table.schema
               parquet_writer = pq.ParquetWriter(path,**parquet_kwargs)#use_deprecated_int96_timestamps=True,

            # Write the table chunk to the Parquet file
            parquet_writer.write_table(pa_table)
            loop += 1
            data_read += chunk_size
            if loop % 30 == 0:
               logging.info(f"{round(data_read/1024/1024/1024,3)} GB / {rows_read} rows read so far") #Convert bytes to GB => bytes /1024³

         logging.info(f"Finished reading {round(data_read/1024/1024/1024,3)} GB / {rows_read} rows.")
         logging.info(str(pa_table.schema))
      except:
         raise
      finally:
         conn.close()
         code = "data _null_; rc = fdelete('_sp_updn'); run;\nfilename _sp_updn;"

         ll = self.submit(code, 'text')
         logf += ll['LOG']
         if parquet_writer:
            parquet_writer.close()

      return

class _read_sock(io.StringIO):
   def __init__(self, **kwargs):
      self.req      = kwargs.get('req')
      self.method   = kwargs.get('method', 'CSV')
      self.rowsep   = kwargs.get('rowsep', b'\n')
      self.rsep     = kwargs.get('rsep', self.rowsep)
      self.errs     = kwargs.get('errors', 'strict')
      self.datar    = b""

   def read(self, size=4096):
      datl    = 0
      size    = max(size, 4096)
      notarow = True

      while datl < size or notarow:
         data = self.req.read(size)
         dl = len(data)

         if dl:
            datl       += dl
            self.datar += data
            if notarow:
               notarow = self.datar.count(self.rsep) <= 0
         else:
            if len(self.datar) <= 0:
               return ''
            else:
               break

      data        = self.datar.rpartition(self.rsep)
      if self.method == 'DISK':
         datap    = (data[0]+data[1]).replace(self.rsep, self.rowsep)
      else:
         datap    = data[0]+data[1]
      self.datar  = data[2]

      return datap.decode(errors=self.errs)

