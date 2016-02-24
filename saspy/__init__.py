import os
from saspy.pysas34 import *
from saspy.SASLogLexer import *
executable = os.environ.get('SAS_EXECUTABLE', 'sas')
if executable=='sas':
    executable='/opt/sasinside/SASHome/SASFoundation/9.4/sas'
e2=executable.split('/')
_path='/'.join(e2[0:e2.index('SASHome')+1])
_version=e2[e2.index('SASFoundation')+1]
