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
# SAS_config_names=['default', 'sasother', 'sas_en', 'sas_utf8', 'http', 'ssh']
#
SAS_config_names = ['default']

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

ssh      = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8',
            'ssh'    : '/usr/bin/ssh',
            'host'   : 'tom64-2'
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
# 'options' - SAS options to include in the start up command line
# 'user'    - not suggested [REQUIRED but PROMTED for at runtime]
# 'pw'      - really not suggested [REQUIRED but PROMTED for at runtime]
# 
#
             
http     = {'ip'      : 'tomspc',
            'port'    :  80,
            'context' : 'Tom1'
            }

httptest = {'ip'      : 'tomspc',
            'port'    :  80
            }


