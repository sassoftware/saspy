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


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from saspy.version import __version__
from saspy.sasbase import SASsession, SASconfig, list_configs
from saspy.sasdata import SASdata
from saspy.sasexceptions import SASIONotSupportedError, SASConfigNotFoundError, SASConfigNotValidError
from saspy.sasproccommons import SASProcCommons
from saspy.sastabulate import Tabulate
from saspy.sasresults import SASresults

import os, sys

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)
logger.propagate=False

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
    from saspy.sas_magic import SASMagic
    get_ipython().register_magics(SASMagic)

def _find_cfg():
   sp    = []
   sp[:] = sys.path
   sp[0] = os.path.abspath(sp[0])
   sp.insert(1, os.path.expanduser('~/.config/saspy'))
   sp.insert(0, __file__.rsplit(os.sep+'__init__.py')[0])

   cfg = 'Not found'

   for dir in sp:
      f1 = dir+os.sep+'sascfg_personal.py'
      if os.path.isfile(f1):
         cfg = f1
         break

   if cfg == 'Not found':
      f1 =__file__.rsplit('__init__.py')[0]+'sascfg.py'
      if os.path.isfile(f1):
         cfg = f1

   return cfg

SAScfg = _find_cfg()
