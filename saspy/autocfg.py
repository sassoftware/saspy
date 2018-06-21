import os
import sys

def main(argv):

   thispgm  = argv[0]

   if len(argv) > 1:
      cfgfile  = argv[1]
   else:
      cfgfile = __file__.replace('autocfg.py','sascfg_personal.py')
   
   # if the file already exists, don't replace it.
   if os.path.exists(cfgfile):
      print("CFGFILE ALREADY EXISTS: "+cfgfile)   
      return
   
   cfg = """
SAS_config_names=['autogen_winlocal']
SAS_config_options = {'lock_down': False,
                      'verbose'  : True
                     }

cpW  =  "SASJARPATH\\sas.svc.connection.jar"
cpW += ";SASJARPATH\\log4j.jar"
cpW += ";SASJARPATH\\sas.security.sspi.jar"
cpW += ";SASJARPATH\\sas.core.jar"
#cpW += ";SASPYJARPATH\\java\\saspyiom.jar"
cpW += ";"+__file__.replace("sascfg_personal.py" ,"java\\saspyiom.jar")

autogen_winlocal = {'java'      : 'java',
                    'encoding'  : 'windows-1252',
                    'classpath' : cpW
                   }
import os
os.environ["PATH"] += ';'+r'SSPIPATH'
"""
   
   # these are the jars we need
   targetsW = ["sas.svc.connection.jar", "log4j.jar",
               "sas.security.sspi.jar", "sas.core.jar"]
   
   # this is the default location on Windows
   depDir = "C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\"
   
   # try to get the folders in that location
   if os.path.isdir(depDir):
    ls = os.walk(depDir)
   else:
    ls = []
   
   sjp = None
   
   # check each folder for the jars we want (only look in deploywiz folder) 
   # and remove from targetsW to avoid duplicates
   for path, _, files in ls:
       for fname in files:
           if fname in targetsW:
               if path.lower().find("deploywiz") > -1:
                  sjp = path
                  break
   
   if sjp:
      cfg = cfg.replace("SASJARPATH", sjp)
      #cfg = cfg.replace("SASPYJARPATH", __file__.replace('\\autocfg.py',''))
   else:
      return("Couldn't find the SAS Jar path.\n")
   
   
   # lets get sspi
   targetsW = ["sspiauth.dll"]
   
   # this is the default location on Windows
   depDir = "C:\\Program Files\\SASHome\\SASFoundation\\9.4\\core\\sasext"
   
   # try to get the folders in that location
   if os.path.isdir(depDir):
    ls = os.walk(depDir)
   else:
    ls = []
   
   sspi = None
   
   # check each folder for the jars we want (only look in deploywiz folder) 
   # and remove from targetsW to avoid duplicates
   for path, _, files in ls:
       for fname in files:
           if fname in targetsW:
               sspi = path
               break
   
   if sspi:
      cfg = cfg.replace("SSPIPATH", sspi)
   else:
      print("Couldn't find the sspiauth.dll path. You'll need to find that and add it to your system PATH variable.\n")
      cfg = cfg = cfg.rsplit('os.environ[')[0]
   
   cfg = cfg.replace("\\", "\\\\")
   
   fd = open(cfgfile, 'w')
   fd.write(cfg)
+   fd.close()
+
+   print("Generated configurations file: "+cfgfile+"\n")
+   
+if __name__ == "__main__":
+   main(sys.argv)
