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

# THIS IS AN EXAMPLE CONFIG FILE. PLEASE CREATE YOUR OWN sascfg_personal.py FILE USING THE APPROPRIATE TEMPLATES FROM BELOW
# SEE THE CONFIGURATION DOC AT https://sassoftware.github.io/saspy/install.html#configuration


# Configuration Names for SAS - python List
# This is the list of allowed configuration definitions that can be used. The definition are defined below.
# if there is more than one name in the list, and cfgname= is not specified in SASsession(), then the user
# will be prompted to choose which configuration to use.
#
# The various options for the different access methods can be specified on the SASsession() i.e.:
# sas = SASsession(cfgname='default', options='-fullstimer', user='me')
#
# Based upon the lock_down configuration option below, you may or may not be able to override option
# that are defined already. Any necessary option (like user, pw for IOM or HTTP) that are not defined will be
# prompted for at run time. To dissallow overrides of as OPTION, when you don't have a value, simply
# specify options=''. This way it's specified so it can't be overridden, even though you don't have any
# specific value you want applied.
#
#SAS_config_names = ['default', 'ssh', 'iomlinux', 'iomwin', 'winlocal', 'winiomlinux', 'winiomwin', 'httpsviya', 'httpviya', 'iomcom']
#

SAS_config_names=['default']



# Configuration options for saspy - python Dict   # not required unless changing any of the defaults
# valid key are:
#
# 'lock_down' - True | False. True = Prevent runtime overrides of SAS_Config values below
#
# 'verbose'   - True | False. True = Allow print statements for debug type messages
#
# 'prompt'    - True | False. True = Allow prompting as necessary
#
SAS_config_options = {'lock_down': False,
                      'verbose'  : True,
                      'prompt'   : True
                     }



# Configuration options for SAS output. By default output is HTML 5.0 (using "ods html5" statement) but certain templates might not work
# properly with HTML 5.0 so it can also be set to HTML 4.0 instead (using "ods html" statement). This option will only work when using IOM
# in local mode. Note that HTML 4.0 will generate images separately which clutters the workspace and if you download the notebook as HTML,
# the HTML file will need to be put in the same folder as the images for them to appear.
# valid keys are:
#
# 'output' = ['html5', 'html']
# 'style'  = any valid style   # this will be the default for SASsession.HTML_Style, which you can also change dynamically in your code
#
#
SAS_output_options = {'output' : 'html5',       # not required unless changing any of the default
                      'style'  : 'HTMLBlue'}


# Configuration Definitions
#
# For STDIO and STDIO over SSH access methods
# These need path to SASHome and optional startup options - python Dict
# The default path to the sas start up script is: /opt/sasinside/SASHome/SASFoundation/9.4/sas
# A usual install path is: /opt/sasinside/SASHome
#
# The encoding is figured out by saspy. You don't need to specify it, unless you just want to get rid of the message about which encoding was determined.
#
# valid keys are:
# 'saspath'  - [REQUIRED] path to SAS startup script i.e.: /opt/sasinside/SASHome/SASFoundation/9.4/sas
# 'options'  - SAS options to include in the start up command line - Python List
# 'encoding' - This is the python encoding value that matches the SAS session encoding your SAS session is using
#
# For passwordless ssh connection, the following are also reuqired:
# 'ssh'     - [REQUIRED] the ssh command to run
# 'host'    - [REQUIRED] the host to connect to
#
# Additional valid keys for ssh:
# 'port'    - [integer] the remote ssh port
# 'tunnel'  - [integer] local port to open via reverse tunnel, if remote host cannot otherwise reach this client
#
default  = {'saspath'  : '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_u8'
            }

ssh      = {'saspath' : '/opt/sasinside/SASHome/SASFoundation/9.4/bin/sas_en',
            'ssh'     : '/usr/bin/ssh',
            'host'    : 'remote.linux.host',
            'encoding': 'latin1',
            'options' : ["-fullstimer"]
            }


# For IOM (Grid Manager or any IOM) and Local Windows via IOM access method
# These configuration definitions are for connecting over IOM. This is designed to be used to connect to any Workspace server, including SAS Grid, via Grid Manager
# and also to connect to a local Windows SAS session. The client side (python and java) for this access method can be either Linux or Windows.
# The STDIO access method above is only for Linux. PC SAS requires this IOM interface.
#
# The absence of the iomhost option triggers local Windows SAS mode. In this case none of 'iomhost', 'iomport', 'omruser', 'omrpw' are needed.
# a local SAS session is started up and connected to.
#
# The encoding is figured out by saspy. You don't need to specify it, unless you just want to get rid of the message about which encoding was determined.

