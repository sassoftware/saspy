import os
import sys
import subprocess
from glob import glob
from saspy import sascfg as ac

def main(cfgfile: str = None, SASHome: str = None, java: str = None):

    if os.name != 'nt':
       print('This function will only run on Windows and create a saspy config file for an IOM Local connection')
       return

    saspydir = ac.__file__.replace('sascfg.py', '')

    if not cfgfile:
       cfgfile = saspydir+'sascfg_personal.py'

    # if the file already exists, don't replace it.
    if os.path.exists(cfgfile):
        print("CFGFILE ALREADY EXISTS: " + cfgfile)
        return

    # handles users who could have different versions
    if not SASHome:
       SASHome = "C:\\Program Files\\SASHome"

    if not java:
       java = 'java'

    depDir  = SASHome+"\\SASDeploymentManager\\"

    try:
        dirList = os.listdir(depDir)
    except:
        while True:
            print("The following SASHome path wasn't found: "+SASHome)
            SASHome = input("Please enter the path to your SASHome directory " +
                "(or q to exit): "
            )
            if SASHome == 'q':
               return
            try:
               print("Trying "+SASHome)
               depDir  = SASHome+"\\SASDeploymentManager\\"
               dirList = os.listdir(depDir)
               break
            except:
               continue

    # prompts the user to enter the version of SAS they want to use if more
    # than one are detected
    if len(dirList) == 1:
        depDir += "{}\\products\\".format(dirList[0])
        sspi = (
            SASHome+"\\SASFoundation\\" +
            "{}\\core\\sasext\\sspiauth.dll".format(dirList[0])
        )
    else:
        while True:
            print(*os.listdir(depDir))
            verFolder = input("Enter the SAS deployement you wish to use " +
                "(or q to exit): "
            )
            if verFolder in os.listdir(depDir):
                depDir += "{}\\products\\".format(verFolder)
                # creates dll path
                sspi = (
                    SASHome+"\\SASFoundation\\" +
                    "{}\\core\\sasext\\sspiauth.dll".format(verFolder)
                )
                break
            elif verFolder == 'q':
                return
            else:
                print('This is not a valid SAS version for your machine.')
                continue

    # adds required config info to cfg
    cfg = ('SAS_config_names=["autogen_winlocal"]\n\n' +
           'SAS_config_options = {\n\t"lock_down": False,' +
           '\n\t"verbose"  : True\n\t}' +
           '\n\nautogen_winlocal = ' +
           '{\n\t"java"      : "'+java+'",\n\t"encoding"  : "windows-1252"' + '}'
          )

    # if dll exists
    if os.path.isfile(sspi):
        cfg += '\n\nimport os\nos.environ["PATH"] += ";{}"'.format(sspi.rsplit('\\sspiauth.dll')[0])
    else:
        print(
            "Couldn't find the sspiauth.dll path. You'll need to find that and "
            "add it to your system PATH variable.\n"
        )

    cfg = cfg.replace('\\', '\\\\')

    fd = open(cfgfile, 'w')
    fd.write(cfg)
    fd.close()

    print("Generated configurations file: " + cfgfile + "\n")

if __name__ == "__main__":
    for i in range(len(sys.argv)):
       if sys.argv[i] == 'None':
          sys.argv[i] =   None
    main(*sys.argv[1:])
