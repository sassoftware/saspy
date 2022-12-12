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
import codecs
import warnings
import io

import logging
logger = logging.getLogger('saspy')

try:
   import pandas as pd
   import numpy  as np
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
      self.classpath = cfg.get('classpath', None)
      self.authkey   = cfg.get('authkey', '')
      self.timeout   = cfg.get('timeout', None)
      self.appserver = cfg.get('appserver', '')
      self.sspi      = cfg.get('sspi', False)
      self.javaparms = cfg.get('javaparms', '')
      self.lrecl     = cfg.get('lrecl', None)
      self.reconnect = cfg.get('reconnect', True)
      self.reconuri  = cfg.get('reconuri', None)
      self.logbufsz  = cfg.get('logbufsz', None)
      self.log4j     = cfg.get('log4j', '2.12.4')

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

      injava = kwargs.get('java', '')
      if len(injava) > 0:
         if lock and len(self.java):
            logger.warning("Parameter 'java' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.java = injava

      inhost = kwargs.get('iomhost', '')
      if len(inhost) > 0:
         if lock and len(self.iomhost):
            logger.warning("Parameter 'iomhost' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.iomhost = inhost

      intout = kwargs.get('timeout', None)
      if intout is not None:
         if lock and self.timeout:
            logger.warning("Parameter 'timeout' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.timeout = intout

      inport = kwargs.get('iomport', None)
      if inport:
         if lock and self.iomport:
            logger.warning("Parameter 'port' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.iomport = inport

      inomruser = kwargs.get('omruser', '')
      if len(inomruser) > 0:
         if lock and len(self.omruser):
            logger.warning("Parameter 'omruser' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.omruser = inomruser

      inomrpw = kwargs.get('omrpw', '')
      if len(inomrpw) > 0:
         if lock and len(self.omrpw):
            logger.warning("Parameter 'omrpw' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.omrpw = inomrpw

      insspi = kwargs.get('sspi', False)
      if insspi:
         if lock and self.sspi:
            logger.warning("Parameter 'sspi' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.sspi = insspi

      inl4j = kwargs.get('log4j', None)
      if inl4j:
         if lock and inl4j:
            logger.warning("Parameter 'log4j' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.log4j = inl4j

      incp = kwargs.get('classpath', None)
      if incp is not None:
         if lock and self.classpath is not None:
            logger.warning("Parameter 'classpath' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.classpath = incp

      if self.classpath is None:
         import importlib.util
         sep   = '\\' if os.name == 'nt' else '/'
         delim = ';'  if os.name == 'nt' else ':'

         cpath = importlib.util.find_spec(self.__module__).origin.replace('sasioiom.py','java')+sep
         cp    = cpath+"saspyiom.jar"

         cpath = cpath+"iomclient"+sep

         if self.log4j not in ['2.17.1', '2.12.4']:
            logger.warning("Parameter 'log4j' passed to SAS_session was invalid. Using the default of 2.12.4.")
            self.log4j = '2.12.4'

         cp   += delim+cpath+"log4j-1.2-api-{}.jar".format(self.log4j)
         cp   += delim+cpath+"log4j-api-{}.jar".format(self.log4j)
         cp   += delim+cpath+"log4j-core-{}.jar".format(self.log4j)

         cp   += delim+cpath+"sas.security.sspi.jar"
         cp   += delim+cpath+"sas.core.jar"
         cp   += delim+cpath+"sas.svc.connection.jar"

         cp   += delim+cpath+"sas.rutil.jar"
         cp   += delim+cpath+"sas.rutil.nls.jar"
         cp   += delim+cpath+"sastpj.rutil.jar"

         cpath = cpath.replace("iomclient", "thirdparty")
         cp   += delim+cpath+"glassfish-corba-internal-api.jar"
         cp   += delim+cpath+"glassfish-corba-omgapi.jar"
         cp   += delim+cpath+"glassfish-corba-orb.jar"
         cp   += delim+cpath+"pfl-basic.jar"
         cp   += delim+cpath+"pfl-tf.jar"

         self.classpath = cp

      inak = kwargs.get('authkey', '')
      if len(inak) > 0:
         if lock and len(self.authkey):
            logger.warning("Parameter 'authkey' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.authkey = inak

      inapp = kwargs.get('appserver', '')
      if len(inapp) > 0:
         if lock and len(self.apserver):
            logger.warning("Parameter 'appserver' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.appserver = inapp

      inencoding = kwargs.get('encoding', 'NoOverride')
      if inencoding != 'NoOverride':
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
            msg  = "The encoding provided ("+self.encoding+") doesn't exist in this Python session. Setting it to ''.\n"
            msg += "The correct encoding will attempt to be determined based upon the SAS session encoding."
            logger.warning(msg)
            self.encoding = ''

      injparms = kwargs.get('javaparms', '')
      if len(injparms) > 0:
         if lock:
            logger.warning("Parameter 'javaparms' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.javaparms = injparms

      inlrecl = kwargs.get('lrecl', None)
      if inlrecl:
         if lock and self.lrecl:
            logger.warning("Parameter 'lrecl' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.lrecl = inlrecl
      if not self.lrecl:
         self.lrecl = 1048576

      inrecon = kwargs.get('reconnect', None)
      if inrecon:
         if lock and self.reconnect:
            logger.warning("Parameter 'reconnect' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.reconnect = bool(inrecon)

      inruri = kwargs.get('reconuri', None)
      if inruri is not None:
         if lock and self.reconuri:
            logger.warning("Parameter 'reconuri' passed to SAS_session was ignored due to configuration restriction.")
         else:
            self.reconuri = inruri

      inlogsz = kwargs.get('logbufsz', None)
      if inlogsz:
         if inlogsz < 32:
            self.logbufsz = 32
         else:
            self.logbufsz = inlogsz

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
      self._log_cnt = 0
      self._log     = ""
      self._tomods1 = b"_tomods1"
      self.sascfg   = SASconfigIOM(self, **kwargs)

      self._startsas()
      self._sb.reconuri = None

   def __del__(self):
      if self.pid:
         self._endsas()
      self._sb.SASpid = None
      return

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
         self.sockin.bind(("127.0.0.1",port))
         #self.sockin.bind(("",32701))

         self.sockout = socks.socket()
         self.sockout.bind(("127.0.0.1",port))
         #self.sockout.bind(("",32702))

         self.sockerr = socks.socket()
         self.sockerr.bind(("127.0.0.1",port))
         #self.sockerr.bind(("",32703))
      except OSError:
         logger.fatal('Error try to open a socket in the _startsas method. Call failed.')
         return None
      self.sockin.listen(1)
      self.sockout.listen(1)
      self.sockerr.listen(1)

      if not zero:
         if self.sascfg.output.lower() == 'html':
            logger.warning("""HTML4 is only valid in 'local' mode (SAS_output_options in sascfg_personal.py).
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
                        user = line.partition(' user')[2].lstrip().partition(' ')[0].partition('\n')[0]
                        pw   = line.partition(' password')[2].lstrip().partition(' ')[0].partition('\n')[0]
                        found = True
                  fid.close()
               except OSError as e:
                  logger.warning('Error trying to read authinfo file:'+pwf+'\n'+str(e))
                  pass
               except:
                  pass

               if not found:
                  logger.warning('Did not find key '+self.sascfg.authkey+' in authinfo file:'+pwf+'\n')

            while len(user) == 0:
               user = self.sascfg._prompt("Please enter the OMR user id: ")
               if user is None:
                  self.sockin.close()
                  self.sockout.close()
                  self.sockerr.close()
                  self.pid = None
                  raise RuntimeError("No SAS OMR User id provided.")

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
      if self.sascfg.logbufsz is not None:
         parms += ["-logbufsz", str(self.sascfg.logbufsz)]
      if self.sascfg.reconuri is not None:
         parms += ["-uri", self.sascfg.reconuri]
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
            msg  = "The OS Error was:\n"+e.strerror+'\n'
            msg += "SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n"
            msg += "Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n"
            msg += "If no OS Error above, try running the following command (where saspy is running) manually to see what is wrong:\n"+s+"\n"
            logger.fatal(msg)
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
               msg  = "The OS Error was:\n"+e.strerror+'\n'
               msg += "SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n"
               msg += "Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n"
               msg += "If no OS Error above, try running the following command (where saspy is running) manually to see what is wrong:\n"+s+"\n"
               logger.fatal(msg)
               os._exit(-6)

      if os.name == 'nt':
         try:
            self.pid.wait(1)

            error  = self.pid.stderr.read(4096).decode()+'\n'
            error += self.pid.stdout.read(4096).decode()
            logger.fatal("Java Error:\n"+error)

            msg  = "Subprocess failed to start. Double check your settings in sascfg_personal.py file.\n"
            msg += "Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n"
            msg += "If no Java Error above, try running the following command (where saspy is running) manually to see if it's a problem starting Java:\n"+s+"\n"
            logger.fatal(msg)
            self.pid = None
            return None
         except:
            pass
      else:

         self.pid     = pidpty[0]
         self.stdinp  = os.fdopen(pin[PIPE_WRITE], mode='wb')
         self.stdoutp = os.fdopen(pout[PIPE_READ], mode='rb')
         self.stderrp = os.fdopen(perr[PIPE_READ], mode='rb')

         fcntl.fcntl(self.stdoutp, fcntl.F_SETFL, os.O_NONBLOCK)
         fcntl.fcntl(self.stderrp, fcntl.F_SETFL, os.O_NONBLOCK)

         sleep(1)
         rc = os.waitpid(self.pid, os.WNOHANG)
         if rc[0] == 0:
            pass
         else:
            error  = self.stderrp.read1(4096).decode()+'\n'
            error += self.stdoutp.read1(4096).decode()
            logger.fatal("Java Error:\n"+error)
            msg  = "SAS Connection failed. No connection established. Staus="+str(rc)+"  Double check your settings in sascfg_personal.py file.\n"
            msg += "Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n"
            msg += "If no Java Error above, try running the following command (where saspy is running) manually to see if it's a problem starting Java:\n"+s+"\n"
            logger.fatal(msg)
            self.pid = None
            return None

      self.stdin  = self.sockin.accept()
      self.stdout = self.sockout.accept()
      self.stderr = self.sockerr.accept()
      self.stdout[0].setblocking(False)
      self.stderr[0].setblocking(False)

      if not zero and not self.sascfg.reconuri:
         if not self.sascfg.sspi:
            while len(pw) == 0:
               pw = self.sascfg._prompt("Please enter the password for OMR user "+self.sascfg.omruser+": ", pw=True)
               if pw is None:
                  if os.name == 'nt':
                     self.pid.kill()
                  else:
                     os.kill(self.pid, signal.SIGKILL)
                  self.pid = None
                  raise RuntimeError("No SAS OMR User password provided.")
            pw += '\n'
            self.stdin[0].send(pw.encode())

      enc = self.sascfg.encoding #validating encoding is done next, so handle it not being set for this one call
      if enc == '':
         self.sascfg.encoding = 'utf-8'
      ll = self.submit("options svgtitle='svgtitle'; options validvarname=any validmemname=extend pagesize=max nosyntaxcheck; ods graphics on;", "text")
      self.sascfg.encoding = enc

      if self.pid is None:
         logger.fatal(ll['LOG'])
         logger.fatal("SAS Connection failed. No connection established. Double check your settings in sascfg_personal.py file.\n")
         logger.fatal("Attempted to run program "+pgm+" with the following parameters:"+str(parms)+"\n")
         if zero:
            logger.fatal("Be sure the path to sspiauth.dll is in your System PATH"+"\n")
         return None

      if self.sascfg.verbose:
         logger.info("SAS Connection established. Subprocess id is "+str(pid)+"\n")
      return self.pid

   def _endsas(self):
      rc = 0
      if self.pid:
         if os.name == 'nt':
            pid = self.pid.pid
         else:
            pid = self.pid

         try: # More Mac OS Python issues that don't work like everywhere else
            self.stdin[0].send(b'\ntom says EOL=ENDSAS                          \n')
            if os.name == 'nt':
               self._javalog  = self.pid.stderr.read(4096).decode()+'\n'
               self._javalog += self.pid.stdout.read(4096).decode()
               self.pid.stdin.close()
               self.pid.stdout.close()
               self.pid.stderr.close()
               try:
                  rc = self.pid.wait(5)
                  self.pid = None
               except (subprocess.TimeoutExpired):
                  if self.sascfg.verbose:
                     logger.info("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
                  self.pid.kill()
            else:
               self._javalog  = self.stderrp.read1(4096).decode()+'\n'
               self._javalog += self.stdoutp.read1(4096).decode()
               self.stdinp.close()
               self.stdoutp.close()
               self.stderrp.close()
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
                     logger.info("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
                  os.kill(self.pid, signal.SIGKILL)
         except:
            pass

         try: # Mac OS Python has bugs with this call
            self.stdin[0].shutdown(socks.SHUT_RDWR)
         except:
            pass
         self.stdin[0].close()
         self.sockin.close()

         try: # Mac OS Python has bugs with this call
            self.stdout[0].shutdown(socks.SHUT_RDWR)
         except:
            pass
         self.stdout[0].close()
         self.sockout.close()

         try: # Mac OS Python has bugs with this call
            self.stderr[0].shutdown(socks.SHUT_RDWR)
         except:
            pass
         self.stderr[0].close()
         self.sockerr.close()

         if self.sascfg.verbose:
            logger.info("SAS Connection terminated. Subprocess id was "+str(pid))
         self.pid        = None
         self._sb.SASpid = None
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
         logger.error("No SAS process attached. SAS process has terminated unexpectedly.")
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

      if ods:
         pgm += odsopen

      pgm += mj+b'\n'+pcodei.encode()+pcodeiv.encode()
      pgm += code.encode()+b'\n'+pcodeo.encode()+b'\n'+mj+b'\n'

      if ods:
         pgm += odsclose

      if printto:
         self.stdin[0].send(b'\ntom says EOL=PRINTTO                         \n')
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
                    lstf += lst
                 else:
                    sleep(0.1)
                    try:
                       log = self.stderr[0].recv(4096)
                    except (BlockingIOError):
                       log = b''

                    if len(log) > 0:
                       logf += log
                       if logf.count(logcodeo) >= 1:
                          bail = True
                       if not bail and bc:
                          #self.stdin[0].send(odsclose+logcodei.encode()+b'tom says EOL='+logcodeo+b'\n')
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

             #self.stdin[0].send(odsclose+logcodei.encode()+b'tom says EOL='+logcodeo+b'\n')

      try:
         lstf = lstf.decode()
      except UnicodeDecodeError:
         try:
            lstf = lstf.decode(self.sascfg.encoding)
         except UnicodeDecodeError:
            lstf = lstf.decode(errors='replace')

      logf = logf.decode(errors='replace').replace(chr(12), chr(10))

      trip = lstf.rpartition("/*]]>*/")
      if len(trip[1]) > 0 and len(trip[2]) < 200:
         lstf = ''

      self._log += logf
      final = logf.partition(logcodei)
      z = final[0].rpartition(chr(10))
      prev = '%08d' %  (self._log_cnt - 1)
      zz = z[0].rpartition("\nE3969440A681A24088859985" + prev +'\n')
      logd = zz[2].replace(mj.decode(), '').replace(chr(12), chr(10))

      lstd = lstf.replace(chr(12), chr(10)).replace('<body class="c body">',
                                                    '<body class="l body">').replace("font-size: x-small;",
                                                                                     "font-size:  normal;")
      if logd.count('\nERROR:') > 0:
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

      if not self.sascfg.reconnect:
         return "Disconnecting and then reconnecting to this workspaceserver has been disabled. Did not disconnect"

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

      res = log.rpartition("DISCONNECT")
      self._sb.reconuri = res[2].rstrip("END_DISCON")

      return res[0]

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

      code += "'"+table.strip().replace("'", "''")+"'n "+self._sb._dsopts(dsopts)+" outfile=x dbms=csv replace; "
      code += self._sb._expopts(opts)+" run\n;"
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
         if _infile_ = '' then delete;
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
         ll = self._asubmit(buf2, 'text')
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

      try:
         fd = open(localfile, 'rb')
      except OSError as e:
         return {'Success' : False,
                 'LOG'     : "File "+str(localfile)+" could not be opened. Error was: "+str(e)}

      fsize = os.path.getsize(localfile)

      if fsize > 0:
         code = "filename _sp_updn '"+remf+"' recfm=N permission='"+permission+"';"
         ll = self.submit(code, 'text')
         log1 = ll['LOG']

         self.stdin[0].send(str(fsize).encode()+b'tom says EOL=UPLOAD                          \n')

         while True:
            buf  = fd.read1(32768)
            sent = 0
            send = len(buf)
            blen = send
            if blen == 0:
               break
            while send:
               try:
                  sent = 0
                  sent = self.stdout[0].send(buf[blen-send:blen])
               except (BlockingIOError):
                  pass
               send -= sent

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

      ll2 = self.submit(code, 'text')
      fd.close()

      return {'Success' : True,
              'LOG'     : log1+ll2['LOG']}

   def download(self, localfile: str, remotefile: str, overwrite: bool = True, **kwargs):
      """
      This method downloads a remote file from the SAS servers file system.
      localfile  - path to the local file to create or overwrite
      remotefile - path to remote file tp dpwnload
      overwrite  - overwrite the output file if it exists?
      """
      logf     = b''
      logn     = self._logcnt()
      logcodei = "%put E3969440A681A24088859985" + logn + ";"
      logcodeo = "\nE3969440A681A24088859985" + logn
      logcodeb = logcodeo.encode()

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

      self.stdin[0].send(b'tom says EOL=DNLOAD                          \n')
      self.stdin[0].send(b'\ntom says EOL='+logcodeb+b'\n')
      #self.stdin[0].send(b'\n'+logcodei.encode()+b'\n'+b'tom says EOL='+logcodeb+b'\n')

      done  = False
      datar = b''
      bail  = False

      while not done:
         while True:
             if os.name == 'nt':
                try:
                   rc = self.pid.wait(0)
                   self.pid = None
                   self._sb.SASpid = None
                   return {'Success' : False,
                           'LOG'     : "SAS process has terminated unexpectedly. RC from wait was: "+str(rc)}
                except:
                   pass
             else:
                rc = os.waitpid(self.pid, os.WNOHANG)
                if rc[1]:
                    self.pid = None
                    self._sb.SASpid = None
                    return {'Success' : False,
                            'LOG'     : "SAS process has terminated unexpectedly. RC from wait was: "+str(rc)}

             if bail:
                if datar.count(logcodeb) >= 1:
                   break
             try:
                data = self.stdout[0].recv(4096)
             except (BlockingIOError):
                data = b''

             if len(data) > 0:
                datar += data
                if len(datar) > 8300:
                   fd.write(datar[:8192])
                   datar = datar[8192:]
             else:
                sleep(0.1)
                try:
                   log = self.stderr[0].recv(4096)
                except (BlockingIOError):
                   log = b''

                if len(log) > 0:
                   logf += log
                   if logf.count(logcodeb) >= 1:
                      bail = True
         done = True

      fd.write(datar.rpartition(logcodeb)[0])
      fd.flush()
      fd.close()

      logf = logf.decode(errors='replace')
      self._log += logf
      final = logf.partition(logcodei)
      z = final[0].rpartition(chr(10))
      prev = '%08d' %  (self._log_cnt - 1)
      zz = z[0].rpartition("\nE3969440A681A24088859985" + prev +'\n')
      logd = ll['LOG'] + zz[2].replace(";*\';*\";*/;", '')

      ll = self.submit("filename _sp_updn;", 'text')
      logd += ll['LOG']

      return {'Success' : True,
              'LOG'     : logd}

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
      encode_errors - 'fail' or 'replace' - default is to 'fail', other choice is to 'replace' invalid chars with the replacement char \
                      'ignore' will not  transcode n Python, so you get whatever happens with your data and SAS
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
               nl     = "'"+'%02x' % ord('\n'.encode(self.sascfg.encoding))+"'x".upper() # for MVS support
               xlate += " '"+colname+"'n = translate('"+colname+"'n, "+nl+", "+lf+");\n"
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
      self._asubmit(code, "text")

      blksz = int(kwargs.get('blocksize', 32767))
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
               if var == 'nan' or len(var) == 0:
                  var = ' '+colsep
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
                        ll = self.submit("quit;", 'text')
                        logger.error("Transcoding error encountered. Data transfer stopped on or before row "+str(row_num))
                        logger.error("DataFrame contains characters that can't be transcoded into the SAS session encoding.\n"+str(e))
                        return row_num
               else:
                 code = code.encode(self.sascfg.encoding, errors='replace').decode(self.sascfg.encoding)

            self._asubmit(code, "text")
            code = ""

      if not noencode:
         if encode_errors == 'fail':
            if CnotB:
               try:
                  chk = code.encode(self.sascfg.encoding)
               except Exception as e:
                  self._asubmit(";;;;\n;;;;", "text")
                  ll = self.submit("quit;", 'text')
                  logger.error("Transcoding error encountered. Data transfer stopped on or before row "+str(row_num))
                  logger.error("DataFrame contains characters that can't be transcoded into the SAS session encoding.\n"+str(e))
                  return  row_num
         else:
            code = code.encode(self.sascfg.encoding, errors='replace').decode(self.sascfg.encoding)

      self._asubmit(code, "text")
      self._asubmit(";;;;\n;;;;", "text")
      ll = self.submit("quit;", 'text')
      if ("We failed in Submit" in ll['LOG']):
         logger.error("Failure in the IOM client code, likely a transcoding error encountered. Data transfer stopped on or before row "+str(row_num))
         logger.error("Rendering the error from the Java layer:\n\n"+ll['LOG'].partition("END We failed in Submit\n")[0])
      return None

   def sasdata2dataframe(self, table: str, libref: str ='', dsopts: dict = None,
                         rowsep: str = '\x01', colsep: str = '\x02',
                         rowrep: str = ' ',    colrep: str = ' ',
                         **kwargs) -> '<Pandas Data Frame object>':
      """
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table   - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref  - the libref for the SAS Data Set.
      rowsep  - the row seperator character to use; defaults to '\x01'
      colsep  - the column seperator character to use; defaults to '\x02'
      rowrep  - the char to convert to for any embedded rowsep chars, defaults to  ' '
      colrep  - the char to convert to for any embedded colsep chars, defaults to  ' '
      """
      dsopts = dsopts if dsopts is not None else {}

      method = kwargs.pop('method', None)
      if   method and method.lower() == 'csv':
         return self.sasdata2dataframeCSV(table, libref, dsopts, **kwargs)
      #elif method and method.lower() == 'disk':
      else:
         return self.sasdata2dataframeDISK(table, libref, dsopts, rowsep, colsep,
                                           rowrep, colrep, **kwargs)


   def sasdata2dataframeCSV(self, table: str, libref: str ='', dsopts: dict = None, opts: dict = None,
                            tempfile: str=None, tempkeep: bool=False, **kwargs) -> '<Pandas Data Frame object>':
      """
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      table    - the name of the SAS Data Set you want to export to a Pandas Data Frame
      libref   - the libref for the SAS Data Set.
      dsopts   - data set options for the input SAS Data Set
      opts     - a dictionary containing any of the following Proc Export options(delimiter, putnames)
      tempfile - file to use to store CSV, else temporary file will be used.
      tempkeep - if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it \
                 tempkeep and tempfile are only use with Local connections as of V3.7.0

      These two options are for advanced usage. They override how saspy imports data. For more info
      see https://sassoftware.github.io/saspy/advanced-topics.html#advanced-sd2df-and-df2sd-techniques

      dtype   - this is the parameter to Pandas read_csv, overriding what saspy generates and uses
      my_fmts - bool: if True, overrides the formats saspy would use, using those on the data set or in dsopts=
      """
      dsopts = dsopts if dsopts is not None else {}
      opts   = opts   if   opts is not None else {}

      logf     = b''
      lstf     = b''
      logn     = self._logcnt()
      logcodei = "%put E3969440A681A24088859985" + logn + ";"
      lstcodeo =   "E3969440A681A24088859985" + logn
      logcodeo = "\nE3969440A681A24088859985" + logn
      logcodeb = logcodeo.encode()

      if libref:
         tabname = libref+".'"+table.strip().replace("'", "''")+"'n "
      else:
         tabname = "'"+table.strip().replace("'", "''")+"'n "

      code  = "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";run;\n"
      code += "data _null_; file LOG; d = open('work.sasdata2dataframe');\n"
      code += "length var $256;\n"
      code += "lrecl = attrn(d, 'LRECL'); nvars = attrn(d, 'NVARS');\n"
      code += "lr='LRECL='; vn='VARNUMS='; vl='VARLIST='; vt='VARTYPE=';\n"
      code += "put lr lrecl; put vn nvars; put vl;\n"
      code += "do i = 1 to nvars; var = compress(varname(d, i), '00'x); put var; end;\n"
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

      code = "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";\nformat "

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

      if self.sascfg.iomhost.lower() in ('', 'localhost', '127.0.0.1'):
         tmpdir  = None

         if tempfile is None:
            tmpdir = tf.TemporaryDirectory()
            tmpcsv = tmpdir.name+os.sep+"tomodsx"
         else:
            tmpcsv  = tempfile

         local   = True
         outname = "_tomodsx"
         code    = "filename _tomodsx '"+tmpcsv+"' lrecl="+str(self.sascfg.lrecl)+" recfm=v  encoding='utf-8';\n"
      else:
         local   = False
         outname = self._tomods1.decode()
         code    = ''

      code += "proc export data=work.sasdata2dataframe outfile="+outname+" dbms=csv replace;\n"
      code += self._sb._expopts(opts)+" run;\n"
      code += "proc delete data=work.sasdata2dataframe(memtype=view);run;\n"

      ll = self._asubmit(code, 'text')

      self.stdin[0].send(b'\ntom says EOL='+logcodeo.encode())
      #self.stdin[0].send(b'\n'+logcodei.encode()+b'\n'+b'tom says EOL='+logcodeo.encode())

      done  = False
      bail  = False

      if not local:
         try:
            sockout = _read_sock(io=self, rowsep=b'\n', encoding=self.sascfg.encoding,
                                 lstcodeo=lstcodeo.encode(), logcodeb=logcodeb)

            df = pd.read_csv(sockout, index_col=idx_col, encoding='utf8', engine=eng, dtype=dts, **kwargs)
         except:
            if os.name == 'nt':
               try:
                  rc = self.pid.wait(0)
                  self.pid = None
                  self._sb.SASpid = None
                  logger.fatal('\nSAS process has terminated unexpectedly. RC from wait was: '+str(rc))
                  return None
               except:
                  pass
            else:
               rc = os.waitpid(self.pid, os.WNOHANG)
               if rc[1]:
                   self.pid = None
                   self._sb.SASpid = None
                   logger.fatal('\nSAS process has terminated unexpectedly. RC from wait was: '+str(rc))
                   return None
            raise
      else:
         while True:
            try:
               lst = self.stdout[0].recv(4096)
            except (BlockingIOError):
               lst = b''

            if len(lst) > 0:
               lstf += lst
               if lstf.count(lstcodeo.encode()) >= 1:
                  done = True;

            try:
               log = self.stderr[0].recv(4096)
            except (BlockingIOError):
               sleep(0.1)
               log = b''

            if len(log) > 0:
               logf += log
               if logf.count(logcodeb) >= 1:
                  bail = True;

            if done and bail:
               break

         df = pd.read_csv(tmpcsv, index_col=idx_col, engine=eng, dtype=dts, **kwargs)

         logd = logf.decode(errors='replace')
         self._log += logd.replace(chr(12), chr(10))
         if logd.count('\nERROR:') > 0:
            warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
            self._sb.check_error_log = True

         if tmpdir:
            tmpdir.cleanup()
         else:
            if not tempkeep:
               os.remove(tmpcsv)

      if k_dts is None:  # don't override these if user provided their own dtypes
         for i in range(nvars):
            if vartype[i] == 'N':
               if varcat[i] in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  df[dvarlist[i]] = pd.to_datetime(df[dvarlist[i]], errors='coerce')

      return df

   def sasdata2dataframeDISK(self, table: str, libref: str ='', dsopts: dict = None,
                             rowsep: str = '\x01', colsep: str = '\x02',
                             rowrep: str = ' ',    colrep: str = ' ', tempfile: str=None,
                             tempkeep: bool=False, **kwargs) -> '<Pandas Data Frame object>':
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

      These two options are for advanced usage. They override how saspy imports data. For more info
      see https://sassoftware.github.io/saspy/advanced-topics.html#advanced-sd2df-and-df2sd-techniques

      dtype   - this is the parameter to Pandas read_csv, overriding what saspy generates and uses
      my_fmts - bool: if True, overrides the formats saspy would use, using those on the data set or in dsopts=
      """
      tmp = kwargs.pop('tempfile', None)
      tmp = kwargs.pop('tempkeep', None)

      dsopts = dsopts if dsopts is not None else {}

      logf     = b''
      lstf     = b''
      logn     = self._logcnt()
      logcodei = "%put E3969440A681A24088859985" + logn + ";"
      lstcodeo =   "E3969440A681A24088859985" + logn
      logcodeo = "\nE3969440A681A24088859985" + logn
      logcodeb = logcodeo.encode()

      if libref:
         tabname = libref+".'"+table.strip().replace("'", "''")+"'n "
      else:
         tabname = "'"+table.strip().replace("'", "''")+"'n "

      code  = "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+tabname+self._sb._dsopts(dsopts)+";run;\n"
      code += "data _null_; file LOG; d = open('work.sasdata2dataframe');\n"
      code += "length var $256;\n"
      code += "lrecl = attrn(d, 'LRECL'); nvars = attrn(d, 'NVARS');\n"
      code += "lr='LRECL='; vn='VARNUMS='; vl='VARLIST='; vt='VARTYPE=';\n"
      code += "put lr lrecl; put vn nvars; put vl;\n"
      code += "do i = 1 to nvars; var = compress(varname(d, i), '00'x); put var; end;\n"
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

      code = "data _null_; set "+tabname+self._sb._dsopts(dsopts)+";\n"

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

      lreclx = max(self.sascfg.lrecl, (lrecl + nvars + 1))

      miss  = {}
      code += "\nfile "+self._tomods1.decode()+" lrecl="+str(lreclx)+" dlm="+cdelim+" recfm=v termstr=NL encoding='utf-8';\n"
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

      ll = self._asubmit(code, "text")
      self.stdin[0].send(b'\ntom says EOL='+logcodeb)
      #self.stdin[0].send(b'\n'+logcodei.encode()+b'\n'+b'tom says EOL='+logcodeb)

      try:
         sockout = _read_sock(io=self, method='DISK', rsep=(colsep+rowsep+'\n').encode(), rowsep=rowsep.encode(),
                              lstcodeo=lstcodeo.encode(), logcodeb=logcodeb)

         df = pd.read_csv(sockout, index_col=idx_col, engine=eng, header=None, names=dvarlist,
                          sep=colsep, lineterminator=rowsep, dtype=dts, na_values=miss,
                          encoding='utf-8', quoting=quoting, **kwargs)
      except:
         if os.name == 'nt':
            try:
               rc = self.pid.wait(0)
               self.pid = None
               self._sb.SASpid = None
               logger.fatal('\nSAS process has terminated unexpectedly. RC from wait was: '+str(rc))
               return None
            except:
               pass
         else:
            rc = os.waitpid(self.pid, os.WNOHANG)
            if rc[1]:
                self.pid = None
                self._sb.SASpid = None
                logger.fatal('\nSAS process has terminated unexpectedly. RC from wait was: '+str(rc))
                return None
         raise

      if k_dts is None:  # don't override these if user provided their own dtypes
         for i in range(nvars):
            if vartype[i] == 'N':
               if varcat[i] in self._sb.sas_date_fmts + self._sb.sas_time_fmts + self._sb.sas_datetime_fmts:
                  df[dvarlist[i]] = pd.to_datetime(df[dvarlist[i]], errors='coerce')

      return df

class _read_sock(io.StringIO):
   def __init__(self, **kwargs):
      self._io      = kwargs.get('io')
      self.method   = kwargs.get('method', 'CSV')
      self.rowsep   = kwargs.get('rowsep')
      self.rsep     = kwargs.get('rsep', self.rowsep)
      self.lstcodeo = kwargs.get('lstcodeo')
      self.logcodeb = kwargs.get('logcodeb')
      self.enc      = kwargs.get('encoding', None)
      self.datar    = b""
      self.logf     = b""
      self.doneLST  = False
      self.doneLOG  = False

   def read(self, size=4096):
      datl    = 0
      size    = max(size, 4096)
      notarow = True

      while datl < size or notarow:
         try:
            data = self._io.stdout[0].recv(4096)
         except (BlockingIOError):
            data = b''
         dl = len(data)

         if dl:
            datl       += dl
            self.datar += data
            if notarow:
               notarow = self.datar.count(self.rsep) <= 0

            if self.datar.count(self.lstcodeo) >= 1:
               self.doneLST = True
               self.datar   = self.datar.rpartition(self.logcodeb)[0]
         else:
            if self.doneLST and self.doneLOG:
               if len(self.datar) <= 0:
                  return ''
               else:
                  break
            try:
               log = self._io.stderr[0].recv(4096)
            except (BlockingIOError):
               log = b''

            if len(log) > 0:
               self.logf += log
               if self.logf.count(self.logcodeb) >= 1:
                  self.doneLOG = True

                  logd = self.logf.decode(errors='replace')
                  self._io._log += logd.replace(chr(12), chr(10))
                  if logd.count('\nERROR:') > 0:
                     warnings.warn("Noticed 'ERROR:' in LOG, you ought to take a look and see if there was a problem")
                     self._io._sb.check_error_log = True


      data        = self.datar.rpartition(self.rsep)
      if self.method == 'DISK':
         datap    = (data[0]+data[1]).replace(self.rsep, self.rowsep)
      else:
         datap    = data[0]+data[1]
      self.datar  = data[2]

      if self.enc is None:
         return datap.decode()
      else:
         return datap.decode(self._io.sascfg.encoding)

