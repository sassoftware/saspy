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



class SASml:
    """
    This class is for SAS Enterprise Miner procedures to be called as python3 objects and use SAS as the computational engine

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
        self.sasproduct = "em"
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sas = session
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

    @procDecorator.proc_decorator({'input', 'target'})
    def hpforest(self, data: ['SASdata', str] = None,
                 freq: str = None,
                 id: str = None,
                 input: [str, list, dict] = None,
                 save: str = None,
                 score: [str, bool, 'SASdata'] = True,
                 target: [str, list, dict] = None,
                 procopts: str = None,
                 stmtpassthrough: str = None,
                 **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPFOREST procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf

        :param data: SASdata object or string. This parameter is required.
        :parm freq: The freq variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable. This parameter is required
        :parm save: The save variable can only be a string type.
        :parm score: The score variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable. This parameter is required
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def hp4score(self, data: ['SASdata', str] = None,
                 id: str = None,
                 importance: str = None,
                 performance: str = None,
                 score: [str, bool, 'SASdata'] = True,
                 procopts: str = None,
                 stmtpassthrough: str = None,
                 **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HP4SCORE procedure

        Documentation link:
        https://go.documentation.sas.com/?docsetId=emhpprcref&docsetTarget=emhpprcref_hp4score_toc.htm&docsetVersion=14.2&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm id: The id variable can only be a string type.
        :parm importance: The importance variable can only be a string type.
        :parm performance: The performance variable can only be a string type.
        :parm score: The score variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'input'})
    def hpcluster(self, data: ['SASdata', str] = None,
                  freq: str = None,
                  id: [str, list] = None,
                  input: [str, list, dict] = None,
                  score: [str, bool, 'SASdata'] = True,
                  procopts: str = None,
                  stmtpassthrough: str = None,
                  **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPCLUS procedure

        Documentation link:
        https://go.documentation.sas.com/?docsetId=emhpprcref&docsetTarget=emhpprcref_hpclus_toc.htm&docsetVersion=14.2&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm freq: The freq variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable. This parameter is required
        :parm score: The score variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'input', 'target', 'train'})
    def hpneural(self, data: ['SASdata', str] = None,
                 architecture: str = None,
                 code: str = None,
                 hidden: [str, int] = None,
                 id: str = None,
                 input: [str, list, dict] = None,
                 partition: str = None,
                 score: [str, bool, 'SASdata'] = True,
                 target: [str, list, dict] = None,
                 train: [str, dict] = None,
                 procopts: str = None,
                 stmtpassthrough: str = None,
                 **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPNEURAL procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf

        :param data: SASdata object or string. This parameter is required.
        :parm architecture: The architecture variable can only be a string type.
        :parm code: The code variable can only be a string type.
        :parm hidden: The hidden variable can only be a string type. This statement is required if there is a Train statement and the architecture is not logistic.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable. This parameter is required
        :parm partition: The partition variable can only be a string type.
        :parm score: The score variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable. This parameter is required
        :parm train: The train variable can be a string or dict type. This parameter is required
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'input', 'target'})
    def treeboost(self, data: ['SASdata', str] = None,
                  assess: str = None,
                  code: str = None,
                  freq: str = None,
                  importance: str = None,
                  input: [str, list, dict] = None,
                  performance: str = None,
                  save: [str, bool] = True,
                  score: [str, bool, 'SASdata'] = True,
                  subseries: str = None,
                  target: [str, list, dict] = None,
                  procopts: str = None,
                  stmtpassthrough: str = None,
                  **kwargs: dict) -> 'SASresults':
        """
        Python method to call the TREEBOOST procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf

        :param data: SASdata object or string. This parameter is required.
        :parm assess: The assess variable can only be a string type.
        :parm code: The code variable can only be a string type.
        :parm freq: The freq variable can only be a string type.
        :parm importance: The importance variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable. This parameter is required
        :parm performance: The performance variable can only be a string type.
        :parm save: The save variable can be a string or boolean type. The default is True to create common output datasets
        :parm score: The score variable can only be a string type.
        :parm subseries: The subseries variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable. This parameter is required
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'input', 'target'})
    def hpbnet(self, data: ['SASdata', str] = None,
               code: str = None,
               freq: str = None,
               id: str = None,
               input: [str, list, dict] = None,
               output: [str, bool, 'SASdata'] = None,
               partition: str = None,
               performance: str = None,
               target: [str, list, dict] = None,
               procopts: str = None,
               stmtpassthrough: str = None,
               **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPBNET procedure

        Documentation link:
        http://go.documentation.sas.com/?docsetId=emhpprcref&docsetVersion=14.2&docsetTarget=emhpprcref_hpbnet_toc.htm&locale=en

        :param data: SASdata object or string. This parameter is required.
        :parm code: The code variable can only be a string type.
        :parm freq: The freq variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable. This parameter is required
        :parm output: The output variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".
        :parm partition: The partition variable can only be a string type.
        :parm performance: The performance variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable. This parameter is required
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """
