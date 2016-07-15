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


class SASml:
    def __init__(self, session, *args, **kwargs):
        """
        Submit an initial set of macros to prepare the SAS system
        """
        self.sasproduct = "em"
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.sas = session
        logging.debug("Initialization of SAS Macro: " + self.sas.saslog())

    def forest(self, **kwargs: dict) -> object:
        """
        Python method to call the HPFOREST procedure

        required_set = {'input', 'target'}
        legal_set= {'freq', 'input', 'id', 'target', 'save', 'score'}

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target'}
        legal_set = {'freq', 'input', 'id', 'target', 'save', 'score', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPFOREST", required_set, legal_set, **kwargs)

    def cluster(self, **kwargs: dict) -> object:
        """
        Python method to call the HPCLUS procedure

        required_set = {'input'}
        legal_set= {'freq', 'input', 'id', 'score'}

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input'}
        legal_set = {'freq', 'input', 'id', 'score', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPCLUS", required_set, legal_set, **kwargs)

    def neural(self, **kwargs: dict) -> object:
        """
        Python method to call the HPNEURAL procedure

        required_set = {'input', 'target', 'train'}
        legal_set= {'freq', 'input', 'id', 'target', 'save', 'score',
                    'architecture', 'weight', 'hidden', 'partition', 'train'}
        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target', 'train'}
        legal_set = {'freq', 'input', 'id', 'target', 'save', 'score',
                     'architecture', 'weight', 'hidden', 'partition', 'train', 'procopts'}
        logging.debug("kwargs type: " + str(type(kwargs)))
        return SASProcCommons._run_proc(self, "HPNEURAL", required_set, legal_set, **kwargs)

    def svm(self, **kwargs: dict) -> object:
        """
        Python method to call the HPSVM procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        pass

    def bnet(self, **kwargs: dict) -> object:
        """
        Python method to call the HPBNET procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        pass
