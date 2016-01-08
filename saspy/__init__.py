import os
from saspy.pysas34 import *
from saspy.sasstat import *
from saspy.sasets  import *
from saspy.SASLogLexer import *
SAS = SAS_session()       
sas = SAS
executable = os.environ.get('SAS_EXECUTABLE', 'sas')
if executable=='sas':
    executable='/opt/sasinside/SASHome/SASFoundation/9.4/sas'
e2=executable.split('/')
_path='/'.join(e2[0:e2.index('SASHome')+1])
_version=e2[e2.index('SASFoundation')+1]
print("SAS session available as 'SAS'. Pid="+str(sas._startsas(path=_path, version=_version)))
