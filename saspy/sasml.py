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


class SASml:
    """
    This class is for SAS Enterprise Miner procedures to be called as python3 objects and use SAS as the computational engine

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
        """
        self.sasproduct = "em"
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sas = session
        logging.debug("Initialization of SAS Macro: " + self.sas.saslog())

    def forest(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPFOREST procedure

        ``required_set = {'input', 'target'}``

        ``legal_set = {'freq', 'input', 'id',
        'target', 'save', 'score'}``

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target'}
        legal_set = {'freq', 'input', 'id', 'target', 'save', 'score', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPFOREST", required_set, legal_set, **kwargs)

    def hp4score(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HP4SCORE procedure

        ``required_set = {}``

        ``legal_set = {'id', 'importance', 'performance', 'score', 'procopts'}``

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {}
        legal_set = {'id', 'importance', 'performance', 'score', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HP4SCORE", required_set, legal_set, **kwargs)

    def cluster(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPCLUS procedure

        ``required_set = {'input'}``

        ``legal_set= {'freq', 'input', 'id', 'score'}``

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input'}
        legal_set = {'freq', 'input', 'id', 'score', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPCLUS", required_set, legal_set, **kwargs)

    def neural(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPNEURAL procedure

        ``required_set = {'input', 'target', 'train'}``

        ``legal_set = {'architecture', 'code', 'hidden', 'id', 'input',
        'partition', 'score', 'target', 'train', 'procopts'}``

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target', 'train'}
        legal_set = {'architecture', 'code', 'hidden', 'id', 'input',
                     'partition', 'score', 'target', 'train',
                     'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPNEURAL", required_set, legal_set, **kwargs)

    def treeboost(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the TREEBOOST procedure

        ``required_set = {'input', 'target'}``

        ``legal_set = {'assess', 'code', 'freq', 'importance', 'input', 'performance',
        'target', 'save', 'score', 'subseries', 'procopts'}``

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target'}
        legal_set = {'assess', 'code', 'freq', 'importance', 'input', 'performance', 'target', 'save', 'score',
                     'subseries', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "TREEBOOST", required_set, legal_set, **kwargs)

    def hpbnet(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPBNET procedure

        ``required_set = {'input', 'target'}``

        ``legal_set = {'id', 'code', 'freq', 'partition', 'input', 'performance', 'target', 'output', 'procopts'}``

        Documentation link:
        http://go.documentation.sas.com/?docsetId=emhpprcref&docsetVersion=14.2&docsetTarget=emhpprcref_hpbnet_toc.htm&locale=en

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target'}
        legal_set = {'id', 'code', 'freq', 'partition', 'input', 'performance', 'target', 'output', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPBNET", required_set, legal_set, **kwargs)
