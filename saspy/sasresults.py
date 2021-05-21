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
try:
   from pygments.formatters import HtmlFormatter
   from pygments import highlight
   from saspy.SASLogLexer import SASLogStyle, SASLogLexer
except:
   pass

class SASresults(object):
    """Return results from a SAS Model object"""

    def __init__(self, attrs, session, objname, nosub=False, log=''):

        if len(attrs)  > 0:
           self._names = attrs
           if len(log) > 0:
               self._names.append("LOG")
        else:
           self._names = ['ERROR_LOG']

        # no valid names start with _ and some procs somehow cause this. causes recursion error
        for item in self._names:
          if item.startswith('_'):
             self._names.remove(item)

        self._name = objname
        self.sas   = session
        self.nosub = nosub
        self._log  = log

        try:
           if SASLogLexer:
              self.nopyg = False
           else:
              self.nopyg = True
        except:
           self.nopyg = True

    def __dir__(self) -> list:
        """Overload dir method to return the attributes"""
        return self._names

    def __getattr__(self, attr, all=False):
        if attr.startswith('_'):
            return getattr(self, attr)
        if attr.upper() == 'LOG' or attr.upper() == 'ERROR_LOG':
            if self.sas.sascfg.display.lower() == 'zeppelin':
               if not self.sas.batch and not self.nopyg:
                   self.sas.DISPLAY(self.sas.HTML(self._colorLog(self._log)))
               else:
                   print(self._log)
               return
            else:
               if not self.sas.batch and not self.nopyg:
                   return self.sas.HTML(self._colorLog(self._log))
               else:
                   return self._log

        if attr.upper() in self._names:
            data = self._go_run_code(attr)
        else:
            if self.nosub:
                print('This SAS Result object was created in teach_me_SAS mode, so it has no results')
                return None
            else:
                print("Result named "+attr+" not found. Valid results are:"+str(self._names))
                return None

        if not self.sas.batch:
           if not isinstance(data, dict):
               return data
           else:
               self.sas.DISPLAY(self.sas.HTML('<h1>' + attr + '</h1>' + data['LST']))
               return None
        else:
           return data

    def _colorLog(self,log:str)-> str:
        color_log = highlight(log, SASLogLexer(), HtmlFormatter(full=True, style=SASLogStyle, lineseparator="<br>"))
        return color_log

    def _go_run_code(self, attr) -> dict:
        lastlog = len(self.sas._io._log)
        graphics = ['PLOT', 'OGRAM', 'PANEL', 'BY', 'MAP']
        if any(x in attr for x in graphics):
            code = '%%getdata(%s, %s);' % (self._name, attr)
            res = self.sas._io.submit(code)
            self.sas._lastlog = self.sas._io._log[lastlog:]
            return res
        else:
            if self.sas.exist(attr, '_'+self._name):
               lref = '_'+self._name
            else:
               lref = self._name

            if self.sas.results.upper() == 'PANDAS':
               df = self.sas.sasdata2dataframe(attr, libref=lref)
            else:
               code = '%%getdata(%s, %s);' % (self._name, attr)
               df   = self.sas._io.submit(code)

            self.sas._lastlog = self.sas._io._log[lastlog:]
            return df


    def sasdata(self, table) -> object:
        x = self.sas.sasdata(table, '_' + self._name)
        return x

    def ALL(self):
        """
        This method shows all the results attributes for a given object
        """
        lastlog = len(self.sas._io._log)
        if not self.sas.batch:
           for i in self._names:
               if i.upper() != 'LOG' and i.upper() != 'ERROR_LOG':
                   x = self.__getattr__(i)
                   if x is not None:
                      if self.sas.sascfg.display.lower() == 'zeppelin':
                         print("%text "+i+"\n"+str(x)+"\n")
                      else:
                         self.sas.DISPLAY(x)
           self.sas._lastlog = self.sas._io._log[lastlog:]
        else:
           ret = []
           for i in self._names:
               if i.upper()!='LOG':
                   ret.append(self.__getattr__(i))
           self.sas._lastlog = self.sas._io._log[lastlog:]
           return ret

