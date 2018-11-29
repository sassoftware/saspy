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


class SASutil:
    """
    This class is for SAS BASE procedures to be called as python3 objects and use SAS as the computational engine

    This class and all the useful work in this package require a licensed version of SAS.

    #. Identify the product of the procedure (SAS/STAT, SAS/ETS, SAS Enterprise Miner, etc).
    #. Find the corresponding file in saspy sasstat.py, sasets.py, sasml.py, etc.
    #. Create a set of valid statements. Here is an example:

        .. code-block::

            lset = {'ARIMA', 'BY', 'ID', 'MACURVES', 'MONTHLY', 'OUTPUT', 'VAR'}

        The case and order of the items will be formated.
    #. Call the `doc_convert` method to generate then method call as well as the docstring markup

        .. code-block::

            import saspy
            print(saspy.sasdecorator.procDecorator.doc_convert(lset, 'x11')['method_stmt'])
            print(saspy.sasdecorator.procDecorator.doc_convert(lset, 'x11')['markup_stmt'])


        The `doc_convert` method takes two arguments: a list of the valid statements and the proc name. It returns a dictionary with two keys, method_stmt and markup_stmt. These outputs can be copied into the appropriate product file.

    #. Add the proc decorator to the new method.
        The decorator should be on the line above the method declaration.
        The decorator takes one argument, the required statements for the procedure. If there are no required statements than an empty list `{}` should be passed.
        Here are two examples one with no required arguments:

        .. code-block::

            @procDecorator.proc_decorator({})
            def esm(self, data: 'SASdata' = None, ...

        And one with required arguments:

        .. code-block::

            @procDecorator.proc_decorator({'model'})
            def mixed(self, data: 'SASdata' = None, ...

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
    def hpimpute(self, data: 'SASdata' = None,
                 code: str = None,
                 freq: str = None,
                 id: str = None,
                 impute: str = None,
                 input: [str, list, dict] = None,
                 performance: str = None,
                 procopts: str = None,
                 stmtpassthrough: str = None,
                 **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPIMPUTE procedure
        Documentation link:
        http://support.sas.com/documentation/cdl/en/stathpug/68163/HTML/default/viewer.htm#stathpug_hpsplit_syntax.htm

        :param data: SASdata object This parameter is required
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
    def hpbin(self, data: 'SASdata' = None,
              cls: [str, list] = None,
              code: str = None,
              grow: str = None,
              id: str = None,
              model: str = None,
              out: [str, bool, 'SASdata'] = None,
              partition: str = None,
              performance: str = None,
              prune: str = None,
              rules: str = None,
              procopts: str = None,
              stmtpassthrough: str = None,
              **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPBIN procedure
        Documentation link:
        http://support.sas.com/documentation/cdl/en/stathpug/68163/HTML/default/viewer.htm#stathpug_hpsplit_syntax.htm

        :param data: SASdata object This parameter is required
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm code: The code variable can only be a string type.
        :parm grow: The grow variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm out: The out variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm partition: The partition variable can only be a string type.
        :parm performance: The performance variable can only be a string type.
        :parm prune: The prune variable can only be a string type.
        :parm rules: The rules variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def hpsample(self, data: 'SASdata' = None,
                 cls: [str, list] = None,
                 code: str = None,
                 grow: str = None,
                 id: str = None,
                 model: str = None,
                 outpartition: str = None,
                 performance: str = None,
                 prune: str = None,
                 rules: str = None,
                 procopts: str = None,
                 stmtpassthrough: str = None,
                 **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPSAMPLE procedure
        Documentation link:
        http://support.sas.com/documentation/cdl/en/stathpug/68163/HTML/default/viewer.htm#stathpug_hpsplit_syntax.htm

        :param data: SASdata object This parameter is required
        :parm cls: The cls variable can be a string or list type. It refers to the categorical, or nominal variables.
        :parm code: The code variable can only be a string type.
        :parm grow: The grow variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm outpartition: The outpartition variable can only be a string type.
        :parm performance: The performance variable can only be a string type.
        :parm prune: The prune variable can only be a string type.
        :parm rules: The rules variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """