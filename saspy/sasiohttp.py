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
import getpass

from time import sleep

try:
   import saspy.sascfg_personal as SAScfg
except ImportError:
   import saspy.sascfg as SAScfg

try:
   import pandas as pd
   from IPython.display import HTML
except ImportError:
   pass

class SASconfigHTTP:
   '''
   This object is not intended to be used directly. Instantiate a SASsession object instead 
   '''
   #def __init__(self, cfgname='', kernel=None, user='', pw='', ip='', port='', context='', options=[]):
   def __init__(self, **kwargs):
      self._kernel  = kwargs.get('kernel', None)   
      self._token   = None

      self.name     = kwargs.get('sascfgname', '')  
      cfg           = getattr(SAScfg, self.name) 

      self.ip       = cfg.get('ip', '')
      self.port     = cfg.get('port', None)
      self.ctxname  = cfg.get('context', '')
      self.options  = cfg.get('options', [])
      user          = cfg.get('user', '')
      pw            = cfg.get('pw', '')
      self.encoding = cfg.get('encoding', '')

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

      inencoding = kwargs.get('encoding', '')
      if len(inencoding) > 0:
         if lock and len(self.encoding):
            print("Parameter 'encoding' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.encoding = inencoding   
      if not self.encoding:
         self.encoding = 'utf-8'  

      while len(self.ip) == 0:
         if not lock:
            self.ip = self._prompt("Please enter the host (ip address) you are trying to connect to: ")
         else:
            print("In lockdown mode and missing ip adress in the config named: "+cfgname )
            return

      if not self.port:
         port = 80

      while len(user) == 0:
         user = self._prompt("Please enter userid: ")

      while len(pw) == 0:
         pw = self._prompt("Please enter password: ", pw = True)

      # get AuthToken
      self._token = self._authenticate(user, pw)

      if not self._token:
         print("Could not acquire an Authentication Token")
         return

      # GET Contexts 
      self.contexts = self._get_contexts()
      if self.contexts == None:
         self._token = None
         return 

      if len(self.ctxname) == 0:
         if len(self.contexts) == 0:
            print("No Contexts found on Compute Service at ip=" + self.ip)
            self._token = None
            return 
         else:
            if len(self.contexts) == 1:
               self.ctxname = self.contexts[0]
               print("Using SAS Context: " + self.ctxname)
            else:
               self.ctxname = self._prompt("Please enter the SAS Context you wish to run. Available contexts are: " +
                                           str(self.contexts)+" ")

      while self.ctxname not in self.contexts:
         if not lock:
            self.ctxname = self._prompt(
                "SAS Context specified was not found. Please enter the SAS Context you wish to run. Available contexts are: " + 
                 str(self.contexts)+" ")
         else:
            msg  = "SAS Context specified in the SASconfig ("+self.ctxname+") was not found on this server, and because " 
            msg += "the SASconfig is in lockdown mode, there is no prompting for other contexts. No connection established."
            print(msg)
            self._token = None
            return 

   def _prompt(self, prompt, pw=False):
      if self._kernel is None:
          if not pw:
              try:
                 return input(prompt)
              except (KeyboardInterrupt):
                 return ''
          else:
              try:
                 return getpass.getpass(prompt)
              except (KeyboardInterrupt):
                 return ''
      else:
          try:
             return self._kernel._input_request(prompt, self._kernel._parent_ident, self._kernel._parent_header,
                                                password=pw)
          except (KeyboardInterrupt):
             return ''
                   
   def _authenticate(self, user, pw):
      #import pdb; pdb.set_trace()

      # POST AuthToken
      conn = hc.HTTPConnection(self.ip, self.port);conn.connect()
      d1 = ("grant_type=password&username="+user+"&password="+pw).encode(self.sascfg.encoding)
      basic = base64.encodestring("sas.tkmtrb:".encode(self.sascfg.encoding))
      authheader = '%s' % basic.splitlines()[0].decode(self.sascfg.encoding)
      headers={"Accept":"application/vnd.sas.compute.session+json","Content-Type":"application/x-www-form-urlencoded",
               "Authorization":"Basic "+authheader}
      try:
         conn.request('POST', "/SASLogon/oauth/token", body=d1, headers=headers)
         req = conn.getresponse()
      except:
         import sys
         print("Failure in GET AuthToken. Could not connect to the logon service. Exception info:\n"+str(sys.exc_info()))
         return None

      status = req.getcode(self.sascfg.encoding)
      resp = req.read()
      conn.close()

      if status > 299:
         print("Failure in GET AuthToken. Status="+str(status)+"\nResponse="+resp.decode(self.sascfg.encoding))
         return None

      js = json.loads(resp.decode(self.sascfg.encoding))
      token = js.get('access_token')
      return token

   def _get_contexts(self):
      #import pdb; pdb.set_trace()
      contexts = []

      # GET Contexts 
      conn = hc.HTTPConnection(self.ip, self.port);conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json","Authorization":"Bearer "+self._token}
      conn.request('GET', "/compute/contexts", headers=headers)
      req = conn.getresponse()
      status = req.getcode(self.sascfg.encoding)
      resp = req.read()
      conn.close()

      if status > 299:
         print("Failure in GET Contexts. Status="+str(status)+"\nResponse="+resp.decode(self.sascfg.encoding))
         return None

      js = json.loads(resp.decode(self.sascfg.encoding))
      items = js.get('items')

      for i in range(len(items)):
          contexts.append(dict(items[i]).get('name')) 
         
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
      self.sascfg     = SASconfigHTTP(**kwargs)
      self._sessionid = None
      self._sb        = kwargs.get('sb', None)

      if self.sascfg._token:
         self._startsas()

   def __del__(self):
      if self._sessionid:
         self._endsas()
      self._sessionid = None

   def _startsas(self):
      if len(self.sascfg.options):
         options = '[';
         for opt in self.sascfg.options:
            options += '"'+opt+'", '
         options = (options.rpartition(','))[0]+']'                                
      else:
         options = '[]'

      # POST Session
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
      d1 = '{"name":"'+self.sascfg.ctxname+'", "description":"saspy session", "version":1, "environment":{"options":'+options+'}}'
      headers={"Accept":"*/*","Content-Type":"application/vnd.sas.compute.session.request+json","Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', "/compute/sessions?contextName="+self.sascfg.ctxname, body=d1, headers=headers)
      req = conn.getresponse()
      status = req.getcode(self.sascfg.encoding)
      resp = req.read()
      conn.close()

      if status > 299:
         print("Failure in POST Session \n"+resp.decode(self.sascfg.encoding))
         print("Could not acquire a SAS Session for context: "+self.sascfg.ctxname)
         return None

      js = json.loads(resp.decode(self.sascfg.encoding))
      self._sessionid = js.get('id')

      if self._sessionid == None:
         print("Could not acquire a SAS Session for context: "+self.sascfg.ctxname)
         return None
      
      self._log = self._getlog()
          
      self.submit("options svgtitle='svgtitle'; options validvarname=any; ods graphics on;", "text")
      print("SAS server started using Context "+self.sascfg.ctxname+" with SESSION_ID="+self._sessionid)       
   
   def _endsas(self):
      rc = 0
      if self._sessionid:
         # DELETE Session
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
         headers={"Accept":"*/*","Content-Type":"application/vnd.sas.compute.session.request+json","Authorization":"Bearer "+self.sascfg._token}
         conn.request('DELETE', "/compute/sessions/"+self._sessionid, headers=headers)
         req = conn.getresponse()
         resp = req.read()
         conn.close()

         print("SAS server terminated for SESSION_ID="+self._sessionid)       
         self._sessionid = None
      return rc


   def _getlog(self, jobid=None):
      start = 0
      logr = ''

      while True:
         # GET Log
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
         headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
         if jobid:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/log?start="+str(start)+"&limit=999999", headers=headers)
         else:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/log?start="+str(start)+"&limit=999999", headers=headers)
         req = conn.getresponse()
         status = req.getcode(self.sascfg.encoding)
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
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      if jobid:
         conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/results?includeTypes=ODS", headers=headers)
      else:
         conn.request('GET', "/compute/sessions/"+self._sessionid+"/results", headers=headers)
      req = conn.getresponse()
      status = req.getcode(self.sascfg.encoding)
      resp = req.read()
      conn.close()

      js = json.loads(resp.decode(self.sascfg.encoding))
      results = js.get('items')

      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      while i < len(results):
         # GET an ODS Result
         if results[i].get('type') == 'ODS':
            conn.request('GET', results[i].get('links')[0].get('href'), headers=headers)
            req = conn.getresponse()
            status = req.getcode(self.sascfg.encoding)
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
   
      while True:
         # GET Log
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
         headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
         if jobid:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/listing?start="+str(start)+"limit=999999", headers=headers)
         else:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/listing?start="+str(start)+"limit=999999", headers=headers)
         req = conn.getresponse()
         status = req.getcode(self.sascfg.encoding)
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
      odsopen  = json.dumps("ods listing close;ods html5 (id=saspy_internal) options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n")
      odsclose = json.dumps("ods html5 (id=saspy_internal) close;ods listing;\n")
      ods      = True;

      if results.upper() != "HTML":
         ods = False
         odsopen  = '""'
         odsclose = '""'
   
      # POST Job
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
      jcode = json.dumps(code)
      d1 = '{"code":['+odsopen+','+jcode+','+odsclose+']}'
      headers={"Accept":"application/json","Content-Type":"application/vnd.sas.compute.job.request+json",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', "/compute/sessions/"+self._sessionid+"/jobs", body=d1, headers=headers)
      req = conn.getresponse()
      resp = req.read()
      conn.close()

      js = json.loads(resp.decode(self.sascfg.encoding))
      jobid = js.get('id')

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
      odsopen  = json.dumps("ods listing close;ods html5 (id=saspy_internal) options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n")
      odsclose = json.dumps("ods html5 (id=saspy_internal) close;ods listing;\n")
      ods      = True;
      pcodei   = ''
      pcodeiv  = ''
      pcodeo   = ''

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
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
      jcode = json.dumps(pcodei+pcodeiv+code+'\n'+pcodeo)
      d1 = '{"code":['+odsopen+','+jcode+','+odsclose+']}'
      headers={"Accept":"application/json","Content-Type":"application/vnd.sas.compute.job.request+json",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', "/compute/sessions/"+self._sessionid+"/jobs", body=d1, headers=headers)
      req = conn.getresponse()
      resp = req.read()
      conn.close()

      js = json.loads(resp.decode(self.sascfg.encoding))
      jobid = js.get('id')
      if not jobid:
         print("Problem submitting job to Compute Service.\n   Status code="+str(js.get('httpStatusCode'))+"\n   Message="+js.get('message'))
         return dict(LOG=j, LST='')

      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
      headers={"Accept":"text/plain", "Authorization":"Bearer "+self.sascfg._token}
      done = False

      while not done:
         try:
            while True:
               # GET Status for JOB
               conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/state", headers=headers)
               req = conn.getresponse()
               resp = req.read()
               if resp == b'completed':
                  done = True
                  break
               sleep(.5)
         except (KeyboardInterrupt, SystemExit):
            print('Exception caught!')
            response = self.sascfg._prompt(
                      "SAS attention handling not yet supported over HTTP. Please enter (Q) to Quit waiting for results or (C) to continue waiting.")
            while True:
               if response.upper() == 'Q':
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
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
         headers={"Accept":"*/*", "Authorization":"Bearer "+self.sascfg._token}
         # this is broke now, always says it's there, so set to work for now till it's fixed
         #conn.request('HEAD', "/compute/sessions/"+self._sessionid+"/data/user", headers=headers)

         conn.request('HEAD', "/compute/sessions/"+self._sessionid+"/data/WORK", headers=headers)
         req = conn.getresponse()
         status = req.getcode(self.sascfg.encoding)
         conn.close()
    
         if status == 200:
            libref = 'USER'
         else:
            libref = 'WORK'

      # HEAD Data Table
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
      headers={"Accept":"*/*", "Authorization":"Bearer "+self.sascfg._token}
      conn.request('HEAD', "/compute/sessions/"+self._sessionid+"/data/"+libref+"/"+table, headers=headers)
      req = conn.getresponse()
      status = req.getcode(self.sascfg.encoding)
      conn.close()

      if status == 200:
         exists = True
      else:
         exists = False
   
      return exists
   
   def read_csv(self, file: str, table: str, libref: str ="", nosub: bool=False) -> '<SASdata object>':
      '''
      This method will import a csv file into a SAS Data Set and return the SASdata object referring to it.
      file    - eithe the OS filesystem path of the file, or HTTP://... for a url accessible file
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      '''
      print("read_csv is not currently implemented in this SAS Connection Interface; HTTP")
      return None
      
      code  = "filename x "
   
      if file.lower().startswith("http"):
         code += "url "
   
      code += "\""+file+"\";\n"
      code += "proc import datafile=x out="
      if len(libref):
         code += libref+"."
      code += table+" dbms=csv replace; run;"
   
      if nosub:
         print(code)
      else:
         ll = self._io.submit(code, "text")
   
   def write_csv(self, file: str, table: str, libref: str ="", nosub: bool =False, dsopts: dict ={}) -> 'The LOG showing the results of the step':
      '''
      This method will export a SAS Data Set to a file in CCSV format.
      file    - the OS filesystem path of the file to be created (exported from the SAS Data Set)
      table   - the name of the SAS Data Set you want to export to a CSV file
      libref  - the libref for the SAS Data Set.
      '''
      print("write_csv is not currently implemented in this SAS Connection Interface; HTTP")
      return None

   def dataframe2sasdata(self, df: '<Pandas Data Frame object>', table: str ='a', libref: str =""):
      '''
      This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      '''
      print("dataframe2sasdata is not currently implemented in this SAS Connection Interface; HTTP")
      return None

   def sasdata2dataframe(self, table: str, libref: str ='', dsopts: dict ={}) -> '<Pandas Data Frame object>':
      '''
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table   - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref  - the libref for the SAS Data Set.
      '''
      print("sasdata2dataframe is not currently FULLY implemented in this SAS Connection Interface; HTTP")
      #import pandas as pd

      # GET Data Table      I don't think this is necessary at all - maybe to get the links?
      #conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
      #headers={"Accept":"application/vnd.sas.compute.data.table+json", "Authorization":"Bearer "+self.sascfg._token}
      #conn.request('GET', "/compute/sessions/"+self._sessionid+"/data/"+libref+"/"+table, headers=headers)
      #req = conn.getresponse()
      #status = req.getcode(self.sascfg.encoding)
      #conn.close()

      #resp = req.read()
      #js = json.loads(resp.decode(self.sascfg.encoding))

      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      conn.request('GET', "/compute/sessions/"+self._sessionid+"/data/"+libref+"/"+table+"/columns", headers=headers)
      req = conn.getresponse()
      status = req.getcode(self.sascfg.encoding)
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

      code  = "data _null_; set "+libref+"."+table+"(obs=1);put 'FMT_CATS=';\n"
      for i in range(nvars):
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "run;\n"
   
      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("FMT_CATS=")
      l2 = l2[2].partition("\n")              
      varcat = l2[2].split("\n", nvars)
      del varcat[nvars]


      '''   until view access start working  or I can supply my own formats
      code  = "data work.saspy_ds2df / view=work.saspy_ds2df; set "+libref+"."+table+";\n format "
      for i in range(nvars):
         if vartype[i] == 'FLOAT':
            if varcat[i] in sas_date_fmts:
               code += "'"+varlist[i]+"'n E8601DA10. "
            else:
               if varcat[i] in sas_time_fmts:
                  code += "'"+varlist[i]+"'n E8601TM15.6 "
               else:
                  if varcat[i] in sas_datetime_fmts:
                     code += "'"+varlist[i]+"'n E8601DT26.6 "
                  else:
                     code += "'"+varlist[i]+"'n best32. "
      code += ";run;\n"
      ll = self.submit(code, "text")
      '''
      code  = "data work.saspy_ds2df / view=work.saspy_ds2df; set "+libref+"."+table+";\n format "
      for i in range(nvars):
         if vartype[i] == 'FLOAT':
            if varcat[i] in sas_date_fmts:
               code += "'"+varlist[i]+"'n E8601DA10. "
            else:
               if varcat[i] in sas_time_fmts:
                  code += "'"+varlist[i]+"'n E8601TM15.6 "
               else:
                  if varcat[i] in sas_datetime_fmts:
                     code += "'"+varlist[i]+"'n E8601DT26.6 "
                  else:
                     code += "'"+varlist[i]+"'n best32. "
      code += ";run;\n"
      ll = self.submit(code, "text")







      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port);conn.connect()
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}

      #    until view access start working  or I can supply my own formats
      conn.request('GET', "/compute/sessions/"+self._sessionid+"/data/WORK/saspy_ds2df/rows", headers=headers)

      #conn.request('GET', "/compute/sessions/"+self._sessionid+"/data/"+libref+"/"+table+"/rows", headers=headers)
      req = conn.getresponse()
      status = req.getcode(self.sascfg.encoding)
      resp = req.read()
      conn.close()

      js = json.loads(resp.decode(self.sascfg.encoding))

      r = []
      lst = js.get('items')
      for i in range(len(lst)):
         r.append(lst[i]['cells'])

      df = pd.DataFrame.from_records(r, columns=varlist)

      for i in range(nvars):
         if vartype[i] == 'N':
            if varcat[i] not in sas_date_fmts + sas_time_fmts + sas_datetime_fmts:
               df[varlist[i]] = pd.to_numeric(df[varlist[i]], errors='coerce') 
            else:
               df[varlist[i]] = pd.to_datetime(df[varlist[i]], errors='ignore') 

      return df

if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(_getlog())
    print(_getlsttxt())

    endsas()

sas_date_fmts = (
'AFRDFDD','AFRDFDE','AFRDFDE','AFRDFDN','AFRDFDWN','AFRDFMN','AFRDFMY','AFRDFMY','AFRDFWDX','AFRDFWKX','ANYDTDTE','B8601DA',
'B8601DA','B8601DJ','CATDFDD','CATDFDE','CATDFDE','CATDFDN','CATDFDWN','CATDFMN','CATDFMY','CATDFMY','CATDFWDX','CATDFWKX',
'CRODFDD','CRODFDE','CRODFDE','CRODFDN','CRODFDWN','CRODFMN','CRODFMY','CRODFMY','CRODFWDX','CRODFWKX','CSYDFDD','CSYDFDE',
'CSYDFDE','CSYDFDN','CSYDFDWN','CSYDFMN','CSYDFMY','CSYDFMY','CSYDFWDX','CSYDFWKX','DANDFDD','DANDFDE','DANDFDE','DANDFDN',
'DANDFDWN','DANDFMN','DANDFMY','DANDFMY','DANDFWDX','DANDFWKX','DATE','DATE','DAY','DDMMYY','DDMMYY','DDMMYYB',
'DDMMYYC','DDMMYYD','DDMMYYN','DDMMYYP','DDMMYYS','DESDFDD','DESDFDE','DESDFDE','DESDFDN','DESDFDWN','DESDFMN','DESDFMY',
'DESDFMY','DESDFWDX','DESDFWKX','DEUDFDD','DEUDFDE','DEUDFDE','DEUDFDN','DEUDFDWN','DEUDFMN','DEUDFMY','DEUDFMY','DEUDFWDX',
'DEUDFWKX','DOWNAME','E8601DA','E8601DA','ENGDFDD','ENGDFDE','ENGDFDE','ENGDFDN','ENGDFDWN','ENGDFMN','ENGDFMY','ENGDFMY',
'ENGDFWDX','ENGDFWKX','ESPDFDD','ESPDFDE','ESPDFDE','ESPDFDN','ESPDFDWN','ESPDFMN','ESPDFMY','ESPDFMY','ESPDFWDX','ESPDFWKX',
'EURDFDD','EURDFDE','EURDFDE','EURDFDN','EURDFDWN','EURDFMN','EURDFMY','EURDFMY','EURDFWDX','EURDFWKX','FINDFDD','FINDFDE',
'FINDFDE','FINDFDN','FINDFDWN','FINDFMN','FINDFMY','FINDFMY','FINDFWDX','FINDFWKX','FRADFDD','FRADFDE','FRADFDE','FRADFDN',
'FRADFDWN','FRADFMN','FRADFMY','FRADFMY','FRADFWDX','FRADFWKX','FRSDFDD','FRSDFDE','FRSDFDE','FRSDFDN','FRSDFDWN','FRSDFMN',
'FRSDFMY','FRSDFMY','FRSDFWDX','FRSDFWKX','HUNDFDD','HUNDFDE','HUNDFDE','HUNDFDN','HUNDFDWN','HUNDFMN','HUNDFMY','HUNDFMY',
'HUNDFWDX','HUNDFWKX','IS8601DA','IS8601DA','ITADFDD','ITADFDE','ITADFDE','ITADFDN','ITADFDWN','ITADFMN','ITADFMY','ITADFMY',
'ITADFWDX','ITADFWKX','JDATEMD','JDATEMDW','JDATEMNW','JDATEMON','JDATEQRW','JDATEQTR','JDATESEM','JDATESMW','JDATEWK','JDATEYDW',
'JDATEYM','JDATEYMD','JDATEYMD','JDATEYMW','JNENGO','JNENGO','JNENGOW','JULDATE','JULDAY','JULIAN','JULIAN','MACDFDD',
'MACDFDE','MACDFDE','MACDFDN','MACDFDWN','MACDFMN','MACDFMY','MACDFMY','MACDFWDX','MACDFWKX','MINGUO','MINGUO','MMDDYY',
'MMDDYY','MMDDYYB','MMDDYYC','MMDDYYD','MMDDYYN','MMDDYYP','MMDDYYS','MMYY','MMYYC','MMYYD','MMYYN','MMYYP',
'MMYYS','MONNAME','MONTH','MONYY','MONYY','ND8601DA','NENGO','NENGO','NLDATE','NLDATE','NLDATEL','NLDATEM',
'NLDATEMD','NLDATEMDL','NLDATEMDM','NLDATEMDS','NLDATEMN','NLDATES','NLDATEW','NLDATEW','NLDATEWN','NLDATEYM','NLDATEYML','NLDATEYMM',
'NLDATEYMS','NLDATEYQ','NLDATEYQL','NLDATEYQM','NLDATEYQS','NLDATEYR','NLDATEYW','NLDDFDD','NLDDFDE','NLDDFDE','NLDDFDN','NLDDFDWN',
'NLDDFMN','NLDDFMY','NLDDFMY','NLDDFWDX','NLDDFWKX','NORDFDD','NORDFDE','NORDFDE','NORDFDN','NORDFDWN','NORDFMN','NORDFMY',
'NORDFMY','NORDFWDX','NORDFWKX','POLDFDD','POLDFDE','POLDFDE','POLDFDN','POLDFDWN','POLDFMN','POLDFMY','POLDFMY','POLDFWDX',
'POLDFWKX','PTGDFDD','PTGDFDE','PTGDFDE','PTGDFDN','PTGDFDWN','PTGDFMN','PTGDFMY','PTGDFMY','PTGDFWDX','PTGDFWKX','QTR',
'QTRR','RUSDFDD','RUSDFDE','RUSDFDE','RUSDFDN','RUSDFDWN','RUSDFMN','RUSDFMY','RUSDFMY','RUSDFWDX','RUSDFWKX','SLODFDD',
'SLODFDE','SLODFDE','SLODFDN','SLODFDWN','SLODFMN','SLODFMY','SLODFMY','SLODFWDX','SLODFWKX','SVEDFDD','SVEDFDE','SVEDFDE',
'SVEDFDN','SVEDFDWN','SVEDFMN','SVEDFMY','SVEDFMY','SVEDFWDX','SVEDFWKX','WEEKDATE','WEEKDATX','WEEKDAY','WEEKU','WEEKU',
'WEEKV','WEEKV','WEEKW','WEEKW','WORDDATE','WORDDATX','XYYMMDD','XYYMMDD','YEAR','YYMM','YYMMC','YYMMD',
'YYMMDD','YYMMDD','YYMMDDB','YYMMDDC','YYMMDDD','YYMMDDN','YYMMDDP','YYMMDDS','YYMMN','YYMMN','YYMMP','YYMMS',
'YYMON','YYQ','YYQ','YYQC','YYQD','YYQN','YYQP','YYQR','YYQRC','YYQRD','YYQRN','YYQRP',
'YYQRS','YYQS','YYQZ','YYQZ','YYWEEKU','YYWEEKV','YYWEEKW',
)

sas_time_fmts = (
'ANYDTTME','B8601LZ','B8601LZ','B8601TM','B8601TM','B8601TZ','B8601TZ','E8601LZ','E8601LZ','E8601TM','E8601TM','E8601TZ',
'E8601TZ','HHMM','HOUR','IS8601LZ','IS8601LZ','IS8601TM','IS8601TM','IS8601TZ','IS8601TZ','JTIMEH','JTIMEHM','JTIMEHMS',
'JTIMEHW','JTIMEMW','JTIMESW','MMSS','ND8601TM','ND8601TZ','NLTIMAP','NLTIMAP','NLTIME','NLTIME','STIMER','TIME',
'TIME','TIMEAMPM','TOD',
)

sas_datetime_fmts = (
'AFRDFDT','AFRDFDT','ANYDTDTM','B8601DN','B8601DN','B8601DT','B8601DT','B8601DZ','B8601DZ','CATDFDT','CATDFDT','CRODFDT',
'CRODFDT','CSYDFDT','CSYDFDT','DANDFDT','DANDFDT','DATEAMPM','DATETIME','DATETIME','DESDFDT','DESDFDT','DEUDFDT','DEUDFDT',
'DTDATE','DTMONYY','DTWKDATX','DTYEAR','DTYYQC','E8601DN','E8601DN','E8601DT','E8601DT','E8601DZ','E8601DZ','ENGDFDT',
'ENGDFDT','ESPDFDT','ESPDFDT','EURDFDT','EURDFDT','FINDFDT','FINDFDT','FRADFDT','FRADFDT','FRSDFDT','FRSDFDT','HUNDFDT',
'HUNDFDT','IS8601DN','IS8601DN','IS8601DT','IS8601DT','IS8601DZ','IS8601DZ','ITADFDT','ITADFDT','JDATEYT','JDATEYTW','JNENGOT',
'JNENGOTW','MACDFDT','MACDFDT','MDYAMPM','MDYAMPM','ND8601DN','ND8601DT','ND8601DZ','NLDATM','NLDATM','NLDATMAP','NLDATMAP',
'NLDATMDT','NLDATML','NLDATMM','NLDATMMD','NLDATMMDL','NLDATMMDM','NLDATMMDS','NLDATMMN','NLDATMS','NLDATMTM','NLDATMTZ','NLDATMW',
'NLDATMW','NLDATMWN','NLDATMWZ','NLDATMYM','NLDATMYML','NLDATMYMM','NLDATMYMS','NLDATMYQ','NLDATMYQL','NLDATMYQM','NLDATMYQS','NLDATMYR',
'NLDATMYW','NLDATMZ','NLDDFDT','NLDDFDT','NORDFDT','NORDFDT','POLDFDT','POLDFDT','PTGDFDT','PTGDFDT','RUSDFDT','RUSDFDT',
'SLODFDT','SLODFDT','SVEDFDT','SVEDFDT','TWMDY','YMDDTTM',
)

