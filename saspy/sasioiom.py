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

import os
import subprocess
import getpass
from time import sleep
import socket as socks

try:
   import saspy.sascfg_personal as SAScfg
except ImportError:
   import saspy.sascfg as SAScfg

try:
   import pandas as pd
except ImportError:
   pass
try:
   from IPython.display import HTML
except ImportError:
   pass
try:
   import fcntl
   import signal
except ImportError:
   pass

class SASconfigIOM:
   '''
   This object is not intended to be used directly. Instantiate a SASsession object instead 
   '''
   def __init__(self, **kwargs):
      self._kernel  = kwargs.get('kernel', None)

      self.name      = kwargs.get('sascfgname', '')
      cfg            = getattr(SAScfg, self.name) 

      self.java      = cfg.get('java', '')
      self.iomhost   = cfg.get('iomhost', '')
      self.iomport   = cfg.get('iomport', None)
      self.omruser   = cfg.get('omruser', '')
      self.omrpw     = cfg.get('omrpw', '')
      self.encoding  = cfg.get('encoding', '')
      self.classpath = cfg.get('classpath', '')
      self.authkey   = cfg.get('authkey', '')
      self.timeout   = cfg.get('timeout', None)
      self.appserver = cfg.get('appserver', '')

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

      injava = kwargs.get('java', '')
      if len(injava) > 0:
         if lock and len(self.java):
            print("Parameter 'java' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.java = injava   

      inhost = kwargs.get('iomhost', '')
      if len(inhost) > 0:
         if lock and len(self.iomhost):
            print("Parameter 'iomhost' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.iomhost = inhost   

      intout = kwargs.get('timeout', None)
      if intout is not None:
         if lock and self.timeout:
            print("Parameter 'timeout' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.timeout = intout   

      inport = kwargs.get('iomport', None)
      if inport:
         if lock and self.iomport:
            print("Parameter 'port' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.iomport = inport   

      inomruser = kwargs.get('omruser', '')
      if len(inomruser) > 0:
         if lock and len(self.omruser):
            print("Parameter 'omruser' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.omruser = inomruser   

      inomrpw = kwargs.get('omrpw', '')
      if len(inomrpw) > 0:
         if lock and len(self.omrpw):
            print("Parameter 'omrpw' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.omrpw = inomrpw   

      incp = kwargs.get('classpath', '')
      if len(incp) > 0:
         if lock and len(self.classpath):
            print("Parameter 'classpath' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.classpath = incp   

      inak = kwargs.get('authkey', '')
      if len(inak) > 0:
         if lock and len(self.authkey):
            print("Parameter 'authkey' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.authkey = inak   

      inapp = kwargs.get('appserver', '')
      if len(inapp) > 0:
         if lock and len(self.apserver):
            print("Parameter 'appserver' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.appserver = inapp   

      inencoding = kwargs.get('encoding', '')
      if len(inencoding) > 0:
         if lock and len(self.encoding):
            print("Parameter 'encoding' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.encoding = inencoding   
      if not self.encoding:
         self.encoding = 'utf-8'  

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
                   
class SASsessionIOM():
   '''
   The SASsession object is the main object to instantiate and provides access to the rest of the functionality.

   cfgname   - value in SAS_config_names List of the sascfg.py file
   kernel    - None - internal use when running the SAS_kernel notebook
   java      - the path to the java executable to use
   iomhost   - for remote IOM case, not local Windows] the resolvable host name, or ip to the IOM server to connect to
   iomport   - for remote IOM case, not local Windows] the port IOM is listening on
   omruser   - user id for IOM access
   omrpw     - pw for user for IOM access
   encoding  - This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
   classpath - classpath to IOM client jars and saspyiom client jar.
   '''
   def __init__(self, **kwargs):
      self.pid    = None
      self.stdin  = None
      self.stderr = None
      self.stdout = None

      self.sascfg   = SASconfigIOM(**kwargs)
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

      # check for local iom server
      if len(self.sascfg.iomhost) > 0:
         zero = False
         if isinstance(self.sascfg.iomhost, list):
            self.sascfg.iomhost = ";".join(self.sascfg.iomhost)
      else:
         zero = True

      port = 0
      try:
         self.sockin  = socks.socket()
         self.sockin.bind(("",port))
         #self.sockin.bind(("",32701))

         self.sockout = socks.socket()
         self.sockout.bind(("",port))
         #self.sockout.bind(("",32702))

         self.sockerr = socks.socket()
         self.sockerr.bind(("",port))
         #self.sockerr.bind(("",32703))
      except OSError:
         print('Error try to open a socket in the _startsas method. Call failed.')
         return None
      self.sockin.listen(0)
      self.sockout.listen(0)
      self.sockerr.listen(0)

      if not zero:
         if self.sascfg.output.lower() == 'html':
            print("""HTML4 is only valid in 'local' mode (SAS_output_options in sascfg.py).
Please see SAS_config_names templates 'default' (STDIO) or 'winlocal' (IOM) in the default sascfg.py.
Will use HTML5 for this SASsession.""")
            self.sascfg.output = 'html5'

         user  = self.sascfg.omruser
         pw    = self.sascfg.omrpw
         found = False
         if self.sascfg.authkey:
            if os.name == 'nt': 
               pwf = os.path.expanduser('~')+os.sep+'_authinfo'
            else:
               pwf = os.path.expanduser('~')+os.sep+'.authinfo'
            try:
               fid = open(pwf, mode='r')
               for line in fid:
                  if line.startswith(self.sascfg.authkey): 
                     user = line.partition('user')[2].lstrip().partition(' ')[0].partition('\n')[0]
                     pw   = line.partition('password')[2].lstrip().partition(' ')[0].partition('\n')[0]
                     found = True
               fid.close()
            except OSError as e:
               print('Error trying to read authinfo file:'+pwf+'\n'+str(e))
               pass
            except:
               pass

            if not found:
               print('Did not find key '+self.sascfg.authkey+' in authinfo file:'+pwf+'\n')

         while len(user) == 0:
            user = self.sascfg._prompt("Please enter the IOM user id: ")

      pgm    = self.sascfg.java
      parms  = [pgm]
      parms += ["-classpath",  self.sascfg.classpath, "pyiom.saspy2j", "-host", "localhost"]
      #parms += ["-classpath", self.sascfg.classpath+":/u/sastpw/tkpy2j", "pyiom.saspy2j_sleep", "-host", "tomspc.na.sas.com"]
      parms += ["-stdinport",  str(self.sockin.getsockname()[1])]
      parms += ["-stdoutport", str(self.sockout.getsockname()[1])]
      parms += ["-stderrport", str(self.sockerr.getsockname()[1])]
      if self.sascfg.timeout is not None:
         parms += ["-timeout", str(self.sascfg.timeout)]
      if self.sascfg.appserver:
         parms += ["-appname", "'"+self.sascfg.appserver+"'"]
      if not zero:
         parms += ["-iomhost", self.sascfg.iomhost, "-iomport", str(self.sascfg.iomport)]     
         parms += ["-user", user]     
      else:
         parms += ["-zero"]     
      parms += ['']

      s = ''
      for i in range(len(parms)):
         if i == 2 and os.name == 'nt':
            s += '"'+parms[i]+'"'+' '
         else:
            s += parms[i]+' '

      if os.name == 'nt': 
         try:
            self.pid = subprocess.Popen(parms, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pid = self.pid.pid
         except OSError as e:
            print("The OS Error was:\n"+e.strerror+'\n')
            print("SAS Connection failed. No connection established. Double check you settings in sascfg.py file.\n")  
            print("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
            print("If no OS Error above, try running the following command (where saspy is running) manually to see what is wrong:\n"+s+"\n")
            return None
      else:
         #signal.signal(signal.SIGCHLD, signal.SIG_IGN)

         PIPE_READ  = 0
         PIPE_WRITE = 1
         
         pin  = os.pipe() 
         pout = os.pipe()
         perr = os.pipe() 
      
         try:
            pidpty = os.forkpty()
         except:
            import pty
            pidpty = pty.fork()

         if pidpty[0]:
            # we are the parent
            self.pid = pidpty[0]
            pid = self.pid

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
               #sleep(5)
               os.execv(pgm, parms)
            except OSError as e:
               print("The OS Error was:\n"+e.strerror+'\n')
               print("SAS Connection failed. No connection established. Double check you settings in sascfg.py file.\n")  
               print("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
               print("If no OS Error above, try running the following command (where saspy is running) manually to see what is wrong:\n"+s+"\n")
               os._exit(-6)

      if os.name == 'nt': 
         try:
            self.pid.wait(1)

            error  = self.pid.stderr.read(4096).decode()+'\n' 
            error += self.pid.stdout.read(4096).decode() 
            print("Java Error:\n"+error)

            print("Subprocess failed to start. Double check you settings in sascfg.py file.\n") 
            print("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
            print("If no Java Error above, try running the following command (where saspy is running) manually to see if it's a problem starting Java:\n"+s+"\n")
            self.pid = None
            return None
         except:
            pass
      else:

         self.pid    = pidpty[0]
         self.stdin  = os.fdopen(pin[PIPE_WRITE], mode='wb')
         self.stderr = os.fdopen(perr[PIPE_READ], mode='rb')
         self.stdout = os.fdopen(pout[PIPE_READ], mode='rb')
   
         fcntl.fcntl(self.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
         fcntl.fcntl(self.stderr, fcntl.F_SETFL, os.O_NONBLOCK)

         sleep(1)
         rc = os.waitpid(self.pid, os.WNOHANG)
         if rc[0] == 0:
            pass
         else:
            error  = self.stderr.read1(4096).decode()+'\n' 
            error += self.stdout.read1(4096).decode() 
            print("Java Error:\n"+error)
            print("SAS Connection failed. No connection established. Staus="+str(rc)+"  Double check you settings in sascfg.py file.\n")  
            print("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
            print("If no Java Error above, try running the following command (where saspy is running) manually to see if it's a problem starting Java:\n"+s+"\n")
            self.pid = None
            return None

      self.stdin  = self.sockin.accept()
      self.stdout = self.sockout.accept()
      self.stderr = self.sockerr.accept()
      self.stdout[0].setblocking(False)
      self.stderr[0].setblocking(False)

      if not zero:
         while len(pw) == 0:
            pw = self.sascfg._prompt("Please enter the password for IOM user "+self.sascfg.omruser+": ", pw=True)
         pw += '\n'
         self.stdin[0].send(pw.encode())

      ll = self.submit("options svgtitle='svgtitle'; options validvarname=any pagesize=max nosyntaxcheck; ods graphics on;", "text")

      if self.pid is None:
         print(ll['LOG'])
         print("SAS Connection failed. No connection established. Double check you settings in sascfg.py file.\n")  
         print("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
         if zero:
            print("Be sure the path to sspiauth.dll is in your System PATH"+"\n")
         return None

      print("SAS Connection established. Subprocess id is "+str(pid)+"\n")  
      return self.pid
   
   def _endsas(self):
      rc = 0
      if self.pid:
         self.stdin[0].send(b'\ntom says EOL=ENDSAS                          \n')
         if os.name == 'nt': 
            pid = self.pid.pid
            try:
               rc = self.pid.wait(5)
               self.pid = None
            except (subprocess.TimeoutExpired):
               print("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
               self.pid.kill()
         else:
            pid = self.pid
            x = 5
            while True:
               rc = os.waitpid(self.pid, os.WNOHANG)
               if rc[0] != 0:
                  break
               x = x - 1
               if x < 1:
                  break
               sleep(1)

            if rc[0] != 0:
               pass
            else:
               print("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
               os.kill(self.pid, signal.SIGKILL)


         self.stdin[0].shutdown(socks.SHUT_RDWR)
         self.stdin[0].close()
         self.sockin.close()

         self.stdout[0].shutdown(socks.SHUT_RDWR)
         self.stdout[0].close()
         self.sockout.close()

         self.stderr[0].shutdown(socks.SHUT_RDWR)
         self.stderr[0].close()
         self.sockerr.close()
      
         print("SAS Connection terminated. Subprocess id was "+str(pid))
         self.pid = None

      return 



   '''
   def _getlog(self, wait=5, jobid=None):
      logf   = b''
      quit   = wait * 2
      logn   = self._logcnt(False)
      code1  = "%put E3969440A681A24088859985"+logn+";\nE3969440A681A24088859985"+logn

      while True:
         try:
            log =  self.stderr[0].recv(4096)
         except (BlockingIOError):
            log = b''

         if len(log) > 0:
            logf += log
         else:
            quit -= 1
            if quit < 0 or len(logf) > 0:
               break
            sleep(0.5)
   
      x = logf.decode(errors='replace').replace(code1, " ")
      self._log += x

      if os.name == 'nt': 
         try:
            rc = self.pid.wait(0)
            self.pid = None
            return 'SAS process has terminated unexpectedly. RC from wait was: '+str(rc)
         except:
            pass
      else:
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
         try:
            lst = self.stdout[0].recv(4096)
         except (BlockingIOError):
            lst = b''

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

      if os.name == 'nt': 
         try:
            rc = self.pid.wait(0)
            self.pid = None
            return 'SAS process has terminated unexpectedly. RC from wait was: '+str(rc)
         except:
            pass
      else:
         if self.pid == None:
            return "No SAS process attached. SAS process has terminated unexpectedly."
         rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
         if rc != None:
            self.pid = None
            return 'SAS process has terminated unexpectedly. Pid State= '+str(rc)
 
      return lstf.decode(errors='replace')
   
   def _getlsttxt(self, wait=5, jobid=None):
      f2 = [None]
      lstf = b''
      quit = wait * 2
      eof = 0
      self._asubmit("data _null_;file print;put 'Tom was here';run;", "text")
   
      while True:
         try:
            lst = self.stdout[0].recv(4096)
         except (BlockingIOError):
            lst = b''

         if len(lst) > 0:
            lstf += lst
   
            lenf = len(lstf)
            eof = lstf.find(b"Tom was here", lenf - 25, lenf)
      
            if (eof != -1):
               final = lstf.partition(b"Tom was here")
               f2 = final[0].decode(errors='replace').rpartition(chr(12))
               break

      lst = f2[0]

      if os.name == 'nt': 
         try:
            rc = self.pid.wait(0)
            self.pid = None
            return 'SAS process has terminated unexpectedly. RC from wait was: '+str(rc)
         except:
            pass
      else:
         if self.pid == None:
            return "No SAS process attached. SAS process has terminated unexpectedly."
         rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
         if rc != None:
            self.pid = None
            return 'SAS process has terminated unexpectedly. Pid State= '+str(rc)
 
      return lst.replace(chr(12), '\n')
   '''



   def _asubmit(self, code, results="html"):
      # as this is an _ method, it's not really to be used. Of note is that if this is used and if what it submitted generates
      # anything to the lst, then unless _getlst[txt] is called, then next submit will happen to get the lst this wrote, plus
      # what it generates. If the two are not of the same type (html, text) it could be problematic, beyond not being what was
      # expected in the first place. __flushlst__() used to be used, but was never needed. Adding this note and removing the
      # unnecessary read in submit as this can't happen in the current code. 
      odsopen = b"ods listing close;ods "+str.encode(self.sascfg.output)+b" (id=saspy_internal) file=_tomods1 options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods "+str.encode(self.sascfg.output)+b" (id=saspy_internal) close;ods listing;\n"
      ods      = True
      pgm      = b""

      if results.upper() != "HTML":
         ods = False
   
      if (ods):
         pgm += odsopen
   
      pgm += code.encode()+b'\n'+b'tom says EOL=ASYNCH                          \n'
   
      if (ods):
         pgm += odsclose

      self.stdin[0].send(pgm)

      return 

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
      #odsopen  = b"ods listing close;ods html5 (id=saspy_internal) file=STDOUT options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n"
      odsopen = b"ods listing close;ods "+str.encode(self.sascfg.output)+b" (id=saspy_internal) file=_tomods1 options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods "+str.encode(self.sascfg.output)+b" (id=saspy_internal) close;ods listing;\n"
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
      pgm      = b''

      if self.pid == None:
         print("No SAS process attached. SAS process has terminated unexpectedly.")
         return dict(LOG="No SAS process attached. SAS process has terminated unexpectedly.", LST='')

      if os.name == 'nt': 
         try:
            rc = self.pid.wait(0)
            self.pid = None
            return dict(LOG='SAS process has terminated unexpectedly. RC from wait was: '+str(rc), LST='')
         except:
            pass
      else:
         if self.pid == None:
            return "No SAS process attached. SAS process has terminated unexpectedly."
         #rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
         rc = os.waitpid(self.pid, os.WNOHANG)
         #if rc != None:
         if rc[1]:
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
         pgm += odsopen
   
      pgm += mj+b'\n'+pcodei.encode()+pcodeiv.encode()
      pgm += code.encode()+b'\n'+pcodeo.encode()+b'\n'+mj
   
      if ods:
         pgm += odsclose

      pgm += b'\n'+logcodei.encode()+b'\n'
      self.stdin[0].send(pgm+b'tom says EOL='+logcodeo.encode()+b'\n')

      while not done:
         try:
             while True:
                 if os.name == 'nt': 
                    try:
                       rc = self.pid.wait(0)
                       self.pid = None
                       return dict(LOG=logf.partition(logcodeo)[0]+'\nSAS process has terminated unexpectedly. RC from wait was: '+str(rc), LST='')
                    except:
                       pass
                 else:
                    #rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
                    rc = os.waitpid(self.pid, os.WNOHANG)
                    #if rc is not None:
                    if rc[1]:
                        self.pid = None
                        return dict(LOG=logf.partition(logcodeo)[0]+'\nSAS process has terminated unexpectedly. Pid State= '+str(rc), LST='')

                 if bail:
                    if lstf.count(logcodeo) >= 1:
                       lstf = lstf.rsplit(logcodeo)[0]
                       break
                 try:
                    lst = self.stdout[0].recv(4096).decode(errors='replace')
                 except (BlockingIOError):
                    lst = b''

                 if len(lst) > 0:
                    #print("LIST = \n"+lst)
                    lstf += lst
                 else:
                    sleep(0.1)
                    try:
                       log = self.stderr[0].recv(4096).decode(errors='replace') 
                    except (BlockingIOError):
                       log = b''

                    if len(log) > 0:
                       #print("LOG = \n"+log)
                       logf += log
                       if logf.count(logcodeo) >= 1:
                          bail = True
                       if not bail and bc:
                          self.stdin[0].send(odsclose+logcodei.encode()+b'tom says EOL='+logcodeo.encode()+b'\n')
                          bc = False
             done = True

         except (ConnectionResetError):
             rc = 0
             if os.name == 'nt': 
                try:
                   rc = self.pid.wait()
                except:
                   pass
             else:
                rc = os.waitpid(self.pid, 0)

             self.pid = None
             return dict(LOG=logf.partition(logcodeo)[0]+'\nConnection Reset: SAS process has terminated unexpectedly. Pid State= '+str(rc), LST='')
             
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

             self.stdin[0].send(odsclose+logcodei.encode()+b'tom says EOL='+logcodeo.encode()+b'\n')

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

        if True:
           response = self.sascfg._prompt(
                     "SAS attention handling is not yet supported over IOM. Please enter (T) to terminate SAS or (C) to continue.")
           while True:
              if response.upper() == 'C':
                 return dict(LOG='', LST='', BC=True)
              if response.upper() == 'T':
                 break
              response = self.sascfg._prompt("Please enter (T) to terminate SAS or (C) to continue.")
              
        if os.name == 'nt': 
           self.pid.kill()
        else:
           interrupt = signal.SIGINT
           os.kill(self.pid, interrupt)
           sleep(.25)

        self.pid = None
        return dict(LOG="SAS process terminated", LST='', ABORT=True)




        '''
        while True:
            rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
            if rc is not None:
                self.pid = None
                outrc = str(rc)
                return dict(LOG='SAS process has terminated unexpectedly. Pid State= '+outrc, LST='', ABORT=True)

            lst = self.stdout.read1(4096).decode(errors='replace')
            lstf += lst
            if len(lst) > 0:
                lsts = lst.rpartition('Select:')
                if lsts[0] != '' and lsts[1] != '':
                    found = True
                    query = lsts[1] + lsts[2].rsplit('\n?')[0] + '\n'
                    print('Processing interrupt\nAttn handler Query is\n\n' + query)
                    response = self.sascfg._prompt("Please enter your Response: ")
                    self.stdin[0].send(response.encode() + b'\n')
                    if (response == 'C' or response == 'c') and query.count("C. Cancel") >= 1:
                       bc = True
                       break
                else:
                    lsts = lst.rpartition('Press')
                    if lsts[0] != '' and lsts[1] != '':
                        query = lsts[1] + lsts[2].rsplit('\n?')[0] + '\n'
                        print('Secondary Query is:\n\n' + query)
                        response = self.sascfg._prompt("Please enter your Response: ")
                        self.stdin[0].send(response.encode() + b'\n')
                        if (response == 'N' or response == 'n') and query.count("N to continue") >= 1:
                           bc = True
                           break
                    else:
                        #print("******************No 'Select' or 'Press' found in lst=")
                        pass
            else:
                log = self.stderr[0].recv(4096).decode(errors='replace')
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
        '''

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
      code += "te='TABLE_EXISTS='; put te e;run;\n"
   
      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("TABLE_EXISTS= ")
      l2 = l2[2].partition("\n")
      exists = int(l2[0])
   
      return exists
   
   def read_csv(self, file: str, table: str, libref: str ="", nosub: bool =False, opts: dict ={}) -> '<SASdata object>':
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
      This method will export a SAS Data Set to a file in CSV format.
      file    - the OS filesystem path of the file to be created (exported from the SAS Data Set)
      table   - the name of the SAS Data Set you want to export to a CSV file
      libref  - the libref for the SAS Data Set.
      dsopts  - a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs)
      opts    - a dictionary containing any of the following Proc Export options(delimiter, putnames)
      '''
      code  = "options nosource;\n"
      code += "filename x \""+file+"\";\n"
      code += "proc export data="+libref+"."+table+self._sb._dsopts(dsopts)+" outfile=x dbms=csv replace; "
      code += self._sb._expopts(opts)+" run\n;"
      code += "options source;\n"

      if nosub:
         print(code)
      else:
         ll = self.submit(code, "text")
         return ll['LOG']

   def dataframe2sasdata(self, df: '<Pandas Data Frame object>', table: str ='a', libref: str =""):
      '''
      This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      '''
      input  = ""
      card   = ""
      format = ""
      length = ""
      dts    = []
      ncols  = len(df.columns)

      for name in range(ncols):
         input += "'"+df.columns[name]+"'n "
         if df.dtypes[df.columns[name]].kind in ('O','S','U','V'):
            col_l = df[df.columns[name]].map(len, 'ignore').max()
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
         code += "length "+length+";\n"
      if len(format):
         code += "format "+format+";\n"
      code += "infile datalines delimiter='03'x;\ninput @;\nif _infile_ = '' then delete;\ninput "+input+";\ndatalines;"
      self._asubmit(code, "text")

      code = ""
      for row in df.itertuples(index=False):
         card  = ""
         for col in range(ncols):
            var = str(row[col])
            if dts[col] == 'N' and var == 'nan':
               var = '.'
            if dts[col] == 'D': 
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

      self._asubmit(code+";\nrun;", "text")
      ll = self.submit("", 'text')
      return
   
   def sasdata2dataframe(self, table: str, libref: str ='', dsopts: dict ={}, rowsep: str = '\x01', colsep: str = '\x02', **kwargs) -> '<Pandas Data Frame object>':
      '''
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table   - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref  - the libref for the SAS Data Set.
      rowsep  - the row seperator character to use; defaults to '\n'
      colsep  - the column seperator character to use; defaults to '\t'
      '''
      datar = ""
      if libref:
         tabname = libref+"."+table
      else:
         tabname = table

      code  = "proc sql; create view sasdata2dataframe as select * from "+tabname+self._sb._dsopts(dsopts)+";quit;\n"
      code += "data _null_; file LOG; d = open('sasdata2dataframe');\n"
      code += "length var $256;\n"
      code += "lrecl = attrn(d, 'LRECL'); nvars = attrn(d, 'NVARS');\n"
      code += "lr='LRECL='; vn='VARNUMS='; vl='VARLIST='; vt='VARTYPE='; vf='VARFMT=';\n"
      code += "put lr lrecl; put vn nvars; put vl;\n"
      code += "do i = 1 to nvars; var = compress(varname(d, i), '00'x); put var; end;\n"
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
   
      topts             = dict(dsopts)
      topts['obs']      = 1
      topts['firstobs'] = ''

      code  = "data _null_; set "+tabname+self._sb._dsopts(topts)+";put 'FMT_CATS=';\n"
      for i in range(nvars):
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "run;"
   
      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("FMT_CATS=")
      l2 = l2[2].partition("\n")              
      varcat = l2[2].split("\n", nvars)
      del varcat[nvars]

      rdelim = "'"+'%02x' % ord(rowsep.encode(self.sascfg.encoding))+"'x"
      cdelim = "'"+'%02x' % ord(colsep.encode(self.sascfg.encoding))+"'x "

      code = "data _null_; set "+tabname+self._sb._dsopts(dsopts)+";\n file _tomods1 termstr=NL; put "
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
            code += cdelim
         else:
            code += rdelim
      code += ";\n run;"

      ll = self.submit(code, 'text')

      if (len(ll['LST']) > 1) and (ll['LST'][0] == "\ufeff"):
         ll['LST'] = ll['LST'][1:len(ll['LST'])]

      r = []
      for i in ll['LST'].split(sep=rowsep+'\n'):
         if i != '':
            r.append(tuple(i.split(sep=colsep)))

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
