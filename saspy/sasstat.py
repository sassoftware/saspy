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
from saspy.sasdecorator import procDecorator
from saspy.sasresults   import SASresults

# from pdb import set_trace as bp


class SASstat:
    """
    This class is for SAS/STAT procedures to be called as python3 objects and use SAS as the computational engine

    This class and all the useful work in this package require a licensed version of SAS.

    #. Identify the product of the procedure (SAS/STAT, SAS/ETS, SAS Enterprise Miner, etc).
    #. Find the corresponding file in saspy sasstat.py, sasets.py, sasml.py, etc.
    #. Create a set of valid statements. Here is an example:

        .. code-block:: ipython3

            lset = {'ARIMA', 'BY', 'ID', 'MACURVES', 'MONTHLY', 'OUTPUT', 'VAR'}

        The case and order of the items will be formated.
    #. Call the `doc_convert` method to generate then method call as well as the docstring markup

        .. code-block:: ipython3

            import saspy
            print(saspy.sasdecorator.procDecorator.doc_convert(lset, 'x11')['method_stmt'])
            print(saspy.sasdecorator.procDecorator.doc_convert(lset, 'x11')['markup_stmt'])


        The `doc_convert` method takes two arguments: a list of the valid statements and the proc name. It returns a dictionary with two keys, method_stmt and markup_stmt. These outputs can be copied into the appropriate product file.

    #. Add the proc decorator to the new method.
        The decorator should be on the line above the method declaration.
        The decorator takes one argument, the required statements for the procedure. If there are no required statements than an empty list `{}` should be passed.
        Here are two examples one with no required arguments:

        .. code-block:: ipython3

            @procDecorator.proc_decorator({})
            def esm(self, data: ['SASdata', str] = None, ...

        And one with required arguments:

        .. code-block:: ipython3

            @procDecorator.proc_decorator({'model'})
            def mixed(self, data: ['SASdata', str] = None, ...

    #. Add a link to the SAS documentation plus any additional details will be helpful to users

    #. Write at least one test to exercise the procedures and include it in the
       appropriate testing file.

    If you have questions, please open an issue in the GitHub repo and the maintainers will be happy to help.
    """

    def __init__(self, session, *args, **kwargs):
        """
        Submit an initial set of macros to prepare the SAS system
        """
        self.sasproduct = 'stat'
        # create logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sas = session
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

    @procDecorator.proc_decorator({})
    def hpsplit(self, data: ('SASdata', str) = None,
                cls: (str, list) = None,
                code: str = None,
                grow: str = None,
                id: str = None,
                input: (str, list, dict) = None,
                model: str = None,
                out: (str, bool, 'SASdata') = None,
                partition: str = None,
                performance: str = None,
                prune: str = None,
                rules: str = None,
                target: (str, list, dict) = None,
                procopts: str = None,
                stmtpassthrough: str = None,
                **kwargs: dict) -> SASresults:
        """
        Python method to call the HPSPLIT procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=stathpug&docsetTarget=stathpug_hpsplit_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm code: The code variable can only be a string type.
        :parm grow: The grow variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm model: The model variable can only be a string type.
        :parm out: The out variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm partition: The partition variable can only be a string type.
        :parm performance: The performance variable can only be a string type.
        :parm prune: The prune variable can only be a string type.
        :parm rules: The rules variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'model'})
    def reg(self, data: ('SASdata', str) = None,
            add: str = None,
            by: str = None,
            code: str = None,
            id: str = None,
            lsmeans: str = None,
            model: str = None,
            out: (str, bool, 'SASdata') = None,
            random: str = None,
            repeated: str = None,
            slice: str = None,
            test: str = None,
            var: str = None,
            weight: str = None,
            procopts: str = None,
            stmtpassthrough: str = None,
            **kwargs: dict) -> SASresults:
        """
        Python method to call the REG procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=statug&docsetTarget=statug_reg_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm add: The add variable can only be a string type.
        :parm by: The by variable can only be a string type.
        :parm code: The code variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm lsmeans: The lsmeans variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm out: The out variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm random: The random variable can only be a string type.
        :parm repeated: The repeated variable can only be a string type.
        :parm slice: The slice variable can only be a string type.
        :parm test: The test variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'model'})
    def mixed(self, data: ('SASdata', str) = None,
              by: str = None,
              cls: (str, list) = None,
              code: str = None,
              contrast: str = None,
              estimate: str = None,
              id: str = None,
              lsmeans: str = None,
              model: str = None,
              out: (str, bool, 'SASdata') = None,
              random: str = None,
              repeated: str = None,
              slice: str = None,
              weight: str = None,
              procopts: str = None,
              stmtpassthrough: str = None,
              **kwargs: dict) -> SASresults:
        """
        Python method to call the MIXED procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=statug&docsetTarget=statug_mixed_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm code: The code variable can only be a string type.
        :parm contrast: The contrast variable can only be a string type.
        :parm estimate: The estimate variable is a string, or list of strings for procs that support multiple estimate statements.
        :parm id: The id variable can only be a string type.
        :parm lsmeans: The lsmeans variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm out: The out variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm random: The random variable can only be a string type.
        :parm repeated: The repeated variable can only be a string type.
        :parm slice: The slice variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object

        """

    @procDecorator.proc_decorator({'model'})
    def glm(self, data: ('SASdata', str) = None,
            absorb: str = None,
            by: str = None,
            cls: (str, list) = None,
            contrast: str = None,
            estimate: str = None,
            freq: str = None,
            id: str = None,
            lsmeans: str = None,
            manova: str = None,
            means: str = None,
            model: str = None,
            out: (str, bool, 'SASdata') = None,
            random: str = None,
            repeated: str = None,
            test: str = None,
            weight: str = None,
            procopts: str = None,
            stmtpassthrough: str = None,
            **kwargs: dict) -> SASresults:
        """
        Python method to call the GLM procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=statug&docsetTarget=statug_glm_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm absorb: The absorb variable can only be a string type.
        :parm by: The by variable can only be a string type.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm contrast: The contrast variable can only be a string type.
        :parm estimate: The estimate variable is a string, or list of strings for procs that support multiple estimate statements.
        :parm freq: The freq variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm lsmeans: The lsmeans variable can only be a string type.
        :parm manova: The manova variable can only be a string type.
        :parm means: The means variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm out: The out variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm random: The random variable can only be a string type.
        :parm repeated: The repeated variable can only be a string type.
        :parm test: The test variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'model'})
    def logistic(self, data: ('SASdata', str) = None,
                 by: str = None,
                 cls: (str, list) = None,
                 contrast: str = None,
                 effect: str = None,
                 effectplot: str = None,
                 estimate: str = None,
                 exact: str = None,
                 freq: str = None,
                 lsmeans: str = None,
                 oddsratio: str = None,
                 out: (str, bool, 'SASdata') = None,
                 roc: str = None,
                 score: (str, bool, 'SASdata') = True,
                 slice: str = None,
                 store: str = None,
                 strata: str = None,
                 units: str = None,
                 weight: str = None,
                 procopts: str = None,
                 stmtpassthrough: str = None,
                 **kwargs: dict) -> SASresults:
        """
        Python method to call the LOGISTIC procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=statug&docsetTarget=statug_logistic_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm absorb: The absorb variable can only be a string type.
        :parm by: The by variable can only be a string type.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm contrast: The contrast variable can only be a string type.
        :parm estimate: The estimate variable is a string, or list of strings for procs that support multiple estimate statements.
        :parm freq: The freq variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm lsmeans: The lsmeans variable can only be a string type.
        :parm manova: The manova variable can only be a string type.
        :parm means: The means variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm out: The out variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm random: The random variable can only be a string type.
        :parm repeated: The repeated variable can only be a string type.
        :parm test: The test variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object

        """

    @procDecorator.proc_decorator({'model'})
    def tpspline(self, data: ('SASdata', str) = None,
                 by: str = None,
                 freq: str = None,
                 id: str = None,
                 model: str = None,
                 output: (str, bool, 'SASdata') = None,
                 score: (str, bool, 'SASdata') = True,
                 procopts: str = None,
                 stmtpassthrough: str = None,
                 **kwargs: dict) -> SASresults:
        """
        Python method to call the TPSPLINE procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=statug&docsetTarget=statug_tpspline_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm freq: The freq variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm output: The output variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm score: The score variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object

        """

    @procDecorator.proc_decorator({'model'})
    def hplogistic(self, data: ('SASdata', str) = None,
                   by: str = None,
                   cls: (str, list) = None,
                   code: str = None,
                   freq: str = None,
                   id: str = None,
                   model: str = None,
                   out: (str, bool, 'SASdata') = None,
                   partition: str = None,
                   score: (str, bool, 'SASdata') = True,
                   selection: str = None,
                   weight: str = None,
                   procopts: str = None,
                   stmtpassthrough: str = None,
                   **kwargs: dict) -> SASresults:
        """
        Python method to call the HPLOGISTIC procedure

        Documentation link.
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=stathpug&docsetTarget=stathpug_hplogistic_toc.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm code: The code variable can only be a string type.
        :parm freq: The freq variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm out: The out variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm partition: The partition variable can only be a string type.
        :parm score: The score variable can only be a string type.
        :parm selection: The selection variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'model'})
    def hpreg(self, data: ('SASdata', str) = None,
              by: str = None,
              cls: (str, list) = None,
              code: str = None,
              freq: str = None,
              id: str = None,
              model: str = None,
              out: (str, bool, 'SASdata') = None,
              partition: str = None,
              performance: str = None,
              score: (str, bool, 'SASdata') = True,
              selection: str = None,
              weight: str = None,
              procopts: str = None,
              stmtpassthrough: str = None,
              **kwargs: dict) -> SASresults:
        """
        Python method to call the HPREG procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=stathpug&docsetTarget=stathpug_hpreg_toc.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm code: The code variable can only be a string type.
        :parm freq: The freq variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm out: The out variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm partition: The partition variable can only be a string type.
        :parm performance: The performance variable can only be a string type.
        :parm score: The score variable can only be a string type.
        :parm selection: The selection variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'model'})
    def phreg(self, data: ('SASdata', str) = None,
              assess: str = None,
              bayes: str = None,
              by: str = None,
              cls: (str, list) = None,
              contrast: str = None,
              effect: str = None,
              estimate: str = None,
              freq: str = None,
              hazardratio: str = None,
              id: str = None,
              lsmeans: str = None,
              lsmestimate: str = None,
              model: str = None,
              out: (str, bool, 'SASdata') = None,
              random: str = None,
              roc: str = None,
              slice: str = None,
              store: str = None,
              strata: str = None,
              test: str = None,
              weight: str = None,
              procopts: str = None,
              stmtpassthrough: str = None,
              **kwargs: dict) -> SASresults:
        """
        Python method to call the PHREG procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=statug&docsetTarget=statug_phreg_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm assess: The assess variable can only be a string type.
        :parm bayes: The bayes variable can only be a string type.
        :parm by: The by variable can only be a string type.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm contrast: The contrast variable can only be a string type.
        :parm effect: The effect variable can only be a string type.
        :parm estimate: The estimate variable is a string, or list of strings for procs that support multiple estimate statements.
        :parm freq: The freq variable can only be a string type.
        :parm hazardratio: The hazardratio variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm lsmeans: The lsmeans variable can only be a string type.
        :parm lsmestimate: The lsmestimate variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm out: The out variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm random: The random variable can only be a string type.
        :parm roc: The roc variable can only be a string type.
        :parm slice: The slice variable can only be a string type.
        :parm store: The store variable can only be a string type.
        :parm strata: The strata variable can only be a string type.
        :parm test: The test variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def ttest(self, data: ('SASdata', str) = None,
              by: str = None,
              cls: (str, list) = None,
              freq: str = None,
              paired: str = None,
              var: str = None,
              weight: str = None,
              procopts: str = None,
              stmtpassthrough: str = None,
              **kwargs: dict) -> SASresults:
        """
        Python method to call the TTEST procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=statug&docsetTarget=statug_ttest_toc.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm freq: The freq variable can only be a string type.
        :parm paired: The paired variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def factor(self, data: ('SASdata', str) = None,
               by: (str, list) = None,
               freq: str = None,
               partial: str = None,
               pathdiagram: str = None,
               priors: str = None,
               var: str = None,
               weight: str = None,
               procopts: str = None,
               stmtpassthrough: str = None,
               **kwargs: dict) -> SASresults:
        """
        Python method to call the FACTOR procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=statug&docsetTarget=statug_factor_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required..
        :parm by: The by variable can be a string or list type.
        :parm freq: The freq variable can only be a string type.
        :parm partial: The partial variable can only be a string type.
        :parm pathdiagram: The pathdiagram variable can only be a string type.
        :parm priors: The priors variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def mi(self, data: ('SASdata', str) = None,
           by: (str, list) = None,
           cls: (str, list) = None,
           em: str = None,
           fcs: str = None,
           freq: str = None,
           mcmc: str = None,
           mnar: str = None,
           monotone: str = None,
           transform: str = None,
           var: str = None,
           procopts: str = None,
           stmtpassthrough: str = None,
           **kwargs: dict) -> 'SASresults':
        """
        Python method to call the MI procedure.

        Documentation link:
        https://go.documentation.sas.com/doc/en/statug/15.2/statug_mi_toc.htm

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can be a string or list type.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm em: The em variable can only be a string type.
        :parm fcs: The fcs variable can only be a string type.
        :parm freq: The freq variable can only be a string type.
        :parm mcmc: The mcmc variable can only be a string type.
        :parm mnar: The mnar variable can only be a string type.
        :parm monotone: The monotone variable can only be a string type.
        :parm transform: The transform variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """
