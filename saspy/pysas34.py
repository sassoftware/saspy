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
from saspy.sasstat import *
#from saspy.sasets  import *

try:
   from IPython.display import HTML
except ImportError:
   pass

class SASconfig:
   def __init__(self, cfgname='', kernel=None, user='', pw='', ip='', port='', context='', options=''):
      self.configs  = []
      self._kernel  = kernel
      self.ip       = ip
      self.port     = port
      self.contexts = []
      self.ctxname  = context
      self.options  = options
      self._token   = None

      # GET Config options
      try:
         self.cfgopts = getattr(sascfg, "SAS_config_options")
      except:
         self.cfgopts = {}
      lock = self.cfgopts.get('lock_down', True)
      # in lock down mode, don't allow runtime overrides of option values from the config file.
      if lock:
         if len(ip) > 0 or len(port) > 0 or len(context) > 0 or len(options) > 0:
            print("Parameters passed to SAS_session were ignored due to configuration restriction.")
         self.ip       = ''
         self.port     = ''
         self.ctxname  = ''
         self.options  = ''

      # GET Config names
      self.configs = getattr(sascfg, "SAS_config_names")

      if len(cfgname) == 0:
         if len(self.configs) == 0:
            print("No SAS Configuration names found in saspy.sascfg")
            return None
         else:
            if len(self.configs) == 1:
               cfgname = self.configs[0]
               if kernel == None:
                  print("Using SAS Config named: "+cfgname)
            else:
               cfgname = self._prompt("Please enter the name of the SAS Config you wish to run. Available Configs are: " +
                                      str(self.configs)+" ")

      while cfgname not in self.configs:
         cfgname = self._prompt(
             "The SAS Config name specified was not found. Please enter the SAS Config you wish to use. Available Configs are: " +
              str(self.contexts)+" ")

      self.name       = cfgname
      cfg             = getattr(sascfg, cfgname) 
      if len(ip)      == 0:
         self.ip      = cfg.get('ip', '')
      if len(port)    == 0:
         self.port    = cfg.get('port', 80)
      if len(context) == 0:
         self.ctxname = cfg.get('context', '')
      if len(options) == 0:
         self.options = cfg.get('options', '')
      if len(user)    == 0:
         user         = cfg.get('user', '')
      if len(pw)      == 0:
         pw           = cfg.get('pw', '')

      while len(self.ip) == 0:
         if not lock:
            self.ip = self._prompt("Please enter the host (ip address) you are trying to connect to: ")
         else:
            print("In lockdown mode and missing ip adress in the config named: "+cfgname )

      while len(user) == 0:
         user = self._prompt("Please enter userid: ")

      while len(pw) == 0:
         pw = self._prompt("Please enter password: ", pw = True)

      # get AuthToken
      self._token = self._authenticate(user, pw)

      if self._token == None:
         print("Could not acquire an Authentication Token")
         return

      # GET Contexts 
      self.contexts = self.get_contexts()

      if len(self.ctxname) == 0:
         if len(self.contexts) == 0:
            print("No Contexts found on Compute Service at ip=" + self.ip)
            return None
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
            print("SAS Context specified in the SA Config was not found and it is in lockdown mode. So no connection can be made to SAS context: "+
                   self.ctxname)

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
      resp = req.read()
      j = json.loads(resp.decode())
      token = j.get('access_token')

      return token

   def get_contexts(self):
      #import pdb; pdb.set_trace()
      contexts = []

      # GET Contexts 
      conn = hc.HTTPConnection(self.ip, self.port)
      headers={"Accept":"application/vnd.sas.collection+json","Authorization":"Bearer "+self._token}
      conn.request('GET', "/compute/contexts", headers=headers)
      req = conn.getresponse()
      resp = req.read()

      j = json.loads(resp.decode())
      items = j.get('items')

      for i in range(len(items)):
          contexts.append(dict(items[i]).get('name')) 
         
      return contexts

                   
class SASsession:
   '''
   cfgname - value in SAS_config_names List of the sascfg.py file
   kernel  - None - internal use when running the SAS_kernel notebook
   user    - userid to use to connect to Compute Service
   pw      - pw for the userid being used to connect to Compute Service
   ip      - overrides IP      Dict entry of cfgname in sascfg.py file
   port    - overrides Port    Dict entry of cfgname in sascfg.py file
   context - overrides Context Dict entry of cfgname in sascfg.py file 
   options - overrides Options Dict entry of cfgname in sascfg.py file
   '''
   def __init__(self, cfgname: str ='', kernel: '<SAS_kernel object>' =None, user: str ='', pw: str ='', 
                      ip: str ='', port: int ='', context: str ='', options: list ='') -> '<SASsession object>':
      self.sascfg     = SASconfig(cfgname, kernel, user, pw, ip, port, context, options)
      self._obj_cnt   = 0
      self._log       = ""
      self.nosub      = False
      self._sessionid = None

      self._startsas(self.sascfg)

   def __del__(self):
      if self._sessionid:
         self._endsas()
      self._sessionid = None

   def _objcnt(self):
       self._obj_cnt += 1
       return '%04d' % self._obj_cnt
                                                               
   def _startsas(self, config):
      # POST Session
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
      d1 = '{"name":self.sascfg.ctxname, "description":"pySAS session", "version":1, "environment":{"options":self.sascfg.options}}'
      headers={"Accept":"*/*","Content-Type":"application/vnd.sas.compute.session.request+json","Authorization":"Bearer "+self.sascfg._token}
      conn.request('POST', "/compute/sessions?contextName="+self.sascfg.ctxname, body=d1, headers=headers)
      req = conn.getresponse()
      resp = req.read()
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
         d1 = '{"name":self.sascfg.ctxname, "description":"pySAS session", "version":1, "environment":{"options":self.sascfg.options}}'
         headers={"Accept":"*/*","Content-Type":"application/vnd.sas.compute.session.request+json","Authorization":"Bearer "+self.sascfg._token}
         conn.request('DELETE', "/compute/sessions/"+self._sessionid, body=d1, headers=headers)
         req = conn.getresponse()
         resp = req.read()
         #resp
         
         print("SAS server terminated for SESSION_ID="+self._sessionid)       
         self._sessionid = None
      return rc


   def _getlog(self, jobid=None):
      logr = ''

      while True:
         # GET Log
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
         headers={"Accept":"application/vnd.sas.compute.logoutput+json", "Authorization":"Bearer "+self.sascfg._token}
         if jobid:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/log", headers=headers)
         else:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/log?start=0", headers=headers)
         req = conn.getresponse()

         status = req.getcode()
                       
         resp = req.read()

         j   = json.loads(resp.decode())
         log = j.get('log')

         if len(log) == 0:
            break

         for i in range(len(log)):
             line = dict(log[i]).get('line')
             logr += line+'\n'

      if jobid != None:   
         self._log += logr

      return logr

   def _getlst(self, jobid=None):
      # GET the list of results
      conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
      headers={"Accept":"application/json", "Authorization":"Bearer "+self.sascfg._token}
      if jobid:
         conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/results", headers=headers)
      else:
         conn.request('GET', "/compute/sessions/"+self._sessionid+"/results", headers=headers)
      req = conn.getresponse()
      status = req.getcode()
      resp = req.read()

      j = json.loads(resp.decode())
      results = j.get('results')

      for i in range(len(results)):
         # GET an ODS Result
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
         headers={"Accept":"application/json+html", "Authorization":"Bearer "+self.sascfg._token}
         conn.request('GET', results[i], headers=headers)
         req = conn.getresponse()
         resp = req.read()
         htm = resp.decode()
   
      lstd = htm.replace(chr(12), chr(10)).replace('<body class="c body">',
                                                   '<body class="l body">').replace("font-size: x-small;",
                                                                                    "font-size:  normal;")
      return lstd
   
   def _getlsttxt(self, jobid=None):
      lstr = ''
   
      while True:
         # GET Log
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
         headers={"Accept":"application/vnd.sas.compute.listoutput+json", "Authorization":"Bearer "+self.sascfg._token}
         if jobid:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/listing", headers=headers)
         else:
            conn.request('GET', "/compute/sessions/"+self._sessionid+"/listing", headers=headers)
         req = conn.getresponse()
         status = req.getcode()
         resp = req.read()

         j   = json.loads(resp.decode())
         lst = j.get('list')

         if len(lst) == 0:
            break

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

   def submit(self, code: str, results: str ="html") -> dict:
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

      if self.nosub:
         return dict(LOG=code, LST='')

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

      while True:
         # GET Status for JOB
         conn = hc.HTTPConnection(self.sascfg.ip, self.sascfg.port)
         headers={"Accept":"text/plain", "Authorization":"Bearer "+self.sascfg._token}
         conn.request('GET', "/compute/sessions/"+self._sessionid+"/jobs/"+jobid+"/state", headers=headers)
         req = conn.getresponse()
         resp = req.read()
         if resp == b'completed':
            break
         sleep(1)

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

   
   def teach_me_SAS(self, nosub: bool):
      '''
      nosub - bool. True means don't submit the code, print it out so I can see what the SAS code would be.
                    False means run normally - submit the code.
      '''
      self.nosub = nosub

   def exist(self, table: str, libref: str ="work") -> bool:
      '''
      table  - the name of the SAS Data Set
      libref - the libref for the Data Set, defaults to WORK

      Returns True it the Data Set exists and False if it does not
      '''
      code  = "data _null_; e = exist('"
      code += libref+"."+table+"');\n" 
      code += "te='TABLE_EXISTS='; put te e;run;"
   
      nosub = self.nosub
      self.nosub = False
      ll = self.submit(code, "text")
      self.nosub = nosub

      l2 = ll['LOG'].rpartition("TABLE_EXISTS= ")
      l2 = l2[2].partition("\n")
      exists = int(l2[0])
   
      return exists
   
   def sasstat(self) -> '<SASstat object>':
       return SASstat(self)

   def sasets(self) -> '<SASets object>':
       return SASets(self)

   def sasdata(self, table: str, libref: str ="work", results: str ='HTML')  -> '<SASdata object>':
      '''
      table   - the name of the SAS Data Set
      libref  - the libref for the Data Set, defaults to WORK
      results - format of results, HTML is default, TEXT is the alternative
      '''
      if self.exist(table, libref):
         return SASdata(self, libref, table, results)
      else:
         return None
   
   def saslib(self, libref: str, engine: str =' ', path: str ='', options: str =' ') -> 'The LOG showing the assignment of the libref':
      '''
      libref  - the libref for be assigned
      engine  - the engine name used to access the SAS Library (engine defaults to BASE, per SAS)
      path    - path to the library (for engines that take a path parameter)
      options - other engine or engine supervisor options
      '''
      code  = "libname "+libref+" "+engine+" "
      if len(path) > 0:
         code += " '"+path+"' "
      code += options+";"

      ll = self.submit(code, "text")
      if self.nosub:
         print(ll['LOG'])
      else:
         print(ll['LOG'])
   
   def read_csv(self, file: str, table: str, libref: str ="work", results: str ='HTML') -> '<SASdata object>':
      '''
      file    - eithe the OS filesystem path of the file, or HTTP://... for a url accessible file
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK
      results - format of results, HTML is default, TEXT is the alternative
      '''
      code  = "filename x "
   
      if file.startswith(("http","HTTP")):
         code += "url "
   
      code += "\'"+file+"\';\n"
      code += "proc import datafile=x out="
      code += libref+"."+table
      code += " dbms=csv replace; run;"
      ll = self.submit(code, "text")
   
      if self.nosub:
         print(ll['LOG'])

      if self.exist(table, libref):
         return SASdata(self, libref, table, results)
      else:
         return None
   
   def df2sd(self, df: '<Pandas Data Frame object>', table: str ='a', libref: str ="work", results: str ='HTML') -> '<SASdata object>':
      '''
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK
      results - format of results, HTML is default, TEXT is the alternative
      '''
      return self.dataframe2sasdata(df, table, libref, results)
   
   def dataframe2sasdata(self, df: '<Pandas Data Frame object>', table: str ='a', libref: str ="work", results: str ='HTML') -> '<SASdata object>':
      '''
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK
      results - format of results, HTML is default, TEXT is the alternative
      '''
      input  = ""
      card   = ""
      length = ""
      dts    = []

      for name in range(len(df.columns)):
         input += "'"+df.columns[name]+"'n "
         if df.dtypes[df.columns[name]].kind in ('O','S','U','V',):
            col_l = df[df.columns[name]].map(len).max()
            length += " '"+df.columns[name]+"'n $"+str(col_l)
            dts.append('C')
         else:
            dts.append('N')
   
      code  = "data "+libref+"."+table+";\n"
      if len(length):
         code += "length"+length+";\n"
      code += "infile datalines delimiter='09'x;\n input "+input+";\n datalines;"

      self._asubmit(code, "text")

      for row in df.iterrows():
         card  = ""
         for col in range(len(row[1])):
            var = str(row[1][col])
            if dts[col] == 'N' and var == 'nan':
               var = '.'
            card += var+chr(9)
         self._asubmit(card, "text")
   
      self._asubmit(";run;", "text")
   
      if self.exist(table, libref):
         return SASdata(self, libref, table, results)
      else:
         return None
   
   def sd2df(self, sd: '<SASdata object>') -> '<Pandas Data Frame object>':
      '''
      sd      - SASdata object that refers to the Sas Data Set you want to export to a Pandas Data Frame
      '''
      return self.sasdata2dataframe(sd)
   
   def sasdata2dataframe(self, sd: '<SASdata object>') -> '<Pandas Data Frame object>':
      '''
      sd      - SASdata object that refers to the Sas Data Set you want to export to a Pandas Data Frame
      '''
      import pandas as pd
      import socket as socks
      datar = ""

      if sd == None:
         print('The SASdata object is not valid; it is \'None\'')
         return None                            
      if sd == None or self.exist(sd.table, sd.libref) == 0:
         print('The SAS Data Set '+sd.libref|'.'+sd.table+' does not exist')
         return None                            
   
      nosub = self.nosub
      self.nosub = False
   
      code  = "data _null_; file STDERR;d = open('"+sd.libref+"."+sd.table+"');\n"
      code += "lrecl = attrn(d, 'LRECL'); nvars = attrn(d, 'NVARS');\n"
      code += "lr='LRECL='; vn='VARNUMS='; vl='VARLIST='; vt='VARTYPE='; vf='VARFMT=';\n"
      code += "put lr lrecl; put vn nvars; put vl;\n"
      code += "do i = 1 to nvars; var = varname(d, i); put var; end;\n"
      code += "put vt;\n"
      code += "do i = 1 to nvars; var = vartype(d, i); put var; end;\n"
      code += "run;"
   
      ll = self.submit(code, "text")
   
      l2 = ll['LOG'].rpartition("LRECL= ")
      l2 = l2[2].partition("\n")
      lrecl = int(l2[0])
   
      l2 = l2[2].partition("VARNUMS= ")
      l2 = l2[2].partition("\n")
      nvars = int(l2[0])
   
      l2 = l2[2].partition("\n")
      varlist = l2[2].split("\n", nvars)
      del varlist[nvars]
   
      l2 = l2[2].partition("VARTYPE=")
      l2 = l2[2].partition("\n")
      vartype = l2[2].split("\n", nvars)
      del vartype[nvars]
   
   
      code  = "data _null_; set "+sd.libref+"."+sd.table+"(obs=1);put 'FMT_CATS=';\n"
      for i in range(len(varlist)):
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "run;\n"
   
      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("FMT_CATS=")
      l2 = l2[2].partition("\n")              
      varcat = l2[2].split("\n", nvars)
      del varcat[nvars]
   
      sock = socks.socket()
      sock.bind(("",0))
      port = sock.getsockname()[1]
   
      code  = ""
      code += "filename sock socket ':"+str(port)+"' lrecl=32767 recfm=v termstr=LF;\n"
      code += " data _null_; set "+sd.libref+"."+sd.table+";\n file sock; put "
      for i in range(len(varlist)):
         code += "'"+varlist[i]+"'n "
         if vartype[i] == 'N' and varcat[i] not in sas_dtdt_fmts:
            code += 'best32. '
         if i < (len(varlist)-1):
            code += "'09'x "
      code += "; run;\n"
   
      sock.listen(0)
      self._asubmit(code, 'text')
      newsock = sock.accept()
   
      while True:
         data = newsock[0].recv(4096)
         if len(data):
            datar += data.decode()
         else:
            break
   
      newsock[0].shutdown(socks.SHUT_RDWR)
      newsock[0].close()
      sock.close()
   
      r = []
      for i in datar.splitlines():
         r.append(tuple(i.split(sep='\t')))
      
      df = pd.DataFrame.from_records(r, columns=varlist)

      self.nosub = nosub
   
      return df.convert_objects(convert_numeric=True, convert_dates=True, copy=False)
   
   
class SASdata:

    def __init__(self, sassession, libref, table, results="HTML"):

        self.sas = sassession

        failed = 0
        if results.upper() == "HTML":
           try:
              from IPython.display import HTML 
           except:
              failed = 1

           if failed:
              self.HTML = 0
           else:
              self.HTML = 1
        else:
           self.HTML = 0

        self.libref = libref 
        self.table  = table

    def set_results(self, results: str):
        '''
        results - set the default result type for this SASdata object. 'HTML' = HTML. Anything else = 'TEXT'.
        '''
        if results.upper() == "HTML":
           self.HTML = 1
        else:
           self.HTML = 0

    def head(self, obs=5):
        code  = "proc print data="
        code += self.libref
        code += "."
        code += self.table
        code += "(obs="
        code += str(obs)
        code += ");run;"
        
        if self.sas.nosub:
           ll = self.sas.submit(code, "text")
           print(ll['LOG'])
           return

        if self.HTML:
           ll = self.sas.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.submit(code, "text")
           print(ll['LST'])

    def tail(self, obs=5):
        code  = "%put lastobs=%sysfunc(attrn(%sysfunc(open("
        code += self.libref
        code += "."
        code += self.table
        code += ")),NOBS)) tom;"

        nosub = self.sas.nosub
        self.sas.nosub = False
        ll = self.sas.submit(code, "text")

        lastobs = ll['LOG'].rpartition("lastobs=")
        lastobs = lastobs[2].partition(" tom")
        lastobs = int(lastobs[0])

        code  = "proc print data="
        code += self.libref
        code += "."
        code += self.table
        code += "(firstobs="
        code += str(lastobs-(obs-1))
        code += " obs="
        code += str(lastobs)
        code += ");run;"
        
        self.sas.nosub = nosub
        if nosub:
           ll = self.sas.submit(code, "text")
           print(ll['LOG'])
           return

        if self.HTML:
           ll = self.sas.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.submit(code, "text")
           print(ll['LST'])

    def contents(self):
        code  = "proc contents data="
        code += self.libref
        code += "."
        code += self.table
        code += ";run;"

        if self.sas.nosub:
           ll = self.sas.submit(code, "text")
           print(ll['LOG'])
           return

        if self.HTML:
           ll = self.sas.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.submit(code, "text")
           print(ll['LST'])

    def describe(self):
        return(self.means())

    def means(self):
        code  = "proc means data="
        code += self.libref
        code += "."
        code += self.table
        code += " n mean std min p25 p50 p75 max;run;"
        
        if self.sas.nosub:
           ll = self.sas.submit(code, "text")
           print(ll['LOG'])
           return

        if self.HTML:
           ll = self.sas.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.submit(code, "text")
           print(ll['LST'])

    def to_csv(self, file: str) -> 'The LOG showing the results of the step':
        '''
        file    - the OS filesystem path of the file to be created (exported from this SAS Data Set)
        '''
        code  = "filename x \""+file+"\";\n"
        code += "proc export data="+self.libref+"."+self.table+" outfile=x"
        code += " dbms=csv replace; run;"
        ll = self.sas.submit(code, "text")

        if self.sas.nosub:
           print(ll['LOG'])
        else:
           return 0

    def to_df(self) -> '<Pandas Data Frame object>':
        '''
        Export this SAS Data Set to a Pandas Data Frame
        '''
        return self.sas.sd2df(self)

    def hist(self, var: str, title: str ='', label: str ='') -> 'a histogram plot of the variable you chose':
        '''
        var   - the variable (column) you want to plot
        title - an optional Title for the chart
        label - LegendLABEL= value for sgplot
        '''
        code  = "proc sgplot data="
        code += self.libref
        code += "."
        code += self.table
        code += ";\n\thistogram "+var+" / scale=count"
        if len(label) > 0:
           code += " LegendLABEL='"+label+"'"
        code += ";\n"
        if len(title) > 0:
           code += '\ttitle "'+title+'";\n'
        code += "\tdensity "+var+';\nrun;\n'+'title \"\";'
        
        if self.sas.nosub:
           ll = self.sas.submit(code, "text")
           print(ll['LOG'])
           return

        if self.HTML:
           ll = self.sas.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.submit(code, "text")
           print(ll['LST'])

if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(_getlog())
    print(_getlsttxt())

    endsas()

sas_dtdt_fmts = (    
'AFRDFDD','AFRDFDE','AFRDFDE','AFRDFDN','AFRDFDT','AFRDFDT','AFRDFDWN',
'AFRDFMN','AFRDFMY','AFRDFMY','AFRDFWDX','AFRDFWKX','ANYDTDTE','ANYDTDTM','ANYDTTME','B8601DA','B8601DA','B8601DJ','B8601DN','B8601DN',
'B8601DT','B8601DT','B8601DZ','B8601DZ','B8601LZ','B8601LZ','B8601TM','B8601TM','B8601TZ','B8601TZ','CATDFDD','CATDFDE','CATDFDE','CATDFDN',
'CATDFDT','CATDFDT','CATDFDWN','CATDFMN','CATDFMY','CATDFMY','CATDFWDX','CATDFWKX','CRODFDD','CRODFDE','CRODFDE','CRODFDN','CRODFDT',
'CRODFDT','CRODFDWN','CRODFMN','CRODFMY','CRODFMY','CRODFWDX','CRODFWKX','CSYDFDD','CSYDFDE','CSYDFDE','CSYDFDN','CSYDFDT','CSYDFDT',
'CSYDFDWN','CSYDFMN','CSYDFMY','CSYDFMY','CSYDFWDX','CSYDFWKX','DANDFDD','DANDFDE','DANDFDE','DANDFDN','DANDFDT','DANDFDT','DANDFDWN','DANDFMN',
'DANDFMY','DANDFMY','DANDFWDX','DANDFWKX','DATE','DATE','DATEAMPM','DATETIME','DATETIME','DAY','DDMMYY','DDMMYY','DDMMYYB','DDMMYYC',
'DDMMYYD','DDMMYYN','DDMMYYP','DDMMYYS','DESDFDD','DESDFDE','DESDFDE','DESDFDN','DESDFDT','DESDFDT','DESDFDWN','DESDFMN','DESDFMY','DESDFMY',
'DESDFWDX','DESDFWKX','DEUDFDD','DEUDFDE','DEUDFDE','DEUDFDN','DEUDFDT','DEUDFDT','DEUDFDWN','DEUDFMN','DEUDFMY','DEUDFMY','DEUDFWDX',
'DEUDFWKX','DOWNAME','DTDATE','DTMONYY','DTWKDATX','DTYEAR','DTYYQC','E8601DA','E8601DA','E8601DN','E8601DN','E8601DT','E8601DT','E8601DZ',
'E8601DZ','E8601LZ','E8601LZ','E8601TM','E8601TM','E8601TZ','E8601TZ','ENGDFDD','ENGDFDE','ENGDFDE','ENGDFDN','ENGDFDT','ENGDFDT','ENGDFDWN',
'ENGDFMN','ENGDFMY','ENGDFMY','ENGDFWDX','ENGDFWKX','ESPDFDD','ESPDFDE','ESPDFDE','ESPDFDN','ESPDFDT','ESPDFDT','ESPDFDWN','ESPDFMN',
'ESPDFMY','ESPDFMY','ESPDFWDX','ESPDFWKX','EURDFDD','EURDFDE','EURDFDE','EURDFDN','EURDFDT','EURDFDT','EURDFDWN','EURDFMN','EURDFMY',
'EURDFMY','EURDFWDX','EURDFWKX','FINDFDD','FINDFDE','FINDFDE','FINDFDN','FINDFDT','FINDFDT','FINDFDWN','FINDFMN','FINDFMY','FINDFMY',
'FINDFWDX','FINDFWKX','FRADFDD','FRADFDE','FRADFDE','FRADFDN','FRADFDT','FRADFDT','FRADFDWN','FRADFMN','FRADFMY','FRADFMY','FRADFWDX',
'FRADFWKX','FRSDFDD','FRSDFDE','FRSDFDE','FRSDFDN','FRSDFDT','FRSDFDT','FRSDFDWN','FRSDFMN','FRSDFMY','FRSDFMY','FRSDFWDX','FRSDFWKX','HHMM',
'HOUR','HUNDFDD','HUNDFDE','HUNDFDE','HUNDFDN','HUNDFDT','HUNDFDT','HUNDFDWN','HUNDFMN','HUNDFMY','HUNDFMY','HUNDFWDX','HUNDFWKX',
'IS8601DA','IS8601DA','IS8601DN','IS8601DN','IS8601DT','IS8601DT','IS8601DZ','IS8601DZ','IS8601LZ','IS8601LZ','IS8601TM','IS8601TM',
'IS8601TZ','IS8601TZ','ITADFDD','ITADFDE','ITADFDE','ITADFDN','ITADFDT','ITADFDT','ITADFDWN','ITADFMN','ITADFMY','ITADFMY','ITADFWDX',
'ITADFWKX','JDATEMD','JDATEMDW','JDATEMNW','JDATEMON','JDATEQRW','JDATEQTR','JDATESEM','JDATESMW','JDATEWK','JDATEYDW','JDATEYM','JDATEYMD',
'JDATEYMD','JDATEYMW','JDATEYT','JDATEYTW','JNENGO','JNENGO','JNENGOT','JNENGOTW','JNENGOW','JTIMEH','JTIMEHM','JTIMEHMS','JTIMEHW',
'JTIMEMW','JTIMESW','JULDATE','JULDAY','JULIAN','JULIAN','MACDFDD','MACDFDE','MACDFDE','MACDFDN','MACDFDT','MACDFDT','MACDFDWN','MACDFMN',
'MACDFMY','MACDFMY','MACDFWDX','MACDFWKX','MDYAMPM','MDYAMPM','MINGUO','MINGUO','MMDDYY','MMDDYY','MMDDYYB','MMDDYYC','MMDDYYD','MMDDYYN',
'MMDDYYP','MMDDYYS','MMSS','MMYY','MMYYC','MMYYD','MMYYN','MMYYP','MMYYS','MONNAME','MONTH','MONYY','MONYY','ND8601DA','ND8601DN','ND8601DT',
'ND8601DZ','ND8601TM','ND8601TZ','NENGO','NENGO','NLDATE','NLDATE','NLDATEL','NLDATEM','NLDATEMD','NLDATEMDL','NLDATEMDM','NLDATEMDS',
'NLDATEMN','NLDATES','NLDATEW','NLDATEW','NLDATEWN','NLDATEYM','NLDATEYML','NLDATEYMM','NLDATEYMS','NLDATEYQ','NLDATEYQL','NLDATEYQM',
'NLDATEYQS','NLDATEYR','NLDATEYW','NLDATM','NLDATM','NLDATMAP','NLDATMAP','NLDATMDT','NLDATML','NLDATMM','NLDATMMD','NLDATMMDL','NLDATMMDM',
'NLDATMMDS','NLDATMMN','NLDATMS','NLDATMTM','NLDATMTZ','NLDATMW','NLDATMW','NLDATMWN','NLDATMWZ','NLDATMYM','NLDATMYML','NLDATMYMM',
'NLDATMYMS','NLDATMYQ','NLDATMYQL','NLDATMYQM','NLDATMYQS','NLDATMYR','NLDATMYW','NLDATMZ','NLDDFDD','NLDDFDE','NLDDFDE','NLDDFDN','NLDDFDT',
'NLDDFDT','NLDDFDWN','NLDDFMN','NLDDFMY','NLDDFMY','NLDDFWDX','NLDDFWKX','NLTIMAP','NLTIMAP','NLTIME','NLTIME','NORDFDD','NORDFDE',
'NORDFDE','NORDFDN','NORDFDT','NORDFDT','NORDFDWN','NORDFMN','NORDFMY','NORDFMY','NORDFWDX','NORDFWKX','POLDFDD','POLDFDE','POLDFDE',
'POLDFDN','POLDFDT','POLDFDT','POLDFDWN','POLDFMN','POLDFMY','POLDFMY','POLDFWDX','POLDFWKX','PTGDFDD','PTGDFDE','PTGDFDE','PTGDFDN',
'PTGDFDT','PTGDFDT','PTGDFDWN','PTGDFMN','PTGDFMY','PTGDFMY','PTGDFWDX','PTGDFWKX','QTR','QTRR','RUSDFDD','RUSDFDE','RUSDFDE','RUSDFDN',
'RUSDFDT','RUSDFDT','RUSDFDWN','RUSDFMN','RUSDFMY','RUSDFMY','RUSDFWDX','RUSDFWKX','SLODFDD','SLODFDE','SLODFDE','SLODFDN','SLODFDT',
'SLODFDT','SLODFDWN','SLODFMN','SLODFMY','SLODFMY','SLODFWDX','SLODFWKX','STIMER','SVEDFDD','SVEDFDE','SVEDFDE','SVEDFDN','SVEDFDT',
'SVEDFDT','SVEDFDWN','SVEDFMN','SVEDFMY','SVEDFMY','SVEDFWDX','SVEDFWKX','TIME','TIME','TIMEAMPM','TOD','TWMDY','WEEKDATE','WEEKDATX',
'WEEKDAY','WEEKU','WEEKU','WEEKV','WEEKV','WEEKW','WEEKW','WORDDATE','WORDDATX','XYYMMDD','XYYMMDD','YEAR','YMDDTTM','YYMM','YYMMC',
'YYMMD','YYMMDD','YYMMDD','YYMMDDB','YYMMDDC','YYMMDDD','YYMMDDN','YYMMDDP','YYMMDDS','YYMMN','YYMMN','YYMMP','YYMMS','YYMON','YYQ',
'YYQ','YYQC','YYQD','YYQN','YYQP','YYQR','YYQRC','YYQRD','YYQRN','YYQRP','YYQRS','YYQS','YYQZ','YYQZ','YYWEEKU','YYWEEKV','YYWEEKW'
)

