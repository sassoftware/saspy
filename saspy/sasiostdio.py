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
import tempfile as tf
from time import sleep
import socket as socks

try:
   import pandas as pd
   import numpy  as np
except ImportError:
   pass
try:
   from IPython.display import HTML
except ImportError:
   pass

class SASconfigSTDIO:
   """
   This object is not intended to be used directly. Instantiate a SASsession object instead
   """
   def __init__(self, session, **kwargs):
      self._kernel  = kwargs.get('kernel', None)

      SAScfg        = session._sb.sascfg.SAScfg
      self.name     = session._sb.sascfg.name
      cfg           = getattr(SAScfg, self.name)

      self.saspath  = cfg.get('saspath', '')
      self.options  = cfg.get('options', [])
      self.ssh      = cfg.get('ssh', '')
      self.identity = cfg.get('identity', None)
      self.tunnel   = cfg.get('tunnel', None)
      self.port     = cfg.get('port', None)
      self.host     = cfg.get('host', '')
      self.encoding = cfg.get('encoding', '')
      self.metapw   = cfg.get('metapw', '')
      self.lrecl    = cfg.get('lrecl', None)
      self.iomc     = cfg.get('iomc', '')

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

      inident = kwargs.get('identity', None)
      if inident is not None:
         if lock:
            print("Parameter 'identity' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.identity = inident

      intunnel = kwargs.get('tunnel', None)
      if intunnel is not None:
         if lock:
            print("Parameter 'tunnel' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.tunnel = intunnel

      inport = kwargs.get('port', None)
      if inport is not None:
         if lock:
            print("Parameter 'port' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.port = inport

      inhost = kwargs.get('host', '')
      if len(inhost) > 0:
         if lock and len(self.host):
            print("Parameter 'host' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.host = inhost

      inencoding = kwargs.get('encoding', '')
      if len(inencoding) > 0:
         if lock and len(self.encoding):
            print("Parameter 'encoding' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.encoding = inencoding
      if not self.encoding:
         self.encoding = 'utf-8'

      inlrecl = kwargs.get('lrecl', None)
      if inlrecl:
         if lock and self.lrecl:
            print("Parameter 'lrecl' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.lrecl = inlrecl
      if not self.lrecl:
         self.lrecl = 1048576

      self._prompt = session._sb.sascfg._prompt

      self.hostip = socks.gethostname()
      try:
         x  = subprocess.Popen(('nslookup', self.hostip), stdout=subprocess.PIPE)
         z  = x.stdout.read()
         ip = z.rpartition(b'Address:')[2].strip().decode()
         try:
            socks.gethostbyaddr(ip)
            self.hostip = ip
         except:
            pass
         x.terminate()
      except:
         pass

      return

class SASsessionSTDIO():
   """
   The SASsession object is the main object to instantiate and provides access to the rest of the functionality.
   cfgname  - value in SAS_config_names List of the sascfg_personal.py file
   kernel   - None - internal use when running the SAS_kernel notebook
   saspath  - overrides saspath Dict entry of cfgname in sascfg_personal.py file
   options  - overrides options Dict entry of cfgname in sascfg_personal.py file
   encoding - This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
   autoexec - This is a string of SAS code that will be submitted upon establishing a connection.
   ssh      - full path of the ssh command; /usr/bin/ssh for instance
   host     - host name of the remote machine
   identity - path to an .ppk identity file to be used with the ssh -i option
   port     - (Optional: integer) The ssh port of the remote machine (equivalent to invoking ssh with the -p option)
   tunnel   - (Optional: integer) Certain methods of saspy require opening a local port and accepting data streamed from the SAS instance.
   """
   #def __init__(self, cfgname: str ='', kernel: '<SAS_kernel object>' =None, saspath :str ='', options: list =[]) -> '<SASsession object>':
   def __init__(self, **kwargs):
      self.pid    = None
      self.stdin  = None
      self.stderr = None
      self.stdout = None

      self._sb      = kwargs.get('sb', None)
      self.sascfg   = SASconfigSTDIO(self, **kwargs)
      self._log_cnt = 0
      self._log     = ""

      self._startsas()

   def __del__(self):
      if self.pid:
         self._endsas()
      self._sb.SASpid = None

   def _logcnt(self, next=True):
       if next == True:
          self._log_cnt += 1
       return '%08d' % self._log_cnt

   def _buildcommand(self, sascfg):
      if sascfg.ssh:
         pgm    = sascfg.ssh
         parms  = [pgm]
         parms += ["-t"]

         if sascfg.identity:
            parms += ["-i", sascfg.identity]

         if sascfg.port:
            parms += ["-p", str(sascfg.port)]

         if sascfg.tunnel:
            parms += ["-R", '%d:localhost:%d' % (sascfg.tunnel,sascfg.tunnel)]

         parms += [sascfg.host, sascfg.saspath]

         if sascfg.output.lower() == 'html':
            print("""HTML4 is only valid in 'local' mode (SAS_output_options in sascfg_personal.py).
Please see SAS_config_names templates 'default' (STDIO) or 'winlocal' (IOM) in the sample sascfg.py.
Will use HTML5 for this SASsession.""")
            sascfg.output = 'html5'
      else:
         pgm    = sascfg.saspath
         parms  = [pgm]

      # temporary hack for testing grid w/ sasgsub and iomc ...
      if sascfg.iomc:
         pgm    = sascfg.iomc
         parms  = [pgm]
         parms += ["user", "sas", "pw", "sas"]
         parms += ['']
      elif sascfg.metapw:
         pgm    = sascfg.ssh
         parms  = [pgm]
         parms += ["-t", "-i", "/u/sastpw/idrsacnn", sascfg.host]
         parms += sascfg.options
         #parms += ['"'+sascfg.saspath+' -nodms -stdio -terminal -nosyntaxcheck -pagesize MAX"']
         parms += ['']
      else:
         parms += sascfg.options
         parms += ["-nodms"]
         parms += ["-stdio"]
         parms += ["-terminal"]
         parms += ["-nosyntaxcheck"]
         parms += ["-pagesize", "MAX"]
         parms += ['']

      return [pgm, parms]

   def _startsas(self):
      #import pdb;pdb.set_trace()
      if self.pid:
         return self.pid

      pgm, parms = self._buildcommand(self.sascfg)

      s = ''
      for i in range(len(parms)):
            s += parms[i]+' '

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
            #sleep(5)
            os.execv(pgm, parms)
         except OSError as e:
            print("The OS Error was:\n"+e.strerror+'\n')
            print("SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n")
            print("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
            print("If no OS Error above, try running the following command (where saspy is running) manually to see what is wrong:\n"+s+"\n")
            os._exit(-6)
         except:
            print("Subprocess failed to start. Double check your settings in sascfg_personal.py file.\n")
            os._exit(-6)

      self.pid    = pidpty[0]
      self.stdin  = os.fdopen(pin[PIPE_WRITE], mode='wb')
      self.stderr = os.fdopen(perr[PIPE_READ], mode='rb')
      self.stdout = os.fdopen(pout[PIPE_READ], mode='rb')

      fcntl.fcntl(self.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
      fcntl.fcntl(self.stderr, fcntl.F_SETFL, os.O_NONBLOCK)

      rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
      if rc != None:
         self.pid = None
         self._sb.SASpid = None
         lst = self.stdout.read1(4096)
         print("stdout from subprocess is:\n"+lst.decode())

      if self.pid is None:
         print("SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n")
         print("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
         print("Try running the following command (where saspy is running) manually to see if you can get more information on what went wrong:\n"+s+"\n")
         return None
      else:
         self.submit("options svgtitle='svgtitle'; options validvarname=any; ods graphics on;", "text")
         if self.pid is None:
            print("SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n")
            print("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
            print("Try running the following command (where saspy is running) manually to see if you can get more information on what went wrong:\n"+s+"\n")
            return None

      if self.sascfg.verbose:
         print("SAS Connection established. Subprocess id is "+str(self.pid)+"\n")
      return self.pid

   def _endsas(self):
      rc  = 0
      ret = None
      if self.pid:
         code = ";*\';*\";*/;\n;quit;endsas;"
         self._getlog(wait=1)
         self._asubmit(code,'text')
         sleep(1)
         try:
            rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
         except (subprocess.TimeoutExpired):
            if self.sascfg.verbose:
               print("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
               ret = rc
            os.kill(self.pid, signal.SIGKILL)
         if self.sascfg.verbose:
            print("SAS Connection terminated. Subprocess id was "+str(self.pid))
         self.pid = None
         self._sb.SASpid = None
      return ret

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

      x = logf.decode(self.sascfg.encoding, errors='replace').replace(code1, " ")
      self._log += x

      if self.pid == None:
         self._sb.SASpid = None
         return "No SAS process attached. SAS process has terminated unexpectedly."
      rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
      if rc != None:
         self.pid = None
         self._sb.SASpid = None
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
         self._sb.SASpid = None
         return "No SAS process attached. SAS process has terminated unexpectedly."
      rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
      if rc != None:
         self.pid = None
         self._sb.SASpid = None
         return 'SAS process has terminated unexpectedly. Pid State= '+str(rc)

      if eof:
         return lstf.decode(errors='replace')
      else:
         return lstf.decode(self.sascfg.encoding, errors='replace')

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
               f2 = final[0].decode(self.sascfg.encoding, errors='replace').rpartition(chr(12))
               break

      lst = f2[0]

      if self.pid == None:
         self._sb.SASpid = None
         return "No SAS process attached. SAS process has terminated unexpectedly."
      rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
      if rc != None:
         self.pid = None
         self._sb.SASpid = None
         return 'SAS process has terminated unexpectedly. Pid State= '+str(rc)

      return lst.replace(chr(12), '\n')

   def _asubmit(self, code, results="html"):
      # as this is an _ method, it's not really to be used. Of note is that if this is used and if what it submitted generates
      # anything to the lst, then unless _getlst[txt] is called, then next submit will happen to get the lst this wrote, plus
      # what it generates. If the two are not of the same type (html, text) it could be problematic, beyond not being what was
      # expected in the first place. __flushlst__() used to be used, but was never needed. Adding this note and removing the
      # unnecessary read in submit as this can't happen in the current code.

      odsopen  = b"ods listing close;ods "+self.sascfg.output.encode()+ \
                 b" (id=saspy_internal) file=stdout options(bitmap_mode='inline') device=svg style="+self._sb.HTML_Style.encode()+ \
                 b"; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods "+self.sascfg.output.encode()+b" (id=saspy_internal) close;ods listing;\n"
      ods      = True;

      if results.upper() != "HTML":
         ods = False

      if (ods):
         self.stdin.write(odsopen)

      out = self.stdin.write(code.encode(self.sascfg.encoding)+b'\n')

      if (ods):
         self.stdin.write(odsclose)

      self.stdin.flush()

      return str(out)

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

      odsopen  = b"ods listing close;ods "+self.sascfg.output.encode()+ \
                 b" (id=saspy_internal) file=stdout options(bitmap_mode='inline') device=svg style="+self._sb.HTML_Style.encode()+ \
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

      if self.pid == None:
         self._sb.SASpid = None
         print("No SAS process attached. SAS process has terminated unexpectedly.")
         return dict(LOG="No SAS process attached. SAS process has terminated unexpectedly.", LST='')

      rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
      if rc != None:
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
         self.stdin.write(odsopen)

      pgm  = mj+b'\n'+pcodei.encode(self.sascfg.encoding)+pcodeiv.encode(self.sascfg.encoding)
      pgm += code.encode(self.sascfg.encoding)+b'\n'+pcodeo.encode(self.sascfg.encoding)+b'\n'+mj
      out  = self.stdin.write(pgm)

      if ods:
         self.stdin.write(odsclose)

      out = self.stdin.write(b'\n'+logcodei.encode(self.sascfg.encoding)+b'\n')
      self.stdin.flush()

      while not done:
         try:
             while True:
                 rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
                 if rc is not None:
                     log = b''
                     try:
                        log = self.stderr.read1(4096)
                        if len(log) > 0:
                            logf += log
                        self._log += logf.decode(self.sascfg.encoding, errors='replace')
                     except:
                        pass
                     self.pid = None
                     self._sb.SASpid = None
                     return dict(LOG='SAS process has terminated unexpectedly. Pid State= ' +
                                 str(rc)+'\n'+logf.decode(self.sascfg.encoding, errors='replace'), LST='')
                 if bail:
                     eof -= 1
                 if eof < 0:
                     break
                 if ods:
                    lst = self.stdout.read1(4096)
                 else:
                    lst = self.stdout.read1(4096)
                 if len(lst) > 0:
                     lstf += lst
                 else:
                     log = self.stderr.read1(4096)
                     if len(log) > 0:
                         logf += log
                         if logf.count(logcodeo) >= 1:
                             bail = True
                         if not bail and bc:
                             self.stdin.write(odsclose+logcodei.encode(self.sascfg.encoding) + b'\n')
                             self.stdin.flush()
                             bc = False
             done = True

         except (ConnectionResetError):
             log = ''
             try:
                log = self.stderr.read1(4096)
                if len(log) > 0:
                   logf += log
                self._log += logf.decode(self.sascfg.encoding, errors='replace')
             except:
                pass
             rc = 0
             rc = os.waitpid(self.pid, 0)
             self.pid = None
             self._sb.SASpid = None
             log = logf.partition(logcodeo)[0]+b'\nConnection Reset: SAS process has terminated unexpectedly. Pid State= '+str(rc).encode()+b'\n'+logf
             return dict(LOG=log.encode(), LST='')

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

             self.stdin.write(odsclose+logcodei.encode(self.sascfg.encoding)+b'\n')
             self.stdin.flush()

      if ods:
         try:
            lstf = lstf.decode()
         except UnicodeDecodeError:
            try:
               lstf = lstf.decode(self.sascfg.encoding)
            except UnicodeDecodeError:
               lstf = lstf.decode(errors='replace')
      else:
         lstf = lstf.decode(self.sascfg.encoding, errors='replace')

      logf = logf.decode(self.sascfg.encoding, errors='replace')

      trip = lstf.rpartition("/*]]>*/")
      if len(trip[1]) > 0 and len(trip[2]) < 100:
         lstf = ''

      self._log += logf
      final = logf.partition(logcodei)
      z = final[0].rpartition(chr(10))
      prev = '%08d' %  (self._log_cnt - 1)
      zz = z[0].rpartition("\nE3969440A681A24088859985" + prev +'\n')
      logd = zz[2].replace(mj.decode(self.sascfg.encoding), '')

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

        if self.sascfg.ssh:
           response = self.sascfg._prompt(
                     "SAS attention handling not supported over ssh. Please enter (T) to terminate SAS or (C) to continue.")
           while True:
              if response is None or response.upper() == 'C':
                 return dict(LOG=b'', LST=b'', BC=True)
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
                self._sb.SASpid = None
                outrc = str(rc)
                return dict(LOG=b'SAS process has terminated unexpectedly. Pid State= '+outrc.encode(), LST=b'',ABORT=True)

            lst = self.stdout.read1(4096)
            lstf += lst
            if len(lst) > 0:
                lsts = lst.rpartition(b'Select:')
                if lsts[0] != b'' and lsts[1] != b'':
                    found = True
                    query = lsts[1] + lsts[2].rsplit(b'\n?')[0] + b'\n'
                    print('Processing interrupt\nAttn handler Query is\n\n' + query.decode(self.sascfg.encoding, errors='replace'))
                    response = None
                    while response is None:
                       response = self.sascfg._prompt("Please enter your Response: ")
                    self.stdin.write(response.encode(self.sascfg.encoding) + b'\n')
                    self.stdin.flush()
                    if (response == 'C' or response == 'c') and query.count("C. Cancel") >= 1:
                       bc = True
                       break
                else:
                    lsts = lst.rpartition(b'Press')
                    if lsts[0] != b'' and lsts[1] != b'':
                        query = lsts[1] + lsts[2].rsplit(b'\n?')[0] + b'\n'
                        print('Secondary Query is:\n\n' + query.decode(self.sascfg.encoding, errors='replace'))
                        response = None
                        while response is None:
                           response = self.sascfg._prompt("Please enter your Response: ")
                        self.stdin.write(response.encode(self.sascfg.encoding) + b'\n')
                        self.stdin.flush()
                        if (response == 'N' or response == 'n') and query.count("N to continue") >= 1:
                           bc = True
                           break
                    else:
                        #print("******************No 'Select' or 'Press' found in lst="+lstf.decode(self.sascfg.encoding, errors='replace'))
                        pass
            else:
                log = self.stderr.read1(4096)
                logf += log
                self._log += log.decode(self.sascfg.encoding, errors='replace')

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
            lst = self.stdout.read1(4096).decode(self.sascfg.encoding, errors='replace')
         else:
            log = self.stderr.read1(4096).decode(self.sascfg.encoding, errors='replace')
            self._log += log
            logn = self._logcnt(False)

            if log.count("\nE3969440A681A24088859985"+logn) >= 1:
               print("******************Found end of step. No interupt processed")
               found = True

            if found:
               ll = self.submit("ods "+self.sascfg.output+" (id=saspy_internal) close;ods listing close;ods listing;libname work list;\n",'text')
               break

            sleep(.25)
            lst = self.stdout.read1(4096).decode(self.sascfg.encoding, errors='replace')

      return log

   def saslog(self):
      """
      this method is used to get the current, full contents of the SASLOG
      """
      return self._log

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
      code += "te='TABLE_EXISTS='; put te e;run;"

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
      code += "proc export data="+libref+"."+table+self._sb._dsopts(dsopts)+" outfile=x"
      code += " dbms=csv replace; "+self._sb._expopts(opts)+" run;"
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
         code += "length"+length+";\n"
      if len(format):
         code += "format "+format+";\n"
      code += "infile datalines delimiter='03'x DSD STOPOVER;\n input "+input+";\n datalines4;"
      self._asubmit(code, "text")

      for row in df.itertuples(index=False):
      #for row in df.iterrows():
         card  = ""
         for col in range(ncols):
            var = str(row[col])
            #var = str(row[1][col])
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
                  #var = str(row[1][col].to_datetime64())
            card += var
            if col < (ncols-1):
               card += chr(3)
         self.stdin.write(card.encode(self.sascfg.encoding)+b'\n')
         #self._asubmit(card, "text")

      self._asubmit(";;;;run;", "text")

   def sasdata2dataframe(self, table: str, libref: str ='', dsopts: dict = None, rowsep: str = '\x01', colsep: str = '\x02', **kwargs) -> '<Pandas Data Frame object>':
      """
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table   - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref  - the libref for the SAS Data Set.
      rowsep  - the row seperator character to use; defaults to '\n'
      colsep  - the column seperator character to use; defaults to '\t'
      port    - port to use for socket. Defaults to 0 which uses a random available ephemeral port
      """
      dsopts = dsopts if dsopts is not None else {}

      method = kwargs.pop('method', None)
      if method and method.lower() == 'csv':
         return self.sasdata2dataframeCSV(table, libref, dsopts, **kwargs)

      port =  kwargs.get('port', 0)

      if port==0 and self.sascfg.tunnel:
         # we are using a tunnel; default to that port
         port = self.sascfg.tunnel

      datar = ""

      if libref:
         tabname = libref+"."+table
      else:
         tabname = table

      code  = "proc sql; create view sasdata2dataframe as select * from "+tabname+self._sb._dsopts(dsopts)+";quit;\n"
      code += "data _null_; file STDERR;d = open('sasdata2dataframe');\n"
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

      topts             = dict(dsopts)
      topts['obs']      = 1
      topts['firstobs'] = ''

      code  = "data _null_; set "+tabname+self._sb._dsopts(topts)+";put 'FMT_CATS=';\n"
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
         if self.sascfg.tunnel:
            sock.bind(('localhost', port))
         else:
            sock.bind(('', port))
         port = sock.getsockname()[1]
      except OSError:
         print('Error try to open a socket in the sasdata2dataframe method. Call failed.')
         return None

      if self.sascfg.ssh:
         if not self.sascfg.tunnel:
            host = self.sascfg.hostip #socks.gethostname()
         else:
            host = 'localhost'
      else:
         host = ''

      rdelim = "'"+'%02x' % ord(rowsep.encode(self.sascfg.encoding))+"'x"
      cdelim = "'"+'%02x' % ord(colsep.encode(self.sascfg.encoding))+"'x "

      code  = ""
      code += "filename sock socket '"+host+":"+str(port)+"' lrecl="+str(self.sascfg.lrecl)+" recfm=v termstr=LF;\n"
      code += " data _null_; set "+tabname+self._sb._dsopts(dsopts)+";\n file sock dlm="+cdelim+"; put "
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
      code += "; run;\n"

      sock.listen(1)
      self._asubmit(code, 'text')

      r     = []
      df    = None
      datar = b''
      trows = kwargs.get('trows', None)
      if not trows:
         trows = 100000

      newsock = (0,0)
      try:
         newsock = sock.accept()
         while True:
            data = newsock[0].recv(4096)

            if len(data):
               datar += data
            else:
               break

            data  = datar.rpartition(colsep.encode()+rowsep.encode()+b'\n')
            datap = data[0]+data[1]
            datar = data[2]

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
      except:
         print("sasdata2dataframe was interupted. Trying to return the saslog instead of a data frame.")
         if newsock[0]:
            newsock[0].shutdown(socks.SHUT_RDWR)
            newsock[0].close()
         sock.close()
         ll = self.submit("", 'text')
         return ll['LOG']

      newsock[0].shutdown(socks.SHUT_RDWR)
      newsock[0].close()
      sock.close()

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
      port     - port to use for socket. Defaults to 0 which uses a random available ephemeral port
      tempfile - file to use to store CSV, else temporary file will be used.
      tempkeep - if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it
      """
      dsopts = dsopts if dsopts is not None else {}

      port =  kwargs.get('port', 0)

      if port==0 and self.sascfg.tunnel:
         # we are using a tunnel; default to that port
         port = self.sascfg.tunnel

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
      code += "data _null_; file STDERR;d = open('sasdata2dataframe');\n"
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

      topts             = dict(dsopts)
      topts['obs']      = 1
      topts['firstobs'] = ''

      code  = "data _null_; set "+tabname+self._sb._dsopts(topts)+";put 'FMT_CATS=';\n"
      for i in range(nvars):
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "run;\n"

      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("FMT_CATS=")
      l2 = l2[2].partition("\n")
      varcat = l2[2].split("\n", nvars)
      del varcat[nvars]

      if self.sascfg.ssh:
         try:
            sock = socks.socket()
            if self.sascfg.tunnel:
               sock.bind(('localhost', port))
            else:
               sock.bind(('', port))
            port = sock.getsockname()[1]
         except OSError:
            print('Error try to open a socket in the sasdata2dataframe method. Call failed.')
            return None

         if not self.sascfg.tunnel:
            host = self.sascfg.hostip  #socks.gethostname()
         else:
            host = 'localhost'
         code  = "filename sock socket '"+host+":"+str(port)+"' lrecl="+str(self.sascfg.lrecl)+" recfm=v encoding='utf-8';\n"
      else:
         host = ''
         code = "filename sock '"+tmpcsv+"' lrecl="+str(self.sascfg.lrecl)+" recfm=v encoding='utf-8';\n"

      code += "data sasdata2dataframe / view=sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";\nformat "

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

      code  = ''
      #code += "options nosource;\n"
      code  = "proc export data=sasdata2dataframe outfile=sock dbms=csv replace; run\n;"
      #code += "options source;\n"

      if self.sascfg.ssh:
         csv = open(tmpcsv, mode='wb')
         sock.listen(1)
         self._asubmit(code, 'text')

         newsock = (0,0)
         try:
            newsock = sock.accept()
            while True:
               data = newsock[0].recv(4096)

               if not len(data):
                  break

               csv.write(data)
         except:
            print("sasdata2dataframe was interupted. Trying to return the saslog instead of a data frame.")
            if newsock[0]:
               newsock[0].shutdown(socks.SHUT_RDWR)
               newsock[0].close()
            sock.close()
            ll = self.submit("", 'text')
            return ll['LOG']

         newsock[0].shutdown(socks.SHUT_RDWR)
         newsock[0].close()
         sock.close()
         ll = self.submit("", 'text')

         #csv.seek(0)
         csv.close()
         df = pd.read_csv(tmpcsv, index_col=False, engine='c', dtype=dts, **kwargs)
         #csv.close()
      else:
         ll = self.submit(code, "text")
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
