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
import saspy.sascfg as sascfg
#from saspy.sasbase import *

try:
   from IPython.display import HTML
except ImportError:
   pass

class SASconfigHTTP:
   '''
   This object is not intended to be used directly. Instantiate a VIYAsession object instead 
   '''
   #def __init__(self, cfgname='', kernel=None, user='', pw='', ip='', port='', context='', options=''):
   def __init__(self, **kwargs):
      self._kernel  = kwargs.get('kernel', None)   
      self.ip       = kwargs.get('ip', '')   
      self.port     = kwargs.get('port', None)   
      self.ctxname  = kwargs.get('context', '')   
      self.options  = kwargs.get('options', '')   
      self._token   = None
      user          = kwargs.get('user', '')  
      pw            = kwargs.get('pw', '')  

      # GET Config options
      try:
         self.cfgopts = getattr(sascfg, "SAS_config_options")
      except:
         self.cfgopts = {}
      lock = self.cfgopts.get('lock_down', True)
      # in lock down mode, don't allow runtime overrides of option values from the config file.
      if lock:
         if len(self.ip) > 0 or self.port or len(self.ctxname) > 0 or len(self.options) > 0:
            print("Parameters passed to SAS_session were ignored due to configuration restriction.")
         self.ip       = ''
         self.port     = ''
         self.ctxname  = ''
         self.options  = ''

      self.name            = kwargs.get('sascfgname', '')  
      cfg                  = getattr(sascfg, self.name) 
      if len(self.ip)      == 0:
         self.ip           = cfg.get('ip', '')
      if len(self.port)    == 0:
         self.port         = cfg.get('port', 80)
      if len(self.ctxname) == 0:
         self.ctxname = cfg.get('context', '')
      if len(self.options) == 0:
         self.options = cfg.get('options', '')
      if len(user)         == 0:
         user              = cfg.get('user', '')
      if len(pw)           == 0:
         pw                = cfg.get('pw', '')

      while len(self.ip) == 0:
         if not lock:
            self.ip = self._prompt("Please enter the host (ip address) you are trying to connect to: ")
         else:
            print("In lockdown mode and missing ip adress in the config named: "+cfgname )
            return

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
      if not self.contexts:
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
            print("SAS Context specified in the SAS Config was not found and it is in lockdown mode. So no connection can be made to SAS context: "+
                   self.ctxname)
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
      conn = hc.HTTPConnection(self.ip, self.port)
      d1 = ("grant_type=password&username="+user+"&password="+pw).encode()
      basic = base64.encodestring("sas.tkmtrb:".encode())
      authheader = '%s' % basic.splitlines()[0].decode()
      headers={"Accept":"application/vnd.sas.compute.session+json","Content-Type":"application/x-www-form-urlencoded",
               "Authorization":"Basic "+authheader}
      conn.request('POST', "/SASLogon/oauth/token", body=d1, headers=headers)
      req = conn.getresponse()
      status = req.getcode()
      resp = req.read()
      if status > 299:
         print("Failure in GET AuthToken \n"+resp.decode())
         return None

      j = json.loads(resp.decode())
      token = j.get('access_token')
      return token

   def _get_contexts(self):
      #import pdb; pdb.set_trace()
      contexts = []

      # GET Contexts 
      conn = hc.HTTPConnection(self.ip, self.port)
      headers={"Accept":"application/vnd.sas.collection+json","Authorization":"Bearer "+self._token}
      conn.request('GET', "/compute/contexts", headers=headers)
      req = conn.getresponse()
      status = req.getcode()
      resp = req.read()
      if status > 299:
         print("Failure in GET Contexts \n"+resp.decode())
         return None

      j = json.loads(resp.decode())
      items = j.get('items')

      for i in range(len(items)):
          contexts.append(dict(items[i]).get('name')) 
         
      return contexts

                   
class SASsessionHTTP():
   '''
   The SASsession object is the main object to instantiate and provides access to the rest of the functionality.
   cfgname - value in SAS_config_names List of the sascfg.py file
   kernel  - None - internal use when running the SAS_kernel notebook
   user    - userid to use to connect to Compute Service
   pw      - pw for the userid being used to connect to Compute Service
   ip      - overrides IP      Dict entry of cfgname in sascfg.py file
   port    - overrides Port    Dict entry of cfgname in sascfg.py file
   context - overrides Context Dict entry of cfgname in sascfg.py file 
   options - overrides Options Dict entry of cfgname in sascfg.py file
   '''
   #def __init__(self, cfgname: str ='', kernel: '<SAS_kernel object>' =None, user: str ='', pw: str ='', 
   #                   ip: str ='', port: int ='', context: str ='', options: list ='') -> '<SASsession object>':
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
      # POST Session
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
      d1 = '{"name":"'+self.sascfg.ctxname+'", "description":"saspy session", "version":1, "environment":{"options":"'+self.sascfg.options+'"}}'
      headers={"Accept":"*/*","Content-Type":"application/vnd.sas.compute.session.request+json","Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', "/compute/sessions?contextName="+self.sascfg.ctxname, body=d1, headers=headers)
      req = conn.getresponse()
      status = req.getcode()
      resp = req.read()
      if status > 299:
         print("Failure in POST Session \n"+resp.decode())
         print("Could not acquire a SAS Session for context: "+self.sascfg.ctxname)
         return None

      j = json.loads(resp.decode())
      self._sessionid = j.get('id')

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
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
         d1 = '{"name":"'+self.sascfg.ctxname+'", "description":"saspy session", "version":1, "environment":{"options":"'+self.sascfg.options+'"}}'
         headers={"Accept":"*/*","Content-Type":"application/vnd.sas.compute.session.request+json","Authorization":"Bearer "+self.sascfg._token}
         conn.request('DELETE', "/compute/sessions/"+self._sessionid, body=d1, headers=headers)
         req = conn.getresponse()
         resp = req.read()
         #resp
         
         print("SAS server terminated for SESSION_ID="+self._sessionid)       
         self._sessionid = None
      return rc


   def _getlog(self, jobid=None):
      start = 0
      logr = ''

      while True:
         # GET Log
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
         headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
         if jobid:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/log?start="+str(start)+"&limit=999999", headers=headers)
         else:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/log?start="+str(start)+"&limit=999999", headers=headers)
         req = conn.getresponse()
         status = req.getcode()
         resp = req.read()

         j   = json.loads(resp.decode())
         log = j.get('items')

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

      # GET the list of results
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
      headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
      if jobid:
         conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/results", headers=headers)
      else:
         conn.request('GET', "/compute/sessions/"+self._sessionid+"/results", headers=headers)
      req = conn.getresponse()
      status = req.getcode()
      resp = req.read()

      j = json.loads(resp.decode())
      results = j.get('items')


      # this is all a kludge as get results for job isn't actually implemented (gets all results for session) 
      if jobid:
         i = len(results) -1
         while i >= 0:
            if results[i].get('type') == 'ODS':
               break
            i -=  1
      else:
         i = 0

      # shouldn't be able to happen, but ... for now
      if i < 0:
         return ''

      while i < len(results):
         # GET an ODS Result
         if results[i].get('type') == 'ODS':
            conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
            headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
            conn.request('GET', results[i].get('links')[0].get('href'), headers=headers)
            req = conn.getresponse()
            status = req.getcode()
            resp = req.read()
            htm += resp.decode()
         i += 1

      lstd = htm.replace(chr(12), chr(10)).replace('<body class="c body">',
                                                   '<body class="l body">').replace("font-size: x-small;",
                                                                                    "font-size:  normal;")
      return lstd
   
   def _getlsttxt(self, jobid=None):
      start = 0
      lstr = ''
   
      while True:
         # GET Log
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
         headers={"Accept":"application/vnd.sas.collection+json", "Authorization":"Bearer "+self.sascfg._token}
         if jobid:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/listing?start="+str(start)+"limit=999999", headers=headers)
         else:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/listing?start="+str(start)+"limit=999999", headers=headers)
         req = conn.getresponse()
         status = req.getcode()
         resp = req.read()

         j   = json.loads(resp.decode())
         lst = j.get('items')

         lines = len(lst)

         if not lines:
            break
         start += lines

         for i in range(len(lst)):
             line = dict(lst[i]).get('line')
             lstr += line+'\n'

      return lstr

   def _asubmit(self, code, results="html"):
      #odsopen  = json.dumps("ods listing close;ods html5 options(bitmap_mode='inline') device=png; ods graphics on / outputfmt=png;\n")
      odsopen  = json.dumps("ods listing close;ods html5 options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n")
      odsclose = json.dumps("ods html5 close;ods listing;\n")
      ods      = True;

      if results.upper() != "HTML":
         ods = False
         odsopen  = '""'
         odsclose = '""'
   
      # POST Job
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
      jcode = json.dumps(code)
      d1 = '{"code":['+odsopen+','+jcode+','+odsclose+']}'
      headers={"Accept":"application/json","Content-Type":"application/vnd.sas.compute.job.request+json",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', "/compute/sessions/"+self._sessionid+"/jobs", body=d1, headers=headers)
      req = conn.getresponse()
      resp = req.read()
      j = json.loads(resp.decode())
      jobid = j.get('id')

      #see if this is the problem, then remove this -  this is a problem, keep it till the bug is fixed!@!!!
      '''   should be fixed now, verify and remove
      quit = 0
      while True:
         # GET Status for JOB
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
         headers={"Accept":"text/plain", "Authorization":"Bearer "+self.sascfg._token}
         conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/state", headers=headers)
         req = conn.getresponse()
         resp = req.read()
         if resp == b'completed' or quit > 60:
            break
         quit += 1
      '''
      return jobid

   def submit(self, code: str, results: str ="html", prompt: list = []) -> dict:
      '''
      code    - the SAS statements you want to execute 
      results - format of results, HTML is default, TEXT is the alternative

      Returns - a Dict containing two keys:values, [LOG, LST]. LOG is text and LST is 'results' (HTML or TEXT)

      NOTE: to view HTML results in the ipykernel, issue: from IPython.display import HTML  and use HTML() instead of print()
      i.e,: results = sas.submit("data a; x=1; run; proc print;run')
            print(results['LOG'])
            HTML(results['LST']) 
      '''
      #odsopen  = json.dumps("ods listing close;ods html5 options(bitmap_mode='inline') device=png; ods graphics on / outputfmt=png;\n")
      odsopen  = json.dumps("ods listing close;ods html5 options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n")
      odsclose = json.dumps("ods html5 close;ods listing;\n")
      ods      = True;

      if results.upper() != "HTML":
         ods = False
         odsopen  = '""'
         odsclose = '""'
   
      # POST Job
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
      jcode = json.dumps(code)
      d1 = '{"code":['+odsopen+','+jcode+','+odsclose+']}'
      headers={"Accept":"application/json","Content-Type":"application/vnd.sas.compute.job.request+json",
               "Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', "/compute/sessions/"+self._sessionid+"/jobs", body=d1, headers=headers)
      req = conn.getresponse()
      resp = req.read()
      j = json.loads(resp.decode())
      jobid = j.get('id')

      done = False
      while not done:
         try:
            while True:
               # GET Status for JOB
               conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
               headers={"Accept":"text/plain", "Authorization":"Bearer "+self.sascfg._token}
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

      '''
      if quit > 10:
         import pdb; pdb.set_trace()
         jobid2 = jobid
         # GET Status for JOB
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
         headers={"Accept":"text/plain", "Authorization":"Bearer "+self.sascfg._token}
         conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid2+"/state", headers=headers)
         req = conn.getresponse()
         resp = req.read()
      '''


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

   def read_csv(self, file: str, table: str, libref: str ="work", results: str ='HTML', nosub: bool=False) -> '<SASdata object>':
      '''
      This method will import a csv file into a SAS Data Set and return the SASdata object referring to it.
      file    - eithe the OS filesystem path of the file, or HTTP://... for a url accessible file
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK
      results - format of results, HTML is default, TEXT is the alternative
      '''
      print("read_csv is not currently implemented in this SAS Connection Interface; HTTP")
      return None
      
      code  = "filename x "
   
      if file.lower().startswith("http"):
         code += "url "
   
      code += "\""+file+"\";\n"
      code += "proc import datafile=x out="
      code += libref+"."+table
      code += " dbms=csv replace; run;"
   
      if nosub:
         print(code)
      else:
         ll = self._io.submit(code, "text")
         if self._sb.exist(table, libref):
            return self._sb.sasdata(table, libref, results)
         else:
            return None
   
   def to_csv(self, file: str, data: '<SASdata object>', nosub: bool =False) -> 'The LOG showing the results of the step':
      '''
      This method will export a SAS Data Set to a file in CCSV format.
      file    - the OS filesystem path of the file to be created (exported from this SAS Data Set)
      '''
      print("to_csv is not currently implemented in this SAS Connection Interface; HTTP")
      return None

   def dataframe2sasdata(self, df: '<Pandas Data Frame object>', table: str ='a', libref: str ="work", results: str ='HTML') -> '<SASdata object>':
      '''
      This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK
      results - format of results, HTML is default, TEXT is the alternative
      '''
      print("dataframe2sasdata is not currently implemented in this SAS Connection Interface; HTTP")
      return None

   def sasdata2dataframe(self, sd: '<SASdata object>') -> '<Pandas Data Frame object>':
      '''
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      sd      - SASdata object that refers to the Sas Data Set you want to export to a Pandas Data Frame
      '''
      print("sasdata2dataframe is not currently implemented in this SAS Connection Interface; HTTP")
      return None

if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(_getlog())
    print(_getlsttxt())

    endsas()

