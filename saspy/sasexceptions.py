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


class SASConfigNotFoundError(Exception):
    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return 'Configuration path {} does not exist.'.format(self.path)


class SASConfigNotValidError(Exception):
    def __init__(self, defn: str, msg: str=None):
        self.defn = defn if defn else 'N/A'
        self.msg = msg

    def __str__(self):
        return 'Configuration definition {} is not valid. {}'.format(self.defn, self.msg)


class SASIONotSupportedError(Exception):
    def __init__(self, method: str, alts: list=None):
        self.method = method
        self.alts = alts

    def __str__(self):
        if self.alts is not None:
            alt_text = 'Try the following: {}'.format(', '.join(self.alts))
        else:
            alt_text = ''

        return 'Cannot use {} I/O module on Windows. {}'.format(self.method, alt_text)


class SASHTTPauthenticateError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return 'Failure in GET AuthToken.\n {}'.format(self.msg)


class SASHTTPconnectionError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return 'Failure in GET Connection.\n {}'.format(self.msg)

class SASHTTPsubmissionError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return 'Failure in submit().\n {}'.format(self.msg)



