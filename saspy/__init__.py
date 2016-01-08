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
import os
print ("after os")
from saspy.pysas34 import *
print ("after pysas34")
from saspy.sasstat import *
from saspy.sasets  import *
from saspy.SASLogLexer import *
print ("after all saspy import")
SAS = SAS_session()       
sas = SAS
executable = os.environ.get('SAS_EXECUTABLE', 'sas')
if executable=='sas':
    executable='/opt/sasinside/SASHome/SASFoundation/9.4/sas'
e2=executable.split('/')
_path='/'.join(e2[0:e2.index('SASHome')+1])
_version=e2[e2.index('SASFoundation')+1]
print ("after exec " + _path + _version)
print("SAS session available as 'SAS'. Pid="+str(sas._startsas(path=_path, version=_version)))
