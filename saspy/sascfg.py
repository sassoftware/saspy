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
# Configuration names for SAS - python List
# 
# SAS_config_names=['default', 'sasother']
#
SAS_config_names = ['default']

# Configuration options for pysas - python Dict
# valid key are:
# 
# 'lock_down' - True | False. True = Prevent runtime overrides of SAS_Config values below
#
SAS_config_options = {'lock_down': True}

# These need path to SASHome and version number - python Dict
# The default path to the sas start up script is: /opt/sasinside/SASHome/SASFoundation/9.4/sas
# A usual install path is: /opt/sasinside/SASHome/SASFoundation/9.4/sas
# valid keys are:
# 'saspath' - path to SAS startup script i.e.: /opt/sasinside/SASHome/SASFoundation/9.4/sas
# 'options' - SAS options to include in the start up command line - Python List
#
#
#
default = {'saspath': '/opt/sasinside/SASHome/SASFoundation/9.4/sas',
           }

# sasother={'saspath' : '/some/other/directory/SASHome/SASFoundation/9.4/sas',
#           'options' : ["-autoexec", "/my/home_dir/my_autoexec.sas", "-set",
#                       "Env_var", "Value", "-fullstimer"]
#           }

