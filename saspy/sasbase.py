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
import subprocess, fcntl, os
#from IPython.display import HTML



class sas_session:
   
   def __init__(self, path="/opt/sasinside/SASHome"):
      #import pdb; pdb.set_trace()

      self.saspid = None
      self.obj_cnt = 0
      self._log= ""
      #self._startsas(path)

   def __del__(self):
      #import pdb; pdb.set_trace()

      if self.saspid:
         self._endsas()
      self.saspid = None
   
   def _objcnt(self):
       self.obj_cnt+=1
       return self.obj_cnt

   def _startsas(self, path="/opt/sasinside/SASHome"):
   
      if self.saspid:
         return self.saspid
   
      parms  = [path+"/SASFoundation/9.4/sas"]
      parms += ["-set", "TKPATH", path+"/SASFoundation/9.4/sasexe:"+path+"/SASFoundation/9.4/utilities/bin"]
      parms += ["-set", "SASROOT", path+"/SASFoundation/9.4"]
      parms += ["-set", "SASHOME", path]
      parms += ["-pagesize", "MAX"]
      parms += ["-stdio"]
   
      self.saspid = subprocess.Popen(parms, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      fcntl.fcntl(self.saspid.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
      fcntl.fcntl(self.saspid.stderr,fcntl. F_SETFL, os.O_NONBLOCK)
     
      self._submit("options svgtitle='svgtitle'; options validvarname=any; options pagesize=max;", "text")
      self._getlog(1)
        
      return self.saspid.pid
   
   def _getlog(self, wait=5):
      #import pdb; pdb.set_trace()
   
      logf =b''
      quit = wait * 2
   
      while True:
         #log = ""
   
         #try:
         #   log = self.saspid.stderr.read(4096)
         #except IOError as e:
   
         log = self.saspid.stderr.read1(4096)
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
         lst = self.saspid.stdout.read1(4096)
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
      self._submit("data _null_;file print;put 'tom was here';run;", "text")
   
      while True:
         #try:
         #   lst = self.saspid.stdout.read(4096)
         #except IOError as e:
   
         lst = self.saspid.stdout.read1(4096)
         if len(lst) > 0:
            lstf += lst
   
            lenf = len(lstf)
            eof = lstf.find(b"tom was here", lenf - 25, lenf)
      
            if (eof != -1):
               final = lstf.partition(b"tom was here")
               f2 = final[0].decode().rpartition(chr(12))
               break
         else:
            quit -= 1
            if quit < 0:
               break
            sleep(0.5)

      lst = f2[0]
      return lst.replace(chr(12), '\n')


   def _getlstlog(self, done='used (Total process time):', count=1):
      #import pdb; pdb.set_trace()
   
      lstf = b''
      logf = b''
      quit = False
      eof = 5
   
      while True:
         if quit:
            eof -= 1
         if eof < 0:
            break
         lst = self.saspid.stdout.read(-1)
         #if len(lst) > 0:
         if lst != None:
            lstf += lst
            print("=====================LST==============\n"+lst.decode()+"\n\n\n\n")
         else:
            log = self.saspid.stderr.read(-1)
            #if len(log) > 0:
            if log != None:
               logf += log
               print("=====================LOG==============\n"+log.decode()+"\n\n\n\n")
               if logf.count(done.encode()) >= count:
                  quit = True

      self._log += logf.decode()
      return lstf.decode()
   
   def _submit(self, code, results="html"):
      #import pdb; pdb.set_trace()
   
      #odsopen = b"ods listing close;ods html5 file=stdout options(svg_mode='inline');               ods graphics on / outputfmt=svg;\n"
      odsopen  = b"ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=png; ods graphics on / outputfmt=png;\n"
      odsclose = b"ods html5 close;ods listing;\n"
      ods      = True;
      htm      = "html HTML"
   
      if (htm.find(results) < 0):
         ods = False
   
      if (ods):
         self.saspid.stdin.write(odsopen)
   
      out = self.saspid.stdin.write(code.encode()+b'\n')
   
      if (ods):
         self.saspid.stdin.write(odsclose)

      self.saspid.stdin.flush()

      return out

   def _endsas(self):
      rc = 0
      if not self.saspid:
         code = b"\n;quit;endsas;\n"
         self._getlog(1)
         self.saspid.stdin.write(code)
         self.saspid.stdin.flush()
         rc = self.saspid.wait(10)
         self.saspid = None
      return rc

   def exist(self, table, libref="work"):
      #import pdb; pdb.set_trace()

      code  = "data _null_; e = exist('"
      code += libref+"."+table+"');\n" 
      code += "te='TABLE_EXISTS='; put te e;run;"
   
      self._getlog(1)
      self._submit(code, "text")
      log = self._getlog()
   
      l2 = log.rpartition("TABLE_EXISTS= ")
      l2 = l2[2].partition("\n")
      exists = int(l2[0])
   
      return exists
   
   
   def sasdata(self, table, libref="work", out='HTML'):
      if self.exist(table, libref):
         return sas_data(self, libref, table, out)
      else:
         return None
   def sasstat(self):
       from saspy import sasstat 
       return sasstat.sas_stat(self)
   
   def read_csv(self, file, table, libref="work", out='HTML'):
   
      code  = "filename x "
   
      if file.startswith(("http","HTTP")):
         code += "url "
   
      code += "\""+file+"\";\n"
      code += "proc import datafile=x out="
      code += libref+"."+table
      code += " dbms=csv replace; run;"
      self._submit(code, "text")
   
      if exist(table, libref):
         return sas_data(self, libref, table, out)
      else:
         return None
   
   def df2sd(self, df, table='a', libref="work", out='HTML'):
       return self.dataframe2sasdata(df, table, libref, out)
   
   def dataframe2sasdata(self, df, table='a', libref="work", out='HTML'):
      #import pdb; pdb.set_trace()

      input = ""
      card  = ""
      length = ""

      for name in range(len(df.columns)):
         input += "'"+df.columns[name]+"'n "
         if df.dtypes[df.columns[name]].kind in ('O','S','U','V',):
            col_l = df[df.columns[name]].map(len).max()
            length += " '"+df.columns[name]+"'n $"+str(col_l)
            #input  += "$ "
   
      code  = "data "+libref+"."+table+";\n"
      if len(length):
         code += "length"+length+";\n"
      code += "infile datalines delimiter='09'x;\n input "+input+";\n datalines;"

      self._submit(code, "text")

      for row in df.iterrows():
         card  = ""
         for col in range(len(row[1])):
            card += str(row[1][col])+chr(9)
         self._submit(card, "text")
   
      self._submit(";run;", "text")
   
      if self.exist(table, libref):
         return sas_data(self, libref, table, out)
      else:
         return None
   
   def sd2df(self, sd):
       return self.sasdata2dataframe(sd)
   
   def sasdata2dataframe(self, sd):
      #import pdb; pdb.set_trace()
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
      #code += "put vf;\n"
      #code += "do i = 1 to nvars; var = varfmt(d, i); put var; end;\n"
      code += "run;"
   
      self._getlog(1)
      self._submit(code, "text")
      log = self._getlog()
   
      l2 = log.rpartition("LRECL= ")
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
   
      self._submit(code, "text")
      log = self._getlog()

      l2 = log.rpartition("FMT_CATS=")
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
      self._submit(code, 'text')
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
   
      return df.convert_objects(convert_numeric=True, convert_dates=True, copy=False)
   
   
class sas_data:

    def __init__(self, sas, libref, table, out="HTML"):

        self.sas =  sas

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
           lst = self.sas.saspid.stdout.read1(4096)
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

        if self.HTML:
           from IPython.display import HTML 
           self.sas._submit(code)
           return HTML(self.sas._getlst())
        else:
           self.sas._submit(code, "text")
           print(self.sas._getlsttxt())
   
    def tail(self, obs=5):
        #import pdb; pdb.set_trace()
        code  = "%put lastobs=%sysfunc(attrn(%sysfunc(open("
        code += self.libref
        code += "."
        code += self.table
        code += ")),NOBS));"

        self.sas._getlog()
        self.sas._submit(code, "text")
        log = self.sas._getlog()

        lastobs = log.rpartition("lastobs=")
        lastobs = lastobs[2].partition(" ")
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
        
        self.__flushlst__()

        if self.HTML:
           from IPython.display import HTML 
           self.sas._submit(code)
           return HTML(self.sas._getlst())
        else:
           self.sas._submit(code, "text")
           print(self.sas._getlsttxt())
   
    def contents(self):
        code  = "proc contents data="
        code += self.libref
        code += "."
        code += self.table
        code += ";run;"

        self.__flushlst__()

        if self.HTML:
           from IPython.display import HTML 
           self.sas._submit(code)
           return HTML(self.sas._getlst())
        else:
           self.sas._submit(code, "text")
           print(self.sas._getlsttxt())
   
    def describe(self):
        return(self.means())

    def means(self):
        code  = "proc means data="
        code += self.libref
        code += "."
        code += self.table
        code += " n mean std min p25 p50 p75 max;run;"
        
        self.__flushlst__()

        if self.HTML:
           from IPython.display import HTML 
           self.sas._submit(code)
           return HTML(self.sas._getlst())
        else:
           self.sas._submit(code, "text")
           print(self.sas._getlsttxt())

    def to_csv(self, file):
        code  = "filename x \""+file+"\";\n"
        code += "proc export data="+self.libref+"."+self.table+" outfile=x"
        code += " dbms=csv replace; run;"
        self.sas._submit(code, "text")
        return 0


if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(_getlog())
    print(_getlsttxt())

    endsas()

sas_dtdt_fmts = (    
'AFRDFDD',
'AFRDFDE',
'AFRDFDE',
'AFRDFDN',
'AFRDFDT',
'AFRDFDT',
'AFRDFDWN',
'AFRDFMN',
'AFRDFMY',
'AFRDFMY',
'AFRDFWDX',
'AFRDFWKX',
'ANYDTDTE',
'ANYDTDTM',
'ANYDTTME',
'B8601DA',
'B8601DA',
'B8601DJ',
'B8601DN',
'B8601DN',
'B8601DT',
'B8601DT',
'B8601DZ',
'B8601DZ',
'B8601LZ',
'B8601LZ',
'B8601TM',
'B8601TM',
'B8601TZ',
'B8601TZ',
'CATDFDD',
'CATDFDE',
'CATDFDE',
'CATDFDN',
'CATDFDT',
'CATDFDT',
'CATDFDWN',
'CATDFMN',
'CATDFMY',
'CATDFMY',
'CATDFWDX',
'CATDFWKX',
'CRODFDD',
'CRODFDE',
'CRODFDE',
'CRODFDN',
'CRODFDT',
'CRODFDT',
'CRODFDWN',
'CRODFMN',
'CRODFMY',
'CRODFMY',
'CRODFWDX',
'CRODFWKX',
'CSYDFDD',
'CSYDFDE',
'CSYDFDE',
'CSYDFDN',
'CSYDFDT',
'CSYDFDT',
'CSYDFDWN',
'CSYDFMN',
'CSYDFMY',
'CSYDFMY',
'CSYDFWDX',
'CSYDFWKX',
'DANDFDD',
'DANDFDE',
'DANDFDE',
'DANDFDN',
'DANDFDT',
'DANDFDT',
'DANDFDWN',
'DANDFMN',
'DANDFMY',
'DANDFMY',
'DANDFWDX',
'DANDFWKX',
'DATE',
'DATE',
'DATEAMPM',
'DATETIME',
'DATETIME',
'DAY',
'DDMMYY',
'DDMMYY',
'DDMMYYB',
'DDMMYYC',
'DDMMYYD',
'DDMMYYN',
'DDMMYYP',
'DDMMYYS',
'DESDFDD',
'DESDFDE',
'DESDFDE',
'DESDFDN',
'DESDFDT',
'DESDFDT',
'DESDFDWN',
'DESDFMN',
'DESDFMY',
'DESDFMY',
'DESDFWDX',
'DESDFWKX',
'DEUDFDD',
'DEUDFDE',
'DEUDFDE',
'DEUDFDN',
'DEUDFDT',
'DEUDFDT',
'DEUDFDWN',
'DEUDFMN',
'DEUDFMY',
'DEUDFMY',
'DEUDFWDX',
'DEUDFWKX',
'DOWNAME',
'DTDATE',
'DTMONYY',
'DTWKDATX',
'DTYEAR',
'DTYYQC',
'E8601DA',
'E8601DA',
'E8601DN',
'E8601DN',
'E8601DT',
'E8601DT',
'E8601DZ',
'E8601DZ',
'E8601LZ',
'E8601LZ',
'E8601TM',
'E8601TM',
'E8601TZ',
'E8601TZ',
'ENGDFDD',
'ENGDFDE',
'ENGDFDE',
'ENGDFDN',
'ENGDFDT',
'ENGDFDT',
'ENGDFDWN',
'ENGDFMN',
'ENGDFMY',
'ENGDFMY',
'ENGDFWDX',
'ENGDFWKX',
'ESPDFDD',
'ESPDFDE',
'ESPDFDE',
'ESPDFDN',
'ESPDFDT',
'ESPDFDT',
'ESPDFDWN',
'ESPDFMN',
'ESPDFMY',
'ESPDFMY',
'ESPDFWDX',
'ESPDFWKX',
'EURDFDD',
'EURDFDE',
'EURDFDE',
'EURDFDN',
'EURDFDT',
'EURDFDT',
'EURDFDWN',
'EURDFMN',
'EURDFMY',
'EURDFMY',
'EURDFWDX',
'EURDFWKX',
'FINDFDD',
'FINDFDE',
'FINDFDE',
'FINDFDN',
'FINDFDT',
'FINDFDT',
'FINDFDWN',
'FINDFMN',
'FINDFMY',
'FINDFMY',
'FINDFWDX',
'FINDFWKX',
'FRADFDD',
'FRADFDE',
'FRADFDE',
'FRADFDN',
'FRADFDT',
'FRADFDT',
'FRADFDWN',
'FRADFMN',
'FRADFMY',
'FRADFMY',
'FRADFWDX',
'FRADFWKX',
'FRSDFDD',
'FRSDFDE',
'FRSDFDE',
'FRSDFDN',
'FRSDFDT',
'FRSDFDT',
'FRSDFDWN',
'FRSDFMN',
'FRSDFMY',
'FRSDFMY',
'FRSDFWDX',
'FRSDFWKX',
'HHMM',
'HOUR',
'HUNDFDD',
'HUNDFDE',
'HUNDFDE',
'HUNDFDN',
'HUNDFDT',
'HUNDFDT',
'HUNDFDWN',
'HUNDFMN',
'HUNDFMY',
'HUNDFMY',
'HUNDFWDX',
'HUNDFWKX',
'IS8601DA',
'IS8601DA',
'IS8601DN',
'IS8601DN',
'IS8601DT',
'IS8601DT',
'IS8601DZ',
'IS8601DZ',
'IS8601LZ',
'IS8601LZ',
'IS8601TM',
'IS8601TM',
'IS8601TZ',
'IS8601TZ',
'ITADFDD',
'ITADFDE',
'ITADFDE',
'ITADFDN',
'ITADFDT',
'ITADFDT',
'ITADFDWN',
'ITADFMN',
'ITADFMY',
'ITADFMY',
'ITADFWDX',
'ITADFWKX',
'JDATEMD',
'JDATEMDW',
'JDATEMNW',
'JDATEMON',
'JDATEQRW',
'JDATEQTR',
'JDATESEM',
'JDATESMW',
'JDATEWK',
'JDATEYDW',
'JDATEYM',
'JDATEYMD',
'JDATEYMD',
'JDATEYMW',
'JDATEYT',
'JDATEYTW',
'JNENGO',
'JNENGO',
'JNENGOT',
'JNENGOTW',
'JNENGOW',
'JTIMEH',
'JTIMEHM',
'JTIMEHMS',
'JTIMEHW',
'JTIMEMW',
'JTIMESW',
'JULDATE',
'JULDAY',
'JULIAN',
'JULIAN',
'MACDFDD',
'MACDFDE',
'MACDFDE',
'MACDFDN',
'MACDFDT',
'MACDFDT',
'MACDFDWN',
'MACDFMN',
'MACDFMY',
'MACDFMY',
'MACDFWDX',
'MACDFWKX',
'MDYAMPM',
'MDYAMPM',
'MINGUO',
'MINGUO',
'MMDDYY',
'MMDDYY',
'MMDDYYB',
'MMDDYYC',
'MMDDYYD',
'MMDDYYN',
'MMDDYYP',
'MMDDYYS',
'MMSS',
'MMYY',
'MMYYC',
'MMYYD',
'MMYYN',
'MMYYP',
'MMYYS',
'MONNAME',
'MONTH',
'MONYY',
'MONYY',
'ND8601DA',
'ND8601DN',
'ND8601DT',
'ND8601DZ',
'ND8601TM',
'ND8601TZ',
'NENGO',
'NENGO',
'NLDATE',
'NLDATE',
'NLDATEL',
'NLDATEM',
'NLDATEMD',
'NLDATEMDL',
'NLDATEMDM',
'NLDATEMDS',
'NLDATEMN',
'NLDATES',
'NLDATEW',
'NLDATEW',
'NLDATEWN',
'NLDATEYM',
'NLDATEYML',
'NLDATEYMM',
'NLDATEYMS',
'NLDATEYQ',
'NLDATEYQL',
'NLDATEYQM',
'NLDATEYQS',
'NLDATEYR',
'NLDATEYW',
'NLDATM',
'NLDATM',
'NLDATMAP',
'NLDATMAP',
'NLDATMDT',
'NLDATML',
'NLDATMM',
'NLDATMMD',
'NLDATMMDL',
'NLDATMMDM',
'NLDATMMDS',
'NLDATMMN',
'NLDATMS',
'NLDATMTM',
'NLDATMTZ',
'NLDATMW',
'NLDATMW',
'NLDATMWN',
'NLDATMWZ',
'NLDATMYM',
'NLDATMYML',
'NLDATMYMM',
'NLDATMYMS',
'NLDATMYQ',
'NLDATMYQL',
'NLDATMYQM',
'NLDATMYQS',
'NLDATMYR',
'NLDATMYW',
'NLDATMZ',
'NLDDFDD',
'NLDDFDE',
'NLDDFDE',
'NLDDFDN',
'NLDDFDT',
'NLDDFDT',
'NLDDFDWN',
'NLDDFMN',
'NLDDFMY',
'NLDDFMY',
'NLDDFWDX',
'NLDDFWKX',
'NLTIMAP',
'NLTIMAP',
'NLTIME',
'NLTIME',
'NORDFDD',
'NORDFDE',
'NORDFDE',
'NORDFDN',
'NORDFDT',
'NORDFDT',
'NORDFDWN',
'NORDFMN',
'NORDFMY',
'NORDFMY',
'NORDFWDX',
'NORDFWKX',
'POLDFDD',
'POLDFDE',
'POLDFDE',
'POLDFDN',
'POLDFDT',
'POLDFDT',
'POLDFDWN',
'POLDFMN',
'POLDFMY',
'POLDFMY',
'POLDFWDX',
'POLDFWKX',
'PTGDFDD',
'PTGDFDE',
'PTGDFDE',
'PTGDFDN',
'PTGDFDT',
'PTGDFDT',
'PTGDFDWN',
'PTGDFMN',
'PTGDFMY',
'PTGDFMY',
'PTGDFWDX',
'PTGDFWKX',
'QTR',
'QTRR',
'RUSDFDD',
'RUSDFDE',
'RUSDFDE',
'RUSDFDN',
'RUSDFDT',
'RUSDFDT',
'RUSDFDWN',
'RUSDFMN',
'RUSDFMY',
'RUSDFMY',
'RUSDFWDX',
'RUSDFWKX',
'SLODFDD',
'SLODFDE',
'SLODFDE',
'SLODFDN',
'SLODFDT',
'SLODFDT',
'SLODFDWN',
'SLODFMN',
'SLODFMY',
'SLODFMY',
'SLODFWDX',
'SLODFWKX',
'STIMER',
'SVEDFDD',
'SVEDFDE',
'SVEDFDE',
'SVEDFDN',
'SVEDFDT',
'SVEDFDT',
'SVEDFDWN',
'SVEDFMN',
'SVEDFMY',
'SVEDFMY',
'SVEDFWDX',
'SVEDFWKX',
'TIME',
'TIME',
'TIMEAMPM',
'TOD',
'TWMDY',
'WEEKDATE',
'WEEKDATX',
'WEEKDAY',
'WEEKU',
'WEEKU',
'WEEKV',
'WEEKV',
'WEEKW',
'WEEKW',
'WORDDATE',
'WORDDATX',
'XYYMMDD',
'XYYMMDD',
'YEAR',
'YMDDTTM',
'YYMM',
'YYMMC',
'YYMMD',
'YYMMDD',
'YYMMDD',
'YYMMDDB',
'YYMMDDC',
'YYMMDDD',
'YYMMDDN',
'YYMMDDP',
'YYMMDDS',
'YYMMN',
'YYMMN',
'YYMMP',
'YYMMS',
'YYMON',
'YYQ',
'YYQ',
'YYQC',
'YYQD',
'YYQN',
'YYQP',
'YYQR',
'YYQRC',
'YYQRD',
'YYQRN',
'YYQRP',
'YYQRS',
'YYQS',
'YYQZ',
'YYQZ',
'YYWEEKU',
'YYWEEKV',
'YYWEEKW'
)
