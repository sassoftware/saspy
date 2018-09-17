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
import sys
import warnings
from functools import wraps


class procDecorator:
    def __init__(self):
        pass

    def proc_decorator(req_set):
        """
        Decorator that provides the wrapped function with an attribute 'actual_kwargs'
        containing just those keyword arguments actually passed in to the function.
        """

        def decorator(func):
            @wraps(func)
            def inner(self, *args, **kwargs):
                inner.proc_decorator = kwargs
                self.logger.debug("processing proc:{}".format(func.__name__))
                self.logger.debug(req_set)
                self.logger.debug("kwargs type: " + str(type(kwargs)))
                if func.__name__.lower() in ['hplogistic', 'hpreg']:
                    kwargs['ODSGraphics'] = kwargs.get('ODSGraphics', False)
                legal_set = set(kwargs.keys())
                self.logger.debug(legal_set)
                return SASProcCommons._run_proc(self, func.__name__.lower(), req_set, legal_set, **kwargs)
            return inner

        return decorator