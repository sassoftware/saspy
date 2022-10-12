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
if os.name != 'nt':
   import fcntl
import signal
import subprocess
import tempfile as tf
from   time import sleep
import socket as socks
import codecs
import select as sel
import warnings
import io
import re

import logging
logger = logging.getLogger('saspy')

try:
   import pandas as pd
   import numpy  as np
except ImportError:
   pass

if os.name == 'nt':
   from queue     import Queue, Empty
   from threading import Thread

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
      self.sshpass  = cfg.get('sshpass', '')
      self.sshpassparms = cfg.get('sshpassparms', '')
      self.identity = cfg.get('identity', None)
      self.luser    = cfg.get('luser', None)
      self.tunnel   = cfg.get('tunnel', None)
      self.rtunnel  = cfg.get('rtunnel', None)
      self.port     = cfg.get('port', None)
      self.host     = cfg.get('host', '')
      self.encoding = cfg.get('encoding', '')
      self.metapw   = cfg.get('metapw', '')
      self.lrecl    = cfg.get('lrecl', None)
      self.iomc     = cfg.get('iomc', '')
      self.dasho    = cfg.get('dasho', None)
      localhost     = cfg.get('localhost', None)

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

      insaspath = kwargs.get('saspath', '')
      if len(insaspath) > 0:
         if lock and len(self.saspath):
            logger.warning("Parameter 'saspath' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.saspath = insaspath

      inoptions = kwargs.get('options', '')
      if len(inoptions) > 0:
         if lock and len(self.options):
            logger.warning("Parameter 'options' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.options = inoptions

      inssh = kwargs.get('ssh', '')
      if len(inssh) > 0:
         if lock and len(self.ssh):
            logger.warning("Parameter 'ssh' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.ssh = inssh

      insshp = kwargs.get('sshpass', '')
      if len(insshp) > 0:
         if lock and len(self.sshpass):
            logger.warning("Parameter 'sshpass' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.sshpass = insshp

      insshpp = kwargs.get('sshpassparms', '')
      if len(insshpp) > 0:
         if lock and len(self.sshpassparms):
            logger.warning("Parameter 'sshpassparms' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.sshpassparms = insshpp

      inident = kwargs.get('identity', None)
      if inident is not None:
         if lock:
            logger.warning("Parameter 'identity' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.identity = inident

      inluser = kwargs.get('luser', None)
      if inluser is not None:
         if lock:
            logger.warning("Parameter 'luser' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.luser = inluser

      intunnel = kwargs.get('tunnel', None)
      if intunnel is not None:
         if lock:
            logger.warning("Parameter 'tunnel' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.tunnel = intunnel

      inrtunnel = kwargs.get('rtunnel', None)
      if inrtunnel is not None:
         if lock:
            logger.warning("Parameter 'rtunnel' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.rtunnel = inrtunnel

      ino = kwargs.get('dasho', None)
      if ino is not None:
         if lock and self.dasho is not None:
            logger.warning("Parameter 'dasho' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.dasho = ino

      inport = kwargs.get('port', None)
      if inport is not None:
         if lock:
            logger.warning("Parameter 'port' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.port = inport

      inloc = kwargs.get('localhost', None)
      if inloc is not None:
         if lock and localhost is not None:
            logger.warning("Parameter 'localhost' passed to SAS_session was ignored due to configuration restriction.")
         else:
            localhost = inloc

      inhost = kwargs.get('host', '')
      if len(inhost) > 0:
         if lock and len(self.host):
            logger.warning("Parameter 'host' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.host = inhost

      inencoding = kwargs.get('encoding', 'NoOverride')
      if inencoding !='NoOverride':
         if lock and len(self.encoding):
            logger.warning("Parameter 'encoding' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.encoding = inencoding
      if not self.encoding:
         self.encoding = ''    # 'utf-8'

      if self.encoding != '':
         try:
            coinfo = codecs.lookup(self.encoding)
         except LookupError:
            logger.warning("The encoding provided ("+self.encoding+") doesn't exist in this Python session. Setting it to ''.")
            logger.warning("The correct encoding will attempt to be determined based upon the SAS session encoding.")
            self.encoding = ''

      inlrecl = kwargs.get('lrecl', None)
      if inlrecl:
         if lock and self.lrecl:
            logger.warning("Parameter 'lrecl' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.lrecl = inlrecl
      if not self.lrecl:
         self.lrecl = 1048576

      self._prompt = session._sb.sascfg._prompt

      if localhost is not None:
         self.hostip = localhost
      else:
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
            x.stdout.close()
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
      self._log_cnt = 0
      self._log     = ""
      self.sascfg   = SASconfigSTDIO(self, **kwargs)

      self._startsas()
      return

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
         if sascfg.sshpass:
            pgm    = sascfg.sshpass
            parms  = [pgm]
            parms += sascfg.sshpassparms
            parms += [sascfg.ssh]
         else:
            pgm    = sascfg.ssh
            parms  = [pgm]

         parms += ["-t"]

         if sascfg.dasho:
            if type(sascfg.dasho) == list:
               for s in sascfg.dasho:
                  parms += ["-o", s]
            else:
               parms += ["-o", sascfg.dasho]

         if sascfg.identity:
            parms += ["-i", sascfg.identity]

         if sascfg.port:
            parms += ["-p", str(sascfg.port)]

         if sascfg.tunnel:
            parms += ["-R", '%d:localhost:%d' % (sascfg.tunnel,sascfg.tunnel)]

         if sascfg.rtunnel:
            parms += ["-L", '%d:localhost:%d' % (sascfg.rtunnel,sascfg.rtunnel)]

         if sascfg.luser:
            parms += [sascfg.luser+'@'+sascfg.host, sascfg.saspath]
         else:
            parms += [sascfg.host, sascfg.saspath]

         if sascfg.output.lower() == 'html':
            logger.warning("""HTML4 is only valid in 'local' mode (SAS_output_options in sascfg_personal.py).
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
      if self.pid:
         return self.pid

      pgm, parms = self._buildcommand(self.sascfg)

      s = ''
      for i in range(len(parms)):
            s += parms[i]+' '

      if os.name == 'nt':
         try:
            self.pid = subprocess.Popen(parms, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pid = self.pid.pid
         except OSError as e:
            msg  = "The OS Error was:\n"+e.strerror+'\n'
            msg += "SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n"
            msg += "Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n"
            msg += "If no OS Error above, try running the following command (where saspy is running) manually to see what is wrong:\n"+s+"\n"
            logger.error(msg)
            return None
      else:
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
               msg  = "The OS Error was:\n"+e.strerror+'\n'
               msg += "SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n"
               msg += "Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n"
               msg += "If no OS Error above, try running the following command (where saspy is running) manually to see what is wrong:\n"+s+"\n"
               logger.error(msg)
               os._exit(-6)
            except:
               logger.error("Subprocess failed to start. Double check your settings in sascfg_personal.py file.\n")
               os._exit(-6)

      if os.name == 'nt':
         try:
            self.pid.wait(1)

            error  = self.pid.stderr.read(4096).decode()+'\n'
            error += self.pid.stdout.read(4096).decode()
            logger.error("SAS Startup Error:\n"+error)

            msg  = "Subprocess failed to start. Double check your settings in sascfg_personal.py file.\n"
            msg += "Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n"
            msg += "If no SAS Startup Error above, try running the following command (where saspy is running) manually to see if it's a problem starting Java:\n"+s+"\n"
            logger.error(msg)
            self.pid = None
            return None
         except:
            # lame windows can't do non-blocking I/O
            self.stdout = Queue()
            self.stderr = Queue()
            self.to = Thread(target=self._read_out, args=())
            self.te = Thread(target=self._read_err, args=())
            self.to.daemon = True
            self.te.daemon = True
            self.to.start()
            self.te.start()
            self.stdin  = self.pid.stdin
      else:
         self.pid    = pidpty[0]
         self.stdin  = os.fdopen(pin[PIPE_WRITE], mode='wb')
         self.stderr = os.fdopen(perr[PIPE_READ], mode='rb')
         self.stdout = os.fdopen(pout[PIPE_READ], mode='rb')

         fcntl.fcntl(self.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
         fcntl.fcntl(self.stderr, fcntl.F_SETFL, os.O_NONBLOCK)

         rc = os.waitpid(self.pid, os.WNOHANG)
         if rc[0] != 0:
            self.pid = None
            self._sb.SASpid = None
            lst = self.stdout.read1(4096)
            logger.error("stdout from subprocess is:\n"+lst.decode())

      if self.pid is None:
         msg  = "SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n"
         msg += "Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n"
         msg += "Try running the following command (where saspy is running) manually to see if you can get more information on what went wrong:\n"+s+"\n"
         logger.error(msg)
         return None
      else:
         enc = self.sascfg.encoding #validating encoding is done next, so handle it not being set for this one call
         if enc == '':
            self.sascfg.encoding = 'utf-8'
         ll = self.submit("options svgtitle='svgtitle'; options validvarname=any validmemname=extend; ods graphics on;", "text")
         self.sascfg.encoding = enc
         if self.pid is None:
            msg  = "SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n"
            msg += "Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n"
            msg += "Try running the following command (where saspy is running) manually to see if you can get more information on what went wrong:\n"+s+"\n"
            logger.error(msg)
            return None

      if self.sascfg.verbose:
         pid = self.pid if os.name != 'nt' else self.pid.pid
         logger.info("SAS Connection established. Subprocess id is "+str(pid)+"\n")
      return self.pid

   if os.name == 'nt':
      def _read_out(self):
         while True:
            lst = self.pid.stdout.read(4096)
            if lst == b'':
               break
            self.stdout.put(lst)

      def _read_err(self):
         while True:
            log = self.pid.stderr.read(4096)
            if log == b'':
               break
            self.stderr.put(log)

   def _endsas(self):
      rc  = 0
      ret = None
      if self.pid:
         if os.name == 'nt':
            pid = self.pid.pid
         else:
            pid = self.pid

         code = b";*\';*\";*/;\n;quit;endsas;\n"
         self._getlog(wait=1)
         if self.pid:
            out = self.stdin.write(code)
            self.stdin.flush()
         sleep(1)

         if self.pid:
            if os.name == 'nt':
               self.pid.stdin.close()
               self.pid.stdout.close()
               self.pid.stderr.close()
               try:
                  rc = self.pid.wait(5)
               except (subprocess.TimeoutExpired):
                  if self.sascfg.verbose:
                     logger.warning("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
                  self.pid.kill()
               self.to.join(5)
               self.te.join(5)
            else:
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
                     logger.warning("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
                  os.kill(self.pid, signal.SIGKILL)

         if self.sascfg.verbose:
            logger.info("SAS Connection terminated. Subprocess id was "+str(pid))
         self.pid        = None
         self._sb.SASpid = None
      return ret

   def _checkLogForError(self, log):
      lines = re.split(r'[\n]\s*', log)
      for line in lines:
         if line[self._sb.logoffset:].startswith('ERROR:'):
            return (True)
      return (False)

   def _getlog(self, wait=5, jobid=None):
      logf   = b''
      quit   = wait * 2
      logn   = self._logcnt(False)
      code1  = "%put E3969440A681A24088859985"+logn+";\nE3969440A681A24088859985"+logn

      if os.name == 'nt':
         try:
            rc = self.pid.wait(0)
            self.pid = None
            return 'SAS process has terminated unexpectedly. RC from wait was: '+str(rc)
         except:
            pass
      else:
         rc = os.waitpid(self.pid, os.WNOHANG)
         if rc[0] != 0:
            self.pid = None
            self._sb.SASpid = None
            return 'SAS process has terminated unexpectedly. Pid State= '+str(rc)

      while True:
         if os.name == 'nt':
            try:
               log = self.stderr.get_nowait()
            except Empty:
               log = b''
         else:
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

      if self._checkLogForError(x):
         warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
         self._sb.check_error_log = True

      if self.pid == None:
         self._sb.SASpid = None
         return "No SAS process attached. SAS process has terminated unexpectedly."
      if os.name == 'nt':
         try:
            rc = self.pid.wait(0)
            self.pid = None
            return 'SAS process has terminated unexpectedly. RC from wait was: '+str(rc)
         except:
            pass
      else:
         rc = os.waitpid(self.pid, os.WNOHANG)
         if rc[0] != 0:
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
         if os.name == 'nt':
            try:
               lst = self.stdout.get_nowait()
            except Empty:
               lst = b''
         else:
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

      if os.name == 'nt':
         try:
            rc = self.pid.wait(0)
            self.pid = None
            return 'SAS process has terminated unexpectedly. RC from wait was: '+str(rc)
         except:
            pass
      else:
         rc = os.waitpid(self.pid, os.WNOHANG)
         if rc[0] != 0:
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
         if os.name == 'nt':
            try:
               lst = self.stdout.get_nowait()
            except Empty:
               lst = b''
         else:
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

      if os.name == 'nt':
         try:
            rc = self.pid.wait(0)
            self.pid = None
            return 'SAS process has terminated unexpectedly. RC from wait was: '+str(rc)
         except:
            pass
      else:
         rc = os.waitpid(self.pid, os.WNOHANG)
         if rc[0] != 0:
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

      pgm = b''

      if (ods):
         pgm += odsopen

      pgm += code.encode(self.sascfg.encoding)+b'\n'

      if (ods):
         pgm += odsclose

      out = self.stdin.write(pgm)

      self.stdin.flush()

      return str(out)

   def submit(self, code: str, results: str ="html", prompt: dict = None, **kwargs) -> dict:
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
      prompt  = prompt if prompt is not None else {}
      printto = kwargs.pop('undo', False)

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
      #logcodei = "%put E3969440A681A24088859985" + logn + ";"
      #logcodeo = b"\nE3969440A681A24088859985" + logn.encode()
      logcodei = "%put %upcase(e3969440a681a24088859985" + logn + ");"
      logcodeo = b"E3969440A681A24088859985" + logn.encode()
      pcodei   = ''
      pcodeiv  = ''
      pcodeo   = ''
      undo     = b'proc printto;run;\n' if printto else b''

      if self.pid == None:
         self._sb.SASpid = None
         logger.error("No SAS process attached. SAS process has terminated unexpectedly.")
         return dict(LOG="No SAS process attached. SAS process has terminated unexpectedly.", LST='')

      if os.name == 'nt':
         try:
            rc = self.pid.wait(0)
            self.pid = None
            return 'SAS process has terminated unexpectedly. RC from wait was: '+str(rc)
         except:
            pass
      else:
         rc = os.waitpid(self.pid, os.WNOHANG)
         if rc[0] != 0:
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
                  raise RuntimeError("No value for prompted macro variable provided.")
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

      pgm = b''
      if ods:
         pgm += odsopen

      pgm += mj+b'\n'+pcodei.encode(self.sascfg.encoding)+pcodeiv.encode(self.sascfg.encoding)
      pgm += code.encode(self.sascfg.encoding)+b'\n'+pcodeo.encode(self.sascfg.encoding)+b'\n'+mj

      if ods:
         pgm += odsclose

      pgm += undo+logcodei.encode(self.sascfg.encoding)+b'\n'

      bof = False
      pos = 0
      end = len(pgm)

      while not done:
         try:
            while True:
               wait = True
               if os.name == 'nt':
                  try:
                     rc = self.pid.wait(0)
                     self.pid = None
                     #return 'SAS process has terminated unexpectedly. RC from wait was: '+str(rc)
                     self._sb.SASpid = None
                     return dict(LOG='SAS process has terminated unexpectedly. Pid State= ' +
                                 str(rc)+'\n'+logf.decode(self.sascfg.encoding, errors='replace'), LST='')
                  except:
                     pass
               else:
                  rc = os.waitpid(self.pid, os.WNOHANG)
                  if rc[0] != 0:
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

               if pos < end:
                  out = self.stdin.write(pgm[pos:min(pos+4096,end)])
                  self.stdin.flush()
                  pos += out

               if bail:
                  eof -= 1
               if eof < 0:
                  break

               while True:
                  if os.name == 'nt':
                     try:
                        lst = self.stdout.get_nowait()
                     except Empty:
                        lst = b''
                  else:
                     lst = self.stdout.read1(4096)

                  if len(lst) > 0:
                     wait = False
                     lstf += lst
                     if ods and not bof and lstf.count(b"<!DOCTYPE html>") > 0:
                        bof = True
                  else:
                     break

               while True:
                  if os.name == 'nt':
                     try:
                        log = self.stderr.get_nowait()
                     except Empty:
                        log = b''
                  else:
                     log = self.stderr.read1(4096)

                  if len(log) > 0:
                     wait = False
                     logf += log

                  if not (pos < end):
                     if not bail and logf.count(logcodeo) >= 1:
                         if ods:
                            lenf = len(lstf)
                            if lenf > 20 and bof:
                               if lstf.count(b"</html>"):
                                  bail = True
                         else:
                            bail = True

                  if not len(log) > 0:
                     break

               if wait:
                  sleep(0.001)

            done = True

         except (KeyboardInterrupt, SystemExit):
            if not self._sb.sascfg.prompt:
               raise KeyboardInterrupt("Interupt handling is disabled due to prompting being disabled.")

            print('Exception caught!')
            ll = self._breakprompt(logcodeo)

            if ll.get('ABORT', False):
               return ll

            logf += ll['LOG']
            lstf += ll['LST']
            bc    = ll['BC']

            if ods and not bof and lstf.count(b"<!DOCTYPE html>") > 0:
               bof = True
            if not bc:
               print('Exception handled :)\n')
            else:
               print('Exception ignored, continuing to process...\n')

            if pos < end:
               pgm += undo+odsclose+logcodei.encode(self.sascfg.encoding)+b'\n'
               end += len(undo+odsclose+logcodei.encode(self.sascfg.encoding)+b'\n')
            else:
               self.stdin.write(undo+odsclose+logcodei.encode(self.sascfg.encoding)+b'\n')
               self.stdin.flush()

         except (ConnectionResetError):
            log = ''
            if os.name == 'nt':
               try:
                  log = self.stderr.get_nowait()
               except Empty:
                  log = b''
            else:
               try:
                  log = self.stderr.read1(4096)
                  if len(log) > 0:
                     logf += log
                  self._log += logf.decode(self.sascfg.encoding, errors='replace')
               except:
                  pass
            rc = 0
            if os.name == 'nt':
               try:
                  rc = self.pid.wait(0)
               except:
                  pass
            else:
               rc = os.waitpid(self.pid, 0)
            self.pid = None
            self._sb.SASpid = None
            log = logf.partition(logcodeo)[0]+b'\nConnection Reset: SAS process has terminated unexpectedly. Pid State= '+str(rc).encode()+b'\n'+logf
            return dict(LOG=log.encode(), LST='')

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

      logf = logf.decode(self.sascfg.encoding, errors='replace').replace(chr(12), chr(10))

      trip = lstf.rpartition("/*]]>*/")
      if len(trip[1]) > 0 and len(trip[2]) < 200:
         lstf = ''

      self._log += logf
      final = logf.partition(logcodei)
      z = final[0].rpartition(chr(10))
      prev = '%08d' %  (self._log_cnt - 1)
      zz = z[0].rpartition("E3969440A681A24088859985" + prev)
      logd = zz[2].replace(mj.decode(self.sascfg.encoding), '').replace(chr(12), chr(10))

      lstd = lstf.replace(chr(12), chr(10)).replace('<body class="c body">',
                                                    '<body class="l body">').replace("font-size: x-small;",
                                                                                     "font-size:  normal;")
      if self._checkLogForError(logd):
         warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
         self._sb.check_error_log = True

      self._sb._lastlog = logd
      return dict(LOG=logd, LST=lstd)

   def _breakprompt(self, eos):
        found = False
        logf  = b''
        lstf  = b''
        bc    = False

        if self.pid is None:
            self._sb.SASpid = None
            return dict(LOG="No SAS process attached. SAS process has terminated unexpectedly.", LST='', ABORT=True)

        if self.sascfg.ssh:
           response = self.sascfg._prompt(
                     "SAS attention handling not supported over ssh. Please enter (T) to terminate SAS or (C) to continue.")
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

        while True:
            if os.name == 'nt':
               try:
                  rc = self.pid.wait(0)
               except:
                  pass
               self.pid = None
               self._sb.SASpid = None
               return dict(LOG='SAS process has terminated unexpectedly. RC from wait was: '+str(rc), LST='',ABORT=True)
            else:
               rc = os.waitpid(self.pid, os.WNOHANG)
               if rc[0] != 0:
                  self.pid = None
                  self._sb.SASpid = None
                  outrc = str(rc)
                  return dict(LOG='SAS process has terminated unexpectedly. Pid State= '+outrc, LST='',ABORT=True)

            lst = self.stdout.read1(4096)
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
                    if (response == 'C' or response == 'c') and query.count(b"C. Cancel") >= 1:
                       bc = True
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
                        if (response == 'N' or response == 'n') and query.count(b"N to continue") >= 1:
                           bc = True
                    else:
                        print("******************No 'Select' or 'Press' found. Here's what was found.")
                        found = True
                        print('Processing interrupt\nAttn handler Query is\n\n' + lst.decode(self.sascfg.encoding, errors='replace'))
                        response = None
                        while response is None:
                           response = self.sascfg._prompt("Please enter your Response: or N/A only if there are no choices: ")
                        if response not in ['N/A', '']:
                           self.stdin.write(response.encode(self.sascfg.encoding) + b'\n')
                           self.stdin.flush()
                        else:
                           lstf += lst
                        bc = True
                        break
            else:
                if bc:
                   break
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

            if log.count("E3969440A681A24088859985"+logn+"\n") >= 1:
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
      sd = table.strip().replace("'", "''")
      code  = 'data _null_; e = exist("'
      if len(libref):
         code += libref+"."
      code += "'"+sd+"'n"+'"'+");\n"
      code += 'v = exist("'
      if len(libref):
         code += libref+"."
      code += "'"+sd+"'n"+'"'+", 'VIEW');\n if e or v then e = 1;\n"
      code += "put 'TABLE_EXISTS=' e 'TAB_EXTEND=';run;"

      ll = self.submit(code, "text")

      exists = int(ll['LOG'].rpartition("TABLE_EXISTS=")[2].rpartition(" TAB_EXTEND=")[0])

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

      code += "'"+table.strip().replace("'", "''")+"'n dbms=csv replace; "+self._sb._impopts(opts)+" run;"

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

      code  = "filename x \""+file+"\";\n"
      code += "options nosource;\n"
      code += "proc export data="

      if len(libref):
         code += libref+"."

      code += "'"+table.strip().replace("'", "''")+"'n "+self._sb._dsopts(dsopts)+" outfile=x dbms=csv replace;\n"
      code += self._sb._expopts(opts)+" run;\n"
      code += "options source;\n"

      if nosub:
         print(code)
      else:
         ll = self.submit(code, "text")
         return ll['LOG']

   def upload_slow(self, localfile: str, remotefile: str, overwrite: bool = True, permission: str = '', **kwargs):
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

      code = """
         filename saspydir '"""+remf+"""' recfm=F encoding=binary lrecl=1 permission='"""+permission+"""';
         data _null_;
         file saspydir;
         infile datalines;
         input;
         lin = length(_infile_);
         outdata = inputc(_infile_, '$hex.', lin);
         lout = lin/2;
         put outdata $varying80. lout;
         datalines4;"""

      buf = fd.read1(40)
      if len(buf):
         self._asubmit(code, "text")
      else:
         code = """
            filename saspydir '"""+remf+"""' recfm=F encoding=binary lrecl=1 permission='"""+permission+"""';
            data _null_;
            fid = fopen('saspydir', 'O');
            if fid then
               rc = fclose(fid);
            run;\n"""

         ll = self.submit(code, 'text')
         fd.close()
         return {'Success' : True,
                 'LOG'     : ll['LOG']}

      while len(buf):
         buf2 = ''
         for i in range(len(buf)):
            buf2 += '%02x' % buf[i]
         self.stdin.write(buf2.encode()+b'\n')
         buf = fd.read1(40)

      self._asubmit(";;;;", "text")
      ll = self.submit("run;\nfilename saspydir;", 'text')
      fd.close()

      return {'Success' : True,
              'LOG'     : ll['LOG']}

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

      port =  kwargs.get('port', 0)

      if self.sascfg.ssh and self.sascfg.rtunnel and port == 0:
         # we are using a rtunnel; default to that port
         port = self.sascfg.rtunnel
         host = 'localhost'
      else:
         return self._upload_client(localfile, remotefile, overwrite, permission, **kwargs)

      try:
         fd = open(localfile, 'rb')
      except OSError as e:
         return {'Success' : False,
                 'LOG'     : "File "+str(localfile)+" could not be opened. Error was: "+str(e)}

      code = """
         filename saspydir '"""+remf+"""' recfm=F encoding=binary lrecl=1 permission='"""+permission+"""';
         filename sock socket ':"""+str(port)+"""' server reconn=0 recfm=S lrecl=4096;

         data _null_; nb = -1;
         infile sock nbyte=nb;
         file saspydir;
         input;
         put _infile_;
         run;

         filename saspydir;
         filename sock;\n"""

      self._asubmit(code, "text")

      sock = socks.socket()
      sock.connect((host, port))

      done = False
      while not done:
         try:
            while True:
               buf  = fd.read1(4096)
               sent = 0
               send = len(buf)
               blen = send
               if blen:
                  while send:
                     try:
                        sent = 0
                        sent = sock.send(buf[blen-send:blen])
                     except (BlockingIOError):
                        pass
                     except (OSError):
                        sock.close()
                        fd.close()
                        sock = socks.socket()
                        sock.connect((host, port))
                        fd = open(localfile, 'rb')
                        sleep(.5)
                        break
                     send -= sent
               else:
                  done = True
                  try: # Mac OS Python has bugs with this call
                     sock.shutdown(socks.SHUT_RDWR)
                  except:
                     pass
                  sock.close()
                  fd.close()
                  break
         except (KeyboardInterrupt, Exception) as e:
            sock.close()
            fd.close()
            ll = self.submit("", 'text')
            return {'Success' : False,
                    'LOG'     : "Download was interrupted. Returning the SAS log:\n\n"+str(e)+"\n\n"+ll['LOG']}

      ll = self.submit("", 'text')
      return {'Success' : True,
              'LOG'     : ll['LOG']}

   def _upload_client(self, localfile: str, remotefile: str, overwrite: bool = True, permission: str = '', **kwargs):
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

      port =  kwargs.get('port', 0)

      if port==0 and self.sascfg.tunnel:
         # we are using a tunnel; default to that port
         port = self.sascfg.tunnel

      if self.sascfg.ssh:
         if not self.sascfg.tunnel:
            host = self.sascfg.hostip #socks.gethostname()
         else:
            host = 'localhost'
      else:
         host = ''

      try:
         fd = open(localfile, 'rb')
      except OSError as e:
         return {'Success' : False,
                 'LOG'     : "File "+str(localfile)+" could not be opened. Error was: "+str(e)}

      try:
         sock = socks.socket()
         if self.sascfg.tunnel:
            sock.bind(('localhost', port))
         else:
            sock.bind(('', port))
         port = sock.getsockname()[1]
      except OSError:
         return {'Success' : False,
                 'LOG'     : "Error try to open a socket in the upload method. Call failed."}

      code = """
         filename saspydir '"""+remf+"""' recfm=F encoding=binary lrecl=1 permission='"""+permission+"""';
         filename sock socket '"""+host+""":"""+str(port)+"""' recfm=S lrecl=4096;
         /* filename sock socket '"""+host+""":"""+str(port)+"""' recfm=S encoding=binary lrecl=4096; */

         data _null_; nb = -1;
         infile sock nbyte=nb;
         file saspydir;
         input;
         put _infile_;
         run;

         filename saspydir;
         filename sock;\n"""

      sock.listen(1)
      self._asubmit(code, 'text')

      if sel.select([sock],[],[],10)[0] == []:
         logger.error("error occured in SAS during upload. Check the returned LOG for issues.")
         sock.close()
         fd.close()
         ll = self.submit("", 'text')
         return {'Success' : False,
                 'LOG'     : "Failure in upload.\n"+ll['LOG']}

      newsock = (0,0)
      try:
         newsock = sock.accept()
         while True:
            buf  = fd.read1(4096)
            sent = 0
            send = len(buf)
            blen = send
            if blen:
               while send:
                  try:
                     sent = 0
                     sent = newsock[0].send(buf[blen-send:blen])
                  except (BlockingIOError):
                     pass
                  send -= sent
            else:
               try: # Mac OS Python has bugs with this call
                  newsock[0].shutdown(socks.SHUT_RDWR)
               except:
                  pass
               newsock[0].close()
               sock.close()
               fd.close()
               break
      except (KeyboardInterrupt, Exception) as e:
         if newsock[0]:
            try: # Mac OS Python has bugs with this call
               newsock[0].shutdown(socks.SHUT_RDWR)
            except:
               pass
            newsock[0].close()
         sock.close()
         fd.close()
         ll = self.submit("", 'text')
         return {'Success' : False,
                 'LOG'     : "Download was interrupted. Returning the SAS log:\n\n"+str(e)+"\n\n"+ll['LOG']}

      ll = self.submit("", 'text')
      return {'Success' : True,
              'LOG'     : ll['LOG']}

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
      except OSError as e:
         return {'Success' : False,
                 'LOG'     : "File "+str(locf)+" could not be opened. Error was: "+str(e)}

      port =  kwargs.get('port', 0)

      if port==0 and self.sascfg.tunnel:
         # we are using a tunnel; default to that port
         port = self.sascfg.tunnel

      try:
         sock = socks.socket()
         if self.sascfg.tunnel:
            sock.bind(('localhost', port))
         else:
            sock.bind(('', port))
         port = sock.getsockname()[1]
      except OSError:
         return {'Success' : False,
                 'LOG'     : "Error try to open a socket in the download method. Call failed."}

      if self.sascfg.ssh:
         if not self.sascfg.tunnel:
            host = self.sascfg.hostip #socks.gethostname()
         else:
            host = 'localhost'
      else:
         host = ''

      code = """
         filename saspydir '"""+remotefile+"""' recfm=F encoding=binary lrecl=4096;
         filename sock socket '"""+host+""":"""+str(port)+"""' recfm=S lrecl=4096;
         /* filename sock socket '"""+host+""":"""+str(port)+"""' recfm=S encoding=binary; */
         data _null_;
         file sock;
         infile saspydir;
         input;
         put _infile_;
         run;\n"""

      sock.listen(1)
      self._asubmit(code, 'text')

      if sel.select([sock],[],[],10)[0] == []:
         logger.error("error occured in SAS during download. Check the returned LOG for issues.")
         sock.close()
         fd.close()
         ll = self.submit("", 'text')
         return {'Success' : False,
                 'LOG'     : "Failure in download.\n"+ll['LOG']}

      datar = b''
      newsock = (0,0)
      try:
         newsock = sock.accept()
         while True:
            data = newsock[0].recv(4096)

            if len(data):
               datar += data
            else:
               if len(datar):
                  fd.write(datar)
               break
            if len(datar) > 8300:
               fd.write(datar[:8192])
               datar = datar[8192:]
      except (KeyboardInterrupt, Exception) as e:
         try:
            if newsock[0]:
               try: # Mac OS Python has bugs with this call
                  newsock[0].shutdown(socks.SHUT_RDWR)
               except:
                  pass
               newsock[0].shutdown(socks.SHUT_RDWR)
               newsock[0].close()
         except:
            pass
         sock.close()
         fd.close()
         ll = self.submit("filename saspydir;", 'text')
         return {'Success' : False,
                 'LOG'     : "Download was interrupted. Returning the SAS log:\n\n"+str(e)+"\n\n"+ll['LOG']}

      try: # Mac OS Python has bugs with this call
         newsock[0].shutdown(socks.SHUT_RDWR)
      except:
         pass
      newsock[0].close()
      sock.close()

      fd.flush()
      fd.close()

      ll = self.submit("filename saspydir;", 'text')
      return {'Success' : True,
              'LOG'     : ll['LOG']}

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
      """
      This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
      keep_outer_quotes - for character columns, have SAS keep any outer quotes instead of stripping them off.
      embedded_newlines - if any char columns have embedded CR or LF, set this to True to get them iported into the SAS data set
      LF - if embedded_newlines=True, the chacter to use for LF when transferring the data; defaults to '\x01'
      CR - if embedded_newlines=True, the chacter to use for CR when transferring the data; defaults to '\x02'
      colsep - the column seperator character used for streaming the delimmited data to SAS defaults to '\x03'
      datetimes - dict with column names as keys and values of 'date' or 'time' to create SAS date or times instead of datetimes
      outfmts - dict with column names and SAS formats to assign to the new SAS data set
      labels  - dict with column names and SAS Labels to assign to the new SAS data set
      outdsopts - a dictionary containing output data set options for the table being created
      encode_errors - 'fail' or 'replace' - default is to 'fail', other choice is to 'replace' invalid chars with the replacement char

      char_lengths - How to determine (and declare) lengths for CHAR variables in the output SAS data set
      """
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

      for name in df.columns:
         colname = str(name).replace("'", "''")
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
         input += ';\n'

      port =  kwargs.get('port', 0)

      if self.sascfg.ssh and self.sascfg.rtunnel and port == 0:
         # we are using a rtunnel; default to that port
         server = True
         port = self.sascfg.rtunnel
         host = 'localhost'
         code = """filename sock socket ':"""+str(port)+"""' server reconn=0 recfm=V termstr=LF lrecl=32767;\n"""
      else:
         server = False
         if port==0 and self.sascfg.tunnel:
            # we are using a tunnel; default to that port
            port = self.sascfg.tunnel

         if self.sascfg.ssh:
            if not self.sascfg.tunnel:
               host = self.sascfg.hostip #socks.gethostname()
            else:
               host = 'localhost'
         else:
            host = ''

         try:
            sock = socks.socket()
            if self.sascfg.tunnel:
               sock.bind(('localhost', port))
            else:
               sock.bind(('', port))
            port = sock.getsockname()[1]
         except OSError as e:
            raise e
         code  = """filename sock socket '"""+host+""":"""+str(port)+"""' recfm=V termstr=LF lrecl=32767;\n"""

      code += "data "
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
         code += "length"+length+";\n"
      if len(format):
         code += "format "+format+";\n"
      code += label
      code += "infile sock nbyte=nb delimiter="+delim+" STOPOVER;\n"
      code += "input @;\nif _infile_ = '' then delete;\nelse do;\n"
      code +=  input+xlate+";\n"
      code += "end;\n"
      code += "run;\nfilename sock;\n"

      if not server:
         sock.listen(1)

      self._asubmit(code, "text")

      if server:
         sleep(1)
         sock = socks.socket()
         sock.connect((host, port))
         ssock = sock

      if not server:
         if sel.select([sock],[],[],10)[0] == []:
            logger.error("error occured in SAS during data transfer. Check the LOG for issues.")
            sock.close()
            ll = self.submit("", 'text')
            return {'Success' : False,
                    'LOG'     : "Failure in upload.\n"+ll['LOG']}
         newsock = (0,0)
         try:
            newsock = sock.accept()
         except (KeyboardInterrupt, Exception) as e:
            try:
               if newsock[0]:
                  try: # Mac OS Python has bugs with this call
                     newsock[0].shutdown(socks.SHUT_RDWR)
                  except:
                     pass
                  newsock[0].close()
            except:
               pass
            sock.close()
            logger.error("error occured in SAS during data transfer. Check the LOG for issues.")
            ll = self.submit("", 'text')
            return {'Success' : False,
                    'LOG'     : "Download was interrupted. Returning the SAS log:\n\n"+str(e)+"\n\n"+ll['LOG']}
         ssock = newsock[0]

      logf  = b''
      first = True
      fail  = False
      blksz = int(kwargs.get('blocksize', 32767))
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
               if var == 'nan' or len(var) == 0:
                  var = ' '+colsep
               else:
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
            first = False
            if encode_errors != 'replace':
               try:
                  code = code.encode(self.sascfg.encoding)
               except Exception as e:
                  try:
                     if server:
                        sock.shutdown(socks.SHUT_RDWR)
                     else:
                        if newsock[0]:
                           try: # Mac OS Python has bugs with this call
                              newsock[0].shutdown(socks.SHUT_RDWR)
                           except:
                              pass
                           newsock[0].close()
                  except:
                     pass
                  sock.close()

                  logd = logf.decode(self.sascfg.encoding, errors='replace')
                  self._log += logd
                  if self._checkLogForError(logd):
                     warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
                     self._sb.check_error_log = True

                  ll = self.submit("", 'text')
                  logger.error("Transcoding error encountered. Data transfer stopped on or before row "+str(row_num))
                  logger.error("DataFrame contains characters that can't be transcoded into the SAS session encoding.\n"+str(e))
                  return row_num
            else:
               code = code.encode(self.sascfg.encoding, errors='replace')

            sent = 0
            send = len(code)
            blen = send
            while send:
               try:
                  sent = 0
                  sent = ssock.send(code[blen-send:blen])
               except (BlockingIOError):
                  pass
               except (OSError) as e:
                  if fail:
                     try:
                        if server:
                           sock.shutdown(socks.SHUT_RDWR)
                        else:
                           if newsock[0]:
                              try: # Mac OS Python has bugs with this call
                                 newsock[0].shutdown(socks.SHUT_RDWR)
                              except:
                                 pass
                              newsock[0].close()
                     except:
                        pass
                     sock.close()
                     logger.error("Failed connecting to server socket. Check the SASLOG to see the error")
                     ll = self.submit("", 'text')
                     return row_num
                  fail = True
                  if server:
                     sock.close()
                     sock = socks.socket()
                     sock.connect((host, port))
                     ssock = sock
                     sleep(1)
                  pass
               send -= sent
            code = ""

            if os.name == 'nt':
               try:
                  log = self.stderr.get_nowait()
               except Empty:
                  log = b''
            else:
               log = self.stderr.read1(4096)

            if len(log) > 0:
               logf += log

      logd = logf.decode(self.sascfg.encoding, errors='replace')
      self._log += logd
      if self._checkLogForError(logd):
         warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
         self._sb.check_error_log = True

      if len(code):
         if encode_errors != 'replace':
            try:
               code = code.encode(self.sascfg.encoding)
            except Exception as e:
               try:
                  if server:
                     sock.shutdown(socks.SHUT_RDWR)
                  else:
                     if newsock[0]:
                        try: # Mac OS Python has bugs with this call
                           newsock[0].shutdown(socks.SHUT_RDWR)
                        except:
                           pass
                        newsock[0].close()
               except:
                  pass
               sock.close()
               ll = self.submit("", 'text')
               logger.error("Transcoding error encountered. Data transfer stopped on row "+str(row_num))
               logger.error("DataFrame contains characters that can't be transcoded into the SAS session encoding.\n"+str(e))
               return row_num
         else:
            code = code.encode(self.sascfg.encoding, errors='replace')

         sent = 0
         send = len(code)
         blen = send
         while send:
            try:
               sent = 0
               sent = ssock.send(code[blen-send:blen])
            except (BlockingIOError):
               pass
            except (OSError) as e:
               if not first:
                  try:
                     if server:
                        sock.shutdown(socks.SHUT_RDWR)
                     else:
                        if newsock[0]:
                           try: # Mac OS Python has bugs with this call
                              newsock[0].shutdown(socks.SHUT_RDWR)
                           except:
                              pass
                           newsock[0].close()
                  except:
                     pass
                  sock.close()
                  logger.error("Failed connecting to server socket. Check the SASLOG to see the error")
                  ll = self.submit("", 'text')
                  return row_num
               first = False
               if server:
                  sock.close()
                  sock = socks.socket()
                  sock.connect((host, port))
                  ssock = sock
                  sleep(1)
               pass
            send -= sent
      try:
         if server:
            sock.shutdown(socks.SHUT_RDWR)
         else:
            try: # Mac OS Python has bugs with this call
               newsock[0].shutdown(socks.SHUT_RDWR)
            except:
               pass
            newsock[0].close()
      except:
         pass
      sock.close()

      ll = self.submit("", 'text')
      return None

   def sasdata2dataframe(self, table: str, libref: str ='', dsopts: dict = None,
                         rowsep: str = '\x01', colsep: str = '\x02',
                         rowrep: str = ' ',    colrep: str = ' ',
                         port: int=0, wait: int=10, **kwargs) -> '<Pandas Data Frame object>':
      """
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table   - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref  - the libref for the SAS Data Set.
      rowsep  - the row seperator character to use; defaults to '\x01'
      colsep  - the column seperator character to use; defaults to '\x02'
      rowrep  - the char to convert to for any embedded rowsep chars, defaults to  ' '
      colrep  - the char to convert to for any embedded colsep chars, defaults to  ' '
      port    - port to use for socket. Defaults to 0 which uses a random available ephemeral port
      wait    - seconds to wait for socket connection from SAS; catches hang if an error in SAS. 0 = no timeout
      """
      dsopts = dsopts if dsopts is not None else {}

      method = kwargs.pop('method', None)
      if   method and method.lower() == 'csv':
         return self.sasdata2dataframeCSV(table, libref, dsopts, port=port, wait=wait, **kwargs)
      #elif method and method.lower() == 'disk':
      else:
         return self.sasdata2dataframeDISK(table, libref, dsopts, rowsep, colsep,
                                           rowrep, colrep, port=port, wait=wait, **kwargs)


   def sasdata2dataframeCSV(self, table: str, libref: str ='', dsopts: dict = None, opts: dict = None,
                            port: int=0, wait: int=10, **kwargs) -> '<Pandas Data Frame object>':
      """
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table    - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref   - the libref for the SAS Data Set.
      dsopts   - data set options for the input SAS Data Set
      opts     - a dictionary containing any of the following Proc Export options(delimiter, putnames)
      tempfile - DEPRECATED
      tempkeep - DEPRECATED
      port     - port to use for socket. Defaults to 0 which uses a random available ephemeral port
      wait     - seconds to wait for socket connection from SAS; catches hang if an error in SAS. 0 = no timeout

      These two options are for advanced usage. They override how saspy imports data. For more info
      see https://sassoftware.github.io/saspy/advanced-topics.html#advanced-sd2df-and-df2sd-techniques

      dtype   - this is the parameter to Pandas read_csv, overriding what saspy generates and uses
      my_fmts - bool: if True, overrides the formats saspy would use, using those on the data set or in dsopts=
      """
      tmp = kwargs.pop('tempfile', None)
      tmp = kwargs.pop('tempkeep', None)

      dsopts = dsopts if dsopts is not None else {}
      opts   = opts   if   opts is not None else {}

      if port==0 and self.sascfg.tunnel:
         # we are using a tunnel; default to that port
         port = self.sascfg.tunnel

      if libref:
         tabname = libref+".'"+table.strip().replace("'", "''")+"'n "
      else:
         tabname = "'"+table.strip().replace("'", "''")+"'n "

      code  = "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";run;\n"
      code += "data _null_; file STDERR;d = open('work.sasdata2dataframe');\n"
      code += "lrecl = attrn(d, 'LRECL'); nvars = attrn(d, 'NVARS');\n"
      code += "lr='LRECL='; vn='VARNUMS='; vl='VARLIST='; vt='VARTYPE=';\n"
      code += "put lr lrecl; put vn nvars; put vl;\n"
      code += "do i = 1 to nvars; var = varname(d, i); put var; end;\n"
      code += "put vt;\n"
      code += "do i = 1 to nvars; var = vartype(d, i); put var; end;\n"
      code += "run;"

      ll = self.submit(code, "text")

      try:
         l2 = ll['LOG'].rpartition("LRECL= ")
         l2 = l2[2].partition("\n")
         lrecl = int(l2[0])

         l2 = l2[2].partition("VARNUMS= ")
         l2 = l2[2].partition("\n")
         nvars = int(l2[0])

         l2 = l2[2].partition("\n")
         varlist = l2[2].split("\n", nvars)
         del varlist[nvars]

         dvarlist = list(varlist)
         for i in range(len(varlist)):
            varlist[i] = varlist[i].replace("'", "''")

         l2 = l2[2].partition("VARTYPE=")
         l2 = l2[2].partition("\n")
         vartype = l2[2].split("\n", nvars)
         del vartype[nvars]
      except Exception as e:
         logger.error("Invalid output produced durring sasdata2dataframe step. Step failed.\
         \nPrinting the error: {}\nPrinting the SASLOG as diagnostic\n{}".format(str(e), ll['LOG']))
         return None

      topts = dict(dsopts)
      topts.pop('firstobs', None)
      topts.pop('obs', None)

      code  = "proc delete data=work.sasdata2dataframe(memtype=view);run;\n"
      code += "data work._n_u_l_l_;output;run;\n"
      code += "data _null_; file STDERR; set work._n_u_l_l_ "+tabname+self._sb._dsopts(topts)+";put 'FMT_CATS=';\n"

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

      try:
         sock = socks.socket()
         if not self.sascfg.ssh or self.sascfg.tunnel:
            sock.bind(('localhost', port))
         else:
            sock.bind(('', port))
         port = sock.getsockname()[1]
      except OSError:
         logger.error('Error try to open a socket in the sasdata2dataframe method. Call failed.')
         return None

      if self.sascfg.ssh and not self.sascfg.tunnel:
         host = self.sascfg.hostip  #socks.gethostname()
      else:
         host = 'localhost'
      code  = "filename sock socket '"+host+":"+str(port)+"' lrecl="+str(self.sascfg.lrecl)+" recfm=v encoding='utf-8';\n"
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

      if k_dts is None:
         dts = {}
         for i in range(nvars):
            if vartype[i] == 'N':
               if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  dts[dvarlist[i]] = 'float'
               else:
                  dts[dvarlist[i]] = 'str'
            else:
               dts[dvarlist[i]] = 'str'
      else:
         dts = k_dts

      code  = ''
      code  = "proc export data=work.sasdata2dataframe outfile=sock dbms=csv replace;\n"
      code += self._sb._expopts(opts)+" run;\n"
      code += "proc delete data=work.sasdata2dataframe(memtype=view);run;\n"

      sock.listen(1)
      self._asubmit(code, 'text')

      if wait > 0 and sel.select([sock],[],[],wait)[0] == []:
         logger.error("error occured in SAS during sasdata2dataframe. Trying to return the saslog instead of a data frame.")
         sock.close()
         ll = self.submit("", 'text')
         return ll['LOG']

      newsock = (0,0)
      try:
         newsock = sock.accept()

         sockout = _read_sock(newsock=newsock, rowsep=b'\n')

         df = pd.read_csv(sockout, index_col=idx_col, encoding='utf8', engine=eng, dtype=dts, **kwargs)

      except (KeyboardInterrupt, Exception) as e:
         logger.error("sasdata2dataframe was interrupted. Trying to return the saslog instead of a data frame.")
         try:
            if newsock[0]:
               try: # Mac OS Python has bugs with this call
                  newsock[0].shutdown(socks.SHUT_RDWR)
               except:
                  pass
               newsock[0].close()
         except:
            pass
         sock.close()
         ll = self.submit("", 'text')
         return str(e)+"\n\n"+ll['LOG']

      try: # Mac OS Python has bugs with this call
         newsock[0].shutdown(socks.SHUT_RDWR)
      except:
         pass
      newsock[0].close()
      sock.close()
      ll = self.submit("", 'text')

      if k_dts is None:  # don't override these if user provided their own dtypes
         for i in range(nvars):
            if vartype[i] == 'N':
               if varcat[i] in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  df[dvarlist[i]] = pd.to_datetime(df[dvarlist[i]], errors='coerce')

      return df

   def sasdata2dataframeDISK(self, table: str, libref: str ='', dsopts: dict = None,
                             rowsep: str = '\x01', colsep: str = '\x02',
                             rowrep: str = ' ',    colrep: str = ' ', port: int=0,
                             wait: int=10, **kwargs) -> '<Pandas Data Frame object>':
      """
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
      port     - port to use for socket. Defaults to 0 which uses a random available ephemeral port
      wait     - seconds to wait for socket connection from SAS; catches hang if an error in SAS. 0 = no timeout

      These two options are for advanced usage. They override how saspy imports data. For more info
      see https://sassoftware.github.io/saspy/advanced-topics.html#advanced-sd2df-and-df2sd-techniques

      dtype   - this is the parameter to Pandas read_csv, overriding what saspy generates and uses
      my_fmts - bool: if True, overrides the formats saspy would use, using those on the data set or in dsopts=
      """
      tmp = kwargs.pop('tempfile', None)
      tmp = kwargs.pop('tempkeep', None)

      dsopts = dsopts if dsopts is not None else {}

      if port==0 and self.sascfg.tunnel:
         # we are using a tunnel; default to that port
         port = self.sascfg.tunnel

      if libref:
         tabname = libref+".'"+table.strip().replace("'", "''")+"'n "
      else:
         tabname = "'"+table.strip().replace("'", "''")+"'n "

      code  = "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";run;\n"
      code += "data _null_; file STDERR;d = open('work.sasdata2dataframe');\n"
      code += "lrecl = attrn(d, 'LRECL'); nvars = attrn(d, 'NVARS');\n"
      code += "lr='LRECL='; vn='VARNUMS='; vl='VARLIST='; vt='VARTYPE=';\n"
      code += "put lr lrecl; put vn nvars; put vl;\n"
      code += "do i = 1 to nvars; var = varname(d, i); put var; end;\n"
      code += "put vt;\n"
      code += "do i = 1 to nvars; var = vartype(d, i); put var; end;\n"
      code += "run;"

      ll = self.submit(code, "text")

      try:
         l2 = ll['LOG'].rpartition("LRECL= ")
         l2 = l2[2].partition("\n")
         lrecl = int(l2[0])

         l2 = l2[2].partition("VARNUMS= ")
         l2 = l2[2].partition("\n")
         nvars = int(l2[0])

         l2 = l2[2].partition("\n")
         varlist = l2[2].split("\n", nvars)
         del varlist[nvars]

         dvarlist = list(varlist)
         for i in range(len(varlist)):
            varlist[i] = varlist[i].replace("'", "''")

         l2 = l2[2].partition("VARTYPE=")
         l2 = l2[2].partition("\n")
         vartype = l2[2].split("\n", nvars)
         del vartype[nvars]
      except Exception as e:
         logger.error("Invalid output produced durring sasdata2dataframe step. Step failed.\
         \nPrinting the error: {}\nPrinting the SASLOG as diagnostic\n{}".format(str(e), ll['LOG']))
         return None

      topts = dict(dsopts)
      topts.pop('firstobs', None)
      topts.pop('obs', None)

      code  = "proc delete data=work.sasdata2dataframe(memtype=view);run;\n"
      code += "data work._n_u_l_l_;output;run;\n"
      code += "data _null_; file STDERR; set work._n_u_l_l_ "+tabname+self._sb._dsopts(topts)+";put 'FMT_CATS=';\n"

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

      try:
         sock = socks.socket()
         if not self.sascfg.ssh or self.sascfg.tunnel:
            sock.bind(('localhost', port))
         else:
            sock.bind(('', port))
         port = sock.getsockname()[1]
      except OSError:
         logger.error('Error try to open a socket in the sasdata2dataframe method. Call failed.')
         return None

      if self.sascfg.ssh and not self.sascfg.tunnel:
         host = self.sascfg.hostip  #socks.gethostname()
      else:
         host = 'localhost'

      lreclx = max(self.sascfg.lrecl, (lrecl + nvars + 1))

      code = "filename sock socket '"+host+":"+str(port)+"' recfm=s encoding='utf-8' lrecl={};\n".format(str(lreclx))

      rdelim = "'"+'%02x' % ord(rowsep.encode(self.sascfg.encoding))+"'x"
      cdelim = "'"+'%02x' % ord(colsep.encode(self.sascfg.encoding))+"'x"

      idx_col = kwargs.pop('index_col', False)
      eng     = kwargs.pop('engine',    'c')
      my_fmts = kwargs.pop('my_fmts',   False)
      k_dts   = kwargs.pop('dtype',     None)
      if k_dts is None and my_fmts:
         logger.warning("my_fmts option only valid when dtype= is specified. Ignoring and using necessary formatting for data transfer.")
         my_fmts = False

      code += "data _null_; set "+tabname+self._sb._dsopts(dsopts)+";\n"

      if not my_fmts:
         for i in range(nvars):
            if vartype[i] == 'N':
               code += "format '"+varlist[i]+"'n "
               if varcat[i] in self._sb.sas_date_fmts:
                  code += 'E8601DA10.'
               else:
                  if varcat[i] in self._sb.sas_time_fmts:
                     code += 'E8601TM15.6'
                  else:
                     if varcat[i] in self._sb.sas_datetime_fmts:
                        code += 'E8601DT26.6'
                     else:
                        code += 'best32.'
               code += '; '
               if i % 10 == 9:
                  code +='\n'

      miss  = {}
      code += "\nfile sock dlm="+cdelim+";\n"
      for i in range(nvars):
         if vartype[i] != 'N':
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
      code += rdelim+";\nrun;"

      if k_dts is None:
         dts = {}
         for i in range(nvars):
            if vartype[i] == 'N':
               if varcat[i] not in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  dts[dvarlist[i]] = 'float'
               else:
                  dts[dvarlist[i]] = 'str'
            else:
               dts[dvarlist[i]] = 'str'
      else:
         dts = k_dts

      quoting = kwargs.pop('quoting', 3)

      sock.listen(1)
      self._asubmit(code, 'text')

      if wait > 0 and sel.select([sock],[],[],wait)[0] == []:
         logger.error("error occured in SAS during sasdata2dataframe. Trying to return the saslog instead of a data frame.")
         sock.close()
         ll = self.submit("", 'text')
         return ll['LOG']

      newsock = (0,0)
      try:
         newsock = sock.accept()

         sockout = _read_sock(newsock=newsock, rowsep=rowsep.encode())

         df = pd.read_csv(sockout, index_col=idx_col, engine=eng, header=None, names=dvarlist,
                          sep=colsep, lineterminator=rowsep, dtype=dts, na_values=miss,
                          encoding='utf8', quoting=quoting, **kwargs)

      except (KeyboardInterrupt, Exception) as e:
         logger.error(e)
         logger.error("sasdata2dataframe was interrupted. Trying to return the saslog instead of a data frame.")
         try:
            if newsock[0]:
               try: # Mac OS Python has bugs with this call
                  newsock[0].shutdown(socks.SHUT_RDWR)
               except:
                  pass
               newsock[0].close()
         except:
            pass
         sock.close()
         ll = self.submit("", 'text')
         return str(e)+"\n\n"+ll['LOG']

      try: # Mac OS Python has bugs with this call
         newsock[0].shutdown(socks.SHUT_RDWR)
      except:
         pass
      newsock[0].close()
      sock.close()
      ll = self.submit("", 'text')

      if k_dts is None:  # don't override these if user provided their own dtypes
         for i in range(nvars):
            if vartype[i] == 'N':
               if varcat[i] in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  df[dvarlist[i]] = pd.to_datetime(df[dvarlist[i]], errors='coerce')

      return df

class _read_sock(io.StringIO):
   def __init__(self, **kwargs):
      self.newsock  = kwargs.get('newsock')
      self.rowsep   = kwargs.get('rowsep')
      self.datar    = b""

   def read(self, size=4096):
      datl    = 0
      size    = max(size, 4096)
      notarow = True

      while datl < size or notarow:
         data = self.newsock[0].recv(size)
         dl = len(data)

         if dl:
            datl       += dl
            self.datar += data
            if notarow:
               notarow = self.datar.count(self.rowsep) <= 0
         else:
            if len(self.datar) <= 0:
               return ''
            else:
               break

      data        = self.datar.rpartition(self.rowsep)
      datap       = data[0]+data[1]
      self.datar  = data[2]

      return datap.decode()

