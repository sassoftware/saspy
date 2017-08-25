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
from saspy.sasbase        import *
from saspy.sasstat        import *
from saspy.sasets         import *
from saspy.sasml          import *
from saspy.sasqc          import *
from saspy.sasresults     import *
from saspy.sasutil        import *
from saspy.sasproccommons import *
from saspy.SASLogLexer    import *
from saspy.version        import __version__

def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

if isnotebook():
	from .sas_magic import SASMagic
	get_ipython().register_magics(SASMagic)
