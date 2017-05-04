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
import logging
from saspy.sasproccommons import SASProcCommons
from saspy.sasresults import SASresults


class SASutil:
    """
    This class is for SAS BASE procedures to be called as python3 objects and use SAS as the computational engine

    This class and all the useful work in this package require a licensed version of SAS.

    To add a new procedure do the following:

    #.  Create a new method for the procedure
    #.  Create the set of required statements. If there are no required statements then create an empty set {}
    #. Create the legal set of statements. This can often be obtained from the documentation of the procedure. 'procopts' should always be included in the legal set to allow flexibility in calling the procedure.
    #. Create the doc string with the following parts at a minimum:

        - Procedure Name
        - Required set
        - Legal set
        - Link to the procedure documentation

    #. Add the return call for the method using an existing procedure as an example
    #. Verify that all the statements in the required and legal sets are listed in _makeProcCallMacro method of sasproccommons.py
    #. Write at least one test to exercise the procedures and include it in the appropriate testing file
    """

    def __init__(self, session, *args, **kwargs):
        """
        Submit an initial set of macros to prepare the SAS system

        :param session:
        :param args:
        :param kwargs:
        """
        self.sasproduct = "util"
        # create logging
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sas = session
        logging.debug("Initialization of SAS Macro: " + self.sas.saslog())

    def hpimpute(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPIMPUTE procedure

        ``required_set = {'impute'}``

        ``legal_set = {'input', 'impute', 'performance', 'id', 'freq', 'code', 'procopts'}``

        For more information on the statements see the Documentation link.
        Documentation link:
        http://support.sas.com/documentation/cdl/en/stathpug/68163/HTML/default/viewer.htm#stathpug_hpsplit_syntax.htm

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'impute'}
        legal_set = {'input', 'impute', 'performance', 'id', 'freq', 'code',
                     'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPIMPUTE", required_set, legal_set, **kwargs)

    def hpbin(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPBIN procedure

        ``required_set = {}``

        ``legal_set= {'cls', 'code', 'grow', 'id', 'model', 'out', 'partition', 'performance', 'prune', 'rules'}``

        cls is an alias for the class statement
        For more information on the statements see the Documentation link.
        Documentation link:
        http://support.sas.com/documentation/cdl/en/stathpug/68163/HTML/default/viewer.htm#stathpug_hpsplit_syntax.htm

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {}
        legal_set = {'code', 'id', 'performance', 'target', 'input', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPBIN", required_set, legal_set, **kwargs)


    def hpsample(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPSAMPLE procedure

        ``required_set = {}``

        ``legal_set= {'cls', 'code', 'grow', 'id', 'model', 'out'
        'partition', 'performance', 'prune', 'rules'}``

        cls is an alias for the class statement
        For more information on the statements see the Documentation link.
        Documentation link:
        http://support.sas.com/documentation/cdl/en/stathpug/68163/HTML/default/viewer.htm#stathpug_hpsplit_syntax.htm

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {}
        legal_set = { 'class', 'performance', 'target', 'var', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPSAMPLE", required_set, legal_set, **kwargs)