# NONE OF THE PATHS IN THESE EAMPLES ARE RIGHT FOR YOUT INSTALL. YOU HAVE TO CHANGE THE PATHS TO BE CORRECT FOR YOUR INSTALLATION
#
# valid keys are:
# 'java'      - [REQUIRED] the path to the java executable to use
# 'iomhost'   - [REQUIRED for remote IOM case, Don't specify to use a local Windows Session] the resolvable host name, or ip to the IOM server to connect to
# 'iomport'   - [REQUIRED for remote IOM case, Don't specify to use a local Windows Session] the port IOM is listening on
# 'authkey'   - identifier for user/password credentials to read from .authinfo file. Eliminates prompting for credentials.
# 'omruser'   - not suggested        [REQUIRED for remote IOM case but PROMPTED for at runtime] Don't specify to use a local Windows Session
# 'omrpw'     - really not suggested [REQUIRED for remote IOM case but PROMPTED for at runtime] Don't specify to use a local Windows Session
# 'encoding'  - This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
# 'appserver' - name of physical workspace server (when more than one app server defined in OMR) i.e.: 'SASApp - Workspace Server'
# 'sspi'      - boolean. use IWA instead of user/pw to connect to the IOM workspace server


iomlinux = {'java'      : '/usr/bin/java',
            'iomhost'   : 'linux.iom.host',
            'iomport'   : 8591,
            }

iomwin   = {'java'      : '/usr/bin/java',
            'iomhost'   : 'windows.iom.host',
            'iomport'   : 8591,
            }

winlocal = {'java'      : 'java',
            'encoding'  : 'windows-1252',
            }

winiomlinux = {'java'   : 'java',
            'iomhost'   : 'linux.iom.host',
            'iomport'   : 8591,
            }

winiomwin  = {'java'    : 'java',
            'iomhost'   : 'windows.iom.host',
            'iomport'   : 8591,
            }

winiomIWA  = {'java'    : 'java',
            'iomhost'   : 'windows.iom.host',
            'iomport'   : 8591,
            'sspi'      : True
            }


# For Remote and Local IOM access methods using COM interface
# These configuration definitions are for connecting over IOM using COM. This
# access method is for Windows clients connecting to remote hosts. Local
# SAS instances may also be supported.
#
# This access method does not require a Java dependency.
#
# Valid Keys:
#   iomhost     - Required for remote connections only. The Resolvable SAS
#                 server dns name.
#   iomport     - Required for remote connections only. The SAS workspace
#                 server port. Generally 8591 on standard remote
#                 installations. For local connections, 0 is the default.
#   class_id    - Required for remote connections only. The IOM workspace
#                 server class identifier. Use `PROC IOMOPERATE` to identify
#                 the correct value. This option is ignored on local connections.
#   provider    - [REQUIRED] IOM provider. "sas.iomprovider" is recommended.
#   encoding    - This is the python encoding value that matches the SAS
#                 session encoding of the IOM server.
#   omruser     - SAS user. This option is ignored on local connections.
#   omrpw       - SAS password. This option is ignored on local connections.
#   authkey     - Identifier for credentials to read from .authinfo file.

iomcom = {
    'iomhost' : 'mynode.mycompany.org',
    'iomport' : 8591,
    'provider': 'sas.iomprovider',
    'encoding': 'windows-1252'}


# HTTP access method to connect to the Compute Service
# These need ip addr, other values will be prompted for - python Dict
# valid keys are:
# 'url'     - (Required if ip not specified) The URL to Viya, of the form "http[s]://host.idenifier[:port]".
#             When this is specified, ip= will not be used, as the host's ip is retrieved from the url. Also, ssl= is
#             set based upon http or https and port= is also parsed from the url, if provided, else defaulted based
#             upon the derived ssl= value. So neither ip, port nor ssl are needed when url= is used.
# 'ip'      - (Required if url not specified) The resolvable host name, or IP address to the Viya Compute Service
# 'port'    - port; the code Defaults this to based upon the 'ssl' key; 443 default else 80
# 'ssl'     - whether to use HTTPS or just HTTP protocal. Default is True, using ssl and poort 443
# 'context' - context name defined on the compute service  [PROMTED for at runtime if more than one defined]
# 'authkey' - identifier for user/password credentials to read from .authinfo file. Eliminates prompting for credentials.
# 'options' - SAS options to include (no '-' (dashes), just option names and values)
# 'user'    - not suggested [REQUIRED but PROMTED for at runtime]
# 'pw'      - really not suggested [REQUIRED but PROMTED for at runtime]
#
#

httpsviya = {'url'     : 'https://viya.deployment.com',
             'context' : 'SAS Studio compute context',
             'authkey' : 'viya_user-pw',
             'options' : ["fullstimer", "memsize=1G"]
             }

httpviya = {'url'     : 'https://sastpw.rndk8s.openstack.sas.com:23456',
           #'port'    :  23456,   # can put different port here or ^ if it's not using the default port
            'context' : 'SAS Studio compute context',
            'authkey' : 'viya_user-pw',
            'options' : ["fullstimer", "memsize=1G"]
            }
