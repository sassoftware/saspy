from saspy.pysas34 import *
from saspy.sasstat import *
SAS = sas_session()       
sas = SAS
print("SAS session available as 'SAS'. Pid="+str(sas._startsas()))
