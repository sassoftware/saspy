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


class SASqc:
    """
    This class is for SAS/QC procedures to be called as python3 objects and use SAS as the computational engine
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
        self.sasproduct = "qc"
        # create logging
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sas = session
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

    @procDecorator.proc_decorator({})
    def cusum(self, data: ['SASdata', str] = None,
              by: str = None,
              inset: str = None,
              xchart: str = None,
              procopts: str = None,
              stmtpassthrough: str = None,
              **kwargs: dict) -> SASresults:
        """
        Python method to call the CUSUM procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=qcug&docsetTarget=qcug_cusum_toc.htm&locale=en
        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm inset: The inset variable can only be a string type.
        :parm xchart: The xchart variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def macontrol(self, data: ['SASdata', str] = None,
                  ewmachart: str = None,
                  machart: str = None,
                  procopts: str = None,
                  stmtpassthrough: str = None,
                  **kwargs: dict) -> SASresults:
        """
        Python method to call the MACONTROL procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=qcug&docsetTarget=qcug_macontrol_toc.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm ewmachart: The ewmachart variable can only be a string type.
        :parm machart: The machart variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def capability(self, data: ['SASdata', str] = None,
                   by: str = None,
                   cdfplot: str = None,
                   comphist: str = None,
                   freq: str = None,
                   histogram: str = None,
                   id: str = None,
                   inset: str = None,
                   intervals: str = None,
                   output: [str, bool, 'SASdata'] = None,
                   ppplot: str = None,
                   probplot: str = None,
                   qqplot: str = None,
                   spec: str = None,
                   weight: str = None,
                   procopts: str = None,
                   stmtpassthrough: str = None,
                   **kwargs: dict) -> SASresults:
        """
        Python method to call the CAPABILITY procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=qcug&docsetTarget=qcug_capability_sect001.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm by: The by variable can only be a string type.
        :parm cdfplot: The cdfplot variable can only be a string type.
        :parm comphist: The comphist variable can only be a string type.
        :parm freq: The freq variable can only be a string type.
        :parm histogram: The histogram variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm inset: The inset variable can only be a string type.
        :parm intervals: The intervals variable can only be a string type.
        :parm output: The output variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm ppplot: The ppplot variable can only be a string type.
        :parm probplot: The probplot variable can only be a string type.
        :parm qqplot: The qqplot variable can only be a string type.
        :parm spec: The spec variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def shewhart(self, data: ['SASdata', str] = None,
                 boxchart: str = None,
                 cchart: str = None,
                 irchart: str = None,
                 mchart: str = None,
                 mrchart: str = None,
                 npchart: str = None,
                 pchart: str = None,
                 rchart: str = None,
                 schart: str = None,
                 uchart: str = None,
                 xrchart: str = None,
                 xschart: str = None,
                 procopts: str = None,
                 stmtpassthrough: str = None,
                 **kwargs: dict) -> SASresults:
        """
        Python method to call the SHEWHART procedure

        Documentation link:
        https://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.4&docsetId=qcug&docsetTarget=qcug_shewhart_toc.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm boxchart: The boxchart variable can only be a string type.
        :parm cchart: The cchart variable can only be a string type.
        :parm irchart: The irchart variable can only be a string type.
        :parm mchart: The mchart variable can only be a string type.
        :parm mrchart: The mrchart variable can only be a string type.
        :parm npchart: The npchart variable can only be a string type.
        :parm pchart: The pchart variable can only be a string type.
        :parm rchart: The rchart variable can only be a string type.
        :parm schart: The schart variable can only be a string type.
        :parm uchart: The uchart variable can only be a string type.
        :parm xrchart: The xrchart variable can only be a string type.
        :parm xschart: The xschart variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """
