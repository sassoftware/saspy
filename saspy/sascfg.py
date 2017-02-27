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
# that are defined already. Any necessary option (like user, pw for IOM or HTTP) that are not defined will be 
# prompted for at run time. To dissallow overrides of OPTION, when you don't have any specified, simply
# specify options=''. This way it's specified so it can't be overridden, even though you don't have any
# extra options you want applied.
# 
# SAS_config_names=['default', 'sasother', 'sas_en', 'sas_utf8', 'http', 'ssh', 'httptest']
#
SAS_config_names = ['default', 'SASgrid',  'http', 'httptest', 'ssh', 'httpfred', 'grid', 'tdi', 'iomj', 'iomc', 'iomjwin', 'winiomj', 'winiomjwin', 'winlocal', 'gridiom', 'wingridiom']


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



# For IOM (Grid Manager or any IOM) and Local Windows via IOM access method
# These configuration definitions are for connecting over IOM. This is designed to be used to connect to a SAS Grid, via Grid Manager
# and also to connect to a local Windows SAS session. The client side (python and java) for this access method can be either Linux or Windows.
# The STDIO access method above is only for Linux. PC SAS requires this IOM interface. 
#
# The 'saspath' option triggers local Windows SAS mode. In this case neither 'iomhost' nor 'iomport' are needed. localhost is used and an available port
# is used for the connection. In this way, you can run multiple python sessions to seperate Windows SAS instances (i.e.: different notbooks in Jupyter).
#
# Since python uses utf-8, running SAS with encoding=utf-8 is the expected use case. By default Windows SAS runs in WindowsLatin1 (cp1252),
# which does not work well as utf-8. So, transcoding has been implemented in the python layer. The 'encoding' option can be specified to match
# the SAS session encoding (see https://docs.python.org/3.5/library/codecs.html#standard-encodings for python encoding values). cp1252 is appropriate
# for the default Windows SAS session encoding
#                                                                                                         
# Since this IOM access method used the Java IOM client, a classpath is required for the java process to find the necessary jars. Use the template below
# to build out a classpath variable and assign that to the 'classpath' option in the configuration definition. The IOM client jars are delivered as part
# of a Base SAS install, so should be available in any SAS install. The saspyiom.jar is available in the saspy repo/install. 
#
# valid keys are:
# 'saspath'   - [REQUIRED for local Windows connection only] path to SAS executable (sas.exe) i.e.: C:\Program Files\SASHome\SASFoundation\9.4\sas.exe
# 'java'      - [REQUIRED] the path to the java executable to use
# 'iomhost'   - [REQUIRED for remote IOM case, not local Windows] the resolvable host name, or ip to the IOM server to connect to
# 'iomport'   - [REQUIRED for remote IOM case, not local Windows] the port IOM is listening on
# 'omruser'   - not suggested [REQUIRED but PROMTED for at runtime] For local Windows SAS, this is a local user account/pw
# 'omrpw'     - really not suggested [REQUIRED but PROMTED for at runtime]
# 'encoding'  - This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
# 'classpath' - classpath to IOM client jars and saspy client jar.
#
# build out a local classpath variable to use below
cp  =  "/opt/tom/gitlab/metis/java/lib/sas.svc.connection.jar"
cp += ":/opt/tom/gitlab/metis/java/lib/log4j.jar"
cp += ":/opt/tom/gitlab/metis/java/lib/sas.security.sspi.jar"
cp += ":/opt/tom/gitlab/metis/java/lib/sas.core.jar"
cp += ":/opt/tom/gitlab/metis/java/saspyiom.jar"

# build out a local classpath variable to use below
cp2  =  "/u/sastpw/tkpy2j/lib2/sas.svc.connection.jar"
cp2 += ":/u/sastpw/tkpy2j/lib2/log4j.jar"
cp2 += ":/u/sastpw/tkpy2j/lib2/sas.security.sspi.jar"
cp2 += ":/u/sastpw/tkpy2j/lib2/sas.core.jar"
cp2 += ":/opt/tom/gitlab/metis/java/saspyiom.jar"

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
           #'omruser'   : 'sascnn1',
           #'omrpw'     : '1connect',
            'iomhost'   : 'bb04cnt10.unx.sas.com',
            'iomport'   : 8594,
            'encoding'  : 'iso-8859-1',
            'classpath' : cp2
            }
         
SASgrid   = {'java'     : '/usr/bin/java',
           #'omruser'   : 'sascnn1',
           #'omrpw'     : '1connect',
            'iomhost'   : 'sgm001.unx.sas.com',
            'iomport'   : 8591,
            'encoding'  : 'iso-8859-1',
            'classpath' : cp2
            }
         
# build out a local classpath variable to use below
cpl  =  "C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.svc.connection.jar"
cpl += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\log4j.jar"
cpl += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.security.sspi.jar"
cpl += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.core.jar"
cpl += ";C:\programData\Anaconda3\Lib\site-packages\saspy\java\saspyiom.jar"

winlocal = {'saspath'   : 'C:\Program Files\SASHome\SASFoundation\9.4\sas.exe',
            'java'      : 'java',
            'omruser'   : '',
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

wingridiom = {'java'      : 'java',
            'omruser'   : 'sascnn1',
            'omrpw'     : '1connect',
            'iomhost'   : 'bb04cnt10.unx.sas.com',
            'iomport'   : 8594,
            'encoding'  : 'iso-8859-1',
            'classpath' : cpl
            }

iomc     = {'iomc'    : '/u/sastpw/tkpy2c/tkext/com/laxnd/tktom',
            'omruser' : 'sas',
            'omrpw'   : 'sas',
            'host'    : 'tom64-3.na.sas.com',
            'port'    : 8591
            }





# test case for sasgsub grid testing
grid     = {'saspath' : '/sas3rd/wky/mva-v940/lax_sgm/SASHome/SASFoundation/9.4/bin/sas_u8',
            'ssh'     : '/usr/bin/ssh',
            'metapw'  : '1connect',
            'host'    : 'sascnn@sgm001.unx.sas.com',
            'options' : ["/sas3rd/wky/mva-v940/lax_sgm/SASAppServerConfig/Lev1/Applications/SASGridManagerClientUtility/9.4/sasgsub", "-gridrunsaslm"]
            }
#           'options' : ["/sas3rd/wky/mva-v940/lax_sgm/SASAppServerConfig/Lev1/Applications/SASGridManagerClientUtility/9.4/sasgsub", "-gridruncmdint"]
#           'options' : ["/sas3rd/wky/mva-v940/lax_sgm/SASAppServerConfig/Lev1/Applications/SASGridManagerClientUtility/9.4/sasgsub", "-gridrunsaslm"]



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


