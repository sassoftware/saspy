from time import sleep
import subprocess, fcntl, os, signal

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

   def _break(self, inlst=''):
      found = False
      lst = inlst

      interupt = signal.SIGINT
      os.kill(self.sasprocess.pid, interupt)
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
            lst = self.sasprocess.stdout.read1(4096).decode()
         else:
            log = self.sasprocess.stderr.read1(4096).decode()
            self._log += log
 
            if log.count("\ntom was here"+('%08d' % self._log_cnt)) >= 1:
               print("******************Found end of step. No interupt processed")
               found = True

            if found:
               ll = self.submit('ods html5 close;ods listing close;ods listing;libname work list;\n','text')
               break

            sleep(.25)
            lst = self.sasprocess.stdout.read1(4096).decode()

      return log

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
   
   def _getlsttxt(self, wait=5):
      f2 = [None]
      lstf = b''
      quit = wait * 2
      eof = 0
      self._asubmit("data _null_;file print;put 'Tom was here';run;", "text")
   
      while True:
         lst = self.sasprocess.stdout.read1(4096)
         if len(lst) > 0:
            lstf += lst
   
            lenf = len(lstf)
            eof = lstf.find(b"Tom was here", lenf - 25, lenf)
      
            if (eof != -1):
               final = lstf.partition(b"Tom was here")
               f2 = final[0].decode().rpartition(chr(12))
               break

      lst = f2[0]
      return lst.replace(chr(12), '\n')

   def _asubmit(self, code, results="html"):
      odsopen  = b"ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=png; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods html5 close;ods listing;\n"
      ods      = True;
      htm      = "html HTML"
      if (htm.find(results) < 0):
         ods = False
   
      if (ods):
         self.sasprocess.stdin.write(odsopen)
   
      out = self.sasprocess.stdin.write(code.encode()+b'\n')
   
      if (ods):
         self.sasprocess.stdin.write(odsclose)

      self.sasprocess.stdin.flush()

      return out

   def submit(self, code, results="html"):
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


      if (htm.find(results) < 0):
         ods = False
   
      if (ods):
         self.sasprocess.stdin.write(odsopen)
   
      out = self.sasprocess.stdin.write(mj+code.encode()+mj)
   
      if (ods):
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
            #if lst != None:
               lstf += lst
               #print("=====================LST==============\n"+lst.decode()+"\n\n\n\n")
            else:
               log = self.sasprocess.stderr.read1(4096)
               if len(log) > 0:
               #if log != None:
                  logf += log
                  #print("=====================LOG==============\n"+log.decode()+"\n\n\n\n")
                  if logf.count(logcodeb) >= 1:
                     quit = True

      except (KeyboardInterrupt, SystemExit):
         print('Exception caught!\n')
         #print('Current lst='+((lstf+lst).decode())[0:100])
         #print('Current log='+logf.decode())
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
