# Configuration names for SAS - python List
# 
#SAS_config_names=['default', 'mysas94', 'stat_http', 'tom1_http']
# 
SAS_config_names=['default', 'stat_http'] 



# These need path to SASHome and version number - python Dict
# A usual install path is: /opt/sasinside/SASHome/SASFoundation/9.4/sas
# valid keys are:
# 'path'    - path to SASHome i.e.: /opt/sasinside/SASHome
# 'version' - version number that is a subdirectory below SASHome subdirectories
# 'options' - SAS options to include in the start up command line - Python List
#
#
#
default={'path'    : '/opt/sasinside/SASHome',
         'version' : '9.4'
         }

#mysas94={'path'    : '/opt/sasinside/SASHome',
#         'options' : ["-autoexec", "/opt/sasinside/SASHome/my_autoexec.sas", "-set", "Env_var", "Value", "-fullstimer"], 
#         'version' : '9.4',
#         }



# Future
# These need ip addr and port (which defaults to 80)  - python Dict
# valid keys are:
# 'ip'      - host address 
# 'port'    - port
# 'context' - context name defined on the compute service
# 'options' - SAS options to include in the start up command line
# 'user'    - not suggested
# 'pw'      - really not suggested
# 
#
             
stat_http={'ip'      : 'tomspc',
           'port'    :  80,
           'context' : 'Stat'
           }

#tom1_http={'ip'      : 'tomspc'}


