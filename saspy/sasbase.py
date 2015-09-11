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
from multiprocessing import Process
from time import sleep
import subprocess, fcntl, os, signal
#from IPython.display import HTML
from saspy.sasstat import *
from saspy.sasets  import *
#import pty, termios


class sasprocess():
   
   def __init__(self):
      self.pid    = None
      self.stdin  = None
      self.stderr = None
      self.stdout = None


class SAS_session:
   
   def __init__(self, path="/opt/sasinside/SASHome"):
      #import pdb; pdb.set_trace()

      self.sasprocess   = sasprocess()
      self._obj_cnt = 0
      self._log_cnt = 0
      self._log     = ""
      self.nosub    = False
      #self._startsas(path)

   def __del__(self):
      #import pdb; pdb.set_trace()

      if self.sasprocess.pid:
         self._endsas()
      self.sasprocess.pid = None

   def _objcnt(self):
       self._obj_cnt += 1
       return '%04d' % self._obj_cnt

   def _logcnt(self):
       self._log_cnt += 1
       return '%08d' % self._log_cnt

   def _startsas_fork(self, path="/opt/sasinside/SASHome"):
      #import pdb; pdb.set_trace()
   
      if self.sasprocess.pid:
         return self.sasprocess.pid
   
      p      = path+"/SASFoundation/9.4/sas"
      parms  = [path+"/SASFoundation/9.4/sas"]
      parms += ["-set", "TKPATH", path+"/SASFoundation/9.4/sasexe:"+path+"/SASFoundation/9.4/utilities/bin"]
      parms += ["-set", "SASROOT", path+"/SASFoundation/9.4"]
      parms += ["-set", "SASHOME", path]
      parms += ["-pagesize", "MAX"]
      parms += ["-nodms"]
      parms += ["-stdio"]
      parms += ["-terminal"]
      parms += ["-nosyntaxcheck"]
      parms += ['']
   
      #parms  = [path+"/sas"]
      #parms += ["-set", "TKPATH", path+":"+path+"/utilities/bin"]
      #parms += ["-set", "SASROOT", path+""]
      #parms += ["-set", "SASHOME", path]
      #parms += ["-pagesize", "MAX"]
      #parms += ["-nodms"]
      #parms += ["-stdio"]
      #parms += ["-terminal"]
      #parms += ["-nosyntaxcheck"]
      
      PIPE_READ  = 0
      PIPE_WRITE = 1
      
      pin  = os.pipe() 
      pout = os.pipe()
      perr = os.pipe() 
      
      pidpty = os.forkpty()
      if pidpty[0]:
         # we are the parent
         #print("Parent. Child pid="+str(pidpty[0])+'. pty fd='+str(pidpty[1]))  

         pid = pidpty[0]
         os.close(pin[PIPE_READ])
         os.close(pout[PIPE_WRITE]) 
         os.close(perr[PIPE_WRITE]) 

      else:
         # we are the child

         #for i in range(1,signal.NSIG):
         #   print('SIG'+str(i)+'='+str(signal.getsignal(i)))
         #   #signal.signal(i, signal.SIG_DFL)

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
         #sys.exit(0)

      #sleep(5)
      self.sasprocess.pid    = pidpty[0]
      self.sasprocess.stdin  = os.fdopen(pin[PIPE_WRITE], mode='wb')
      self.sasprocess.stderr = os.fdopen(perr[PIPE_READ], mode='rb')
      self.sasprocess.stdout = os.fdopen(pout[PIPE_READ], mode='rb')

      fcntl.fcntl(self.sasprocess.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
      fcntl.fcntl(self.sasprocess.stderr, fcntl.F_SETFL, os.O_NONBLOCK)
     
      self.submit("options svgtitle='svgtitle'; options validvarname=any; ods graphics on;", "text")
        
      return self.sasprocess.pid

   def _startsas(self, path="/opt/sasinside/SASHome"):
      #import pdb; pdb.set_trace()

      return self._startsas_fork(path)

      if self.sasprocess.pid:
         return self.sasprocess.pid
   
      parms  = [path+"/SASFoundation/9.4/sas"]
      parms += ["-set", "TKPATH", path+"/SASFoundation/9.4/sasexe:"+path+"/SASFoundation/9.4/utilities/bin"]
      parms += ["-set", "SASROOT", path+"/SASFoundation/9.4"]
      parms += ["-set", "SASHOME", path]
      parms += ["-pagesize", "MAX"]
      parms += ["-nodms"]
      parms += ["-stdio"]
      #parms += ["-SYSIN", "__STDIN__"]
      #parms += ["-PRINT", "__STDOUT__"]
      #parms += ["-LOG",   "__STDERR__"]
      parms += ["-terminal"]
      parms += ["-nosyntaxcheck"]
   
      #parms  = [path+"/sas"]
      #parms += ["-set", "TKPATH", path+":"+path+"/utilities/bin"]
      #parms += ["-set", "SASROOT", path+""]
      #parms += ["-set", "SASHOME", path]
      #parms += ["-pagesize", "MAX"]
      #parms += ["-nodms"]
      #parms += ["-stdio"]
      #parms += ["-terminal"]
      #parms += ["-nosyntaxcheck"]
      
      self.popenstruct = subprocess.Popen(parms, start_new_session=False, preexec_fn=self._pty(), restore_signals=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

      #parms  = '/opt/sasinside/SASHome/sas -set TKPATH /opt/sasinside/SASHome/sasexe:/opt/sasinside/SASHome/utilities/bin '
      #parms += ' -set SASROOT /opt/sasinside/SASHome -set SASHOME /opt/sasinside/SASHome -pagesize MAX - SYSIN __STDIN__ -PRINT __STDOUT__ -LOG __STDERR__ -nodms -terminal -nosyntaxcheck '
      #parms  = '/sasgen/dev/mva-v940m3/SAS/laxnd/sas -verify_paths -set SASROOT /sasgen/dev/mva-v940m3/SAS/laxnd -config /sasgen/dev/mva-v940m3/SAS/laxnd/sasv9.cfg '
      #parms += ' -config /sasgen/dev/mva-v940m3/SAS/laxnd/nls/en/sasv9.cfg -helphost d72275.na.sas.com'
      #popenstruct = subprocess.Popen(parms,  shell=False, start_new_session=False, restore_signals=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

      self.sasprocess.pid    = popenstruct.pid   
      self.sasprocess.stdin  = popenstruct.stdin 
      self.sasprocess.stderr = popenstruct.stderr
      self.sasprocess.stdout = popenstruct.stdout

      fcntl.fcntl(self.sasprocess.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
      fcntl.fcntl(self.sasprocess.stderr, fcntl.F_SETFL, os.O_NONBLOCK)
     
      self.submit("options svgtitle='svgtitle'; options validvarname=any; options pagesize=max; ods graphics on;", "text")
        
      return self.sasprocess.pid
   
   def _break(self, inlst=''):
      #import pdb; pdb.set_trace()
      found = False
      lst = inlst

      interupt = signal.SIGINT
      #print('new session True, restore signals True  -   Signaling pid='+str(self.sasprocess.pid)+' with signal='+str(interupt))
      #self.popenstruct.send_signal(signal.SIGINT)
      os.kill(self.sasprocess.pid, interupt)
      sleep(.25)
      self._asubmit('','text')
      #print('1st estae lst='+lst[0:50]+'...'+lst[len(lst)-50:len(lst)])

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
            #print('Post-Sel/Press estae lst='+lst)
         else:
            log = self.sasprocess.stderr.read1(4096).decode()
            self._log += log
 
            if log.count("\ntom was here"+('%08d' % self._log_cnt)) >= 1:
               print("******************Found end of step. No interupt processed")
               found = True

            #print("no lst log ="+log)
            if found:
               ll = self.submit('ods html5 close;ods listing close;ods listing;libname work list;\n','text')
               #print(ll['LST'])
               #print(ll['LOG'])
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
            #rc = self.popenstruct.wait(5)
            rc = os.waitid(os.P_PID, self.sasprocess.pid, os.WEXITED | os.WNOHANG)
         except (subprocess.TimeoutExpired):
            print("SAS didn't shutdown w/in 5 seconds; killing it to be sure")
            os.kill(self.sasprocess.pid, signal.SIGKILL)
         self.sasprocess.pid = None
      return rc


   def _getlog(self, wait=5):
      #import pdb; pdb.set_trace()
   
      logf   = b''
      quit   = wait * 2
      #logn   = self._logcnt()
      #code   = "%put tom was here"+logn+";"
      #codeb  = ("\ntom was here"+logn).encode()

      #self._asubmit(code, "text")
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
      #import pdb; pdb.set_trace()
   
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
      #import pdb; pdb.set_trace()
   
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
      #import pdb; pdb.set_trace()
   
      #odsopen = b"ods listing close;ods html5 file=stdout options(svg_mode='inline');               ods graphics on / outputfmt=svg;\n"
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

   def teach_me_SAS(self, nosub):
      self.nosub = nosub

   def submit(self, code, results="html"):
      #import pdb; pdb.set_trace()
   
      odsopen  = b"ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=png; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods html5 close;ods listing;\n"
      ods      = True;
      htm      = "html HTML"
      mj       = b";*\';*\";*/;\n"

      lstf = b''
      logf = b''
      quit = False
      eof = 5

      if self.nosub:
         return dict(LOG=code, LST='')

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

   
   def exist(self, table, libref="work"):
      #import pdb; pdb.set_trace()

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
   
   
   def sasstat(self):
       return SAS_stat(self)

   def sasets(self):
       return SAS_ets(self)

   def sasdata(self, table, libref="work", out='HTML'):
      if self.exist(table, libref):
         return SAS_data(self, libref, table, out)
      else:
         return None
   
   def saslib(self, libref, engine=' ', path='', options=' '):
      code  = "libname "+libref+" "+engine+" "
      if len(path) > 0:
         code += " '"+path+"' "
      code += options+";"

      ll = self.submit(code, "text")
      if self.nosub:
         print(ll['LOG'])
      else:
         print(ll['LOG'].rsplit(";*\';*\";*/;\n")[2]) 
   
   def read_csv(self, file, table, libref="work", out='HTML'):
   
      code  = "filename x "
   
      if file.startswith(("http","HTTP")):
         code += "url "
   
      code += "\""+file+"\";\n"
      code += "proc import datafile=x out="
      code += libref+"."+table
      code += " dbms=csv replace; run;"
      ll = self.submit(code, "text")
   
      if self.nosub:
         print(ll['LOG'])

      if self.exist(table, libref):
         return SAS_data(self, libref, table, out)
      else:
         return None
   
   def df2sd(self, df, table='a', libref="work", out='HTML'):
       return self.dataframe2sasdata(df, table, libref, out)
   
   def dataframe2sasdata(self, df, table='a', libref="work", out='HTML'):
      #import pdb; pdb.set_trace()

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
         return SAS_data(self, libref, table, out)
      else:
         return None
   
   def sd2df(self, sd):
       return self.sasdata2dataframe(sd)
   
   def sasdata2dataframe(self, sd):
      #import pdb; pdb.set_trace()
      import pandas as pd
      import socket as socks
      datar = ""

      if sd == None:
         print('The SAS_data object is not valid; it is \'None\'')
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
      #code += "put vf;\n"
      #code += "do i = 1 to nvars; var = varfmt(d, i); put var; end;\n"
      code += "run;"
   
      #self._getlog(1)
      #self._submit(code, "text")
      #log = self._getlog()
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
   
      #l2 = l2[2].partition("VARFMT=")
      #l2 = l2[2].partition("\n")
      #varfmt = l2[2].split("\n", nvars)
      #del varfmt[nvars]
   
      code  = "data _null_; set "+sd.libref+"."+sd.table+"(obs=1);put 'FMT_CATS=';\n"
      for i in range(len(varlist)):
         #code += "_tom = fmtinfo(vformatn('"+varlist[i]+"'n), 'cat'); put _tom;\n"
         code += "_tom = vformatn('"+varlist[i]+"'n);put _tom;\n"
      code += "run;\n"
   
      #self._submit(code, "text")
      #log = self._getlog()
      ll = self.submit(code, "text")

      l2 = ll['LOG'].rpartition("FMT_CATS=")
      l2 = l2[2].partition("\n")              
      varcat = l2[2].split("\n", nvars)
      del varcat[nvars]
   
      sock = socks.socket()
      sock.bind(("",0))
      port = sock.getsockname()[1]
   
      code  = ""
      #code  = "data _null_; x = sleep(1,1);run;\n"
      code += "filename sock socket ':"+str(port)+"' lrecl=32767 recfm=v termstr=LF;\n"
      code += " data _null_; set "+sd.libref+"."+sd.table+";\n file sock; put "
      for i in range(len(varlist)):
         code += "'"+varlist[i]+"'n "
         #if vartype[i] == 'N' and varcat[i] in ('num', 'curr', 'binary'):
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
   
   
class SAS_data:

    def __init__(self, sassession, libref, table, out="HTML"):

        self.sas =  sassession

        failed = 0
        if out == "HTML" or out == 'html':
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

    def __flushlst__(self):
        lst = b'hi'
        while(len(lst) > 0):
           lst = self.sas.sasprocess.stdout.read1(4096)
           continue

    def set_out(self, out):
        if out == "HTML" or out == 'html':
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
        
        self.__flushlst__()

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
        #import pdb; pdb.set_trace()
        code  = "%put lastobs=%sysfunc(attrn(%sysfunc(open("
        code += self.libref
        code += "."
        code += self.table
        code += ")),NOBS)) tom;"

        #self.sas._getlog()
        #self.sas._submit(code, "text")
        #log = self.sas._getlog()

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
        
        #self.__flushlst__()

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

        self.__flushlst__()

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
        
        self.__flushlst__()

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

    def to_csv(self, file):
        code  = "filename x \""+file+"\";\n"
        code += "proc export data="+self.libref+"."+self.table+" outfile=x"
        code += " dbms=csv replace; run;"
        ll = self.sas.submit(code, "text")

        if self.sas.nosub:
           print(ll['LOG'])
        else:
           return 0

    def hist(self, var, title='', label=''):
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
        
        self.__flushlst__()

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
