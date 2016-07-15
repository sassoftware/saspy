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

class SASets:
    def __init__(self, session, *args, **kwargs):
        """Submit an initial set of macros to prepare the SAS system"""
        self.sasproduct="ets"
        # create logging
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.NullHandler)
        self.logger.setLevel(logging.DEBUG)
        self.sas=session
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

    def timeseries(self, **kwargs):
        """
        Python method to call the TIMESERIES procedure
        required_set={'id'}
        legal_set={ 'by', 'corr', 'crosscorr', 'decomp', 'id', 'season', 'trend', 'var', 'crossvar', 'out'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeseries_syntax.htm
        """
        required_set = {'id'}
        legal_set = { 'by', 'corr', 'crosscorr', 'decomp', 'id', 'season', 'trend', 'var', 'crossvar', 'out', 'procopts'}
        self.logger.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "TIMESERIES", required_set, legal_set, **kwargs)

    def arima(self, **kwargs):
        """
        Python method to call the ARIMA procedure
        required_set={'identify'}
        legal_set={ 'by', 'identify', 'estimate', 'outlier', 'forecast', 'out'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_arima_syntax.htm
        """
        required_set = {'identify'}
        legal_set = { 'by', 'identify', 'estimate', 'outlier', 'forecast', 'out', 'procopts'}
        return SASProcCommons._run_proc(self, "ARIMA", required_set, legal_set, **kwargs)

    def ucm(self, **kwargs):
        """
        Python method to call the UCM procedure
        required_set={'model'}
        legal_set= {'autoreg', 'blockseason', 'by', 'cycle', 'deplag', 'estimate', 'forecast', 'id', 'irregular'
                    'level', 'model', 'nloptions', 'performance', 'out', 'outlier', 'randomreg', 'season', 'slope'
                    'splinereg', 'splineseason'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_ucm_syntax.htm
        """
        required_set = {'model'}
        legal_set = {'autoreg', 'blockseason', 'by', 'cycle', 'deplag', 'estimate', 'forecast', 'id', 'irregular'
                    'level', 'model', 'nloptions', 'performance', 'out', 'outlier', 'randomreg', 'season', 'slope'
                    'splinereg', 'splineseason', 'procopts'}
        return SASProcCommons._run_proc(self, "UCM", required_set, legal_set, **kwargs)

    def esm(self, **kwargs):
        """
        Python method to call the ESM procedure
        required_set = {}
        legal_set = { 'by', 'id', 'forecast', 'out'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_esm_syntax.htm
        """
        required_set = {}
        legal_set = { 'by', 'id', 'forecast', 'out', 'procopts'}
        return SASProcCommons._run_proc(self, "ESM", required_set, legal_set, **kwargs)

    def timeid(self, **kwargs):
        """
        Python method to call the TIMEID procedure
        required_set = {}
        legal_set = { 'by', 'id', 'out'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeid_syntax.htm
        """
        required_set = {}
        legal_set = { 'by', 'id', 'out', 'procopts'}
        return SASProcCommons._run_proc(self, "TIMEID", required_set, legal_set, **kwargs)

    def timedata(self, **kwargs):
        """
        Python method to call the TIMEDATA procedure
        required_set = {}
        legal_set = {'by', 'id', 'fcmport', 'out', 'outarrays', 'outscalars', 'var', 'prog_stmts'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timedata_syntax.htm
        """
        required_set = {}
        legal_set = {'by', 'id', 'fcmport', 'out', 'outarrays', 'outscalars', 'var', 'prog_stmts', 'procopts'}
        return SASProcCommons._run_proc(self, "TIMEIDATA", required_set, legal_set, **kwargs)

