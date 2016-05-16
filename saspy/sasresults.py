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
from IPython import display as dis
from IPython.core.display import HTML


class SASresults(object):
    """Return results from a SAS Model object"""

    def __init__(self, attrs, session, objname, nosub=False):

        self._attrs = attrs
        self._name = objname
        self.sas = session
        self.nosub = nosub

    def __dir__(self):
        """Overload dir method to return the attributes"""
        return self._attrs

    def __getattr__(self, attr):
        if attr.startswith('_'):
            return getattr(self, attr)
        if attr.upper() in self._attrs:
            # print(attr.upper())
            data = self._go_run_code(attr)
            '''
            if not attr.lower().endswith('plot'):
                libname, table = data.split()
                table_data = sasdata(libname, table)
                content = table_data.contents()
                # parse content
                headers = content[0]

                res = namedtuple('SAS Result', headers)
                results = [ res(x) for x in headers[1:] ]
            '''

        else:
            if self.nosub:
                print('This SAS Result object was created in teach_me_SAS mode, so it has no results')
                return
            else:
                #raise AttributeError
                print("Result named "+attr+" not found. Valid results are:"+str(self._attrs))
                return

        if not self.sas.batch:
           return HTML('<h1>' + attr + '</h1>' + data['LST'])
        else:
           return data

    def _go_run_code(self, attr):
        # print(self._name, attr)
        code = '%%getdata(%s, %s);' % (self._name, attr)
        # print (code)
        res = self.sas.submit(code)
        return res
        #return res['LST']

    def sasdata(self, table):
        x = self.sas.sasdata(table, '_' + self._name)
        return x

    def ALL(self):
        """
        This method shows all the results attributes for a given object
        """
        if not self.sas.batch:
           for i in self._attrs:
               dis.display(self.__getattr__(i))
        else:
           ret = []
           for i in self._attrs:
               ret.append(self.__getattr__(i))
           return ret

