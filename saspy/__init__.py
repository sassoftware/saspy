from saspy.pysas34 import *
from saspy.sasstat import *
from saspy.sasets  import *
from saspy.SASLogLexer import *
SAS = SAS_session()       
sas = SAS
print("SAS session available as 'SAS'. Pid="+str(sas._startsas()))
