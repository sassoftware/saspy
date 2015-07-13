from multiprocessing import Process
from time import sleep
import subprocess, fcntl, os
from IPython.display import HTML

saspid = None


def getdata(table, libref="work"):
   return sasdata(libref, table)

def startsas(path=""):
   global saspid
   defpath ="/opt/sasinside/SASHome"

   if len(path) == 0:
      path = defpath

   parms  = [path+"/SASFoundation/9.4/sas"]
   parms += ["-set", "TKPATH", path+"/SASFoundation/9.4/sasexe:"+path+"/SASFoundation/9.4/utilities/bin"]
   parms += ["-set", "SASROOT", path+"/SASFoundation/9.4"]
   parms += ["-set", "SASHOME", path]
   parms += ["-stdio"]

   saspid = subprocess.Popen(parms, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   fcntl.fcntl(saspid.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
   fcntl.fcntl(saspid.stderr,fcntl. F_SETFL, os.O_NONBLOCK)

   submit("options svgtitle='svgtitle';", "text")

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
            lstf = final[0]
            break
      else:
         quit -= 1
         if quit < 0:
            break
         sleep(0.5)

   return lstf.decode()


def submit(code, results="html"):
   #import pdb; pdb.set_trace()
   odsopen  = b"ods listing close;ods html5 file=stdout options(svg_mode='inline'); ods graphics on / outputfmt=svg;\n"
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

    def __init__(self, libref, table):
        self.libref = libref
        self.table  = table

    def head(self, obs=5):
        code  = "proc print data="
        code += self.libref
        code += "."
        code += self.table
        code += "(obs="
        code += str(obs)
        code += ");run;"
        submit(code)
        return HTML(getlst())

    def contents(self):
        code  = "proc contents data="
        code += self.libref
        code += "."
        code += self.table
        code += ";run;"
        submit(code)
        return HTML(getlst())

    def means(self):
        code  = "proc means data="
        code += self.libref
        code += "."
        code += self.table
        code += ";run;"
        submit(code)
        return HTML(getlst())

    def read_csv(self, file, table, libref="work"):
        code  = "filename x url "+file+";\n"
        code += "proc import datafile=x out="
        code += libref+"."+table
        code += " dbms=csv replace; run;"
        submit(code)
        return sasdata(libref, table)

def getdata(table, libref="work"):
   return sasdata(libref, table)



if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(getlog())
    print(getlsttxt())

    endsas()




