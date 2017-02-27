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
# prompted for at run time. To disallow overrides of OPTION, when you don't have any specified, simply
# specify options=' '. This way it's specified so it can't be overridden, even though you don't have any
# extra options you want applied.
#
# This is the list of configurations that a user will be presented if they haven't specified one specifically.
# If you add a new configuration make sure to add it to the list.
SAS_config_names = ['default', 'ssh', 'grid', 'winlocal']

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
# For passwordless ssh connection, the following are also required:
# 'ssh'     - [REQUIRED] the ssh command to run
# 'host'    - [REQUIRED] the host to connect to
#
default = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8'
           }

ssh = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8',
       'ssh'    : '/usr/bin/ssh',
       'host'   : 'tom64-2',
       'options': ["-fullstimer"]
       }

# build out a local classpath variable to use below
# These jars are distributed with your SAS deployment.
# They will need to be accessible to the system where saspy is called
cp = "/opt/tom/gitlab/metis/java/lib/sas.svc.connection.jar"
cp += ":/opt/tom/gitlab/metis/java/lib/log4j.jar"
cp += ":/opt/tom/gitlab/metis/java/lib/sas.security.sspi.jar"
cp += ":/opt/tom/gitlab/metis/java/lib/sas.core.jar"
# these jars are from the saspy pip package
cp += ":path/to/saspy/java/pyiom"
cp += ":path/to/saspy/java/tools"
cp += ":path/to/saspy/java"

# java      - the path to your java executable. If java is in your path only 'java' is needed
# omruser   - username to authenticate with SAS
# omrpw     - password to authenticate with SAS
#             if the username  and password are empty '' then you will be prompted for them
# iomhost   - the DNS name (or IP address) for your object spawner
# iomport   - the port of the object spawner listener. All connections go throught this port and then are redirected
grid = {'java'     : '/usr/bin/java',
        'omruser'  : '',
        'omrpw'    : '',
        'iomhost'  : 'foobar.sas.com',
        'iomport'  : 8591,
        'classpath': cp
        }

# build out a local classpath variable to use below
# These jars are part of your SAS deployment search your system for them
cpl = "C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.svc.connection.jar"
cpl += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\log4j.jar"
cpl += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.security.sspi.jar"
cpl += ";C:\Program Files\SASHome\SASDeploymentManager\9.4\products\deploywiz__94472__prt__xx__sp0__1\deploywiz\sas.core.jar"

# these jars are from the saspy pip package below is the default location for anaconda
cpl += ";C:\Users\jadean\AppData\Local\Continuum\Anaconda3\Lib\site-packages\saspy\java\pyiom"
cpl += ";C:\Users\jadean\AppData\Local\Continuum\Anaconda3\Lib\site-packages\saspy\tools"
cpl += ";C:\Users\jadean\AppData\Local\Continuum\Anaconda3\Lib\site-packages\saspy\java"

# saspath   - the path to your sas.exe file. The default path is shown below
# java      - the path to your java executable. If java is in your path only 'java' is needed
# omruser   - your user id for the PC no domain is required
# encoding  - since python is all utf-8 transcode could be needed info about cp1252 https://en.wikipedia.org/wiki/Windows-1252
# classpath - the collection of jars from directly above
winlocal = {'saspath'  : 'C:\Program Files\SASHome\SASFoundation\9.4\sas.exe',
            'java'     : 'java',
            'omruser'  : 'jadean',
            'encoding' : 'cp1252',
            'classpath': cpl
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

http = {'ip'     : 'tomspc',
        'port'   : 80,
        'context': 'Tom2'
        }

httpfred = {'ip'     : '10.63.24.180',
            'port'   : 7980,
            'context': 'Tom2'
            }

httptest = {'ip'     : 'tomspc',
            'port'   : 80,
            'options': ["fullstimer", "memsize=1G"]
            }


