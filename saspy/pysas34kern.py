from multiprocessing import Process
from time import sleep
import subprocess, fcntl, os, signal
import os

class sasprocess():
   
   def __init__(self):
      self.pid    = None
      self.stdin  = None
      self.stderr = None
      self.stdout = None


class SAS_session:
   
   def __init__(self, path="/opt/sasinside/SASHome", version="9.4"):
      self.sasprocess   = sasprocess()
      self._log_cnt = 0
      self._log     = ""

   def __del__(self):
      if self.sasprocess.pid:
         self._endsas()
      self.sasprocess.pid = None

   def _logcnt(self):
       self._log_cnt += 1
       return '%08d' % self._log_cnt

   def _startsas(self, path="/opt/sasinside/SASHome", version='9.4'):
      if self.sasprocess.pid:
         return self.sasprocess.pid
      p  = path+"/SASFoundation/"+ version +"/sas"
      parms  = [path+"/SASFoundation/"+ version +"/sas"]
      parms += ["-set", "TKPATH", path+"/SASFoundation/"+ version +"/sasexe:"+path+"/SASFoundation/"+ version +"/utilities/bin"]
      parms += ["-set", "SASROOT", path+"/SASFoundation/"+ version]
      parms += ["-set", "SASHOME", path]
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

         os.execv(p, parms)

      self.sasprocess.pid    = pidpty[0]
      self.sasprocess.stdin  = os.fdopen(pin[PIPE_WRITE], mode='wb')
      self.sasprocess.stderr = os.fdopen(perr[PIPE_READ], mode='rb')
      self.sasprocess.stdout = os.fdopen(pout[PIPE_READ], mode='rb')

      fcntl.fcntl(self.sasprocess.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
      fcntl.fcntl(self.sasprocess.stderr, fcntl.F_SETFL, os.O_NONBLOCK)
      
      self.submit("options svgtitle='svgtitle'; options validvarname=any; ods graphics on;", "text")
        
      return self.sasprocess.pid


   def _endsas(self):
      rc = 0
      if self.sasprocess.pid:
         code = b";*\';*\";*/;\n;quit;endsas;\n"
         self._getlog(1)
         self.sasprocess.stdin.write(code)
         self.sasprocess.stdin.flush()
         sleep(1)
         try:
            rc = os.waitid(os.P_PID, self.sasprocess.pid, os.WEXITED | os.WNOHANG)
         except (subprocess.TimeoutExpired):
            print("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
            os.kill(self.sasprocess.pid, signal.SIGKILL)
         self.sasprocess.pid = None
      return rc

   def _getlog(self, wait=5):
      logf   = b''
      quit   = wait * 2

      while True:
         log = self.sasprocess.stderr.read1(4096)
         if len(log) > 0:
            logf += log
         else:
            quit -= 1
            if quit < 0 or len(logf) > 0:
               break
            sleep(0.5)
   
      x = logf.decode()
      self._log += x
      return x

   def _getlst(self, wait=5):
      lstf = b''
      quit = wait * 2
      eof = 0
      bof = False
      lenf = 0
   
      while True:
         lst = self.sasprocess.stdout.read1(4096)
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
   
      return lstf.decode()
   
   def submit(self, code):
      odsopen  = b"ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=png; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods html5 close;ods listing;\n"
      ods      = True;
      htm      = "html HTML"
      mj       = b";*\';*\";*/;\n"

      lstf = b''
      logf = b''
      quit = False
      eof = 5

      logn     = self._logcnt()
      logcode  = "%put tom was here"+logn+";"
      logcodeb = ("\ntom was here"+logn).encode()

      self.sasprocess.stdin.write(odsopen)
   
      out = self.sasprocess.stdin.write(mj+code.encode()+mj)
   
      self.sasprocess.stdin.write(odsclose)

      out = self.sasprocess.stdin.write(b'\n'+logcode.encode()+b'\n')

      self.sasprocess.stdin.flush()

      try:
         while True:
            if quit:
               eof -= 1
            if eof < 0:
               break
            lst = self.sasprocess.stdout.read1(4096)
            if len(lst) > 0:
               lstf += lst
            else:
               log = self.sasprocess.stderr.read1(4096)
               if len(log) > 0:
                  logf += log
                  if logf.count(logcodeb) >= 1:
                     quit = True

      except (KeyboardInterrupt, SystemExit):
         print('Exception caught!\n')
         logr = self._break((lstf+lst).decode())
         print('Exception handled :)\n')
         return dict(LOG=logr, LST='')

      final = logf.partition(logcode.encode())
      z = final[0].decode().rpartition(chr(10))

      logd = z[0]
      lstd = lstf.decode().replace(chr(12), chr(10))
 
      self._log += logf.decode()

      return dict(LOG=logd, LST=lstd)


if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(_getlog())
    print(_getlsttxt())

    endsas()

