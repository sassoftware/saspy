import saspy 

sas = saspy.SASsession(url="http://localhost:8081", serverid="0001", reuse_session=True)