#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# Configuration Names for SAS - python List
# This is the list of allowed configuration definitions that can be used. The definition are defined below.
# The various options for the different access methods can be specified on the SASsession() i.e.:
# sas = SASsession(cfgname='default', options='-fullstimer', user='me')
#
# based upon the lock_down configuration option below, you may or may not be able to override option
# that are defined already. Any necessary option (like user, pw for HTTP) that are not defined will be 
# prompted for at run time. To dissallow overrides of OPTION, when you don't have any specified, simply
# specify options=' '. This way it's specified so it can't be overridden, even though you don't have any
# extra options you want applied.
# 
# SAS_config_names=['default', 'sasother', 'sas_en', 'sas_utf8', 'http', 'ssh', 'httptest']
#
SAS_config_names = ['default', 'http', 'httptest', 'ssh', 'httpfred', 'grid', 'tdi', 'iomj', 'iomc', 'iomjwin', 'winiomj', 'winiomjwin', 'winlocal', 'gridiom', 'gridiomw']

# Configuration options for pysas - python Dict
# valid key are:
# 
# 'lock_down' - True | False. True = Prevent runtime overrides of SAS_Config values below
#
SAS_config_options = {'lock_down': True}

# Configuration Definitions
#
# For STDIO and STDIO over SSH access methods
# These need path to SASHome and optional startup options - python Dict
# The default path to the sas start up script is: /opt/sasinside/SASHome/SASFoundation/9.4/sas
# A usual install path is: /opt/sasinside/SASHome
#
# Since python uses utf-8, running SAS with encoding=utf-8 is the expected use case. By default
# linux SAS runs in Latin1, which works fine as long as you stick with the lower half of the code page.
# SAS is installed with a link ('sas') to the bin/sas_en startup script, and the link can be swapped
# to point to the utf8 start up script (bin/sas_u8), or another link made (sasutf8) to point to that.  
#
# valid keys are:
# 'saspath' - [REQUIRED] path to SAS startup script i.e.: /opt/sasinside/SASHome/SASFoundation/9.4/sas
# 'options' - SAS options to include in the start up command line - Python List
#
# For passwordless ssh connection, the following are also reuqired:
# 'ssh'     - [REQUIRED] the ssh command to run
# 'host'    - [REQUIRED] the host to connect to
#
default  = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8'
            }

tdi      = {'saspath' : '/tdi/mva-v940m4/usrlibsas/laxno/SASFoundation/9.4/bin/sas_u8'
            }

ssh      = {'saspath' : '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8',
            'ssh'     : '/usr/bin/ssh',
            'host'    : 'tom64-2', 
            'options' : ["-fullstimer"]
            }

grid     = {'saspath' : '/sas3rd/wky/mva-v940/lax_sgm/SASHome/SASFoundation/9.4/bin/sas_u8',
            'ssh'     : '/usr/bin/ssh',
            'metapw'  : '1connect',
            'host'    : 'sascnn@sgm001.unx.sas.com',
            'options' : ["/sas3rd/wky/mva-v940/lax_sgm/SASAppServerConfig/Lev1/Applications/SASGridManagerClientUtility/9.4/sasgsub", "-gridrunsaslm"]
            }
#           'options' : ["/sas3rd/wky/mva-v940/lax_sgm/SASAppServerConfig/Lev1/Applications/SASGridManagerClientUtility/9.4/sasgsub", "-gridruncmdint"]
#           'options' : ["/sas3rd/wky/mva-v940/lax_sgm/SASAppServerConfig/Lev1/Applications/SASGridManagerClientUtility/9.4/sasgsub", "-gridrunsaslm"]


# build out a local classpath variable to use below
cp  =  "/opt/tom/gitlab/metis/java/lib/sas.svc.connection.jar"
cp += ":/opt/tom/gitlab/metis/java/lib/sas.codepolicy.jar"
cp += ":/opt/tom/gitlab/metis/java/lib/log4j.jar"
cp += ":/opt/tom/gitlab/metis/java/lib/sas.security.sspi.jar"
cp += ":/opt/tom/gitlab/metis/java/lib/sas.core.jar"
cp += ":/opt/tom/gitlab/metis/java/tools/ConnectionHelper.java"
cp += ":/opt/tom/gitlab/metis/java/pyiom"
cp += ":/opt/tom/gitlab/metis/java/tools"
cp += ":/opt/tom/gitlab/metis/java"

