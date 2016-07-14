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
import re
import logging
from saspy.sasproccommons import SASProcCommons

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# create logging
# logging = logging.getLogger('')
# logging.setLevel(logging.WARN)


class SASstat:
    def __init__(self, session, *args, **kwargs):
        """
        Submit an initial set of macros to prepare the SAS system
        """
        self.sas=session
        logging.debug("Initialization of SAS Macro: " + self.sas.saslog())

    def hpsplit(self, **kwargs: dict) -> object:
        """
        Python method to call the HPSPLIT procedure

        required_set = {}
        legal_set= {'cls', 'code', 'grow', 'id', 'model', 'out'
                    'partition', 'performance', 'prune', 'rules'}
        For more information on the statements see the Documentation link.
        cls is an alias for the class statement
        Documentation link:
        http://support.sas.com/documentation/cdl/en/stathpug/68163/HTML/default/viewer.htm#stathpug_hpsplit_syntax.htm
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {}
        legal_set= {'cls', 'code', 'grow', 'id', 'model', 'out',
                    'partition', 'performance', 'prune', 'rules', 'target','input'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPSPLIT", required_set, legal_set, **kwargs)

    def reg(self, **kwargs: dict) -> object:
        """
        Python method to call the REG procedure
        For more information on the statements see the Documentation link.
        required_set={'model'}
        legal_set= {'add', 'by', 'code', 'id', 'var',
                    'lsmeans', 'model', 'random', 'repeated',
                    'slice', 'test', 'weight', 'out'}
        Documentation link:
        http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_reg_syntax.htm

        :param kwargs: dict
        :return: SAS result object
        """
        required_set={'model'}
        legal_set= {'add', 'by', 'code', 'id', 'var',
                    'lsmeans', 'model', 'random', 'repeated',
                    'slice', 'test', 'weight', 'out'}

        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "REG", required_set, legal_set, **kwargs)

    def mixed(self, **kwargs: dict) -> object:
        """
        Python method to call the MIXED procedure
        For more information on the statements see the Documentation link.
        required_set={'model'}
        legal_set= {'by', 'cls', 'code', 'contrast', 'estimate', 'id',
                    'lsmeans', 'model', 'out', 'random', 'repeated',
                    'slice', 'weight'}
        cls is an alias for the class statement
        Documentation link:
        http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_mixed_toc.htm

        :param kwargs: dict
        :return: SAS result object
        """
        required_set={'model'}
        legal_set= {'by', 'cls', 'code', 'contrast', 'estimate', 'id',
                    'lsmeans', 'model', 'out', 'random', 'repeated',
                    'slice', 'weight'}

        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "MIXED", required_set, legal_set, **kwargs)

    def glm(self, **kwargs: dict) -> object:
        """
        Python method to call the GLM procedure
        For more information on the statements see the Documentation link.
        required_set={'model'}
        legal_set= {'absorb', 'by', 'cls', 'contrast', 'estimate', 'freq', 'id',
                    'lsmeans', 'manova', 'means', 'model', 'out', 'random', 'repeated',
                    'test', 'weight'}

        cls is an alias for the class statement
        Documentation link:
        http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_glm_toc.htm

        :param kwargs: dict
        :return: SAS result object
        """
        required_set={'model'}
        legal_set= {'absorb', 'by', 'cls', 'contrast', 'estimate', 'freq', 'id',
                    'lsmeans', 'manova', 'means', 'model', 'out', 'random', 'repeated',
                    'test', 'weight'}

        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc("GLM", required_set, legal_set, **kwargs)

    def logistic(self, **kwargs: dict) -> object:
        """
        Python method to call the LOGISTIC procedure
        For more information on the statements see the Documentation link.

        required_set={'model'}
        legal_set= {'by', 'cls', 'contrast', 'effect', 'effectplot', 'estimate',
                    'exact', 'freq', 'lsmeans', 'oddsratio', 'out', 'roc', 'score', 'slice',
                    'store', 'strata', 'units', 'weight'}

        cls is an alias for the class statement
        Documentation link:
        http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_logistic_toc.htm

        The PROC LOGISTIC and MODEL statements are required.
        The CLASS and EFFECT statements (if specified) must
        precede the MODEL statement, and the CONTRAST, EXACT,
        and ROC statements (if specified) must follow the MODEL
        statement.

        :param kwargs: dict
        :return: SAS result object
        """
        required_set={'model'}
        legal_set= {'by', 'cls', 'contrast', 'effect', 'effectplot', 'estimate',
                    'exact', 'freq', 'lsmeans', 'oddsratio', 'out', 'roc', 'score', 'slice',
                    'store', 'strata', 'units', 'weight'}

        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc("LOGISTIC", required_set, legal_set, **kwargs)

