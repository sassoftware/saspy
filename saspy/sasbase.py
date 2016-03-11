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
from time import sleep
import subprocess, fcntl, os, signal
import saspy.sascfg as sascfg

class SAS_config:
   
   def __init__(self, cfgname='', Kernel=None, saspath='', options=''):
      #import pdb; pdb.set_trace()

      self.configs  = []
      self._kernel  = Kernel
      self.saspath  = saspath
      self.options  = options

      # GET Config
      self.configs = getattr(sascfg, "SAS_config_names")

      if len(cfgname) == 0:
         if len(self.configs) == 0:
            print("No SAS Configuration names found in saspy.sascfg")
            return None
         else:
            if len(self.configs) == 1:
               cfgname = self.configs[0]
               if Kernel == None:
                  print("Using SAS Config named: "+cfgname)
            else:
               cfgname = self._prompt("Please enter the name of the SAS Config you wish to run. Available Configs are: "+str(self.configs)+" ")

      while cfgname not in self.configs:
         cfgname = self._prompt("The SAS Config name specified was not found. Please enter the SAS Config you wish to use. Available Configs are: "+str(self.configs)+" ")

      self.name        = cfgname
      cfg              = getattr(sascfg, cfgname) 
      if len(saspath) == 0:
         self.saspath  = cfg.get('saspath', '/opt/sasinside/SASHome/SASFoundation/9.4/sas')
      if len(options) == 0:
         self.options  = cfg.get('options', '')

   def _prompt(self, prompt, pw=False):
      if self._kernel == None:
         if pw == False:
            return input(prompt)
         else:
            return getpass.getpass(prompt)
      else:
         return self._kernel._input_request(prompt, self._kernel._parent_ident, self._kernel._parent_header, password = pw)

                   
class SAS_session:
   
   def __init__(self, cfgname='', Kernel=None, saspath='', options=''):
      self.pid    = None
      self.stdin  = None
      self.stderr = None
      self.stdout = None

      self.sascfg   = SAS_config(cfgname, Kernel, saspath, options)
      self._log_cnt = 0
      self._log     = ""

      self._startsas(self.sascfg)

   def __del__(self):
      if self.pid:
         self._endsas()
      self.pid = None

   def _logcnt(self, next=True):
       if next == True:
          self._log_cnt += 1
       return '%08d' % self._log_cnt

   def _startsas(self, sascfg):
      if self.pid:
         return self.pid

      pgm    = sascfg.saspath
      parms  = [pgm]
      parms += sascfg.options
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

         os.execv(pgm, parms)

      self.pid    = pidpty[0]
      self.stdin  = os.fdopen(pin[PIPE_WRITE], mode='wb')
      self.stderr = os.fdopen(perr[PIPE_READ], mode='rb')
      self.stdout = os.fdopen(pout[PIPE_READ], mode='rb')

      fcntl.fcntl(self.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
      fcntl.fcntl(self.stderr, fcntl.F_SETFL, os.O_NONBLOCK)
      
      self.submit("options svgtitle='svgtitle'; options validvarname=any; ods graphics on;", "text")
        
      return self.pid

   def _breakprompt(self, inlst=''):
      found = False
      lst = inlst

      interupt = signal.SIGINT
      os.kill(self.pid, interupt)
      sleep(.25)
      self.stdin.write(b'\n')
      self.stdin.flush()

      while True:
         if len(lst) >  0:
            lsts = lst.rpartition('Select:')
            if lsts[0] != '' and lsts[1] != '':
               found = True
               print('Processing interupt\nAttn handler Query is\n\n'+lsts[1]+lsts[2].rsplit('\n?')[0]+'\n')
               response = self.sascfg._prompt("Please enter your Response: ")
               self.stdin.write(response.encode()+b'\n')
               self.stdin.flush()
            else:
               lsts = lst.rpartition('Press')
               if lsts[0] != '' and lsts[1] != '':
                  print('Seconday Query is:\n\n'+lsts[1]+lsts[2].rsplit('\n?')[0]+'\n')
                  response = self.sascfg._prompt("Please enter your Response: ")
                  self.stdin.write(response.encode()+b'\n')
                  self.stdin.flush()
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

   def _endsas(self):
      rc = 0
      if self.pid:
         code = b";*\';*\";*/;\n;quit;endsas;\n"
         self.stderr.read1(4096)
         self.stdin.write(code)
         self.stdin.flush()
         sleep(1)
         try:
            rc = os.waitid(os.P_PID, self.pid, os.WEXITED | os.WNOHANG)
         except (subprocess.TimeoutExpired):
            print("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
            os.kill(self.pid, signal.SIGKILL)
         self.pid = None
      return rc

   def submit(self, code, results="html"):
      odsopen  = b"ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=png; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods html5 close;ods listing;\n"
      ods      = True;
      htm      = "html HTML"
      mj       = b";*\';*\";*/;"

      lstf = b''
      logf = b''
      quit = False
      eof = 5

      logn     = self._logcnt()
      logcodei = "%put E3969440A681A24088859985"+logn+";"
      logcodeo =    "\nE3969440A681A24088859985"+logn

      if (htm.find(results) < 0):
         ods = False
   
      if (ods):
         self.stdin.write(odsopen)
   
      out = self.stdin.write(mj+b'\n'+code.encode()+b'\n'+mj)
   
      if (ods):
         self.stdin.write(odsclose)

      out = self.stdin.write(b'\n'+logcodei.encode()+b'\n')

      self.stdin.flush()

      try:
         while True:
            if quit:
               eof -= 1
            if eof < 0:
               break
            lst = self.stdout.read1(4096)
            if len(lst) > 0:
               lstf += lst
            else:
               log = self.stderr.read1(4096)
               if len(log) > 0:
                  logf += log
                  if logf.count(logcodeo.encode()) >= 1:
                     quit = True

      except (KeyboardInterrupt, SystemExit):
         print('Exception caught!')
         logr = self._breakprompt((lstf+lst).decode())
         print('Exception handled :)\n')
         return dict(LOG=logr, LST='')


      final = logf.partition(logcodei.encode())
      z = final[0].decode().rpartition(chr(10))

      logd = z[0].replace(mj.decode(), '')
      lstd = lstf.decode().replace(chr(12), chr(10)).replace('<body class="c body">', '<body class="l body">').replace("font-size: x-small;", "font-size: normal;")
 
      self._log += logf.decode().replace(logcodei, " ").replace(logcodeo, " ")

      return dict(LOG=logd, LST=lstd)


if __name__ == "__main__":
    startsas()

    ll = submit(sys.argv[1], "text")

    print(ll['LOG'])
    print(ll['LST'])

    endsas()
