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
from typing import TYPE_CHECKING
from saspy.sasdecorator import procDecorator

if TYPE_CHECKING:
    from saspy.sasresults import SASresults
    from saspy.sasbase import SASdata


class SASets:
    """
    This class is for SAS/ETS procedures to be called as python3 objects and use SAS as the computational engine

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
        """Submit an initial set of macros to prepare the SAS system"""
        self.sasproduct = "ets"
        # create logging
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sas = session
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

    @procDecorator.proc_decorator({'id'})
    def timeseries(self, data: ['SASdata', str] = None,
                   by: str = None,
                   corr: str = None,
                   crosscorr: str = None,
                   crossvar: str = None,
                   decomp: str = None,
                   id: str = None,
                   out: [str, 'SASdata'] = None,
                   season: str = None,
                   trend: str = None,
                   var: str = None,
                   procopts: str = None,
                   stmtpassthrough: str = None,
                   **kwargs: dict) -> 'SASresults':
        """
        Python method to call the TIMESERIES procedure

        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeseries_syntax.htm

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm corr: The corr variable can only be a string type.
        :parm crosscorr: The crosscorr variable can only be a string type.
        :parm crossvar: The crossvar variable can only be a string type.
        :parm decomp: The decomp variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm out: The out variable can be a string or SASdata type.
        :parm season: The season variable can only be a string type.
        :parm trend: The trend variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'identify'})
    def arima(self, data: ['SASdata', str] = None,
              by: str = None,
              estimate: str = None,
              forecast: str = None,
              identify: str = None,
              out: [str, 'SASdata'] = None,
              outlier: str = None,
              procopts: str = None,
              stmtpassthrough: str = None,
              **kwargs: dict) -> 'SASresults':
        """
        Python method to call the ARIMA procedure

        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_arima_syntax.htm

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm estimate: The estimate variable can only be a string type.
        :parm forecast: The forecast variable can only be a string type.
        :parm identify: The identify variable can only be a string type.
        :parm out: The out variable can be a string or SASdata type.
        :parm outlier: The outlier variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'model'})
    def ucm(self, data: ['SASdata', str] = None,
            autoreg: str = None,
            blockseason: str = None,
            by: str = None,
            cycle: str = None,
            deplag: str = None,
            estimate: [str, bool] = None,
            forecast: str = None,
            id: str = None,
            irregular: [str, bool] = None,
            level: [str, bool] = None,
            model: str = None,
            nloptions: str = None,
            out: [str, 'SASdata'] = None,
            outlier: str = None,
            performance: str = None,
            randomreg: str = None,
            season: str = None,
            slope: [str, bool] = None,
            splinereg: str = None,
            splineseason: str = None,
            procopts: str = None,
            stmtpassthrough: str = None,
            **kwargs: dict) -> 'SASresults':
        """
        Python method to call the UCM procedure

        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_ucm_syntax.htm

        :param data: SASdata object or string. This parameter is required.
        :parm autoreg: The autoreg variable can only be a string type.
        :parm blockseason: The blockseason variable can only be a string type.
        :parm by: The by variable can only be a string type.
        :parm cycle: The cycle variable can only be a string type.
        :parm deplag: The deplag variable can only be a string type.
        :parm estimate: The estimate variable can be a string or boolean type.
        :parm forecast: The forecast variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm irregular: The irregular variable can be a string or boolean type.
        :parm level: The level variable can be a string or boolean type.
        :parm model: The model variable can only be a string type.
        :parm nloptions: The nloptions variable can only be a string type.
        :parm out: The out variable can be a string or SASdata type.
        :parm outlier: The outlier variable can only be a string type.
        :parm performance: The performance variable can only be a string type.
        :parm randomreg: The randomreg variable can only be a string type.
        :parm season: The season variable can only be a string type.
        :parm slope: The slope variable can be a string or boolean type.
        :parm splinereg: The splinereg variable can only be a string type.
        :parm splineseason: The splineseason variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def esm(self, data: ['SASdata', str] = None,
            by: str = None,
            forecast: str = None,
            id: str = None,
            out: [str, 'SASdata'] = None,
            procopts: str = None,
            stmtpassthrough: str = None,
            **kwargs: dict) -> 'SASresults':
        """
        Python method to call the ESM procedure

        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_esm_syntax.htm

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm forecast: The forecast variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm out: The out variable can be a string or SASdata type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def timeid(self, data: ['SASdata', str] = None,
               by: str = None,
               id: str = None,
               out: [str, 'SASdata'] = None,
               procopts: str = None,
               stmtpassthrough: str = None,
               **kwargs: dict) -> 'SASresults':
        """
        Python method to call the TIMEID procedure

        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeid_syntax.htm

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm out: The out variable can be a string or SASdata type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def timedata(self, data: ['SASdata', str] = None,
                 by: str = None,
                 fcmport: str = None,
                 id: str = None,
                 out: [str, 'SASdata'] = None,
                 outarrays: str = None,
                 outscalars: str = None,
                 prog_stmts: str = None,
                 var: str = None,
                 procopts: str = None,
                 stmtpassthrough: str = None,
                 **kwargs: dict) -> 'SASresults':
        """
        Python method to call the TIMEDATA procedure

        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timedata_syntax.htm

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm fcmport: The fcmport variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm out: The out variable can be a string or SASdata type.
        :parm outarrays: The outarrays variable can only be a string type.
        :parm outscalars: The outscalars variable can only be a string type.
        :parm prog_stmts: The prog_stmts variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def x11(self, data: ['SASdata', str] = None,
            arima: str = None,
            by: [str, list] = None,
            id: [str, list] = None,
            macurves: str = None,
            monthly: str = None,
            output: [str, bool, 'SASdata'] = None,
            pdweights: str = None,
            quarterly: str = None,
            sspan: str = None,
            tables: str = None,
            var: str = None,
            procopts: [str, list] = None,
            stmtpassthrough: [str, list] = None,
            **kwargs: dict) -> 'SASresults':
        """
        Python method to call the X11 procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=etsug&docsetTarget=etsug_x11_syntax.htm&locale=en

        Either the MONTHLY or QUARTERLY statement must be specified, depending on the type of time series data you have.
        The PDWEIGHTS and MACURVES statements can be used only with the MONTHLY statement. The TABLES statement controls
        the printing of tables, while the OUTPUT statement controls the creation of the OUT= data set.

        :param data: SASdata object or string. This parameter is required.
        :parm arima: The arima variable can only be a string type.
        :parm by: The by variable can be a string or list type.
        :parm id: The id variable can be a string or list type.
        :parm macurves: The macurves variable can only be a string type.
        :parm monthly: The monthly variable can only be a string type.
        :parm output: The output variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm pdweights: The pdweights variable can only be a string type.
        :parm quarterly: The quarterly variable can only be a string type.
        :parm sspan: The sspan variable can only be a string type.
        :parm tables: The tables variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def x12(self, data: ['SASdata', str] = None,
            adjust: str = None,
            arima: str = None,
            automdl: str = None,
            by: [str, list] = None,
            check: str = None,
            estimate: [str, bool] = True,
            event: str = None,
            forecast: str = None,
            id: [str, list] = None,
            identify: str = None,
            input: [str, list, dict] = None,
            outlier: str = None,
            output: [str, bool, 'SASdata'] = None,
            pickmdl: str = None,
            regression: str = None,
            seatsdecomp: str = None,
            tables: str = None,
            transform: str = None,
            userdefined: str = None,
            var: str = None,
            x11: str = None,
            procopts: str = None,
            stmtpassthrough: str = None,
            **kwargs: dict) -> 'SASresults':
        """
        Python method to call the X12 procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=etsug&docsetTarget=etsug_x12_toc.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm adjust: The adjust variable can only be a string type.
        :parm arima: The arima variable can only be a string type.
        :parm automdl: The automdl variable can only be a string type.
        :parm by: The by variable can be a string or list type.
        :parm check: The check variable can only be a string type.
        :parm estimate: The estimate variable can only be a string type.
        :parm event: The event variable can only be a string type.
        :parm forecast: The forecast variable can only be a string type.
        :parm id: The id variable can be a string or list type.
        :parm identify: The identify variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm outlier: The outlier variable can only be a string type.
        :parm output: The output variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm pickmdl: The pickmdl variable can only be a string type.
        :parm regression: The regression variable can only be a string type.
        :parm seatsdecomp: The seatsdecomp variable can only be a string type.
        :parm tables: The tables variable can only be a string type.
        :parm transform: The transform variable can only be a string type.
        :parm userdefined: The userdefined variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm x11: The x11 variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def varmax(self, data: ['SASdata', str] = None,
               bound: str = None,
               by: [str, list] = None,
               causal: str = None,
               cointeg: str = None,
               condfore: str = None,
               garch: str = None,
               id: [str, list] = None,
               initial: str = None,
               model: str = None,
               nloptions: str = None,
               output: [str, bool, 'SASdata'] = None,
               restrict: str = None,
               test: str = None,
               procopts: str = None,
               stmtpassthrough: str = None,
               **kwargs: dict) -> 'SASresults':
        """
        Python method to call the VARMAX procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=etsug&docsetTarget=etsug_varmax_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm adjust: The adjust variable can only be a string type.
        :parm arima: The arima variable can only be a string type.
        :parm automdl: The automdl variable can only be a string type.
        :parm by: The by variable can be a string or list type.
        :parm check: The check variable can only be a string type.
        :parm estimate: The estimate variable can only be a string type.
        :parm event: The event variable can only be a string type.
        :parm forecast: The forecast variable can only be a string type.
        :parm id: The id variable can be a string or list type.
        :parm identify: The identify variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm outlier: The outlier variable can only be a string type.
        :parm output: The output variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm pickmdl: The pickmdl variable can only be a string type.
        :parm regression: The regression variable can only be a string type.
        :parm seatsdecomp: The seatsdecomp variable can only be a string type.
        :parm tables: The tables variable can only be a string type.
        :parm transform: The transform variable can only be a string type.
        :parm userdefined: The userdefined variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm x11: The x11 variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def autoreg(self, data: ['SASdata', str] = None,
                by: [str, list] = None,
                cls: [str, list] = None,
                hetero: str = None,
                model: str = None,
                nloptions: str = None,
                output: [str, bool, 'SASdata'] = None,
                restrict: str = None,
                test: str = None,
                procopts: str = None,
                stmtpassthrough: str = None,
                **kwargs: dict) -> 'SASresults':
        """
        Python method to call the AUTOREG procedure

        Documentation link:

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can be a string or list type.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm hetero: The hetero variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm nloptions: The nloptions variable can only be a string type.
        :parm output: The output variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm restrict: The restrict variable can only be a string type.
        :parm test: The test variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """


    @procDecorator.proc_decorator({})
    def expand(self, data: ['SASdata', str] = None,
               by: [str, list] = None,
               convert: str = None,
               id: [str, list] = None,
               procopts: str = None,
               stmtpassthrough: str = None,
               **kwargs: dict) -> 'SASresults':
        """
        Python method to call the EXPAND procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=etsug&docsetTarget=etsug_expand_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can be a string or list type.
        :parm convert: The convert variable can only be a string type.
        :parm id: The id variable can be a string or list type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """
