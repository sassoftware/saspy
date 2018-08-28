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
import sys
from functools import wraps
from saspy.sasproccommons import SASProcCommons
from saspy.sasresults import SASresults
from saspy.sasbase import SASdata
#from pdb import set_trace as bp


class SASstat:
    """
    This class is for SAS/STAT procedures to be called as python3 objects and use SAS as the computational engine

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
        self.sasproduct = "stat"
        # create logging
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sas = session
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())
        if sys.version_info[0] < 3 or (sys.version_info[0] >= 3 and sys.version_info[1] >= 4):
            raise SyntaxWarning("Python 3.4 is required to get correct tab complete and docstring "
                                "information for methods")


    def proc_decorator(req_set):
        """
        Decorator that provides the wrapped function with an attribute 'actual_kwargs'
        containing just those keyword arguments actually passed in to the function.
        """

        def decorator(func):
            @wraps(func)
            def inner(self, *args, **kwargs):
                inner.proc_decorator = kwargs
                self.logger.debug("processing proc:{}".format(func.__name__))
                self.logger.debug(kwargs.keys())
                self.logger.debug(req_set)
                legal_set = set(kwargs.keys())
                self.logger.debug(legal_set)
                self.logger.debug("kwargs type: " + str(type(kwargs)))
                return SASProcCommons._run_proc(self, func.__name__.lower(), req_set, legal_set, **kwargs)
            return inner

        return decorator

    @proc_decorator({})
    def hpsplit(self, data: 'SASData' = None,
                target: [str, list, dict] = None,
                input: [str, list, dict] = None,
                partition: [str, dict] = 'Rolevar',
                score: [bool, str] = True,
                **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPSPLIT procedure
        For more information on the statements see the Documentation link.
        Documentation link:
        http://support.sas.com/documentation/cdl/en/stathpug/68163/HTML/default/viewer.htm#stathpug_hpsplit_syntax.htm

        ``legal_set= {'cls', 'code', 'grow', 'id', 'model', 'out', 'partition', 'performance', 'prune', 'rules'}``


        :param data: SASData object This parameter is required
        :param target: The target can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :param input:   The input can be a string, list or dict type. It refers to the independent or X variables.
        :param partition:
        :param score:
        :return: SAS result object
        """
    @proc_decorator({'model'})
    def reg(self, data: 'SASData' = None,
            model: str = None,
            by: str = None,
            id: str = None,
            var: [str, list] = None,
            lsmeans: str = None,
            random: str = None,
            repeated: str = None,
            slice: str = None,
            test: str = None,
            weight: str = None,
            score: [bool, 'SASdata'] = True,
            **kwargs: dict) -> 'SASresults':
        """
        Python method to call the REG procedure

        For more information on the statements see the Documentation link.
        Documentation link:
        http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_reg_syntax.htm

        :param data:
        :param model:
        :param by:
        :param id:
        :param var:
        :param lsmeans:
        :param random:
        :param repeated:
        :param slice:
        :param test:
        :param weight: takes a single variable
        :param score:
        :param kwargs: dict
        :return: SAS result object
        """
    def mixed(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the MIXED procedure

        cls is an alias for the class statement
        For more information on the statements see the Documentation link.

        ``required_set={'model'}``

        ``legal_set= {'by', 'cls', 'code', 'contrast', 'estimate', 'id', 'lsmeans', 'model',
        'out', 'random', 'repeated', 'slice', 'weight'}``

        Documentation link:
        http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_mixed_toc.htm

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'model'}
        legal_set = {'by', 'cls', 'code', 'contrast', 'estimate', 'id',
                     'lsmeans', 'model', 'out', 'random', 'repeated',
                     'slice', 'weight', 'procopts'}

        self.logger.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "MIXED", required_set, legal_set, **kwargs)

    def glm(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the GLM procedure

        For more information on the statements see the Documentation link.

        ``required_set={'model'}``

        ``legal_set= {'absorb', 'by', 'cls', 'contrast', 'estimate', 'freq', 'id', 'lsmeans', 'manova',
        'means', 'model', 'out', 'random', 'repeated', 'test', 'weight'}``

        cls is an alias for the class statement

        Documentation link:
        http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_glm_toc.htm

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'model'}
        legal_set = {'absorb', 'by', 'cls', 'contrast', 'estimate', 'freq', 'id',
                     'lsmeans', 'manova', 'means', 'model', 'out', 'random', 'repeated',
                     'test', 'weight', 'procopts'}

        self.logger.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "GLM", required_set, legal_set, **kwargs)

    def logistic(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the LOGISTIC procedure

        For more information on the statements see the Documentation link.

        ``required_set={'model'}``

        ``legal_set= {'by', 'cls', 'contrast', 'effect', 'effectplot', 'estimate', 'exact', 'freq',
        'lsmeans', 'oddsratio', 'out', 'roc', 'score', 'slice', 'store', 'strata', 'units', 'weight'}``

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
        required_set = {'model'}
        legal_set = {'by', 'cls', 'contrast', 'effect', 'effectplot', 'estimate',
                     'exact', 'freq', 'lsmeans', 'oddsratio', 'out', 'roc', 'score', 'slice',
                     'store', 'strata', 'units', 'weight', 'procopts'}

        self.logger.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "LOGISTIC", required_set, legal_set, **kwargs)

    def tpspline(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the TPSPLINE procedure

        For more information on the statements see the Documentation link.

        ``required_set = {'model'}``

        ``legal_set = {'by', 'freq', 'id', 'model', 'output', 'score', 'procopts'}``

        cls is an alias for the class statement

        Documentation link:
        http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_tpspline_toc.htm

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'model'}
        legal_set = {'by', 'freq', 'id', 'model', 'output', 'score', 'procopts'}

        self.logger.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "TPSPLINE", required_set, legal_set, **kwargs)

    def hplogistic(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPLOGISTIC procedure

        For more information on the statements see the Documentation link.

        ``required_set={'model'}``

        ``legal_set= {'by', 'cls', 'code', 'freq', 'id', 'model',
        'out', 'partition', 'score', 'selection', 'weight'}``

        cls is an alias for the class statement
        Documentation link:
        https://support.sas.com/documentation/onlinedoc/stat/141/hplogistic.pdf

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'model'}
        legal_set = {'by', 'cls', 'code', 'freq', 'id', 'model', 'out',
                     'partition', 'score', 'selection', 'weight'}

        self.logger.debug("kwargs type: " + str(type(kwargs)))

        # ODS graphics are created by default for STAT this stops them form generation
        kwargs['ODSGraphics']=False
        return SASProcCommons._run_proc(self, "HPLOGISTIC", required_set, legal_set, **kwargs)

    def hpreg(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPREG procedure
        For more information on the statements see the Documentation link.

        ``required_set={'model'}``

        ``legal_set = {'by', 'cls', 'code', 'freq', 'id', 'model', 'out',
        'partition', 'performance', 'score', 'selection', 'weight'}``

        cls is an alias for the class statement

        Documentation link:
        https://support.sas.com/documentation/onlinedoc/stat/141/hpreg.pdf

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'model'}
        legal_set = {'by', 'cls', 'code', 'freq', 'id', 'model', 'out',
                     'partition', 'performance', 'score', 'selection', 'weight'}

        self.logger.debug("kwargs type: " + str(type(kwargs)))
        kwargs['ODSGraphics']=False
        return SASProcCommons._run_proc(self, "HPREG", required_set, legal_set, **kwargs)

    def phreg(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the PHREG procedure
        For more information on the statements see the Documentation link.

        ``required_set = {'model'}``

        ``legal_set = {'assess', 'bayes', 'by', 'cls', 'contrast', 'freq', 'effect', 'estimate', 
                     'hazardratio', 'id', 'lsmeans', 'lsmestimate', 'model', 'out', 'roc', 
                     'random', 'slice', 'store', 'strata', 'test', 'weight', 'procopts'}``

        cls is an alias for the class statement

        Documentation link:
        http://go.documentation.sas.com/?docsetId=statug&docsetTarget=statug_phreg_toc.htm&docsetVersion=14.2&locale=en

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'model'}
        legal_set = {'assess', 'bayes', 'by', 'cls', 'contrast', 'freq', 'effect', 'estimate',
                     'hazardratio', 'id', 'lsmeans', 'lsmestimate', 'model', 'out', 'roc',
                     'random', 'slice', 'store', 'strata', 'test', 'weight', 'procopts'}

        self.logger.debug("kwargs type: " + str(type(kwargs)))
        kwargs['ODSGraphics']=True
        return SASProcCommons._run_proc(self, "PHREG", required_set, legal_set, **kwargs)

    def ttest(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the PHREG procedure
        For more information on the statements see the Documentation link.

        ``required_set = {}``

        ``legal_set = {'by', 'cls', 'freq', 'paired', 'var', 'weight', 'procopts'}``

        cls is an alias for the class statement

        Documentation link:
        http://go.documentation.sas.com/?docsetId=statug&docsetVersion=14.2&docsetTarget=statug_ttest_overview.htm&locale=en

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {}
        legal_set = {'by', 'cls', 'freq', 'paired', 'var', 'weight', 'procopts'}

        self.logger.debug("kwargs type: " + str(type(kwargs)))
        kwargs['ODSGraphics']=True
        return SASProcCommons._run_proc(self, "TTEST", required_set, legal_set, **kwargs)

    def factor(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the PHREG procedure
        For more information on the statements see the Documentation link.

        ``required_set = {}``

        ``legal_set = {'by', 'cls', 'freq', 'paired', 'var', 'weight', 'procopts'}``

        Documentation link:
        http://go.documentation.sas.com/?docsetId=statug&docsetVersion=14.2&docsetTarget=statug_factor_overview.htm&locale=en

        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {}
        legal_set = {'by', 'freq', 'priors', 'pathdiagram', 'partial', 'var', 'weight', 'procopts'}

        self.logger.debug("kwargs type: " + str(type(kwargs)))
        kwargs['ODSGraphics']=True
        return SASProcCommons._run_proc(self, "FACTOR", required_set, legal_set, **kwargs)

