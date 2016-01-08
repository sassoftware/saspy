import os
print ("after os")
from saspy.pysas34 import *
print ("after pysas34")
from saspy.sasstat import *
from saspy.sasets  import *
from saspy.SASLogLexer import *
print ("after all saspy import")
SAS = SAS_session()       
sas = SAS
executable = os.environ.get('SAS_EXECUTABLE', 'sas')
if executable=='sas':
    executable='/opt/sasinside/SASHome/SASFoundation/9.4/sas'
e2=executable.split('/')
_path='/'.join(e2[0:e2.index('SASHome')+1])
_version=e2[e2.index('SASFoundation')+1]
print ("after exec " + _path + _version)
print("SAS session available as 'SAS'. Pid="+str(sas._startsas(path=_path, version=_version)))
