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

    # Windows commands to find deployement folders
    p = subprocess.Popen(
        r'dir "{}deploywiz" /AD /s/b'.format(depDir),
        stdout=subprocess.PIPE, shell=True
    )

    # processes command output
    cmdOut = p.stdout.read().decode('utf-8').split('\r\n')
    cmdOut.pop()

    # deployement wizard folder
    depWiz = cmdOut[0]

    # creates a set for the targets with their full path
    targetsW = set([
        depWiz + "\\sas.svc.connection.jar", depWiz + "\\log4j.jar",
        depWiz + "\\sas.security.sspi.jar", depWiz + "\\sas.core.jar"
    ])

    # creates list out of the set intersection between all jars and targets
    jarList = list(set(glob("{}\\*.jar".format(depWiz))).intersection(targetsW))

    # creates saspy jar path
    sasIOM = saspydir+'java\\saspyiom.jar'

    # there are 4 required jars, if not all 4 are located the program will stop
    if len(jarList) < len(targetsW):
        print(
            "The creation process could not be completed becasue not all "
            "required jar files exist on this system."
        )
        return
    # if all jars are detected cfg will be built
    else:
        cfg = ('SAS_config_names=["autogen_winlocal"]\n\n' +
            'SAS_config_options = {\n\t"lock_down": False,' +
            '\n\t"verbose"  : True\n\t}' +
            '\n\ncpW  =  "{}"'.format(jarList[0]) +
            '\ncpW += ";{}"'.format(jarList[1]) +
            '\ncpW += ";{}"'.format(jarList[2]) +
            '\ncpW += ";{}"'.format(jarList[3])
        )

    # determines if saspy jar exists and if so appends it to cfg
    if os.path.isfile(sasIOM):
        cfg += '\ncpW += ";{}"'.format(sasIOM)
    # if it does not exist cfg will be written with the option to add it
    else:
        print(
            "The saspyiom.jar file could not be located, you will need to "
            "locate this file and add it to the cpW where labeled SASPYJAR"
        )
        cfg += '\ncpW += ";{}"'.format('SASPYJAR')

    # adds required config info to cfg
    cfg += (
        '\n\nautogen_winlocal = ' +
        '{\n\t"java"      : "'+java+'",\n\t"encoding"  : "windows-1252",' +
        '\n\t"classpath" : cpW\n\t}'
    )

    # if dll exists
    if os.path.isfile(sspi):
        cfg += '\n\nimport os\nos.environ["PATH"] += ";{}"'.format(sspi)
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
