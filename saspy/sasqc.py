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


class SASqc:
    def __init__(self, session, *args, **kwargs):
        """Submit an initial set of macros to prepare the SAS system"""
        self.sasproduct = "qc"
        # create logging
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.sas = session
        logging.debug("Initialization of SAS Macro: " + self.sas.saslog())
    
    def cusum(self, **kwargs):
        """
        Python method to call the CUSUM procedure
        required_set = {}
        legal_set = {'by','xchart'}
        Documentation link:
        http://support.sas.com/documentation/cdl/en/qcug/68161/HTML/default/viewer.htm#qcug_cusum_sect001.htm
        """
        required_set = {}
        legal_set = {'by', 'xchart', 'procopts'}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "CUSUM", required_set, legal_set, **kwargs)

    def macontrol(self, **kwargs):
        """
        Python method to call the MACONTROL procedure

        Documentation link:
        http://support.sas.com/documentation/cdl/en/qcug/68161/HTML/default/viewer.htm#qcug_macontrol_toc.htm
        """
        required_set = {}
        legal_set = {'procopts'}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "MACONTROL", required_set, legal_set, **kwargs)

    def capability(self, **kwargs):
        """
        Python method to call the CUSUM procedure
        required_set = {}
        legal_set = {'cdfplot', 'comphist', 'histogram', 'inset', 'intervals', 'output', 'ppplot', 'probplot',
                     'qqplot', 'freq', 'weight', 'id', 'by', 'spec'}
        Documentation link:
        http://support.sas.com/documentation/cdl/en/qcug/68161/HTML/default/viewer.htm#qcug_capability_sect001.htm
        """
        required_set = {}
        legal_set = {'cdfplot', 'comphist', 'histogram', 'inset', 'intervals', 'output', 'ppplot', 'probplot',
                     'qqplot', 'freq', 'weight', 'id', 'by', 'spec', 'out', 'procopts'}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "CAPABILITY", required_set, legal_set, **kwargs)

    def shewhart(self, **kwargs):
        """
        Python method to call the SHEWHART procedure\n
        Documentation link:
        http://support.sas.com/documentation/cdl/en/qcug/68161/HTML/default/viewer.htm#qcug_shewhart_toc.htm
        """
        required_set = {}
        legal_set = {'procopts'}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "SHEWHART", required_set, legal_set, **kwargs)

