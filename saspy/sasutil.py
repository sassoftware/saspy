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
from saspy.sasdata      import SASdata


class SASutil:
    """
    This class is for SAS BASE procedures to be called as python3 objects and use SAS as the computational engine

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
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

    @procDecorator.proc_decorator({})
    def hpimpute(self, data: ('SASdata', str) = None,
                 code: str = None,
                 freq: str = None,
                 id: str = None,
                 impute: str = None,
                 input: (str, list, dict) = None,
                 performance: str = None,
                 procopts: str = None,
                 stmtpassthrough: str = None,
                 **kwargs: dict) -> SASresults:
        """
        Python method to call the HPIMPUTE procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=prochp&docsetTarget=prochp_hpimpute_toc.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm code: The code variable can only be a string type.
        :parm freq: The freq variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm impute: The impute variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm performance: The performance variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def hpbin(self, data: ('SASdata', str) = None,
              code: str = None,
              freq: str = None,
              id: (str, list) = None,
              input: (str, list, dict) = None,
              performance: str = None,
              target: (str, list, dict) = None,
              procopts: str = None,
              stmtpassthrough: str = None,
              **kwargs: dict) -> SASresults:
        """
        Python method to call the HPBIN procedure.

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=prochp&docsetTarget=prochp_hpbin_syntax.htm&locale=en

        :param data: SASdata object or string. This parameter is required..
        :parm code: The code variable can only be a string type.
        :parm freq: The freq variable can only be a string type.
        :parm id: The id variable can be a string or list type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm performance: The performance variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def hpsample(self, data: ('SASdata', str) = None,
                 cls: (str, list) = None,
                 performance: str = None,
                 target: (str, list, dict) = None,
                 var: str = None,
                 procopts: (str, list, dict) = None,
                 stmtpassthrough: (str, list, dict) = None,
                 **kwargs: dict) -> SASresults:
        """
        Python method to call the HPSAMPLE procedure.

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=prochp&docsetTarget=prochp_hpsample_toc.htm&locale=en

        :param data: SASdata object or string. This parameter is required..
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm performance: The performance variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm var: The var variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def univariate(self, data: ('SASdata', str) = None,
                   by: (str, list) = None,
                   cdfplot: str = None,
                   cls: (str, list) = None,
                   freq: str = None,
                   histogram: str = None,
                   id: (str, list) = None,
                   inset: str = None,
                   output: (str, bool, 'SASdata') = None,
                   ppplot: str = None,
                   probplot: str = None,
                   qqplot: str = None,
                   var: str = None,
                   weight: str = None,
                   procopts: str = None,
                   stmtpassthrough: str = None,
                   **kwargs: dict) -> SASresults:
        """
        Python method to call the UNIVARIATE procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=procstat&docsetTarget=procstat_univariate_syntax.htm&locale=en

        The PROC UNIVARIATE statement invokes the procedure. The VAR statement specifies the numeric variables to be analyzed, and it is required if
        the OUTPUT statement is used to save summary statistics in an output data set. If you do not use the VAR statement, all numeric variables in
        the data set are analyzed. The plot statements (CDFPLOT, HISTOGRAM, PPPLOT, PROBPLOT, and QQPLOT) create graphical displays, and the INSET
        statement enhances these displays by adding a table of summary statistics directly on the graph. You can specify one or more of each of the
        plot statements, the INSET statement, and the OUTPUT statement. If you use a VAR statement, the variables listed in a plot statement must be
        a subset of the variables listed in the VAR statement.

        You can specify a BY statement to obtain separate analyses for each BY group. The FREQ statement specifies a variable whose values provide the
        frequency for each observation. The ID statement specifies one or more variables to identify the extreme observations. The WEIGHT statement
        specifies a variable whose values are used to weight certain statistics.

        You can use a CLASS statement to specify one or two variables that group the data into classification levels. The analysis is carried out for each
        combination of levels in the input data set, or within each BY group if you also specify a BY statement. You can use the CLASS statement with plot
        statements to create comparative displays, in which each cell contains a plot for one combination of classification levels.




        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can be a string or list type.
        :parm cdfplot: The cdfplot variable can only be a string type.
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm freq: The freq variable can only be a string type.
        :parm histogram: The histogram variable can only be a string type.
        :parm id: The id variable can be a string or list type.
        :parm inset: The inset variable can only be a string type.
        :parm output: The output variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm ppplot: The ppplot variable can only be a string type.
        :parm probplot: The probplot variable can only be a string type.
        :parm qqplot: The qqplot variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """
