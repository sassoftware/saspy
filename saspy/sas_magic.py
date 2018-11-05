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
from IPython.display import HTML
import IPython.core.magic as ipym
import re
from saspy.SASLogLexer import SASLogStyle, SASLogLexer
from saspy.sasbase import SASsession
from pygments.formatters import HtmlFormatter
from pygments import highlight


@ipym.magics_class
class SASMagic(ipym.Magics):
    """
    A set of magics useful for interactive work with SAS via saspy
    All the SAS magic cells in a single notebook share a SAS session
    """

    def __init__(self, shell):
        super(SASMagic, self).__init__(shell)
        self.lst_len = -99  # initialize the length to a negative number to trigger function
        self.mva = None
        if self.lst_len < 0 and isinstance(self.mva, SASsession) :
            self._get_lst_len()

    @ipym.cell_magic
    def SAS(self, line, cell):
        """
        %%SAS - send the code in the cell to a SAS Server

        This cell magic will execute the contents of the cell in a SAS
        session and return any generated output

        Example:
            %%SAS
            proc print data=sashelp.class;
            run;
            data a;
                set sashelp.cars;
            run;
        """
        
        mva = self.mva
        if len(line) and line in self.shell.user_ns:  # session supplied
            _mva = self.shell.user_ns[line]
            if isinstance(_mva, SASsession):
                mva = _mva
            else:
                return 'Invalid SAS Session object supplied'
        elif len(line) and not line in self.shell.user_ns:  # string supplied but not a session
            return 'Invalid SAS Session object supplied'
        else:  # no string should default to unnamed session
            try:
                if mva is None:
                    mva = SASsession()
                    self.mva = mva  # save the session for reuse
                else:
                    mva = self.mva
            except:
                return "this shouldn't happen"
        saveOpts="proc optsave out=__jupyterSASKernel__; run;"
        restoreOpts="proc optload data=__jupyterSASKernel__; run;"
        if len(line)>0:  # Save current SAS Options
            mva.submit(saveOpts)

        if line.lower()=='smalllog':
            mva.submit("options nosource nonotes;")

        elif line is not None and line.startswith('option'):
            mva.submit(line + ';')

        res = mva.submit(cell)
        dis = self._which_display(res['LOG'], res['LST'])

        if len(line)>0:  # Restore SAS options 
            mva.submit(restoreOpts)

        return dis

    @ipym.cell_magic
    def IML(self,line,cell):
        """
        %%IML - send the code in the cell to a SAS Server
                for processing by PROC IML

        This cell magic will execute the contents of the cell in a
        PROC IML session and return any generated output. The leading
        PROC IML and trailing QUIT; are submitted automatically.

        Example:
           %%IML
           a = I(6); * 6x6 identity matrix;
           b = j(5,5,0); *5x5 matrix of 0's;
           c = j(6,1); *6x1 column vector of 1's;
           d=diag({1 2 4});
           e=diag({1 2, 3 4});

        """
        res = self.mva.submit("proc iml; " + cell + " quit;")
        dis = self._which_display(res['LOG'], res['LST'])
        return dis

    @ipym.cell_magic
    def OPTMODEL(self, line, cell):
        """
        %%OPTMODEL - send the code in the cell to a SAS Server
                for processing by PROC OPTMODEL

        This cell magic will execute the contents of the cell in a
        PROC OPTMODEL session and return any generated output. The leading
        PROC OPTMODEL and trailing QUIT; are submitted automatically.

        Example:
        proc optmodel;
           /* declare variables */
           var choco >= 0, toffee >= 0;

           /* maximize objective function (profit) */
           maximize profit = 0.25*choco + 0.75*toffee;

           /* subject to constraints */
           con process1:    15*choco +40*toffee <= 27000;
           con process2:           56.25*toffee <= 27000;
           con process3: 18.75*choco            <= 27000;
           con process4:    12*choco +50*toffee <= 27000;
           /* solve LP using primal simplex solver */
           solve with lp / solver = primal_spx;
           /* display solution */
           print choco toffee;
        quit;

        """
        res = self.mva.submit("proc optmodel; " + cell + " quit;")
        dis = self._which_display(res['LOG'], res['LST'])
        return dis

    def _get_lst_len(self):
        code="data _null_; run;"
        res = self.mva.submit(code)
        assert isinstance(res, dict)
        self.lst_len=len(res['LST'])
        assert isinstance(self.lst_len,int)
        return

    @staticmethod
    def _which_display(log, output):
        lst_len = 30762
        lines = re.split(r'[\n]\s*', log)
        i = 0
        elog = []
        for line in lines:
            i += 1
            e = []
            if line.startswith('ERROR'):
                e = lines[(max(i - 15, 0)):(min(i + 16, len(lines)))]
            elog = elog + e
        if len(elog) == 0 and len(output) > lst_len:   # no error and LST output
            return HTML(output)
        elif len(elog) == 0 and len(output) <= lst_len:   # no error and no LST
            color_log = highlight(log, SASLogLexer(), HtmlFormatter(full=True, style=SASLogStyle, lineseparator="<br>"))
            return HTML(color_log)
        elif len(elog) > 0 and len(output) <= lst_len:   # error and no LST
            color_log = highlight(log, SASLogLexer(), HtmlFormatter(full=True, style=SASLogStyle, lineseparator="<br>"))
            return HTML(color_log)
        else:   # errors and LST
            color_log = highlight(log, SASLogLexer(), HtmlFormatter(full=True, style=SASLogStyle, lineseparator="<br>"))
            return HTML(color_log + output)


def load_ipython_extension(ipython):
    """Load the extension in Jupyter"""
    ipython.register_magics(SASMagic)


if __name__ == '__main__':
    from IPython import get_ipython

    get_ipython().register_magics(SASMagic)
