# Configuration names for SAS - python List
# 
#SAS_config_names=['default', 'mysas94', 'stat_http', 'tom1_http']
# 
SAS_config_names=['default', 'stat_http'] 



# These need path to SASHome and version number - python Dict
# The default path to the sas start up script is: /opt/sasinside/SASHome/SASFoundation/9.4/sas
# valid keys are:
# 'saspath' - path to SAS startup script i.e.: /opt/sasinside/SASHome/SASFoundation/9.4/sas
# 'options' - SAS options to include in the start up command line - Python List
#
#
#
default={'saspath' : '/opt/sasinside/SASHome/SASFoundation/9.4/sas',
         }

#mysas94={'saspath' : '/opt/sasinside/SASHome/SASFoundation/9.4/sas',
#         'options' : ["-autoexec", "/opt/sasinside/SASHome/my_autoexec.sas", "-set", "Env_var", "Value", "-fullstimer"], 
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


