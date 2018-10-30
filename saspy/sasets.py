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
from saspy.sasresults import SASresults


class SASets:
    """
    This class is for SAS/ETS procedures to be called as python3 objects and use SAS as the computational engine

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
        """Submit an initial set of macros to prepare the SAS system"""
        self.sasproduct = "ets"
        # create logging
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sas = session
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

    @procDecorator.proc_decorator({'id'})
    def timeseries(self, data: 'SASData' = None,
                   by: str = None,
                   corr: str = None,
                   crosscorr: str = None,
                   crossvar: str = None,
                   decomp: str = None,
                   id: str = None,
                   out: str = None,
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

        :param data: SASData object This parameter is required
        :parm by: The by variable can only be a string type.
        :parm corr: The corr variable can only be a string type.
        :parm crosscorr: The crosscorr variable can only be a string type.
        :parm crossvar: The crossvar variable can only be a string type.
        :parm decomp: The decomp variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm out: The out variable can only be a string type.
        :parm season: The season variable can only be a string type.
        :parm trend: The trend variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'identify'})
    def arima(self, data: 'SASData' = None,
              by: str = None,
              estimate: str = None,
              forecast: str = None,
              identify: str = None,
              out: str = None,
              outlier: str = None,
              procopts: str = None,
              stmtpassthrough: str = None,
              **kwargs: dict) -> 'SASresults':
        """
        Python method to call the ARIMA procedure
        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_arima_syntax.htm

        :param data: SASData object This parameter is required
        :parm by: The by variable can only be a string type.
        :parm estimate: The estimate variable can only be a string type.
        :parm forecast: The forecast variable can only be a string type.
        :parm identify: The identify variable can only be a string type.
        :parm out: The out variable can only be a string type.
        :parm outlier: The outlier variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({'model'})
    def ucm(self, data: 'SASData' = None,
            autoreg: str = None,
            blockseason: str = None,
            by: str = None,
            cycle: str = None,
            deplag: str = None,
            estimate: str = None,
            forecast: str = None,
            id: str = None,
            irregular: str = None,
            level: str = None,
            model: str = None,
            nloptions: str = None,
            out: str = None,
            outlier: str = None,
            performance: str = None,
            randomreg: str = None,
            season: str = None,
            slope: str = None,
            splinereg: str = None,
            splineseason: str = None,
            procopts: str = None,
            stmtpassthrough: str = None,
            **kwargs: dict) -> 'SASresults':
        """
        Python method to call the UCM procedure
        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_ucm_syntax.htm

        :param data: SASData object This parameter is required
        :parm autoreg: The autoreg variable can only be a string type.
        :parm blockseason: The blockseason variable can only be a string type.
        :parm by: The by variable can only be a string type.
        :parm cycle: The cycle variable can only be a string type.
        :parm deplag: The deplag variable can only be a string type.
        :parm estimate: The estimate variable can only be a string type.
        :parm forecast: The forecast variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm irregular: The irregular variable can only be a string type.
        :parm level: The level variable can only be a string type.
        :parm model: The model variable can only be a string type.
        :parm nloptions: The nloptions variable can only be a string type.
        :parm out: The out variable can only be a string type.
        :parm outlier: The outlier variable can only be a string type.
        :parm performance: The performance variable can only be a string type.
        :parm randomreg: The randomreg variable can only be a string type.
        :parm season: The season variable can only be a string type.
        :parm slope: The slope variable can only be a string type.
        :parm splinereg: The splinereg variable can only be a string type.
        :parm splineseason: The splineseason variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def esm(self, data: 'SASData' = None,
            by: str = None,
            forecast: str = None,
            id: str = None,
            out: str = None,
            procopts: str = None,
            stmtpassthrough: str = None,
            **kwargs: dict) -> 'SASresults':
        """
        Python method to call the ESM procedure
        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_esm_syntax.htm

        :param data: SASData object This parameter is required
        :parm by: The by variable can only be a string type.
        :parm forecast: The forecast variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm out: The out variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def timeid(self, data: 'SASData' = None,
               by: str = None,
               id: str = None,
               out: str = None,
               procopts: str = None,
               stmtpassthrough: str = None,
               **kwargs: dict) -> 'SASresults':
        """
        Python method to call the TIMEID procedure
        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeid_syntax.htm

        :param data: SASData object This parameter is required
        :parm by: The by variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm out: The out variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """

    @procDecorator.proc_decorator({})
    def timedata(self, data: 'SASData' = None,
                 by: str = None,
                 fcmport: str = None,
                 id: str = None,
                 out: str = None,
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

        :param data: SASData object This parameter is required
        :parm by: The by variable can only be a string type.
        :parm fcmport: The fcmport variable can only be a string type.
        :parm id: The id variable can only be a string type.
        :parm out: The out variable can only be a string type.
        :parm outarrays: The outarrays variable can only be a string type.
        :parm outscalars: The outscalars variable can only be a string type.
        :parm prog_stmts: The prog_stmts variable can only be a string type.
        :parm var: The var variable can only be a string type.
        :parm procopts: The procopts variable is a generic option available for advanced use. It can only be a string type.
        :parm stmtpassthrough: The stmtpassthrough variable is a generic option available for advanced use. It can only be a string type.
        :return: SAS Result Object
        """
