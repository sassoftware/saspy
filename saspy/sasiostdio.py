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
import fcntl
import os
import signal
import subprocess
import getpass
from time import sleep
import saspy.sascfg as SAScfg

try:
   from IPython.display import HTML
except ImportError:
   pass

class SASconfigSTDIO:
   '''
   This object is not intended to be used directly. Instantiate a SASsession object instead 
   '''
   def __init__(self, **kwargs):
      self._kernel  = kwargs.get('kernel', None)

      self.name     = kwargs.get('sascfgname', '')
      cfg           = getattr(SAScfg, self.name) 

      self.saspath  = cfg.get('saspath', '')
      self.options  = cfg.get('options', [])
      self.ssh      = cfg.get('ssh', '')
      self.host     = cfg.get('host', '')

      # GET Config options
      try:
         self.cfgopts = getattr(SAScfg, "SAS_config_options")
      except:
         self.cfgopts = {}

      lock = self.cfgopts.get('lock_down', True)
      # in lock down mode, don't allow runtime overrides of option values from the config file.


      insaspath = kwargs.get('saspath', '')   
      if len(insaspath) > 0:
         if lock and len(self.saspath):
            print("Parameter 'saspath' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.saspath = insaspath   

      inoptions = kwargs.get('options', '')
      if len(inoptions) > 0:
         if lock and len(self.options):
            print("Parameter 'options' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.options = inoptions   

      inssh = kwargs.get('ssh', '')
      if len(inssh) > 0:
         if lock and len(self.ssh):
            print("Parameter 'ssh' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.ssh = inssh   

      inhost = kwargs.get('host', '')
      if len(inhost) > 0:
         if lock and len(self.host):
            print("Parameter 'host' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.host = inhost   

      while len(self.saspath) == 0:
         if not lock:
            self.saspath = self._prompt("Please enter the path to the SAS start up script: ")
         else:
            print("In lockdown mode and missing saspath in the config named: "+cfgname )
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
                   
class SASsessionSTDIO():
   '''
   The SASsession object is the main object to instantiate and provides access to the rest of the functionality.
   cfgname - value in SAS_config_names List of the sascfg.py file
   kernel  - None - internal use when running the SAS_kernel notebook
   saspath - overrides saspath Dict entry of cfgname in sascfg.py file
   options - overrides options Dict entry of cfgname in sascfg.py file

   and for running STDIO over passwordless ssh
   ssh     - full path of the ssh command; /usr/bin/ssh for instance
   host    - host name of the remote machine
   '''
   #def __init__(self, cfgname: str ='', kernel: '<SAS_kernel object>' =None, saspath :str ='', options: list =[]) -> '<SASsession object>':
   def __init__(self, **kwargs):
      self.pid    = None
      self.stdin  = None
      self.stderr = None
      self.stdout = None

      self.sascfg   = SASconfigSTDIO(**kwargs)
      self._log_cnt = 0
      self._log     = ""
      self._sb      = kwargs.get('sb', None)

      self._startsas()

   def __del__(self):
      if self.pid:
         self._endsas()
      self.pid = None

   def _logcnt(self, next=True):
       if next == True:
          self._log_cnt += 1
       return '%08d' % self._log_cnt

   def _startsas(self):
      if self.pid:
         return self.pid

      if self.sascfg.ssh:
         pgm    = self.sascfg.ssh
         parms  = [pgm]
         parms += ["-t", self.sascfg.host, self.sascfg.saspath]
      else:
         pgm    = self.sascfg.saspath
         parms  = [pgm]

      parms += self.sascfg.options
      parms += ["-pagesize", "MAX"]
      parms += ["-nodms"]
      parms += ["-stdio"]
      parms += ["-terminal"]
      parms += ["-nosyntaxcheck"]
      parms += ['']

      PIPE_READ  = 0
      PIPE_WRITE = 1
      
      pin  = os.pipe() 
      pout = os.pipe()
      perr = os.pipe() 
      
      pidpty = os.forkpty()
      if pidpty[0]:
         # we are the parent

         pid = pidpty[0]
         os.close(pin[PIPE_READ])
         os.close(pout[PIPE_WRITE]) 
         os.close(perr[PIPE_WRITE]) 

      else:
         # we are the child
         signal.signal(signal.SIGINT, signal.SIG_DFL)

         os.close(0)
         os.close(1)
         os.close(2)

         os.dup2(pin[PIPE_READ],   0)
         os.dup2(pout[PIPE_WRITE], 1)
         os.dup2(perr[PIPE_WRITE], 2)

         os.close(pin[PIPE_READ])
         os.close(pin[PIPE_WRITE])
         os.close(pout[PIPE_READ])
         os.close(pout[PIPE_WRITE]) 
         os.close(perr[PIPE_READ])
         os.close(perr[PIPE_WRITE]) 

         try:
            os.execv(pgm, parms)
         except:
            os._exit(-6)

      self.pid    = pidpty[0]
      self.stdin  = os.fdopen(pin[PIPE_WRITE], mode='wb')
      self.stderr = os.fdopen(perr[PIPE_READ], mode='rb')
      self.stdout = os.fdopen(pout[PIPE_READ], mode='rb')

      fcntl.fcntl(self.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
      fcntl.fcntl(self.stderr, fcntl.F_SETFL, os.O_NONBLOCK)
      
      self.submit("options svgtitle='svgtitle'; options validvarname=any; ods graphics on;", "text")
      print("SAS Connection established. Subprocess id is "+str(self.pid))  
      return self.pid

   def _endsas(self):
      rc = 0
      if self.pid:
         code = ";*\';*\";*/;\n;quit;endsas;"
         self._getlog(wait=1)
         self._asubmit(code,'text')
         sleep(1)
         try:
            rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
         except (subprocess.TimeoutExpired):
            print("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
            os.kill(self.pid, signal.SIGKILL)
         print("SAS Connection terminated. Subprocess id was "+str(self.pid))
         self.pid = None
      return rc

   def _getlog(self, wait=5, jobid=None):
      logf   = b''
      quit   = wait * 2
      logn   = self._logcnt(False)
      code1  = "%put E3969440A681A24088859985"+logn+";\nE3969440A681A24088859985"+logn

      while True:
         log = self.stderr.read1(4096)
         if len(log) > 0:
            logf += log
         else:
            quit -= 1
            if quit < 0 or len(logf) > 0:
               break
            sleep(0.5)
   
      x = logf.decode().replace(code1, " ")
      self._log += x

      if self.pid == None:
         return "No SAS process attached. SAS process has terminated unexpectedly."
      rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
      if rc != None:
         self.pid = None
         return 'SAS process has terminated unexpectedly. Pid State= '+str(rc)

      return x

   def _getlst(self, wait=5, jobid=None):
      lstf = b''
      quit = wait * 2
      eof = 0
      bof = False
      lenf = 0
   
      while True:
         lst = self.stdout.read1(4096)
         if len(lst) > 0:
            lstf += lst
                             
            if ((not bof) and lst.count(b"<!DOCTYPE html>", 0, 20) > 0):
               bof = True
         else:
            lenf = len(lstf)
      
            if (lenf > 15):
               eof = lstf.count(b"</html>", (lenf - 15), lenf)
      
            if (eof > 0):
                  break
            
            if not bof:
               quit -= 1
               if quit < 0:
                  break
               sleep(0.5)

      if self.pid == None:
         return "No SAS process attached. SAS process has terminated unexpectedly."
      rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
      if rc != None:
         self.pid = None
         return 'SAS process has terminated unexpectedly. Pid State= '+str(rc)

      return lstf.decode()
   
   def _getlsttxt(self, wait=5, jobid=None):
      f2 = [None]
      lstf = b''
      quit = wait * 2
      eof = 0
      self._asubmit("data _null_;file print;put 'Tom was here';run;", "text")
   
      while True:
         lst = self.stdout.read1(4096)
         if len(lst) > 0:
            lstf += lst
   
            lenf = len(lstf)
            eof = lstf.find(b"Tom was here", lenf - 25, lenf)
      
            if (eof != -1):
               final = lstf.partition(b"Tom was here")
               f2 = final[0].decode().rpartition(chr(12))
               break

      lst = f2[0]

      if self.pid == None:
         return "No SAS process attached. SAS process has terminated unexpectedly."
      rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
      if rc != None:
         self.pid = None
         return 'SAS process has terminated unexpectedly. Pid State= '+str(rc)

      return lst.replace(chr(12), '\n')

   def _asubmit(self, code, results="html"):
      # as this is an _ method, it's not really to be used. Of note is that if this is used and if what it submitted generates
      # anything to the lst, then unless _getlst[txt] is called, then next submit will happen to get the lst this wrote, plus
      # what it generates. If the two are not of the same type (html, text) it could be problematic, beyond not being what was
      # expected in the first place. __flushlst__() used to be used, but was never needed. Adding this note and removing the
      # unnecessary read in submit as this can't happen in the current code. 
      odsopen  = b"ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods html5 close;ods listing;\n"
      ods      = True;

      if results.upper() != "HTML":
         ods = False
   
      if (ods):
         self.stdin.write(odsopen)
   
      out = self.stdin.write(code.encode()+b'\n')
   
      if (ods):
         self.stdin.write(odsclose)

      self.stdin.flush()

      return str(out)

   def submit(self, code: str, results: str ="html", prompt: dict ={}) -> dict:
      '''
      This method is used to submit any SAS code. It returns the Log and Listing as a python dictionary.
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
      odsopen  = b"ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods html5 close;ods listing;\n"
      ods      = True;
      mj       = b";*\';*\";*/;"
      lstf     = ''
      logf     = ''
      bail     = False
      eof      = 5
      bc       = False
      done     = False
      logn     = self._logcnt()
      logcodei = "%put E3969440A681A24088859985" + logn + ";"
      logcodeo = "\nE3969440A681A24088859985" + logn
      pcodei   = ''
      pcodeiv  = ''
      pcodeo   = ''

      if self.pid == None:
         print("No SAS process attached. SAS process has terminated unexpectedly.")
         return dict(LOG="No SAS process attached. SAS process has terminated unexpectedly.", LST='')

      rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
      if rc != None:
         self.pid = None
         return dict(LOG='SAS process has terminated unexpectedly. Pid State= '+str(rc), LST='')

      # to cover the possibility of an _asubmit w/ lst output not read; no known cases now; used to be __flushlst__()
      # removing this and adding comment in _asubmit to use _getlst[txt] so this will never be necessary; delete later
      #while(len(self.stdout.read1(4096)) > 0):
      #   continue

      if results.upper() != "HTML":
         ods = False
   
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
               pcodei += '%let '+key+'='+var+';\n'
               pcodeo += '%symdel '+key+';\n'
            else:
               pcodeiv += '%let '+key+'='+var+';\n'
         pcodei += 'options source notes;\n'
         pcodeo += 'options source notes;\n'

      if ods:
         self.stdin.write(odsopen)
   
      out = self.stdin.write(mj+b'\n'+pcodei.encode()+pcodeiv.encode()+code.encode()+b'\n'+pcodeo.encode()+b'\n'+mj)
   
      if ods:
         self.stdin.write(odsclose)

      out = self.stdin.write(b'\n'+logcodei.encode()+b'\n')
      self.stdin.flush()

      while not done:
         try:
             while True:
                 rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
                 if rc is not None:
                     self.pid = None
                     return dict(LOG='SAS process has terminated unexpectedly. Pid State= ' +
                                 str(rc), LST='')
                 if bail:
                     eof -= 1
                 if eof < 0:
                     break
                 lst = self.stdout.read1(4096).decode()
                 if len(lst) > 0:
                     lstf += lst
                 else:
                     log = self.stderr.read1(4096).decode() 
                     if len(log) > 0:
                         logf += log
                         if logf.count(logcodeo) >= 1:
                             bail = True
                         if not bail and bc:
                             self.stdin.write(odsclose+logcodei.encode() + b'\n')
                             self.stdin.flush()
                             bc = False
             done = True

         except (KeyboardInterrupt, SystemExit):
             print('Exception caught!')
             ll = self._breakprompt(logcodeo)

             if ll.get('ABORT', False):
                return ll

             logf += ll['LOG']
             lstf += ll['LST']
             bc    = ll['BC']

             if not bc:
                print('Exception handled :)\n')
             else:
                print('Exception ignored, continuing to process...\n')

             self.stdin.write(odsclose+logcodei.encode()+b'\n')
             self.stdin.flush()

      trip = lstf.rpartition("/*]]>*/")      
      if len(trip[1]) > 0 and len(trip[2]) < 100:
         lstf = ''

      self._log += logf
      final = logf.partition(logcodei)
      z = final[0].rpartition(chr(10))
      prev = '%08d' %  (self._log_cnt - 1)
      zz = z[0].rpartition("\nE3969440A681A24088859985" + prev +'\n')
      logd = zz[2].replace(mj.decode(), '')

      lstd = lstf.replace(chr(12), chr(10)).replace('<body class="c body">',
                                                    '<body class="l body">').replace("font-size: x-small;",
                                                                                     "font-size:  normal;")
      return dict(LOG=logd, LST=lstd)

   def _breakprompt(self, eos):
        found = False
        logf  = ''
        lstf  = ''
        bc    = False

        if self.pid is None:
            return dict(LOG="No SAS process attached. SAS process has terminated unexpectedly.", LST='', ABORT=True)

        if self.sascfg.ssh:
           response = self.sascfg._prompt(
                     "SAS attention handling not supported over ssh. Please enter (T) to terminate SAS or (C) to continue.")
           while True:
              if response.upper() == 'C':
                 return dict(LOG='', LST='', BC=True)
              if response.upper() == 'T':
                 break
              response = self.sascfg._prompt("Please enter (T) to terminate SAS or (C) to continue.")
              
        interrupt = signal.SIGINT
        os.kill(self.pid, interrupt)
        sleep(.25)

        while True:
            rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
            if rc is not None:
                self.pid = None
                outrc = str(rc)
                return dict(LOG='SAS process has terminated unexpectedly. Pid State= ' +
                            outrc, LST='',ABORT=True)

            lst = self.stdout.read1(4096).decode()
            lstf += lst
            if len(lst) > 0:
                lsts = lst.rpartition('Select:')
                if lsts[0] != '' and lsts[1] != '':
                    found = True
                    query = lsts[1] + lsts[2].rsplit('\n?')[0] + '\n'
                    print('Processing interrupt\nAttn handler Query is\n\n' + query)
                    response = self.sascfg._prompt("Please enter your Response: ")
                    self.stdin.write(response.encode() + b'\n')
                    self.stdin.flush()
                    if (response == 'C' or response == 'c') and query.count("C. Cancel") >= 1:
                       bc = True
                       break
                else:
                    lsts = lst.rpartition('Press')
                    if lsts[0] != '' and lsts[1] != '':
                        query = lsts[1] + lsts[2].rsplit('\n?')[0] + '\n'
                        print('Secondary Query is:\n\n' + query)
                        response = self.sascfg._prompt("Please enter your Response: ")
                        self.stdin.write(response.encode() + b'\n')
                        self.stdin.flush()
                        if (response == 'N' or response == 'n') and query.count("N to continue") >= 1:
                           bc = True
                           break
                    else:
                        #print("******************No 'Select' or 'Press' found in lst=")
                        pass
            else:
                log = self.stderr.read1(4096).decode()
                logf += log
                self._log += log

                if log.count(eos) >= 1:
                    print("******************Found end of step. No interrupt processed")
                    found = True

                if found:
                    break

            sleep(.25)

        lstr = lstf
        logr = logf

        return dict(LOG=logr, LST=lstr, BC=bc)

   def _break(self, inlst=''):
      found = False
      lst = inlst

      interupt = signal.SIGINT
      os.kill(self.pid, interupt)
      sleep(.25)
      self._asubmit('','text')

      while True:
         if len(lst) >  0:
            lsts = lst.rpartition('Select:')
            if lsts[0] != '' and lsts[1] != '':
               found = True
               print('Processing interupt\nAttn handler Query is\n\n'+lsts[1]+lsts[2].rsplit('\n?')[0]+'\n')
               opt = lsts[2].partition('Cancel Submitted Statements')
               if opt[0] != '' and opt[1] != '':
                  response = opt[0].rpartition('.')[0].rpartition(' ')[2]
               else:
                  opt = lsts[2].partition('Halt DATA')
                  if opt[0] != '' and opt[1] != '':
                     response = opt[0].rpartition('.')[0].rpartition(' ')[2]
                  else:
                     opt = lsts[2].partition('Cancel the dialog')
                     if opt[0] != '' and opt[1] != '':
                        response = opt[0].rpartition('.')[0].rpartition(' ')[2]
                     else:
                        print("Unknown 'Select' choices found: ")
                        response = ''
   
               print("'Select' Response="+response+'\n')
               self._asubmit(response+'\n','text')
            else:
               lsts = lst.rpartition('Press')
               if lsts[0] != '' and lsts[1] != '':
                  print('Seconday Query is:\n\n'+lsts[1]+lsts[2].rsplit('\n?')[0]+'\n')
                  opt = lsts[2].partition(' to exit ')
                  if opt[0] != '' and opt[1] != '':
                     response = opt[0].rpartition(' ')[2]
                  else:
                     opt = lsts[2].partition('N to continue')
                     if opt[0] != '' and opt[1] != '':
                        response = 'Y'
                     else:
                        response = 'X'

                  print("'Press' Response="+response+'\n')
                  self._asubmit(response+'\n','text')
               else:
                  #print("******************No 'Select' or 'Press' found in lst=")
                  pass

            sleep(.25)
            lst = self.stdout.read1(4096).decode()
         else:
            log = self.stderr.read1(4096).decode()
            self._log += log
            logn = self._logcnt(False)

            if log.count("\nE3969440A681A24088859985"+logn) >= 1:
               print("******************Found end of step. No interupt processed")
               found = True

            if found:
               ll = self.submit('ods html5 close;ods listing close;ods listing;libname work list;\n','text')
               break

            sleep(.25)
            lst = self.stdout.read1(4096).decode()

      return log

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
      code  = "data _null_; e = exist('"
      if len(libref):
         code += libref+"."
      code += table+"');\n" 
      code += "te='TABLE_EXISTS='; put te e;run;"
   
      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("TABLE_EXISTS= ")
      l2 = l2[2].partition("\n")
      exists = int(l2[0])
   
      return exists
   
   def read_csv(self, file: str, table: str, libref: str ="", results: str ='HTML', nosub: bool =False) -> '<SASdata object>':
      '''
      This method will import a csv file into a SAS Data Set and return the SASdata object referring to it.
      file    - eithe the OS filesystem path of the file, or HTTP://... for a url accessible file
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      results - format of results, HTML is default, TEXT is the alternative
      '''
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
         ll = self.submit(code, "text")
         if self._sb.exist(table, libref):
            return self._sb.sasdata(table, libref, results)
         else:
            return None
   
   def to_csv(self, file: str, data: '<SASdata object>', nosub: bool =False) -> 'The LOG showing the results of the step':
      '''
      This method will export a SAS Data Set to a file in CSV format.
      file    - the OS filesystem path of the file to be created (exported from this SAS Data Set)
      '''
      code  = "options nosource;\n"
      code += "filename x \""+file+"\";\n"
      code += "proc export data="+data.libref+"."+data.table+" outfile=x"
      code += " dbms=csv replace; run;"
      code += "options source;\n"

      if nosub:
         print(code)
      else:
         ll = self.submit(code, "text")
         print(ll['LOG'])

   def dataframe2sasdata(self, df: '<Pandas Data Frame object>', table: str ='a', libref: str ="", results: str ='HTML') -> '<SASdata object>':
      '''
      This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      results - format of results, HTML is default, TEXT is the alternative
      '''
      input  = ""
      card   = ""
      format = ""
      length = ""
      dts    = []

      for name in range(len(df.columns)):
         input += "'"+df.columns[name]+"'n "
         if df.dtypes[df.columns[name]].kind in ('O','S','U','V'):
            col_l = df[df.columns[name]].map(len).max()
            length += " '"+df.columns[name]+"'n $"+str(col_l)
            dts.append('C')
         else:
            if df.dtypes[df.columns[name]].kind in ('M'):
               length += " '"+df.columns[name]+"'n 8"
               input  += ":E8601DT26.6 "
               format += "'"+df.columns[name]+"'n E8601DT26.6 "
               dts.append('D')
            else:
               length += " '"+df.columns[name]+"'n 8"
               dts.append('N')

      code = "data "
      if len(libref):
         code += libref+"."
      code += table+";\n"
      if len(length):
         code += "length"+length+";\n"
      if len(format):
         code += "format "+format+";\n"
      code += "infile datalines delimiter='09'x;\n input "+input+";\n datalines;"
      self._asubmit(code, "text")

      for row in df.iterrows():
         card  = ""
         for col in range(len(row[1])):
            var = str(row[1][col])
            if dts[col] == 'N' and var == 'nan':
               var = '.'
            if dts[col] == 'D': 
               if var == 'nan':
                  var = '.'
               else:
                  var = str(row[1][col].to_datetime64())
            card += var+chr(9)
         self._asubmit(card, "text")
   
      self._asubmit(";run;", "text")
   
   def sasdata2dataframe(self, sd: '<SASdata object>', **kwargs) -> '<Pandas Data Frame object>':
      '''
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      sd      - SASdata object that refers to the Sas Data Set you want to export to a Pandas Data Frame
      port    - port to use for socket. Defaults to 0 which uses a random available ephemeral port
      '''
      port =  kwargs.get('port', 0)
      import pandas as pd
      import socket as socks
      datar = ""

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
      for i in range(nvars):
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "run;\n"
   
      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("FMT_CATS=")
      l2 = l2[2].partition("\n")              
      varcat = l2[2].split("\n", nvars)
      del varcat[nvars]
   
      try:
         sock = socks.socket()
         sock.bind(("",port))
         port = sock.getsockname()[1]
      except OSError:
         print('Error try to open a socket in the sasdata2dataframe method. Call failed.')
         return None

      if self.sascfg.ssh:
         host = socks.gethostname()
      else:
         host = ''
   
      code  = ""
      code += "filename sock socket '"+host+":"+str(port)+"' lrecl=32767 recfm=v termstr=LF;\n"
      code += " data _null_; set "+sd.libref+"."+sd.table+";\n file sock; put "
      for i in range(nvars):
         code += "'"+varlist[i]+"'n "
         if vartype[i] == 'N':
            if varcat[i] in sas_date_fmts:
               code += 'E8601DA10. '
            else:
               if varcat[i] in sas_time_fmts:
                  code += 'E8601TM15.6 '
               else:
                  if varcat[i] in sas_datetime_fmts:
                     code += 'E8601DT26.6 '
                  else:
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


