from multiprocessing import Process
from time import sleep
import subprocess, fcntl, os
#from IPython.display import HTML

saspid = None


def getdata(table, libref="work"):
   return sasdata(libref, table)

def startsas(path="/opt/sasinside/SASHome"):
   global saspid 

   parms  = [path+"/SASFoundation/9.4/sas"]
   parms += ["-set", "TKPATH", path+"/SASFoundation/9.4/sasexe:"+path+"/SASFoundation/9.4/utilities/bin"]
   parms += ["-set", "SASROOT", path+"/SASFoundation/9.4"]
   parms += ["-set", "SASHOME", path]
   parms += ["-pagesize", "MAX"]
   parms += ["-stdio"]

   saspid = subprocess.Popen(parms, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   fcntl.fcntl(saspid.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
   fcntl.fcntl(saspid.stderr,fcntl. F_SETFL, os.O_NONBLOCK)
  
   submit("options svgtitle='svgtitle'; options validvarname=any;", "text")
     
   return saspid.pid

def getlog(wait=5):
   #import pdb; pdb.set_trace()
   logf =b''
   quit = wait * 2

   while True:
      #log = ""

      #try:
      #   log = saspid.stderr.read(4096)
      #except IOError as e:

      log = saspid.stderr.read1(4096)
      if len(log) > 0:
         logf += log
      else:
         quit -= 1
         if quit < 0 or len(logf) > 0:
            break
         sleep(0.5)

   return logf.decode()

def getlst(wait=5):
   #import pdb; pdb.set_trace()
   lstf = b''
   quit = wait * 2
   eof = 0
   bof = False
   lenf = 0

   while True:
      lst = saspid.stdout.read1(4096)
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

def getlsttxt(wait=5):
   #import pdb; pdb.set_trace()
   lstf = b''
   quit = wait * 2
   eof = 0
   submit("data _null_;file print;put 'tom was here';run;", "text")

   while True:
      #try:
      #   lst = saspid.stdout.read(4096)
      #except IOError as e:

      lst = saspid.stdout.read1(4096)
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

   return f2[0]


def getlstlog(done='used (Total process time):', count=1):
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
      lst = saspid.stdout.read(-1)
      #if len(lst) > 0:
      if lst != None:
         lstf += lst
         print("=====================LST==============\n"+lst.decode()+"\n\n\n\n")
      else:
         log = saspid.stderr.read(-1)
         #if len(log) > 0:
         if log != None:
            logf += log
            print("=====================LOG==============\n"+log.decode()+"\n\n\n\n")
            if logf.count(done.encode()) >= count:
               quit = True

   return lstf.decode()

def submit(code, results="html"):
   #import pdb; pdb.set_trace()
   #odsopen  = b"ods listing close;ods html5 file=stdout options(svg_mode='inline'); ods graphics on / outputfmt=svg;\n"
   odsopen  = b"ods listing close;ods html5 file=stdout options(bitmap_mode='inline') device=png; ods graphics on / outputfmt=png;\n"
   odsclose = b"ods html5 close;ods listing;\n"
   ods      = True;
   htm      = "html HTML"

   if (htm.find(results) < 0):
      ods = False

   if (ods):
      saspid.stdin.write(odsopen)

   out = saspid.stdin.write(code.encode()+b'\n')
   saspid.stdin.flush()

   if (ods):
       saspid.stdin.write(odsclose)
       saspid.stdin.flush()

   return out

def endsas():
   code = b"\n;quit;endsas;\n"
   saspid.stdin.write(code)
   saspid.stdin.flush()
   return saspid.wait(10)


class sasdata:

    def __init__(self, libref, table, out="HTML"):
        failed = 0
        if out == "HTML":
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
           lst = saspid.stdout.read1(4096)
           continue

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
           submit(code)
           return HTML(getlst())
        else:
           submit(code, "text")
           print(getlsttxt())
   
    def tail(self, obs=5):
        #import pdb; pdb.set_trace()
        code  = "%put lastobs=%sysfunc(attrn(%sysfunc(open("
        code += self.libref
        code += "."
        code += self.table
        code += ")),NOBS));"

        getlog()
        submit(code, "text")
        log = getlog()

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
           submit(code)
           return HTML(getlst())
        else:
           submit(code, "text")
           print(getlsttxt())
   
    def contents(self):
        code  = "proc contents data="
        code += self.libref
        code += "."
        code += self.table
        code += ";run;"

        self.__flushlst__()

        if self.HTML:
           from IPython.display import HTML 
           submit(code)
           return HTML(getlst())
        else:
           submit(code, "text")
           print(getlsttxt())
   
    def means(self):
        code  = "proc means data="
        code += self.libref
        code += "."
        code += self.table
        code += " n mean std min p25 p50 p75 max;run;"
        
        self.__flushlst__()

        if self.HTML:
           from IPython.display import HTML 
           submit(code)
           return HTML(getlst())
        else:
           submit(code, "text")
           print(getlsttxt())

def getdata(table, libref="work"):
   return sasdata(libref, table)


def dataframe2sasdata(df, table='a', libref="work", out='HTML'):
   #import pdb; pdb.set_trace()
   input = ""
   card  = ""

   for name in range(len(df.columns)):
      input += "'"+df.columns[name]+"'n "
      if str(df.dtypes[name]) == 'character' or str(df.dtypes[name]) == 'object':
         input += "$ "

   submit("data "+libref+"."+table+";\n input "+input+";\n datalines;\n", "text")

   for row in df.iterrows():
      card  = ""
      for col in range(len(row[1])):
         card += str(row[1][col])+" "   
      submit(card, "text")

   submit(";run;", "text")

   return sasdata(libref, table, out=out)

def sd2df(sd):
    return sasdata2dataframe(sd)

def sasdata2dataframe(sd):
   #import pdb; pdb.set_trace()
   import pandas as pd
   import socket as socks
   datar = ""


   code  = "data _null_; file STDERR;d = open('"
   code += sd.libref
   code += "."
   code += sd.table
   code += "');\n lrecl = attrn(d, 'LRECL'); nvars = attrn(d, 'NVARS'); lr='LRECL='; vn='VARNUMS='; vl='VARLIST=';\n"
   code += "put lr lrecl; put vn nvars; put vl;\n"
   code += "do i = 1 to nvars; var = varname(d, i); put var; end; run;"

   getlog()
   submit(code, "text")
   log = getlog()


   l2 = log.rpartition("LRECL= ")
   l2 = l2[2].partition("\n")
   lrecl = int(l2[0])

   l2 = l2[2].partition("VARNUMS= ")
   l2 = l2[2].partition("\n")
   nvars = int(l2[0])

   l2 = l2[2].partition("\n")
   varlist = l2[2].split("\n", nvars)
   del varlist[nvars]

   sock = socks.socket()
   sock.bind(("",0))
   port = sock.getsockname()[1]

   code  = "data _null_; x = sleep(1,1);run;\n"
   code += "filename sock socket ':"+str(port)+"' lrecl=32767 recfm=v termstr=LF;\n"
   code += " data _null_; set "+sd.libref+"."+sd.table+";\n file sock; put "
   for i in range(len(varlist)):
      code += "'"+varlist[i]+"'n "
      if i < (len(varlist)-1):
         code += "'09'x "
   code += "; run;\n"

   sock.listen(0)
   submit(code, 'text')
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

   return df.convert_objects(convert_numeric=True)

   #return datar
   #return pd.DataFrame(data=datar, columns=varlist, coerce_float=True)

def read_csv(file, table, libref="work"):
   code  = "filename x url \""+file+"\";\n"
   code += "proc import datafile=x out="
   code += libref+"."+table
   code += " dbms=csv replace; run;"
   submit(code, "text")
   return sasdata(libref, table)


if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(getlog())
    print(getlsttxt())

    endsas()