iomj     = {'java'      : '/usr/bin/java',
            'omruser'   : 'sas',
            'omrpw'     : 'sas',
            'iomhost'   : 'tom64-3.na.sas.com',
            'iomport'   : 8591,
            'classpath' : cp
            }           

iomjwin  = {'java'      : '/usr/bin/java',
            'omruser'   : 'sasiom1@carynt',
            'omrpw'     : '1bridge',
            'iomhost'   : 'd77422.na.sas.com',
            'iomport'   : 18591,
            'encoding'  : 'cp1252',
            'classpath' : cp
            }

gridiom  = {'java'      : '/usr/bin/java',
            'omruser'   : 'sascnn1',
            'omrpw'     : '1connect',
            'iomhost'   : 'bb04cnt10.unx.sas.com',
            'iomport'   : 8594,
            'encoding'  : 'iso-8859-1',
            'classpath' : cp
            }
         
# build out a local classpath variable to use below
cpl  =  "C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\java\lib\sas.svc.connection.jar"
cpl += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\java\lib\sas.codepolicy.jar"
cpl += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\java\lib\log4j.jar"
cpl += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\java\lib\sas.security.sspi.jar"
cpl += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\java\lib\sas.core.jar"
cpl += ";E:\metis-master-85c5ead4636c675fabfbae571e7d1958d10fc31d\java\ConnectionHelper.java"
cpl += ";E:\metis-master-85c5ead4636c675fabfbae571e7d1958d10fc31d\java\pyiom"
cpl += ";E:\metis-master-85c5ead4636c675fabfbae571e7d1958d10fc31d\java\tools"
cpl += ";E:\metis-master-85c5ead4636c675fabfbae571e7d1958d10fc31d\java"

winlocal = {'saspath'   : 'C:\Program Files\SASHome\SASFoundation\9.4\sas.exe',
            'java'      : 'java',
            'omruser'   : 'sastpw',
            'encoding'  : 'cp1252',
            'classpath' : cpl
            }

winiomj  = {'java'      : 'java',
            'omruser'   : 'sas',
            'omrpw'     : 'sas',
            'iomhost'   : 'tom64-3.na.sas.com',
            'iomport'   : 8591,
            'classpath' : cpl
            }

winiomjwin = {'java'    : 'java',
            'omruser'   : 'sasiom1@carynt',
            'omrpw'     : '1bridge',
            'iomhost'   : 'd77422.na.sas.com',
            'iomport'   : 18591,
            'encoding'  : 'cp1252',
            'classpath' : cpl
            }

gridiomw = {'java'      : 'java',
            'omruser'   : 'sascnn1',
            'omrpw'     : '1connect',
            'iomhost'   : 'bb04cnt10.unx.sas.com',
            'iomport'   : 8594,
            'encoding'  : 'cp1252',
            'classpath' : cpl
            }

iomc     = {'iomc'    : '/u/sastpw/tkpy2c/tkext/com/laxnd/tktom',
            'omruser' : 'sas',
            'omrpw'   : 'sas',
            'host'    : 'tom64-3.na.sas.com',
            'port'    : 8591
            }

# sas_en   = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/sas'
#             }
#
# sas_utf8 = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/sasutf8'
#             }
#
# sasother = {'saspath' : '/some/other/directory/SASHome/SASFoundation/9.4/sas',
#             'options' : ["-autoexec", "/my/home_dir/my_autoexec.sas", "-set",
#                          "Env_var", "Value", "-fullstimer"]
#             }


# Future - for the HTTP access method to connect to the Compute Service
# These need ip addr and port, other values will be prompted for - python Dict
# valid keys are:
# 'ip'      - [REQUIRED] host address 
# 'port'    - [REQUIRED] port; the code Defaults this to 80 (the Compute Services default port)
# 'context' - context name defined on the compute service  [PROMTED for at runtime if more than one defined]
# 'options' - SAS options to include (no '-' (dashes), just option names and values)
# 'user'    - not suggested [REQUIRED but PROMTED for at runtime]
# 'pw'      - really not suggested [REQUIRED but PROMTED for at runtime]
# 
#
             
http     = {'ip'      : 'tomspc',
            'port'    :  80,
            'context' : 'Tom2'
            }

httpfred = {'ip'      : '10.63.24.180',
            'port'    :  7980,
            'context' : 'Tom2'
            }

httptest = {'ip'      : 'tomspc',
            'port'    :  80, 
            'options' : ["fullstimer", "memsize=1G"]
            }


