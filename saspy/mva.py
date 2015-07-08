from saspy import pysas

def startsas(path=""):
   pid = pysas.startsas(path)
   return pid

def getlst():
   lstf = ""
   x=0
   eof = 0
   bof = False
   lenf = 0

   while True:
       x +=1
       lst = pysas.getlst()

       if len(lst) > 0:

          lstf += lst
          if ((not bof) and lst.count("<!DOCTYPE html>", 0, 20) > 0):
             bof = True
       else:
          lenf = len(lstf)

          if (lenf > 15):
             eof = lstf.count("</html>", (lenf - 15), lenf)

          if (eof > 0):
                break

          if (x > 1000 and (not bof)):
             break
          else:
             continue

   return lstf

def getlsttxt():
   lstf = ""
   eof = 0
   submit("data _null_;file print;put 'tom was here';run;", "text")

   while True:
       lst = pysas.getlst()

       if len(lst) > 0:
          lstf += lst
          lf = len(lstf)
          eof = lstf.find("tom was here", lf - 25, lf)

          if (eof != -1):
             final = lstf.partition("tom was here")
             lstf = final[0]
             break
          else:
             continue

   return lstf

def getlog():
   logf = ""
   while True:
       log = pysas.getlog()
       if len(log) > 0:
          logf += log
       else:
          break

   return logf


def submit(code, results="html"):
   odsopen  = "ods listing close;ods html5 file=stdout options(svg_mode='inline'); ods graphics on / outputfmt=svg;"
   odsclose = "ods html5 close;ods listing;"
   ods      = True;
   htm      = "html HTML"

   if (htm.find(results) < 0):
      ods = False

   if (ods):
      pysas.submit(odsopen)

   rc = pysas.submit(code)

   if (ods):
       pysas.submit(odsclose)

   return rc

def endsas():
   return pysas.endsas()



if __name__ == "__main__":
    import pysas

    startsas()

    submit(sys.argv[1], "text")

    print(getlog())
    print(getlsttxt())

    endsas()

