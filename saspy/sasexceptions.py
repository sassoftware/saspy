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

        extra  = "\n\nPlease refer to the Configuration Instructions in the SASPy Documentation at "
        extra += "https://sassoftware.github.io/saspy/configuration\n"
        extra += "You can also look for the error you've recieved in the Troublshooting guide at "
        extra += "https://sassoftware.github.io/saspy/troubleshooting\n"
        extra += "If you need more help, please open an Issue on the SASPy GitHub site at "
        extra += "https://github.com/sassoftware/saspy/issues"

        return 'Cannot use {} I/O module on Windows. {}'.format(self.method, alt_text+extra)


class SASIOConnectionError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        extra  = "\n\nPlease refer to the Configuration Instructions in the SASPy Documentation at "
        extra += "https://sassoftware.github.io/saspy/configuration\n"
        extra += "You can also look for the error you've recieved in the Troublshooting guide at "
        extra += "https://sassoftware.github.io/saspy/troubleshooting\n"
        extra += "If you need more help, please open an Issue on the SASPy GitHub site at "
        extra += "https://github.com/sassoftware/saspy/issues"

        return 'Failure establishing SASsession.\n{}'.format(self.msg+extra)


class SASIOConnectionTerminated(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return 'No SAS process attached. SAS process has terminated unexpectedly.\n{}'.format(self.msg)


class SASHTTPauthenticateError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return 'Failure in GET AuthToken.\n{}'.format(self.msg)


class SASHTTPconnectionError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return 'Failure in GET Connection.\n{}'.format(self.msg)

class SASHTTPsubmissionError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return 'Failure in submit().\n{}'.format(self.msg)

class SASResultsError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return 'Failure creating SASResults object.\n{}'.format(self.msg)

class SASDFNamesToLongError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return 'Column name(s) in DataFrame are too long for SAS. Rename to 32 bytes (in SAS Session encoding) or less.\n'



