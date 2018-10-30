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


class SASViyaML:
    """
    This class is for SAS Viya procedures to be called as python3 objects and use SAS as the computational engine
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
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.sas = session
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

    @procDecorator.proc_decorator({'input', 'target'})
    def factmac(self, data: 'SASData' = None,
                autotune: str = None,
                code: str = None,
                display: str = None,
                displayout: str = None,
                id: str = None,
                input: [str, list, dict] = None,
                output: str = None,
                savestate: str = None,
                target: [str, list, dict] = None,
                procopts: str = None,
                stmtpassthrough: str = None,
                **kwargs: dict) -> object:
        """
        Python method to call the FACTMAC procedure
        Documentation link:
        https://go.documentation.sas.com/?docsetId=casml&docsetTarget=casml_factmac_syntax.htm&docsetVersion=8.3&locale=en

        :param data: SASData object This parameter is required
        :parm autotune: The autotune variable can only be a string type.
        :parm code: The code variable can only be a string type.
        :parm display: The display variable can only be a string type.
        :parm displayout: The displayout variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm output: The output variable can only be a string type.
        :parm savestate: The savestate variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'input'})
    def fastknn(self, data: 'SASData' = None,
                display: str = None,
                displayout: str = None,
                id: str = None,
                input: [str, list, dict] = None,
                output: str = None,
                procopts: str = None,
                stmtpassthrough: str = None,
                **kwargs: dict) -> object:
        """
        Python method to call the FASTKNN procedure
        Documentation link:
        https://go.documentation.sas.com/?docsetId=casml&docsetTarget=casml_fastknn_toc.htm&docsetVersion=8.3&locale=en

        :param data: SASData object This parameter is required
        :parm display: The display variable can only be a string type.
        :parm displayout: The displayout variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm output: The output variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'input', 'target'})
    def forest(self, data: 'SASData' = None,
               autotune: str = None,
               code: str = None,
               crossvalidation: str = None,
               grow: str = None,
               id: str = None,
               input: [str, list, dict] = None,
               output: str = None,
               partition: str = None,
               savestate: str = None,
               target: [str, list, dict] = None,
               viicode: str = None,
               weight: str = None,
               procopts: str = None,
               stmtpassthrough: str = None,
               **kwargs: dict) -> 'SASresults':
        """
        Python method to call the FOREST procedure
        Documentation link:
        https://go.documentation.sas.com/?docsetId=casml&docsetTarget=casml_forest_toc.htm&docsetVersion=8.3&locale=en

        :param data: SASData object This parameter is required
        :parm autotune: The autotune variable can only be a string type.
        :parm code: The code variable can only be a string type.
        :parm crossvalidation: The crossvalidation variable can only be a string type.
        :parm grow: The grow variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm output: The output variable can only be a string type.
        :parm partition: The partition variable can only be a string type.
        :parm savestate: The savestate variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm viicode: The viicode variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'input', 'target'})
    def gradboost(self, data: 'SASData' = None,
                  autotune: str = None,
                  code: str = None,
                  crossvalidation: str = None,
                  id: str = None,
                  input: [str, list, dict] = None,
                  output: str = None,
                  partition: str = None,
                  savestate: str = None,
                  target: [str, list, dict] = None,
                  transferlearn: str = None,
                  viicode: str = None,
                  weight: str = None,
                  procopts: str = None,
                  stmtpassthrough: str = None,
                  **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPCLUS procedure
        Documentation link:
        https://go.documentation.sas.com/?docsetId=casml&docsetTarget=casml_gradboost_toc.htm&docsetVersion=8.3&locale=en

        :param data: SASData object This parameter is required
        :parm autotune: The autotune variable can only be a string type.
        :parm code: The code variable can only be a string type.
        :parm crossvalidation: The crossvalidation variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm output: The output variable can only be a string type.
        :parm partition: The partition variable can only be a string type.
        :parm savestate: The savestate variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm transferlearn: The transferlearn variable can only be a string type.
        :parm viicode: The viicode variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'input', 'target', 'train'})
    def nnet(self, data: 'SASData' = None,
             architecture: str = None,
             autotune: str = None,
             code: str = None,
             crossvalidation: str = None,
             hidden: str = None,
             input: [str, list, dict] = None,
             optimization: str = None,
             output: str = None,
             partition: str = None,
             target: [str, list, dict] = None,
             train: str = None,
             weight: str = None,
             procopts: str = None,
             stmtpassthrough: str = None,
             **kwargs: dict) -> 'SASresults':
        """
        Python method to call the HPNEURAL procedure
        Documentation link:
        https://go.documentation.sas.com/?docsetId=casml&docsetTarget=casml_nnet_toc.htm&docsetVersion=8.3&locale=en

        :param data: SASData object This parameter is required
        :parm architecture: The architecture variable can only be a string type.
        :parm autotune: The autotune variable can only be a string type.
        :parm code: The code variable can only be a string type.
        :parm crossvalidation: The crossvalidation variable can only be a string type.
        :parm hidden: The hidden variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm optimization: The optimization variable can only be a string type.
        :parm output: The output variable can only be a string type.
        :parm partition: The partition variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm train: The train variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'input'})
    def svdd(self, data: 'SASData' = None,
             code: str = None,
             id: str = None,
             input: [str, list, dict] = None,
             kernel: str = None,
             savestate: str = None,
             solver: str = None,
             weight: str = None,
             procopts: str = None,
             stmtpassthrough: str = None,
             **kwargs: dict) -> 'SASresults':
        """
        Python method to call the SVDD procedure
        Documentation link:
        https://go.documentation.sas.com/?docsetId=casml&docsetTarget=casml_svdd_toc.htm&docsetVersion=8.3&locale=en

        :param data: SASData object This parameter is required
        :parm code: The code variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm kernel: The kernel variable can only be a string type.
        :parm savestate: The savestate variable can only be a string type.
        :parm solver: The solver variable can only be a string type.
        :parm weight: The weight variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'input'})
    def svmachine(self, data: 'SASData' = None,
                  autotune: str = None,
                  code: str = None,
                  id: str = None,
                  input: [str, list, dict] = None,
                  kernel: str = None,
                  output: str = None,
                  partition: str = None,
                  savestate: str = None,
                  solver: str = None,
                  target: [str, list, dict] = None,
                  procopts: str = None,
                  stmtpassthrough: str = None,
                  **kwargs: dict) -> object:
        """
        Python method to call the SVMACHINE procedure
        Documentation link:
        https://go.documentation.sas.com/?docsetId=casml&docsetTarget=casml_svmachine_toc.htm&docsetVersion=8.3&locale=en

        :param data: SASData object This parameter is required
        :parm autotune: The autotune variable can only be a string type.
        :parm code: The code variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm input: The input variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm kernel: The kernel variable can only be a string type.
        :parm output: The output variable can only be a string type.
        :parm partition: The partition variable can only be a string type.
        :parm savestate: The savestate variable can only be a string type.
        :parm solver: The solver variable can only be a string type.
        :parm target: The target variable can be a string, list or dict type. It refers to the dependent, y, or label variable.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """
