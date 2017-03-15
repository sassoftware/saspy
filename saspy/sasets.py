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
from saspy.sasproccommons import SASProcCommons
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

    def timeseries(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the TIMESERIES procedure

        ``required_set={'id'}``

        ``legal_set={ 'by', 'corr', 'crosscorr', 'decomp', 'id', 'season', 'trend', 'var', 'crossvar', 'out'}``

        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeseries_syntax.htm
        """
        required_set = {'id'}
        legal_set = {'by', 'corr', 'crosscorr', 'decomp', 'id', 'season', 'trend', 'var', 'crossvar', 'out', 'procopts'}
        self.logger.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "TIMESERIES", required_set, legal_set, **kwargs)

    def arima(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the ARIMA procedure

        ``required_set={'identify'}``

        ``legal_set={ 'by', 'identify', 'estimate', 'outlier', 'forecast', 'out'}``

        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_arima_syntax.htm
        """
        required_set = {'identify'}
        legal_set = {'by', 'identify', 'estimate', 'outlier', 'forecast', 'out', 'procopts'}
        return SASProcCommons._run_proc(self, "ARIMA", required_set, legal_set, **kwargs)

    def ucm(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the UCM procedure

        ``required_set={'model'}``

        ``legal_set= {'autoreg', 'blockseason', 'by', 'cycle', 'deplag', 'estimate', 'forecast', 'id', 'irregular',
        'level', 'model', 'nloptions', 'performance', 'out', 'outlier', 'randomreg', 'season', 'slope',
        'splinereg', 'splineseason'}``

        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_ucm_syntax.htm
        """
        required_set = {'model'}
        legal_set = {'autoreg', 'blockseason', 'by', 'cycle', 'deplag', 'estimate', 'forecast', 'id', 'irregular'
                                                                                                      'level', 'model',
                     'nloptions', 'performance', 'out', 'outlier', 'randomreg', 'season', 'slope'
                                                                                          'splinereg', 'splineseason',
                     'procopts'}
        return SASProcCommons._run_proc(self, "UCM", required_set, legal_set, **kwargs)

    def esm(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the ESM procedure

        ``required_set = {}``

        ``legal_set = { 'by', 'id', 'forecast', 'out'}``

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_esm_syntax.htm
        """
        required_set = {}
        legal_set = {'by', 'id', 'forecast', 'out', 'procopts'}
        return SASProcCommons._run_proc(self, "ESM", required_set, legal_set, **kwargs)

    def timeid(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the TIMEID procedure

        ``required_set = {}``

        ``legal_set = { 'by', 'id', 'out'}``

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeid_syntax.htm
        """
        required_set = {}
        legal_set = {'by', 'id', 'out', 'procopts'}
        return SASProcCommons._run_proc(self, "TIMEID", required_set, legal_set, **kwargs)

    def timedata(self, **kwargs: dict) -> 'SASresults':
        """
        Python method to call the TIMEDATA procedure

        ``required_set = {}``

        ``legal_set = {'by', 'id', 'fcmport', 'out', 'outarrays', 'outscalars', 'var', 'prog_stmts'}``

        Documentation link:
        http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timedata_syntax.htm
        """
        required_set = {}
        legal_set = {'by', 'id', 'fcmport', 'out', 'outarrays', 'outscalars', 'var', 'prog_stmts', 'procopts'}
        return SASProcCommons._run_proc(self, "TIMEDATA", required_set, legal_set, **kwargs)
