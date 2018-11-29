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
from time import sleep
import socket as socks
import tempfile as tf

try:
   import pandas as pd
   import numpy  as np
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
   """
   This object is not intended to be used directly. Instantiate a SASsession object instead
   """
   def __init__(self, session, **kwargs):
      self._kernel  = kwargs.get('kernel', None)

      SAScfg         = session._sb.sascfg.SAScfg
      self.name      = session._sb.sascfg.name
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
      self.sspi      = cfg.get('sspi', False)
      self.javaparms = cfg.get('javaparms', '')
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

      self.verbose = self.cfgopts.get('verbose', True)
      self.verbose = kwargs.get('verbose', self.verbose)

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

      insspi = kwargs.get('sspi', False)
      if insspi:
         if lock and self.sspi:
            print("Parameter 'sspi' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.sspi = insspi

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

      injparms = kwargs.get('javaparms', '')
      if len(injparms) > 0:
         if lock:
            print("Parameter 'javaparms' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.javaparms = injparms

      inlrecl = kwargs.get('lrecl', None)
      if inlrecl:
         if lock and self.lrecl:
            print("Parameter 'lrecl' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.lrecl = inlrecl
      if not self.lrecl:
         self.lrecl = 1048576

      self._prompt = session._sb.sascfg._prompt

      return

class SASsessionIOM():
   """
   The SASsession object is the main object to instantiate and provides access to the rest of the functionality.

   cfgname   - value in SAS_config_names List of the sascfg_personal.py file
   kernel    - None - internal use when running the SAS_kernel notebook
   java      - the path to the java executable to use
   iomhost   - for remote IOM case, not local Windows] the resolvable host name, or ip to the IOM server to connect to
   iomport   - for remote IOM case, not local Windows] the port IOM is listening on
   omruser   - user id for IOM access
   omrpw     - pw for user for IOM access
   encoding  - This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
   classpath - classpath to IOM client jars and saspyiom client jar.
   autoexec  - This is a string of SAS code that will be submitted upon establishing a connection.
   authkey   - Key value for finding credentials in .authfile
   timeout   - Timeout value for establishing connection to workspace server
   appserver - Appserver name of the workspace server to connect to
   sspi      - Boolean for using IWA to connect to a workspace server configured to use IWA
   javaparms - for specifying java commandline options if necessary
   """
   def __init__(self, **kwargs):
      self.pid    = None
      self.stdin  = None
      self.stderr = None
      self.stdout = None

      self._sb      = kwargs.get('sb', None)
      self.sascfg   = SASconfigIOM(self, **kwargs)
      self._log_cnt = 0
      self._log     = ""
      self._tomods1 = b"_tomods1"

      self._startsas()

   def __del__(self):
      if self.pid:
         self._endsas()
      self._sb.SASpid = None

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
      self.sockin.listen(1)
      self.sockout.listen(1)
      self.sockerr.listen(1)

      if not zero:
         if self.sascfg.output.lower() == 'html':
            print("""HTML4 is only valid in 'local' mode (SAS_output_options in sascfg_personal.py).
Please see SAS_config_names templates 'default' (STDIO) or 'winlocal' (IOM) in the sample sascfg.py.
Will use HTML5 for this SASsession.""")
            self.sascfg.output = 'html5'

         if not self.sascfg.sspi:
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
               if user is None:
                  self.sockin.close()
                  self.sockout.close()
                  self.sockerr.close()
                  self.pid = None
                  raise KeyboardInterrupt

      pgm    = self.sascfg.java
      parms  = [pgm]
      if len(self.sascfg.javaparms) > 0:
         parms += self.sascfg.javaparms
      parms += ["-classpath",  self.sascfg.classpath, "pyiom.saspy2j", "-host", "localhost"]
      #parms += ["-classpath", self.sascfg.classpath+":/u/sastpw/tkpy2j", "pyiom.saspy2j_sleep", "-host", "tomspc.na.sas.com"]
      #parms += ["-classpath", self.sascfg.classpath+";U:\\tkpy2j", "pyiom.saspy2j_sleep", "-host", "tomspc.na.sas.com"]
      parms += ["-stdinport",  str(self.sockin.getsockname()[1])]
      parms += ["-stdoutport", str(self.sockout.getsockname()[1])]
      parms += ["-stderrport", str(self.sockerr.getsockname()[1])]
      if self.sascfg.timeout is not None:
         parms += ["-timeout", str(self.sascfg.timeout)]
      if self.sascfg.appserver:
         parms += ["-appname", "'"+self.sascfg.appserver+"'"]
      if not zero:
         parms += ["-iomhost", self.sascfg.iomhost, "-iomport", str(self.sascfg.iomport)]
         if not self.sascfg.sspi:
            parms += ["-user", user]
         else:
            parms += ["-spn"]
      else:
         parms += ["-zero"]
      parms += ["-lrecl", str(self.sascfg.lrecl)]
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
            print("SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n")
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
               print("SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n")
               print("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
               print("If no OS Error above, try running the following command (where saspy is running) manually to see what is wrong:\n"+s+"\n")
               os._exit(-6)

      if os.name == 'nt':
         try:
            self.pid.wait(1)

            error  = self.pid.stderr.read(4096).decode()+'\n'
            error += self.pid.stdout.read(4096).decode()
            print("Java Error:\n"+error)

            print("Subprocess failed to start. Double check your settings in sascfg_personal.py file.\n")
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
            print("SAS Connection failed. No connection established. Staus="+str(rc)+"  Double check your settings in sascfg_personal.py file.\n")
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
         if not self.sascfg.sspi:
            while len(pw) == 0:
               pw = self.sascfg._prompt("Please enter the password for IOM user "+self.sascfg.omruser+": ", pw=True)
               if pw is None:
                  if os.name == 'nt':
                     self.pid.kill()
                  else:
                     os.kill(self.pid, signal.SIGKILL)
                  self.pid = None
                  raise KeyboardInterrupt
            pw += '\n'
            self.stdin[0].send(pw.encode())

      ll = self.submit("options svgtitle='svgtitle'; options validvarname=any pagesize=max nosyntaxcheck; ods graphics on;", "text")

      if self.pid is None:
         print(ll['LOG'])
         print("SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n")
         print("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
         if zero:
            print("Be sure the path to sspiauth.dll is in your System PATH"+"\n")
         return None

      if self.sascfg.verbose:
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
               if self.sascfg.verbose:
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
               if self.sascfg.verbose:
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

         if self.sascfg.verbose:
            print("SAS Connection terminated. Subprocess id was "+str(pid))
         self.pid = None

      return



   """
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
   """



   def _asubmit(self, code, results="html"):
      # as this is an _ method, it's not really to be used. Of note is that if this is used and if what it submitted generates
      # anything to the lst, then unless _getlst[txt] is called, then next submit will happen to get the lst this wrote, plus
      # what it generates. If the two are not of the same type (html, text) it could be problematic, beyond not being what was
      # expected in the first place. __flushlst__() used to be used, but was never needed. Adding this note and removing the
      # unnecessary read in submit as this can't happen in the current code.

      odsopen  = b"ods listing close;ods "+self.sascfg.output.encode()+ \
                 b" (id=saspy_internal) file="+self._tomods1+b" options(bitmap_mode='inline') device=svg style="+self._sb.HTML_Style.encode()+ \
                 b"; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods "+self.sascfg.output.encode()+b" (id=saspy_internal) close;ods listing;\n"
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

   def submit(self, code: str, results: str ="html", prompt: dict = None) -> dict:
      '''
      This method is used to submit any SAS code. It returns the Log and Listing as a python dictionary.
      code    - the SAS statements you want to execute
      results - format of results, HTML is default, TEXT is the alternative
      prompt  - dict of names:flags to prompt for; create macro variables (used in submitted code), then keep or delete
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
      prompt = prompt if prompt is not None else {}

      #odsopen  = b"ods listing close;ods html5 (id=saspy_internal) file=STDOUT options(bitmap_mode='inline') device=svg; ods graphics on / outputfmt=png;\n"
      odsopen  = b"ods listing close;ods "+self.sascfg.output.encode()+ \
                 b" (id=saspy_internal) file="+self._tomods1+b" options(bitmap_mode='inline') device=svg style="+self._sb.HTML_Style.encode()+ \
                 b"; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods "+self.sascfg.output.encode()+b" (id=saspy_internal) close;ods listing;\n"
      ods      = True;
      mj       = b";*\';*\";*/;"
      lstf     = b''
      logf     = b''
      bail     = False
      eof      = 5
      bc       = False
      done     = False
      logn     = self._logcnt()
      logcodei = "%put E3969440A681A24088859985" + logn + ";"
      logcodeo = b"\nE3969440A681A24088859985" + logn.encode()
      pcodei   = ''
      pcodeiv  = ''
      pcodeo   = ''
      pgm      = b''

      if self.pid == None:
         self._sb.SASpid = None
         print("No SAS process attached. SAS process has terminated unexpectedly.")
         return dict(LOG="No SAS process attached. SAS process has terminated unexpectedly.", LST='')

      if os.name == 'nt':
         try:
            rc = self.pid.wait(0)
            self.pid = None
            self._sb.SASpid = None
            return dict(LOG='SAS process has terminated unexpectedly. RC from wait was: '+str(rc), LST='')
         except:
            pass
      else:
         if self.pid == None:
            self._sb.SASpid = None
            return "No SAS process attached. SAS process has terminated unexpectedly."
         #rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
         rc = os.waitpid(self.pid, os.WNOHANG)
         #if rc != None:
         if rc[1]:
            self.pid = None
            self._sb.SASpid = None
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
               if var is None:
                  raise KeyboardInterrupt
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
      self.stdin[0].send(pgm+b'tom says EOL='+logcodeo+b'\n')

      while not done:
         try:
             while True:
                 if os.name == 'nt':
                    try:
                       rc = self.pid.wait(0)
                       self.pid = None
                       self._sb.SASpid = None
                       log = logf.partition(logcodeo)[0]+b'\nSAS process has terminated unexpectedly. RC from wait was: '+str(rc).encode()
                       return dict(LOG=log.decode(errors='replace'), LST='')
                    except:
                       pass
                 else:
                    #rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
                    rc = os.waitpid(self.pid, os.WNOHANG)
                    #if rc is not None:
                    if rc[1]:
                       self.pid = None
                       self._sb.SASpid = None
                       log = logf.partition(logcodeo)[0]+b'\nSAS process has terminated unexpectedly. Pid State= '+str(rc).encode()
                       return dict(LOG=log.decode(errors='replace'), LST='')

                 if bail:
                    if lstf.count(logcodeo) >= 1:
                       x = lstf.rsplit(logcodeo)
                       lstf = x[0]
                       if len(x[1]) > 7 and b"_tomods" in x[1]:
                          self._tomods1 = x[1]
                          #print("Tomods is now "+ self._tomods1.decode())
                       break
                 try:
                    lst = self.stdout[0].recv(4096)
                 except (BlockingIOError):
                    lst = b''

                 if len(lst) > 0:
                    #print("LIST = \n"+lst)
                    lstf += lst
                 else:
                    sleep(0.1)
                    try:
                       log = self.stderr[0].recv(4096)
                    except (BlockingIOError):
                       log = b''

                    if len(log) > 0:
                       #print("LOG = \n"+log)
                       logf += log
                       if logf.count(logcodeo) >= 1:
                          bail = True
                       if not bail and bc:
                          self.stdin[0].send(odsclose+logcodei.encode()+b'tom says EOL='+logcodeo+b'\n')
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
             self._sb.SASpid = None
             log =logf.partition(logcodeo)[0]+b'\nConnection Reset: SAS process has terminated unexpectedly. Pid State= '+str(rc).encode()
             return dict(LOG=log.decode(errors='replace'), LST='')

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

             self.stdin[0].send(odsclose+logcodei.encode()+b'tom says EOL='+logcodeo+b'\n')

      try:
         lstf = lstf.decode()
      except UnicodeDecodeError:
         try:
            lstf = lstf.decode(self.sascfg.encoding)
         except UnicodeDecodeError:
            lstf = lstf.decode(errors='replace')

      logf = logf.decode(errors='replace')

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
        logf  = b''
        lstf  = b''
        bc    = False

        if self.pid is None:
            self._sb.SASpid = None
            return dict(LOG=b"No SAS process attached. SAS process has terminated unexpectedly.", LST=b'', ABORT=True)

        if True:
           response = self.sascfg._prompt(
                     "SAS attention handling is not yet supported over IOM. Please enter (T) to terminate SAS or (C) to continue.")
           while True:
              if response is None or response.upper() == 'C':
                 return dict(LOG=b'', LST=b'', BC=True)
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
        self._sb.SASpid = None
        return dict(LOG=b"SAS process terminated", LST=b'', ABORT=True)




        """
        while True:
            rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
            if rc is not None:
                self.pid = None
                self._sb.SASpid = None
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
        """

   def saslog(self):
      """
      this method is used to get the current, full contents of the SASLOG
      """
      return self._log


   def disconnect(self):
      """
      This method disconnects an IOM session to allow for reconnecting when switching networks
      """

      pgm = b'\n'+b'tom says EOL=DISCONNECT                      \n'
      self.stdin[0].send(pgm)

      while True:
         try:
            log = self.stderr[0].recv(4096).decode(errors='replace')
         except (BlockingIOError):
            log = b''

         if len(log) > 0:
            if log.count("DISCONNECT") >= 1:
               break

      return log.rstrip("DISCONNECT")


   def exist(self, table: str, libref: str ="") -> bool:
      """
      table  - the name of the SAS Data Set
      libref - the libref for the Data Set, defaults to WORK, or USER if assigned

      Returns True it the Data Set exists and False if it does not
      """
      code  = "data _null_; e = exist('"
      if len(libref):
         code += libref+"."
      code += table+"');\n"
      code += "v = exist('"
      if len(libref):
         code += libref+"."
      code += table+"', 'VIEW');\n if e or v then e = 1;\n"
      code += "te='TABLE_EXISTS='; put te e;run;\n"

      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("TABLE_EXISTS= ")
      l2 = l2[2].partition("\n")
      exists = int(l2[0])

      return bool(exists)

   def read_csv(self, file: str, table: str, libref: str ="", nosub: bool =False, opts: dict = None) -> '<SASdata object>':
      """
      This method will import a csv file into a SAS Data Set and return the SASdata object referring to it.
      file    - eithe the OS filesystem path of the file, or HTTP://... for a url accessible file
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      opts    - a dictionary containing any of the following Proc Import options(datarow, delimiter, getnames, guessingrows)
      """
      opts = opts if opts is not None else {}

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

   def write_csv(self, file: str, table: str, libref: str ="", nosub: bool =False, dsopts: dict = None, opts: dict = None) -> 'The LOG showing the results of the step':
      """
      This method will export a SAS Data Set to a file in CSV format.
      file    - the OS filesystem path of the file to be created (exported from the SAS Data Set)
      table   - the name of the SAS Data Set you want to export to a CSV file
      libref  - the libref for the SAS Data Set.
      dsopts  - a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs)
      opts    - a dictionary containing any of the following Proc Export options(delimiter, putnames)
      """
      dsopts = dsopts if dsopts is not None else {}
      opts = opts if opts is not None else {}

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

   def dataframe2sasdata(self, df: '<Pandas Data Frame object>', table: str ='a', libref: str ="", keep_outer_quotes: bool=False):
      """
      This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      """
      input  = ""
      card   = ""
      format = ""
      length = ""
      dts    = []
      ncols  = len(df.columns)

      for name in range(ncols):
         input += "'"+str(df.columns[name])+"'n "
         if df.dtypes[df.columns[name]].kind in ('O','S','U','V'):
            col_l = df[df.columns[name]].astype(str).map(len, 'ignore').max()
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
            if dts[col] == 'N' and var == 'nan':
               var = '.'
            if dts[col] == 'C' and var == 'nan':
               var = ' '
            if dts[col] == 'B':
               var = str(int(row[col]))
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

      self._asubmit(code+";;;;\nrun;", "text")
      ll = self.submit("", 'text')
      return

   def sasdata2dataframe(self, table: str, libref: str ='', dsopts: dict = None, rowsep: str = '\x01', colsep: str = '\x02', **kwargs) -> '<Pandas Data Frame object>':
      """
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table   - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref  - the libref for the SAS Data Set.
      rowsep  - the row seperator character to use; defaults to '\n'
      colsep  - the column seperator character to use; defaults to '\t'
      """
      dsopts = dsopts if dsopts is not None else {}

      method = kwargs.pop('method', None)
      if method and method.lower() == 'csv':
         return self.sasdata2dataframeCSV(table, libref, dsopts, **kwargs)

      logf     = ''
      logn     = self._logcnt()
      logcodei = "%put E3969440A681A24088859985" + logn + ";"
      logcodeo = "\nE3969440A681A24088859985" + logn

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

      code = "data _null_; set "+tabname+self._sb._dsopts(dsopts)+";\n file "+self._tomods1.decode()+" dlm="+cdelim+" termstr=NL; put "

      for i in range(nvars):
         code += "'"+varlist[i]+"'n "
         if vartype[i] == 'N':
            if varcat[i] in self._sb.sas_date_fmts:
               code += 'E8601DA10. '+cdelim
            else:
               if varcat[i] in self._sb.sas_time_fmts:
                  code += 'E8601TM15.6 '+cdelim
               else:
                  if varcat[i] in self._sb.sas_datetime_fmts:
                     code += 'E8601DT26.6 '+cdelim
                  else:
                     code += 'best32. '+cdelim
         if not (i < (len(varlist)-1)):
            code += rdelim
      code += ";\n run;"

      ll = self._asubmit(code, 'text')

      self.stdin[0].send(b'\n'+logcodei.encode()+b'\n'+b'tom says EOL='+logcodeo.encode()+b'\n')


      BOM   = "\ufeff".encode()
      done  = False
      first = True
      datar = b''
      bail  = False
      r     = []
      df    = None
      trows = kwargs.get('trows', None)
      if not trows:
         trows = 100000

      while not done:
         while True:
             if os.name == 'nt':
                try:
                   rc = self.pid.wait(0)
                   self.pid = None
                   self._sb.SASpid = None
                   print('\nSAS process has terminated unexpectedly. RC from wait was: '+str(rc))
                   return None
                except:
                   pass
             else:
                rc = os.waitpid(self.pid, os.WNOHANG)
                if rc[1]:
                    self.pid = None
                    self._sb.SASpid = None
                    print('\nSAS process has terminated unexpectedly. RC from wait was: '+str(rc))
                    return None

             if bail:
                if datar.count(logcodeo.encode()) >= 1:
                   break
             try:
                data = self.stdout[0].recv(4096)
             except (BlockingIOError):
                data = b''

             if len(data) > 0:
                if first:
                   if data[0:3] == BOM:
                      data = data[3:len(data)]
                   first = False

                datar += data
                data   = datar.rpartition(colsep.encode()+rowsep.encode()+b'\n')
                datap  = data[0]+data[1]
                datar  = data[2]

                datap = datap.decode(self.sascfg.encoding, errors='replace')
                for i in datap.split(sep=colsep+rowsep+'\n'):
                   if i != '':
                      r.append(tuple(i.split(sep=colsep)))

                if len(r) > trows:
                   tdf = pd.DataFrame.from_records(r, columns=varlist)

                   for i in range(nvars):
                      if vartype[i] == 'N':
                         if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                            if tdf.dtypes[tdf.columns[i]].kind not in ('f','u','i','b','B','c','?'):
                               tdf[varlist[i]] = pd.to_numeric(tdf[varlist[i]], errors='coerce')
                         else:
                            if tdf.dtypes[tdf.columns[i]].kind not in ('M'):
                               tdf[varlist[i]] = pd.to_datetime(tdf[varlist[i]], errors='coerce')
                      else:
                         tdf[varlist[i]].replace(' ', np.NaN, True)

                   if df is not None:
                      df = df.append(tdf, ignore_index=True)
                   else:
                      df = tdf
                   r = []
             else:
                sleep(0.1)
                try:
                   log = self.stderr[0].recv(4096).decode(self.sascfg.encoding, errors='replace')
                except (BlockingIOError):
                   log = b''

                if len(log) > 0:
                   logf += log
                   if logf.count(logcodeo) >= 1:
                      bail = True
         done = True

      if len(r) > 0:
         tdf = pd.DataFrame.from_records(r, columns=varlist)

         for i in range(nvars):
            if vartype[i] == 'N':
               if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  if tdf.dtypes[tdf.columns[i]].kind not in ('f','u','i','b','B','c','?'):
                     tdf[varlist[i]] = pd.to_numeric(tdf[varlist[i]], errors='coerce')
               else:
                  if tdf.dtypes[tdf.columns[i]].kind not in ('M'):
                     tdf[varlist[i]] = pd.to_datetime(tdf[varlist[i]], errors='coerce')
            else:
               tdf[varlist[i]].replace(' ', np.NaN, True)

         if df is not None:
            df = df.append(tdf, ignore_index=True)
         else:
            df = tdf

      return df

   def sasdata2dataframeCSV(self, table: str, libref: str ='', dsopts: dict = None, tempfile: str=None, tempkeep: bool=False, **kwargs) -> '<Pandas Data Frame object>':
      """
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table    - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref   - the libref for the SAS Data Set.
      dsopts   - data set options for the input SAS Data Set
      tempfile - file to use to store CSV, else temporary file will be used.
      tempkeep - if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it
      """
      dsopts = dsopts if dsopts is not None else {}

      logf     = ''
      lstf     = ''
      logn     = self._logcnt()
      logcodei = "%put E3969440A681A24088859985" + logn + ";"
      lstcodeo =   "E3969440A681A24088859985" + logn
      logcodeo = "\nE3969440A681A24088859985" + logn

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

      code = "data sasdata2dataframe / view=sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";\nformat "

      for i in range(nvars):
         if vartype[i] == 'N':
            code += "'"+varlist[i]+"'n "
            if varcat[i] in self._sb.sas_date_fmts:
               code += 'E8601DA10. '
            else:
               if varcat[i] in self._sb.sas_time_fmts:
                  code += 'E8601TM15.6 '
               else:
                  if varcat[i] in self._sb.sas_datetime_fmts:
                     code += 'E8601DT26.6 '
                  else:
                     code += 'best32. '
      code += ";\n run;\n"
      ll = self.submit(code, "text")

      if self.sascfg.iomhost.lower() in ('', 'localhost', '127.0.0.1'):
         local   = True
         outname = "_tomodsx"
         code    = "filename _tomodsx '"+tmpcsv+"' lrecl="+str(self.sascfg.lrecl)+" recfm=v  encoding='utf-8';\n"
      else:
         local   = False
         outname = self._tomods1.decode()
         code    = ''

      #code += "options nosource;\n"
      code += "proc export data=sasdata2dataframe outfile="+outname+" dbms=csv replace; run\n;"
      #code += "options source;\n"

      ll = self._asubmit(code, 'text')

      self.stdin[0].send(b'\n'+logcodei.encode()+b'\n'+b'tom says EOL='+logcodeo.encode())

      done  = False
      bail  = False
      datar = b""

      dts = kwargs.pop('dtype', '')
      if dts == '':
         dts = {}
         for i in range(nvars):
            if vartype[i] == 'N':
               if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  dts[varlist[i]] = 'float'
               else:
                  dts[varlist[i]] = 'str'
            else:
               dts[varlist[i]] = 'str'

      if not local:
         csv = open(tmpcsv, mode='wb')
         while not done:
                while True:
                    if os.name == 'nt':
                       try:
                          rc = self.pid.wait(0)
                          self.pid = None
                          self._sb.SASpid = None
                          print('\nSAS process has terminated unexpectedly. RC from wait was: '+str(rc))
                          return None
                       except:
                          pass
                    else:
                       rc = os.waitpid(self.pid, os.WNOHANG)
                       if rc[1]:
                           self.pid = None
                           self._sb.SASpid = None
                           print('\nSAS process has terminated unexpectedly. RC from wait was: '+str(rc))
                           return None

                    try:
                       data = self.stdout[0].recv(4096)
                    except (BlockingIOError):
                       data = b''

                    if len(data) > 0:
                       datar += data
                       data   = datar.rpartition(b'\n')
                       datap  = data[0]+data[1]
                       datar  = data[2]

                       if datap.count(lstcodeo.encode()) >= 1:
                          done  = True
                          datar = datap.rpartition(logcodeo.encode())
                          datap = datar[0]

                       csv.write(datap.decode(self.sascfg.encoding, errors='replace').encode())
                       if bail and done:
                          break
                    else:
                       if datar.count(lstcodeo.encode()) >= 1:
                          done = True
                       if bail and done:
                          break
                       sleep(0.1)
                       try:
                          log = self.stderr[0].recv(4096).decode(errors='replace')
                       except (BlockingIOError):
                          log = b''

                       if len(log) > 0:
                          logf += log
                          if logf.count(logcodeo) >= 1:
                             bail = True
                done = True
                self._log += logf

         #csv.seek(0)
         csv.close()
         df = pd.read_csv(tmpcsv, index_col=False, engine='c', dtype=dts, **kwargs)
         #csv.close()
      else:
         while True:
            try:
               lst = self.stdout[0].recv(4096).decode(errors='replace')
            except (BlockingIOError):
               lst = b''

            if len(lst) > 0:
               lstf += lst
               if lstf.count(lstcodeo) >= 1:
                  done = True;

            try:
               log = self.stderr[0].recv(4096).decode(errors='replace')
            except (BlockingIOError):
               sleep(0.1)
               log = b''

            if len(log) > 0:
               logf += log
               if logf.count(logcodeo) >= 1:
                  bail = True;
                  self._log += logf

            if done and bail:
               break

         df = pd.read_csv(tmpcsv, index_col=False, engine='c', dtype=dts, **kwargs)

      if tmpdir:
         tmpdir.cleanup()
      else:
         if not tempkeep:
            os.remove(tmpcsv)

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
