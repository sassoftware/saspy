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


# create logging
# logging = logging.getLogger(__name__)
# logging.addHandler(logging.NullHandler)
# logging.setLevel(logging.DEBUG)


class SASViyaML:
    """
    This class is for SAS/STAT procedures to be called as python3 objects and use SAS as the computational engine
    This class and all the useful work in this package require a licensed version of SAS.
    To add a new procedure do the following:
    1. Create a new method for the procedure
    2. Create the set of required statements. If there are no required statements then create an empty set {}
    3. Create the legal set of statements. This can often be obtained from the documentation of the procedure.
        'procopts' should always be included in the legal set to allow flexibility in calling the procedure.
    4. Create the doc string with the following parts at a minimum:
        A. Procedure Name
        B. Required set
        C. Legal set
        D. Link to the procedure documentation
    5. Add the return call for the method using an existing procedure as an example
    6. Verify that all the statements in the required and legal sets are listed in _makeProcCallMacro method
        of sasproccommons.py
    7. Write at least one test to exercise the procedures and include it in the appropriate testing file
    """
    def __init__(self, session, *args, **kwargs):
        """
        Submit an initial set of macros to prepare the SAS system
        """
        self.sasproduct = "vddml"
        # create logging
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sas = session
        logging.debug("Initialization of SAS Macro: " + self.sas.saslog())

    def factmac(self, **kwargs: dict) -> object:
        """
        Python method to call the FACTMAC procedure

        required_set = {'input', 'target'}
        legal_set= {'code','input', 'id', 'output', 'savestate', 'target', 'autotune'}

        Documentation link:
        http://documentation.sas.com/?docsetId=casml&docsetTarget=viyaml_factmac_toc.htm&docsetVersion=8.2&locale=en
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target'}
        legal_set = {'code', 'input', 'id', 'output', 'savestate', 'target', 'autotune'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc("FACTMAC", required_set, legal_set, **kwargs)

    def fastknn(self, **kwargs: dict) -> object:
        """
        Python method to call the FASTKNN procedure

        required_set = {'input', 'id'}
        legal_set = {'input', 'id', 'output'}

        Documentation link:
        http://documentation.sas.com/?docsetId=casml&docsetTarget=viyaml_fastknn_toc.htm&docsetVersion=8.2&locale=en
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'id'}
        legal_set = {'input', 'id', 'output'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc("FASTKNN", required_set, legal_set, **kwargs)

    def forest(self, **kwargs: dict) -> object:
        """

        Python method to call the FOREST procedure

        required_set = {'input', 'target'}
        legal_set = {'autotune', 'code', 'crossvalidation', 'grow', 'id', 'input',
                     'output', 'partition', 'savestate', 'target', 'weight', 'procopts'}

        Documentation link:
        http://documentation.sas.com/?docsetId=casml&docsetTarget=viyaml_forest_toc.htm&docsetVersion=8.2&locale=en
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target'}
        legal_set = {'autotune', 'code', 'crossvalidation', 'grow', 'id', 'input',
                     'output', 'partition', 'savestate', 'target', 'weight', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc("FOREST", required_set, legal_set, **kwargs)

    def gradboost(self, **kwargs: dict) -> object:
        """
        Python method to call the HPCLUS procedure

        legal_set = {'autotune', 'code', 'crossvalidation', 'id', 'input',
                     'output', 'partition', 'savestate', 'target', 'weight', 'procopts'}

        Documentation link:
        http://documentation.sas.com/?docsetId=casml&docsetTarget=viyaml_gradboost_toc.htm&docsetVersion=8.2&locale=en
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target'}
        legal_set = {'autotune', 'code', 'crossvalidation', 'id', 'input',
                     'output', 'partition', 'savestate', 'target', 'weight', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc("GRADBOOST", required_set, legal_set, **kwargs)

    def nnet(self, **kwargs: dict) -> object:
        """
        Python method to call the HPNEURAL procedure

        required_set = {'input', 'target', 'train'}
        legal_set= {'input', 'hidden', 'target', 'train', 'crossvalidation', 'code',
                    'architecture', 'weight', 'optimization', 'partition', 'procopts'}
        Documentation link:
        http://documentation.sas.com/?docsetId=casml&docsetTarget=viyaml_nnet_toc.htm&docsetVersion=8.2&locale=en
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target', 'train'}
        legal_set = {'input', 'hidden', 'target', 'train', 'crossvalidation', 'code',
                     'architecture', 'weight', 'optimization', 'partition', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc("NNET", required_set, legal_set, **kwargs)

    def svdd(self, **kwargs: dict) -> object:
        """
        Python method to call the SVDD procedure

        required_set = {'input'}
        legal_set = {'code', 'input', 'id', 'solver', 'savestate', 'kernel',
                     'weight', 'procopts'}
        Documentation link:
        http://documentation.sas.com/?docsetId=casml&docsetTarget=viyaml_svdd_toc.htm&docsetVersion=8.2&locale=en
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input'}
        legal_set = {'code', 'input', 'id', 'solver', 'savestate', 'kernel',
                     'weight', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc("SVDD", required_set, legal_set, **kwargs)

    def svmachine(self, **kwargs: dict) -> object:
        """
        Python method to call the SVMACHINE procedure
        required_set = {'input'}
        legal_set = {'autotune', 'code', 'input', 'id', 'solver', 'savestate', 'kernel', 'partition','

                     'target', 'procopts'}

        Documentation link:
        http://documentation.sas.com/?docsetId=casml&docsetTarget=viyaml_svmachine_toc.htm&docsetVersion=8.2&locale=en
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target'}
        legal_set = {'autotune', 'code', 'input', 'id', 'savestate', 'kernel',
                     'partition', 'target', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc("SVMACHINE", required_set, legal_set, **kwargs)

    def textmine(self, **kwargs: dict) -> object:
        """
        Python method to call the HPBNET procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        pass
