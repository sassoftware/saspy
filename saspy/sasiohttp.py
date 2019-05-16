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

import tempfile as tf
from time import sleep

try:
   import pandas as pd
   import numpy  as np
except ImportError:
   pass

class SASconfigHTTP:
   '''
   This object is not intended to be used directly. Instantiate a SASsession object instead 
   '''
   def __init__(self, session, **kwargs):
      self._kernel  = kwargs.get('kernel', None)   
      self._token   = None

      SAScfg         = session._sb.sascfg.SAScfg
      self.name      = session._sb.sascfg.name
      cfg            = getattr(SAScfg, self.name)

      self.ip        = cfg.get('ip', '')
      self.port      = cfg.get('port', None)
      self.ctxname   = cfg.get('context', '')
      self.ctx       = {}
      self.options   = cfg.get('options', [])
      self.ssl       = cfg.get('ssl', True)
      self.verify    = cfg.get('verify', True)
      user           = cfg.get('user', '')
      pw             = cfg.get('pw', '')
      self.encoding  = cfg.get('encoding', '')
      self.authkey   = cfg.get('authkey', '')
      self._prompt   = session._sb.sascfg._prompt
      self.lrecl     = cfg.get('lrecl', None)

      try:
         self.outopts = getattr(SAScfg, "SAS_output_options")
         self.output  = self.outopts.get('output', 'html5')
      except:
         self.output  = 'html5'

      if self.output.lower() not in ['html', 'html5']:
         print("Invalid value specified for SAS_output_options. Using the default of HTML5")
         self.output  = 'html5'

      # GET Config options
      try:
         self.cfgopts = getattr(SAScfg, "SAS_config_options")
      except:
         self.cfgopts = {}

      lock = self.cfgopts.get('lock_down', True)
      # in lock down mode, don't allow runtime overrides of option values from the config file.

      inip = kwargs.get('ip', '')             
      if len(inip) > 0:
         if lock and len(self.ip):
            print("Parameter 'ip' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.ip = inip   

      inport = kwargs.get('port', None)         
      if inport:
         if lock and self.port:
            print("Parameter 'port' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.port = inport

      inctxname = kwargs.get('context', '')   
      if len(inctxname) > 0:
         if lock and len(self.ctxname):
            print("Parameter 'context' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.ctxname = inctxname

      inoptions = kwargs.get('options', [])   
      if len(inoptions) > 0:
         if lock and len(self.options):
           print("Parameter 'options' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.options = inoptions

      inssl = kwargs.get('ssl', None)         
      if inssl is not None:
         if lock and self.ssl:
            print("Parameter 'ssl' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.ssl = bool(inssl)

      inver = kwargs.get('verify', None)         
      if inver is not None:
         if lock and self.ssl:
            print("Parameter 'verify' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.verify = bool(inver)

      inuser = kwargs.get('user', '')              
      if len(inuser) > 0:
         if lock and len(user):
            print("Parameter 'user' passed to SAS_session was ignored due to configuration restriction.")
         else:
            user = inuser

      inpw = kwargs.get('pw', '')                  
      if len(inpw) > 0:
         if lock and len(pw):
            print("Parameter 'pw' passed to SAS_session was ignored due to configuration restriction.")
         else:
            pw = inpw

      inencoding = kwargs.get('encoding', 'NoOverride')
      if inencoding != 'NoOverride':
         if lock and len(self.encoding):
            print("Parameter 'encoding' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.encoding = inencoding   
      if not self.encoding:
         self.encoding = 'utf_8'

      inlrecl = kwargs.get('lrecl', None)
      if inlrecl:
         if lock and self.lrecl:
            print("Parameter 'lrecl' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.lrecl = inlrecl
      if not self.lrecl:
         self.lrecl = 1048576

      inak = kwargs.get('authkey', '')
      if len(inak) > 0:
         if lock and len(self.authkey):
            print("Parameter 'authkey' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.authkey = inak   

      while len(self.ip) == 0:
         if not lock:
            self.ip = self._prompt("Please enter the host (ip address) you are trying to connect to: ")
         else:
            print("In lockdown mode and missing ip adress in the config named: "+cfgname )
            return

      if not self.port:
         if self.ssl:
            port = 443
         else:
            port = 80

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
                  user = line.partition('user')[2].lstrip().partition(' ')[0].partition('\n')[0]
                  pw   = line.partition('password')[2].lstrip().partition(' ')[0].partition('\n')[0]
                  found = True
                  break
            fid.close()
         except OSError as e:
            print('Error trying to read authinfo file:'+pwf+'\n'+str(e))
            pass
         except:
            pass
   
         if not found:
            print('Did not find key '+self.authkey+' in authinfo file:'+pwf+'\n')

      while len(user) == 0:
         user = self._prompt("Please enter userid: ")
         if user is None:
            self._token = None
            return 

      while len(pw) == 0:
         pw = self._prompt("Please enter password: ", pw = True)
         if pw is None:
            self._token = None
            return 

      if self.ssl:
         if self.verify:
            # handle having self signed certificate default on Viya w/out copies on client; still ssl, just not verifyable
            try:
               self.HTTPConn = hc.HTTPSConnection(self.ip, self.port)
               self._token = self._authenticate(user, pw)
            except ssl.SSLError as e:
               print("SSL connection failed, creating an unverified ssl connection. Error was:"+str(e))
               self.HTTPConn = hc.HTTPSConnection(self.ip, self.port, context=ssl._create_unverified_context())
               print("You can set 'verify=False' to get rid of this message ")
               self._token   = self._authenticate(user, pw)
         else:
            self.HTTPConn = hc.HTTPSConnection(self.ip, self.port, context=ssl._create_unverified_context())
            self._token = self._authenticate(user, pw)
      else:
         self.HTTPConn = hc.HTTPConnection(self.ip, self.port)
         self._token   = self._authenticate(user, pw)

      # get AuthToken
      #self._token = self._authenticate(user, pw)

      if not self._token:
         print("Could not acquire an Authentication Token")
         return

      # GET Contexts 
      contexts = self._get_contexts()
      if contexts == None:
         self._token = None
         return 

      ctxnames = []
      for i in range(len(contexts)):
         ctxnames.append(contexts[i].get('name'))

      if len(self.ctxname) == 0:
         if len(ctxnames) == 0:
            print("No Contexts found on Compute Service at ip=" + self.ip)
            self._token = None
            return 
         else:
            if len(ctxnames) == 1:
               self.ctxname = ctxnames[0]
               print("Using SAS Context: " + self.ctxname)
            else:
               self.ctxname = self._prompt("Please enter the SAS Context you wish to run. Available contexts are: " +
                                            str(ctxnames)+" ")
               if self.ctxname is None:
                  self._token = None
                  return 

      while self.ctxname not in ctxnames:
         if not lock:
            createctx = self._prompt(
                "SAS Context specified was not found. Do you want to create a new context named "+self.ctxname+" [Yes|No]?")
            if createctx.upper() in ('YES', 'Y'):
               contexts = self._create_context(user)
            else:
               self.ctxname = self._prompt(
                   "SAS Context specified was not found. Please enter the SAS Context you wish to run. Available contexts are: " + 
                    str(ctxnames)+" ")
               if self.ctxname is None:
                  self._token = None
                  return 
         else:
            msg  = "SAS Context specified in the SASconfig ("+self.ctxname+") was not found on this server, and because " 
            msg += "the SASconfig is in lockdown mode, there is no prompting for other contexts. No connection established."
            print(msg)
            self._token = None
            return 

      for i in range(len(contexts)):
         if contexts[i].get('name') == self.ctxname:
            self.ctx = contexts[i]
            break

      return

   def _authenticate(self, user, pw):
      #import pdb; pdb.set_trace()

      # POST AuthToken
      conn = self.HTTPConn; conn.connect()
      d1 = ("grant_type=password&username="+user+"&password="+pw).encode(self.encoding)
      basic = base64.encodebytes("sas.tkmtrb:".encode(self.encoding))
      authheader = '%s' % basic.splitlines()[0].decode(self.encoding)
      headers={"Accept":"application/vnd.sas.compute.session+json","Content-Type":"application/x-www-form-urlencoded",
               "Authorization":"Basic "+authheader}
      try:
         conn.request('POST', "/SASLogon/oauth/token", body=d1, headers=headers)
         req = conn.getresponse()
      except:
         import sys
         print("Failure in GET AuthToken. Could not connect to the logon service. Exception info:\n"+str(sys.exc_info()))
         return None

      status = req.status
      resp = req.read()
      conn.close()

      if status > 299:
         print("Failure in GET AuthToken. Status="+str(status)+"\nResponse="+resp.decode(self.encoding))
         return None

      js = json.loads(resp.decode(self.encoding))
      token = js.get('access_token')
      return token

   def _get_contexts(self):
      #import pdb; pdb.set_trace()

      # GET Contexts 
      conn = self.HTTPConn; conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json",
               "Accept-Item":"application/vnd.sas.compute.context.summary+json",
               "Authorization":"Bearer "+self._token}
      conn.request('GET', "/compute/contexts", headers=headers)
      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      if status > 299:
         print("Failure in GET Contexts. Status="+str(status)+"\nResponse="+resp.decode(self.encoding))
         return None

      js = json.loads(resp.decode(self.encoding))
      contexts = js.get('items')

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
         print("Failure in POST Context. Status="+str(status)+"\nResponse="+resp.decode(self.encoding))
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
      for ld in self.sascfg.ctx.get('links'):
         if ld.get('method') == 'POST':
            uri = ld.get('uri')
            break

      conn = self.sascfg.HTTPConn; conn.connect()
      d1 = '{"name":"'+self.sascfg.ctxname+'", "description":"saspy session", "version":1, "environment":{"options":'+options+'}}'
      headers={"Accept":"application/vnd.sas.compute.session+json","Content-Type":"application/vnd.sas.compute.session.request+json","Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', uri, body=d1, headers=headers)
      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      if status > 299:
         print("Failure in POST Session \n"+resp.decode(self.sascfg.encoding))
         print("Could not acquire a SAS Session for context: "+self.sascfg.ctxname)
         return None

      self._session = json.loads(resp.decode(self.sascfg.encoding))

      if self._session == None:
         print("Could not acquire a SAS Session for context: "+self.sascfg.ctxname)
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

      self._log = self._getlog()

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

      jobid = json.loads(resp.decode(self.sascfg.encoding))
      if not jobid or status > 299:
         print("Compute server had issues starting:\n")
         for key in jobid:
            print(key+"="+str(jobid.get(key)))
         return None

      self.submit("options svgtitle='svgtitle'; options validvarname=any pagesize=max nosyntaxcheck; ods graphics on;", "text")
      print("SAS server started using Context "+self.sascfg.ctxname+" with SESSION_ID="+self.pid)       

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

         print("SAS server terminated for SESSION_ID="+self._session.get('id'))       
         self._session   = None
         self.pid        = None
         self._sb.SASpid = None
      return rc


   def _getlog(self, jobid=None):
      start = 0
      logr = ''

      # GET Log
      if jobid:
         lines = 9999999 #jobid.get('logInfo').get('lineCount')
         for ld in jobid.get('links'):
            if ld.get('method') == 'GET' and ld.get('rel') == 'log':
               uri = ld.get('uri')
               break
      else:
         lines = 9999999 #self._session.get('logStatistics').get('lineCount')
         uri   = self._uri_log

      while True:
         # GET Log
         conn = self.sascfg.HTTPConn; conn.connect()
         headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
         conn.request('GET', uri+"?start="+str(start)+"&limit="+str(lines+1), headers=headers)
         req = conn.getresponse()
         status = req.status
         resp = req.read()
         conn.close()

         js  = json.loads(resp.decode(self.sascfg.encoding))
         log = js.get('items')

         lines = len(log)

         if not lines:
            break
         start += lines

         for i in range(len(log)):
             line = dict(log[i]).get('line')
             logr += line+'\n'

      if jobid != None:   
         self._log += logr

      return logr

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

      js = json.loads(resp.decode(self.sascfg.encoding))
      results = js.get('items')

      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      while i < len(results):
         # GET an ODS Result
         if results[i].get('type') == 'ODS':
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
         lines = 9999999 #jobid.get('listInfo').get('lineCount')
      else:
         lines = 9999999 #self._session.get('listingStatistics').get('lineCount')
         uri   = self._uri_lst

      while True:
         conn = self.sascfg.HTTPConn; conn.connect()
         headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
         conn.request('GET', uri+"?start="+str(start)+"&limit="+str(lines+1), headers=headers)
         req = conn.getresponse()
         status = req.status
         resp = req.read()
         conn.close()

         js  = json.loads(resp.decode(self.sascfg.encoding))
         lst = js.get('items')

         lines = len(lst)

         if not lines:
            break
         start += lines

         for i in range(len(lst)):
             line = dict(lst[i]).get('line')
             lstr += line+'\n'

      return lstr

   def _asubmit(self, code, results="html"):
      #odsopen  = json.dumps("ods listing close;ods html5 (id=saspy_internal) options(bitmap_mode='inline') device=png; ods graphics on / outputfmt=png;\n")
      #odsopen  = json.dumps("ods listing close;ods html5 (id=saspy_internal) options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n")
      #odsclose = json.dumps("ods html5 (id=saspy_internal) close;ods listing;\n")
      odsopen  = json.dumps("ods listing close;ods "+self.sascfg.output+" (id=saspy_internal) options(bitmap_mode='inline') device=svg style="+self._sb.HTML_Style+"; ods graphics on / outputfmt=png;\n")
      odsclose = json.dumps("ods "+self.sascfg.output+" (id=saspy_internal) close;ods listing;\n")
      ods      = True;

      if results.upper() != "HTML":
         ods = False
         odsopen  = '""'
         odsclose = '""'
   
      # POST Job
      conn = self.sascfg.HTTPConn; conn.connect()
      jcode = json.dumps(code)
      d1 = '{"code":['+odsopen+','+jcode+','+odsclose+']}'
      headers={"Accept":"application/json","Content-Type":"application/vnd.sas.compute.job.request+json",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', self._uri_exe, body=d1, headers=headers)
      req = conn.getresponse()
      resp = req.read()
      conn.close()

      jobid = json.loads(resp.decode(self.sascfg.encoding))

      return jobid

   def submit(self, code: str, results: str ="html", prompt: dict = []) -> dict:
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
      #odsopen  = json.dumps("ods listing close;ods html5 (id=saspy_internal) options(bitmap_mode='inline') device=png; ods graphics on / outputfmt=png;\n")
      #odsopen  = json.dumps("ods listing close;ods html5 (id=saspy_internal) options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n")
      #odsclose = json.dumps("ods html5 (id=saspy_internal) close;ods listing;\n")
      odsopen  = json.dumps("ods listing close;ods "+self.sascfg.output+" (id=saspy_internal) options(bitmap_mode='inline') device=svg style="+self._sb.HTML_Style+"; ods graphics on / outputfmt=png;\n")
      odsclose = json.dumps("ods "+self.sascfg.output+" (id=saspy_internal) close;ods listing;\n")
      ods      = True;
      pcodei   = ''
      pcodeiv  = ''
      pcodeo   = ''

      if self._session == None:
         print("No SAS process attached. SAS process has terminated unexpectedly.")
         return dict(LOG="No SAS process attached. SAS process has terminated unexpectedly.", LST='')

      if results.upper() != "HTML":
         ods = False
         odsopen  = '""'
         odsclose = '""'
   
      if len(prompt):
         pcodei += 'options nosource nonotes;\n'
         pcodeo += 'options nosource nonotes;\n'
         for key in prompt:
            gotit = False
            while not gotit:
               var = self.sascfg._prompt('Please enter value for macro variable '+key+' ', pw=prompt[key])
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

      # POST Job
      conn = self.sascfg.HTTPConn; conn.connect()
      jcode = json.dumps(pcodei+pcodeiv+code+'\n'+pcodeo)
      d1 = '{"code":['+odsopen+','+jcode+','+odsclose+']}'
      headers={"Accept":"application/json","Content-Type":"application/vnd.sas.compute.job.request+json",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', self._uri_exe, body=d1, headers=headers)
      req = conn.getresponse()
      status = req.status
      resp = req.read()
      conn.close()

      jobid = json.loads(resp.decode(self.sascfg.encoding))
      if not jobid or status > 299:
         print("Problem submitting job to Compute Service.\n   Status code="+str(jobid.get('httpStatusCode'))+"\n   Message="+jobid.get('message'))
         return dict(LOG=str(jobid), LST='')

      for ld in jobid.get('links'):
         if ld.get('method') == 'GET' and ld.get('rel') == 'state':
            uri = ld.get('uri')
            break

      conn    = self.sascfg.HTTPConn; conn.connect()
      headers = {"Accept":"text/plain", "Authorization":"Bearer "+self.sascfg._token}
      done    = False

      while not done:
         try:
            while True:
               # GET Status for JOB
               conn.request('GET', uri, headers=headers)
               req = conn.getresponse()
               resp = req.read()
               if resp not in [b'running', 'pending']:
                  done = True
                  break
               sleep(.5)
         except (KeyboardInterrupt, SystemExit):
            print('Exception caught!')
            response = self.sascfg._prompt(
                      "SAS attention handling not yet supported over HTTP. Please enter (Q) to Quit waiting for results or (C) to continue waiting.")
            while True:
               if response.upper() == 'Q':
                  conn.close()
                  return dict(LOG='', LST='', BC=True)
               if response.upper() == 'C':
                  break
               response = self.sascfg._prompt("Please enter (Q) to Quit waiting for results or (C) to continue waiting.")

      conn.close()

      logd = self._getlog(jobid)

      if ods:
         lstd = self._getlst(jobid)
      else:
         lstd = self._getlsttxt(jobid)

      return dict(LOG=logd, LST=lstd)

   def saslog(self):
      '''
      this method is used to get the current, full contents of the SASLOG
      '''
      return self._getlog()

   def exist(self, table: str, libref: str ="") -> bool:
      '''
      table  - the name of the SAS Data Set
      libref - the libref for the Data Set, defaults to WORK, or USER if assigned

      Returns True it the Data Set exists and False if it does not
      '''
      #can't have an empty libref, so check for user or work
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
   
   def read_csv(self, file: str, table: str, libref: str ="", nosub: bool=False, opts: dict ={}) -> '<SASdata object>':
      '''
      This method will import a csv file into a SAS Data Set and return the SASdata object referring to it.
      file    - eithe the OS filesystem path of the file, or HTTP://... for a url accessible file
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      opts    - a dictionary containing any of the following Proc Import options(datarow, delimiter, getnames, guessingrows)
      '''
      code  = "filename x "
   
      if file.lower().startswith("http"):
         code += "url "
   
      code += "\""+file+"\";\n"
      code += "proc import datafile=x out="
      if len(libref):
         code += libref+"."
      code += table+" dbms=csv replace; "+self._sb._impopts(opts)+" run;"
   
      if nosub:
         print(code)
      else:
         ll = self.submit(code, "text")
   
   def write_csv(self, file: str, table: str, libref: str ="", nosub: bool =False, dsopts: dict ={}, opts: dict ={}) -> 'The LOG showing the results of the step':
      '''
      This method will export a SAS Data Set to a file in CCSV format.
      file    - the OS filesystem path of the file to be created (exported from the SAS Data Set)
      table   - the name of the SAS Data Set you want to export to a CSV file
      libref  - the libref for the SAS Data Set.
      opts    - a dictionary containing any of the following Proc Export options(delimiter, putnames)
      '''
      code  = "filename x \""+file+"\";\n"
      code += "options nosource;\n"
      code += "proc export data="+libref+"."+table+self._sb._dsopts(dsopts)+" outfile=x dbms=csv replace; "
      code += self._sb._expopts(opts)+" run\n;"
      code += "options source;\n"

      if nosub:
         print(code)
      else:
         ll = self.submit(code, "text")
         return ll['LOG']

   def upload(self, localfile: str, remotefile: str, overwrite: bool = True, permission: str = '', **kwargs):
      """
      This method uploads a local file to the SAS servers file system.
      localfile  - path to the local file to upload 
      remotefile - path to remote file to create or overwrite
      overwrite  - overwrite the output file if it exists?
      permission - permissions to set on the new file. See SAS Filename Statement Doc for syntax
      """
      valid = self._sb.file_info(remotefile, quiet = True)

      if valid is None:
         remf = remotefile
      else:
         if valid == {}:
            remf = remotefile + self._sb.hostsep + localfile.rpartition(os.sep)[2]
         else:
            remf = remotefile
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

         while True:
            buf = fd.read1(32768)
            if len(buf) == 0:
               conn.send(b"0\r\n\r\n")
               break

            lenstr = "%s\r\n" % hex(len(buf))[2:]
            conn.send(lenstr.encode())
            conn.send(buf)
            conn.send(b"\r\n")

         req    = conn.getresponse()
         status = req.status
         resp   = req.read()
         conn.close()
         print("status="+str(status))
         print("resp="+resp.decode())

         code = "filename _sp_updn;"
      else:
         log1 = ''
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

      return {'Success' : True, 
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

      fd.write(req.read())
      fd.flush()
      fd.close()
      conn.close()

      ll = self.submit("filename _sp_updn;", 'text')
      logf += ll['LOG']
      
      return {'Success' : True, 
              'LOG'     : logf}
 
   def _getbytelen(self, x):
      return len(x.encode(self.sascfg.encoding))

   def dataframe2sasdata(self, df: '<Pandas Data Frame object>', table: str ='a', 
                         libref: str ="", keep_outer_quotes: bool=False):
      '''
      This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      keep_outer_quotes - for character columns, have SAS keep any outer quotes instead of stripping them off.
      '''
      input  = ""
      card   = ""
      format = ""
      length = ""
      dts    = []
      ncols  = len(df.columns)

      for name in range(ncols):
         input += "'"+str(df.columns[name])+"'n "
         if df.dtypes[df.columns[name]].kind in ('O','S','U','V'):
            try:
               col_l = df[df.columns[name]].astype(str).apply(self._getbytelen).max()
            except Exception as e:
               print("Transcoding error encountered.")
               print("DataFrame contains characters that can't be transcoded into the SAS session encoding.\n"+str(e))
               return None
            if col_l == 0:
               col_l = 8
            length += " '"+str(df.columns[name])+"'n $"+str(col_l)
            if keep_outer_quotes:
               input  += "~ "
            dts.append('C')
         else:
            if df.dtypes[df.columns[name]].kind in ('M'):
               length += " '"+str(df.columns[name])+"'n 8"
               input  += ":E8601DT26.6 "
               format += "'"+str(df.columns[name])+"'n E8601DT26.6 "
               dts.append('D')
            else:
               length += " '"+str(df.columns[name])+"'n 8"
               if df.dtypes[df.columns[name]] == 'bool':
                  dts.append('B')
               else:
                  dts.append('N')

      code = "data "
      if len(libref):
         code += libref+"."
      code += table+";\n"
      if len(length):
         code += "length "+length+";\n"
      if len(format):
         code += "format "+format+";\n"
      code += "infile datalines delimiter='03'x DSD STOPOVER;\ninput @;\nif _infile_ = '' then delete;\ninput "+input+";\ndatalines4;"
      self._asubmit(code, "text")

      code = ""
      for row in df.itertuples(index=False):
         card  = ""
         for col in range(ncols):
            var = str(row[col])

            if   dts[col] == 'N' and var == 'nan':
               var = '.'
            elif dts[col] == 'C' and var == 'nan':
               var = ' '
            elif dts[col] == 'B':
               var = str(int(row[col]))
            elif dts[col] == 'D':
               if var == 'nan':
                  var = '.'
               else:
                  var = str(row[col].to_datetime64())[:26]

            card += var
            if col < (ncols-1):
               card += chr(3)
         code += card+"\n"
         if len(code) > 4000:
            self._asubmit(code, "text")
            code = ""

      self._asubmit(code+";;;;", "text")
      ll = self.submit("run;", 'text')
      return

   def sasdata2dataframe(self, table: str, libref: str ='', dsopts: dict ={}, **kwargs) -> '<Pandas Data Frame object>':
      '''
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table   - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref  - the libref for the SAS Data Set.
      '''

      method = kwargs.pop('method', None)
      if method and method.lower() == 'csv':
         return self.sasdata2dataframeCSV(table, libref, dsopts, **kwargs)

      if libref:
         tabname = libref+"."+table
      else:
         tabname = table

      code  = "proc sql; create view work.sasdata2dataframe as select * from "+tabname+self._sb._dsopts(dsopts)+";quit;\n"

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

      js = json.loads(resp.decode(self.sascfg.encoding))

      varlist = []
      vartype = []
      nvars = js.get('count')
      lst = js.get('items')
      for i in range(len(lst)):
         varlist.append(lst[i].get('name'))
         vartype.append(lst[i].get('type'))

      code  = "data _null_; set work.sasdata2dataframe(obs=1);put 'FMT_CATS=';\n"
      for i in range(nvars):
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "run;\n"
   
      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("FMT_CATS=")
      l2 = l2[2].partition("\n")              
      varcat = l2[2].split("\n", nvars)
      del varcat[nvars]

      code  = "data work.saspy_ds2df / view=work.saspy_ds2df; set "+tabname+self._sb._dsopts(dsopts)+";\n format "
      for i in range(nvars):
         if vartype[i] == 'FLOAT':
            if varcat[i] in self._sb.sas_date_fmts:
               code += "'"+varlist[i]+"'n E8601DA10. "
            else:
               if varcat[i] in self._sb.sas_time_fmts:
                  code += "'"+varlist[i]+"'n E8601TM15.6 "
               else:
                  if varcat[i] in self._sb.sas_datetime_fmts:
                     code += "'"+varlist[i]+"'n E8601DT26.6 "
                  else:
                     code += "'"+varlist[i]+"'n best32. "
      code += ";run;\n"
      ll = self.submit(code, "text")

      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      uri = "/compute/sessions/"+self.pid+"/data/work/saspy_ds2df/rows"

      r     = []
      df    = None
      trows = kwargs.get('trows', None)
      if not trows:
         trows = 100000

      while True:
         conn.request('GET', uri, headers=headers)
         req    = conn.getresponse()
         status = req.status
         resp   = req.read()
         conn.close()
   
         js = json.loads(resp.decode(self.sascfg.encoding))
   
         lst = js.get('items')

         if not lst:
            break

         for i in range(len(lst)):
            r.append(lst[i]['cells'])

         if len(r) > trows:   
            tdf = pd.DataFrame.from_records(r, columns=varlist)
                       
            for i in range(nvars):
               if vartype[i] == 'FLOAT':
                  if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                     if tdf.dtypes[tdf.columns[i]].kind not in ('f','u','i','b','B','c','?'):
                        tdf[varlist[i]] = pd.to_numeric(tdf[varlist[i]], errors='coerce') 
                  else:
                     if tdf.dtypes[tdf.columns[i]].kind not in ('M'):
                        tdf[varlist[i]] = pd.to_datetime(tdf[varlist[i]], errors='coerce') 
               else:
                  tdf[varlist[i]] = tdf[varlist[i]].apply(str.strip)
                  tdf[varlist[i]].replace('', np.NaN, True)
                                          
            if df is not None:
               df = df.append(tdf, ignore_index=True)
            else:
               df = tdf
            r = []
               
         uri = None
         for ld in js.get('links'):
            if ld.get('method') == 'GET' and ld.get('rel') == 'next':
               uri = ld.get('uri')
               break

         if not uri:
            break

      if len(r) > 0:   
         tdf = pd.DataFrame.from_records(r, columns=varlist)

         for i in range(nvars):
            if vartype[i] == 'FLOAT':
               if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  tdf[varlist[i]] = pd.to_numeric(tdf[varlist[i]], errors='coerce') 
               else:
                  tdf[varlist[i]] = pd.to_datetime(tdf[varlist[i]], errors='ignore') 
            else:
               tdf[varlist[i]] = tdf[varlist[i]].apply(str.strip)
               tdf[varlist[i]].replace('', np.NaN, True)

         if df is not None:
            df = df.append(tdf, ignore_index=True)
         else:
            df = tdf

      return df


   def sasdata2dataframeCSV(self, table: str, libref: str ='', dsopts: dict ={}, tempfile: str=None, tempkeep: bool=False, **kwargs) -> '<Pandas Data Frame object>':
      '''
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table    - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref   - the libref for the SAS Data Set.
      dsopts   - data set options for the input SAS Data Set
      tempfile - file to use to store CSV, else temporary file will be used.
      tempkeep - if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it
      '''

      if libref:
         tabname = libref+"."+table
      else:
         tabname = table

      tmpdir  = None

      if tempfile is None:
         tmpdir = tf.TemporaryDirectory()
         tmpcsv = tmpdir.name+os.sep+"tomodsx"
      else:
         tmpcsv  = tempfile

      code  = "proc sql; create view work.sasdata2dataframe as select * from "+tabname+self._sb._dsopts(dsopts)+";quit;\n"

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

      js = json.loads(resp.decode(self.sascfg.encoding))

      varlist = []
      vartype = []
      nvars = js.get('count')
      lst = js.get('items')
      for i in range(len(lst)):
         varlist.append(lst[i].get('name'))
         vartype.append(lst[i].get('type'))

      code  = "data _null_; set work.sasdata2dataframe(obs=1);put 'FMT_CATS=';\n"
      for i in range(nvars):
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "run;\n"
   
      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("FMT_CATS=")
      l2 = l2[2].partition("\n")              
      varcat = l2[2].split("\n", nvars)
      del varcat[nvars]

      code  = "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";\nformat "
      for i in range(nvars):
         if vartype[i] == 'FLOAT':
            if varcat[i] in self._sb.sas_date_fmts:
               code += "'"+varlist[i]+"'n E8601DA10. "
            else:
               if varcat[i] in self._sb.sas_time_fmts:
                  code += "'"+varlist[i]+"'n E8601TM15.6 "
               else:
                  if varcat[i] in self._sb.sas_datetime_fmts:
                     code += "'"+varlist[i]+"'n E8601DT26.6 "
                  else:
                     code += "'"+varlist[i]+"'n best32. "
      code += ";run;\n"
      ll = self.submit(code, "text")

      conn = self.sascfg.HTTPConn; conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      uri = "/compute/sessions/"+self.pid+"/data/work/saspy_ds2df/rows"

      dts = kwargs.pop('dtype', '')
      if dts == '':
         dts = {}
         for i in range(nvars):
            if vartype[i] == 'FLOAT':
               if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  dts[varlist[i]] = 'float'
               else:
                  dts[varlist[i]] = 'str'
            else:
               dts[varlist[i]] = 'str'

      #code += "options nosource;\n"
      code  = "filename _tomodsx '"+self._sb.workpath+"_tomodsx' lrecl="+str(self.sascfg.lrecl)+" recfm=v  encoding='utf-8';\n"
      code += "proc export data=work.sasdata2dataframe outfile=_tomodsx dbms=csv replace; run\n;"
      #code += "options source;\n"

      ll = self.submit(code, 'text')

      ll = self.download(tmpcsv, self._sb.workpath+"_tomodsx")

      df = pd.read_csv(tmpcsv, index_col=False, engine='c', dtype=dts, **kwargs)

      for i in range(nvars):
         if varcat[i] in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
            df[varlist[i]] = pd.to_datetime(df[varlist[i]], errors='coerce')

      return df


if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(_getlog())
    print(_getlsttxt())

    endsas()

