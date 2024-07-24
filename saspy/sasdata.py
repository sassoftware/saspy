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

#so the doc will generate for df methods
try:
   import pandas
except Exception as e:
   pass

import logging
logger = logging.getLogger('saspy')

import re
import saspy as sp2

class SASdata:
    """
    **Overview**

    The SASdata object is a reference to a SAS Data Set or View. It is used to access data that exists in the SAS session.
    You create a SASdata object by using the sasdata() method of the SASsession object.

    Parms for the sasdata() method of the SASsession object are:

    :param table: [Required] the name of the SAS Data Set or View
    :param libref: [Defaults to WORK] the libref for the SAS Data Set or View.
    :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives
    :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs, format):

        - where is a string
        - keep are strings or list of strings.
        - drop are strings or list of strings.
        - obs is a numbers - either string or int
        - firstobs is a numbers - either string or int
        - format is a string or dictionary { var: format }
        - encoding is a string

        .. code-block:: python

                         {'where'    : 'msrp < 20000 and make = "Ford"' ,
                          'keep'     : 'msrp enginesize Cylinders Horsepower Weight' ,
                          'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight'] ,
                          'obs'      :  20 ,
                          'firstobs' : '10' ,
                          'format'   : {'money': 'dollar10', 'time': 'tod5.'} ,
                          'encoding' : 'latin9'
                         }

    """

    def __init__(self, sassession, libref, table, results='', dsopts: dict=None):
        self.sas = sassession

        if results == '':
           results = sassession.results

        failed = 0
        if results.upper() == "HTML":
           if self.sas.sascfg.display.lower() == 'jupyter':
              try:
                 from IPython.display import HTML
              except:
                 failed = 1

              if failed and not self.sas.batch:
                  self.HTML = 0
              else:
                  self.HTML = 1
           else:
              self.HTML = 1
        else:
           self.HTML = 0

        if len(libref):
            self.libref = libref

            code  = "%let engine=BAD;\n"
            code += "proc sql;select distinct engine into :engine from "
            code += "sashelp.VLIBNAM where libname = '{}';".format(libref.upper())
            code += ";%put engstart=&engine engend=;\nquit;"
            ll = self.sas._io.submit(code, "text")

            eng = ll['LOG'].rpartition("engstart=")
            eng = eng[2].partition(" engend=")
            self.engine = eng[0].strip()
        else:
            self.engine = 'BASE'
            if self.sas.exist(table, libref='user'):
                self.libref = 'USER'
            else:
                self.libref = 'WORK'

            # hack till the bug gets fixed
            if self.sas.sascfg.mode == 'HTTP':
                self.libref = 'WORK'

        self.table    = table.strip()
        self.dsopts   = dsopts if dsopts is not None else {}
        self.results  = results
        self.tabulate = sp2.Tabulate(sassession, self)

    def __getitem__(self, key):
        print(key)
        print(type(key))

    def __repr__(self):
        """
        display info about this object ...

        :return: output
        """
        x  = "Libref  = %s\n" % self.libref
        x += "Table   = %s\n" % self.table
        x += "Dsopts  = %s\n" % str(self.dsopts)
        x += "Results = %s\n" % self.results
        return(x)

    def set_results(self, results: str):
        """
        This method set the results attribute for the SASdata object; it stays in effect till changed
        results - set the default result type for this SASdata object. 'Pandas' or 'HTML' or 'TEXT'.

        :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives
        :return: None
        """
        if results.upper() == "HTML":
            self.HTML = 1
        else:
            self.HTML = 0
        self.results = results

    def _is_valid(self):
        if self.sas.exist(self.table, self.libref):
            return None
        else:
            msg = "The SAS Data Set that this SASdata object refers to, " + self.libref + '.' + self.table + ", does not exist in this SAS session at this time."
            ll = {'LOG': msg, 'LST': msg}
            return ll

    def _checkLogForError(self, log):
        lines = re.split(r'[\n]\s*', log)
        for line in lines:
            if line[self.sas.logoffset:].startswith('ERROR'):
                return (False, line)
        return (True, '')

    def _returnPD(self, code, tablename, **kwargs):
        """
        private function to take a sas code normally to create a table, generate pandas data frame and cleanup.

        :param code: string of SAS code
        :param tablename: the name of the SAS Data Set
        :param kwargs:
        :return: Pandas Data Frame
        """
        if self.sas.sascfg.pandas:
           raise type(self.sas.sascfg.pandas)(self.sas.sascfg.pandas.msg)

        libref = kwargs.get('libref','work')
        ll = self.sas._io.submit(code)
        check, errorMsg = self._checkLogForError(ll['LOG'])
        if not check:
            raise ValueError("Internal code execution failed: " + errorMsg)
        if isinstance(tablename, str):
            df = self.sas.sasdata2dataframe(tablename, libref)
            self.sas._io.submit("proc delete data=%s.%s; run;" % (libref, tablename))
        elif isinstance(tablename, list):
            df = dict()
            for t in tablename:
                # strip leading '_' from names and capitalize for dictionary labels
                if self.sas.exist(t, libref):
                   df[t.replace('_', '').capitalize()] = self.sas.sasdata2dataframe(t, libref)
                self.sas._io.submit("proc delete data=%s.%s; run;" % (libref, t))
        else:
            raise SyntaxError("The tablename must be a string or list %s was submitted" % str(type(tablename)))

        return df

    def _dsopts(self):
        """
        This method builds out data set options clause for this SASdata object: '(where= , keeep=, obs=, ...)'
        """
        return self.sas._dsopts(self.dsopts)

    def where(self, where: str) -> 'SASdata':
        """
        This method returns a clone of the SASdata object, with the where attribute set. The original SASdata object is not affected.

        :param where: the where clause to apply
        :return: SAS data object
        """
        sd = SASdata(self.sas, self.libref, self.table, dsopts=dict(self.dsopts))
        sd.HTML = self.HTML
        sd.dsopts['where'] = where
        return sd

    def head(self, obs=5):
        """
        display the first n rows of a table

        :param obs: the number of rows of the table that you want to display. The default is 5
        :return:
        """
        lastlog = len(self.sas._io._log)

        topts   = dict(self.dsopts)
        optkeys = self.dsopts.keys()

        if self.engine != 'SPDE':
           firstobs = topts.get('firstobs', 1)
           topts['obs'] = min(topts.get('obs', firstobs+obs-1), firstobs+obs-1)
        else:
           firstobs = topts.get('startobs', 1)
           topts['endobs'] = min(topts.get('endobs', topts.get('obs', firstobs+obs-1)), firstobs+obs-1)

           if 'obs' in optkeys:
              del topts['obs']

        code = "proc print data=" + self.libref + ".'" + self.table.replace("'", "''") + "'n " + self.sas._dsopts(topts) + ";run;"

        if self.sas.nosub:
            print(code)
            return

        if self.results.upper() == 'PANDAS':
            code = "data work._head ; set %s.'%s'n %s; run;" % (self.libref, self.table.replace("'", "''"), self.sas._dsopts(topts))
            df   = self._returnPD(code, '_head')
            self.sas._lastlog = self.sas._io._log[lastlog:]
            return df
        else:
            ll = self._is_valid()
            self.sas._lastlog = self.sas._io._log[lastlog:]
            if self.HTML:
                if not ll:
                    ll = self.sas._io.submit(code)
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                if not self.sas.batch:
                   self.sas._render_html_or_log(ll)
                else:
                    return ll
            else:
                if not ll:
                    ll = self.sas._io.submit(code, "text")
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                if not self.sas.batch:
                    print(ll['LST'])
                else:
                    return ll

    def tail(self, obs=5):
        """
        display the last n rows of a table

        :param obs: the number of rows of the table that you want to display. The default is 5
        :return:
        """
        lastlog = len(self.sas._io._log)

        nosub = self.sas.nosub
        self.sas.nosub = False
        nobs = self.obs()
        self.sas.nosub = nosub

        if nobs is None:
            return None

        if nobs < obs:
            obs = nobs

        topts   = dict(self.dsopts)
        optkeys = topts.keys()

        if self.engine != 'SPDE':
           firstobs = topts.get('firstobs', 1)
           lastobs  = topts.get('obs', nobs+firstobs-1)
           firstobs = max(lastobs - obs+1, firstobs)

           topts['obs']      = lastobs
           topts['firstobs'] = firstobs

        else:
           firstobs = topts.get('startobs', 1)
           lastobs  = topts.get('endobs', topts.get('obs', nobs+firstobs-1))
           firstobs = max(lastobs - obs+1, firstobs)

           topts['endobs']   = lastobs
           topts['startobs'] = firstobs

           if 'obs' in optkeys:
              del topts['obs']

        code  = "proc print data=" + self.libref + ".'"
        code += self.table.replace("'", "''") + "'n " + self.sas._dsopts(topts) + ";run;"

        if self.sas.nosub:
            print(code)
            return

        if self.results.upper() == 'PANDAS':
            code = "data work._tail ; set %s.'%s'n %s; run;" % (self.libref, self.table.replace("'", "''"), self.sas._dsopts(topts))
            df   = self._returnPD(code, '_tail')
            self.sas._lastlog = self.sas._io._log[lastlog:]
            return df
        else:
            le = self._is_valid()
            if self.HTML:
                if not le:
                    ll = self.sas._io.submit(code)
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                else:
                    ll = le
                if not self.sas.batch:
                    self.sas._render_html_or_log(ll)
                else:
                    return ll
            else:
                if not le:
                    ll = self.sas._io.submit(code, "text")
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                else:
                    ll = le
                if not self.sas.batch:
                    print(ll['LST'])
                else:
                    return ll

    def obs(self, force: bool = False) -> int:
        """
        :param force: if nobs isn't availble, set to True to force it to be calculated; may take time
        :return: int # the number of observations for your SASdata object
        """
        lastlog = len(self.sas._io._log)

        if self.engine == 'SPDE':
           if self.dsopts.get('startobs', None) or self.dsopts.get('endobs', None):
              force = True

        code  = "%let lastobs=-1;\n"
        if not force:
           code += "proc sql;select count(*) format best32. into :lastobs from "+ self.libref + ".'"
           code +=  self.table.replace("'", "''") + "'n " + self._dsopts() + ";"
           code += "%put lastobs=&lastobs lastobsend=;\nquit;"
        else:
           code += "data work.sasdata2dataframe / view=work.sasdata2dataframe; set "+ self.libref + ".'"
           code +=  self.table.replace("'", "''") + "'n " + self._dsopts() +";run;\n"
           code += "proc sql;select count(*) format best32. into :lastobs from work.sasdata2dataframe;"
           code += "%put lastobs=&lastobs lastobsend=;\nquit;\n"
           code += "proc delete data=work.sasdata2dataframe(memtype=view);run;"

        if self.sas.nosub:
            print(code)
            return

        le = self._is_valid()
        if not le:
            ll = self.sas._io.submit(code, "text")

            lastobs = ll['LOG'].rpartition("lastobs=")
            lastobs = lastobs[2].partition(" lastobsend=")
            lastobs = int(lastobs[0])
        else:
            logger.error("The SASdata object is not valid. The table doesn't exist in this SAS session at this time.")
            lastobs = None

        if lastobs == -1:
            logger.error("The number of obs was not able to be determined. You can specify obs(force=True) to force it to be calculated")
            #print(ll['LOG'])
            lastobs = None

        self.sas._lastlog = self.sas._io._log[lastlog:]
        return lastobs

    def partition(self, var: str = '', fraction: float = .7, seed: int = 9878, kfold: int = 1,
                  out: 'SASdata' = None, singleOut: bool = True) -> object:
        """
        Partition a sas data object using SRS sampling or if a variable is specified then
        stratifying with respect to that variable

        :param var: variable(s) for stratification. If multiple then space delimited list
        :param fraction: fraction to split
        :param seed: random seed
        :param kfold: number of k folds
        :param out: the SAS data object
        :param singleOut: boolean to return single table or seperate tables
        :return: Tuples or SAS data object
        """
        lastlog = len(self.sas._io._log)
        # loop through for k folds cross-validation
        i = 1
        # initialize code string so that loops work
        code = ''
        # Make sure kfold was an integer
        try:
            k = int(kfold)
        except ValueError:
            logger.error("Kfold must be an integer")
        if out is None:
            out_table = self.table
            out_libref = self.libref
        elif not isinstance(out, str):
            out_table = out.table
            out_libref = out.libref
        else:
            try:
                out_table = out.split('.')[1].strip()
                out_libref = out.split('.')[0]
            except IndexError:
                out_table = out.strip()
                out_libref = 'work'
        while i <= k:
            # get the list of variables
            if k == 1:
                code += "proc hpsample data=%s.'%s'n %s out=%s.'%s'n %s samppct=%s seed=%s Partition;\n" % (
                    self.libref, self.table.replace("'", "''"), self._dsopts(), out_libref, out_table.replace("'", "''"), self._dsopts(), fraction * 100,
                    seed)
            else:
                seed += 1
                code += "proc hpsample data=%s.'%s'n %s out=%s.'%s'n %s samppct=%s seed=%s partition PARTINDNAME=_cvfold%s;\n" % (
                    self.libref, self.table.replace("'", "''"), self._dsopts(), out_libref, out_table.replace("'", "''"), self._dsopts(), fraction * 100,
                    seed, i)

            # Get variable info for stratified sampling
            if len(var) > 0:
                if i == 1:
                    num_string = """
                        data _null_; file LOG;
                          d = open("{0}.'{1}'n");
                          nvars = attrn(d, 'NVARS');
                          put 'VARLIST=';
                          do i = 1 to nvars;
                             vart = vartype(d, i);
                             var  = varname(d, i);
                             if vart eq 'N' then
                                put %upcase('var=') var %upcase('varEND=');
                          end;
                          put 'VARLISTEND=';
                        run;
                        """
                    # ignore teach_me_SAS mode to run contents
                    nosub = self.sas.nosub
                    self.sas.nosub = False
                    ll = self.sas._io.submit(num_string.format(self.libref, self.table.replace("'", "''") + self._dsopts()))
                    self.sas.nosub = nosub

                    numlist = []
                    log = ll['LOG'].rpartition('VARLISTEND=')[0].rpartition('VARLIST=')

                    for vari in range(log[2].count('VAR=')):
                       log = log[2].partition('VAR=')[2].partition(' VAREND=')
                       numlist.append(log[0].strip())

                   # check if var is in numlist
                    if isinstance(var, str):
                        tlist = var.split()
                    elif isinstance(var, list):
                        tlist = var
                    else:
                        raise SyntaxError("var must be a string or list you submitted: %s" % str(type(var)))
                if set(numlist).isdisjoint(tlist):
                    if isinstance(var, str):
                        code += "class _character_;\ntarget %s;\nvar _numeric_;\n" % var
                    else:
                        code += "class _character_;\ntarget %s;\nvar _numeric_;\n" % " ".join(var)
                else:
                    varlist = [x for x in numlist if x not in tlist]
                    varlist.extend(["_cvfold%s" % j for j in range(1, i) if k > 1 and i > 1])
                    code += "class %s _character_;\ntarget %s;\nvar %s;\n" % (var, var, " ".join(varlist))

            else:
                code += "class _character_;\nvar _numeric_;\n"
            code += "run;\n"
            i += 1
        # split_code is used if singleOut is False it generates the needed SAS code to break up the kfold partition set.
        split_code = ''
        if not singleOut:
            split_code += 'DATA '
            for j in range(1, k + 1):
                split_code += "\t%s.'%s%s_train'n (drop=_Partind_ _cvfold:)\n" % (out_libref, out_table.replace("'", "''"), j)
                split_code += "\t%s.'%s%s_score'n (drop=_Partind_ _cvfold:)\n" % (out_libref, out_table.replace("'", "''"), j)
            split_code += ";\n \tset %s.'%s'n;\n" % (out_libref, out_table.replace("'", "''"))
            for z in range(1, k + 1):
                split_code += "\tif _cvfold%s = 1 or _partind_ = 1 then output %s.'%s%s_train'n;\n" % (z, out_libref, out_table.replace("'", "''"), z)
                split_code += "\telse output %s.'%s%s_score'n;\n" % (out_libref, out_table.replace("'", "''"), z)
            split_code += 'run;'
        runcode = True
        if self.sas.nosub:
            print(code + '\n\n' + split_code)
            runcode = False
        ll = self._is_valid()
        self.sas._lastlog = self.sas._io._log[lastlog:]
        if ll:
            runcode = False
        if runcode:
            ll = self.sas._io.submit(code + split_code, "text")
            self.sas._lastlog = self.sas._io._log[lastlog:]
            elog = []
            for line in ll['LOG'].splitlines():
                if line[self.sas.logoffset:].startswith('ERROR'):
                    elog.append(line)
            if len(elog):
                raise RuntimeError("\n".join(elog))
            if not singleOut:
                outTableList = []
                if k == 1:
                    ret =  (self.sas.sasdata(out_table + str(k) + "_train", out_libref, dsopts=self._dsopts()),
                            self.sas.sasdata(out_table + str(k) + "_score", out_libref, dsopts=self._dsopts()))
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                    return ret
                for j in range(1, k + 1):
                    outTableList.append((self.sas.sasdata(out_table + str(j) + "_train", out_libref, dsopts=self._dsopts()),
                                         self.sas.sasdata(out_table + str(j) + "_score", out_libref, dsopts=self._dsopts())))
                self.sas._lastlog = self.sas._io._log[lastlog:]
                return outTableList
            if out:
                if not isinstance(out, str):
                    return out
                else:
                    ret = self.sas.sasdata(out_table, out_libref, self.results)
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                    return ret
            else:
                return self

    def contents(self, results=None):
        """
        display metadata about the table. size, number of rows, columns and their data type ...
        You can override the format of the output with the results= option for this invocation

        :return: output
        """
        lastlog = len(self.sas._io._log)
        code = "proc contents data=" + self.libref + ".'" + self.table.replace("'", "''") + "'n " + self._dsopts() + ";run;"

        if self.sas.nosub:
            print(code)
            return

        results = self.results.upper() if results is None else results.upper()

        ll = self._is_valid()
        if results == 'PANDAS':
            code  = "proc contents data=%s.'%s'n %s ;" % (self.libref, self.table.replace("'", "''"), self._dsopts())
            code += "ods output Attributes=work._attributes;"
            code += "ods output EngineHost=work._EngineHost;"
            code += "ods output Variables=work._Variables;"
            code += "ods output Sortedby=work._Sortedby;"
            code += "run;"
            df = self._returnPD(code, ['_attributes', '_EngineHost', '_Variables', '_Sortedby'])
            self.sas._lastlog = self.sas._io._log[lastlog:]
            return df
        else:
            if results == 'HTML' and self.HTML:
                if not ll:
                    ll = self.sas._io.submit(code)
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                if not self.sas.batch:
                    self.sas._render_html_or_log(ll)
                else:
                    return ll
            else:
                if not ll:
                    ll = self.sas._io.submit(code, "text")
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                if not self.sas.batch:
                    print(ll['LST'])
                else:
                    return ll

    def columnInfo(self):
        """
        display metadata about the table, size, number of rows, columns and their data type
        """
        lastlog = len(self.sas._io._log)
        code = "proc contents data=" + self.libref + ".'" + self.table.replace("'", "''") + "'n " + self._dsopts() + ";ods select Variables;run;"

        if self.sas.nosub:
            print(code)
            return

        if self.results.upper() == 'PANDAS':
            code = "proc contents data=%s.'%s'n %s ;ods output Variables=work._variables ;run;" % (self.libref, self.table.replace("'", "''"), self._dsopts())
            df = self._returnPD(code, '_variables')
            df['Type'] = df['Type'].str.rstrip()
            self.sas._lastlog = self.sas._io._log[lastlog:]
            return df

        else:
            ll = self._is_valid()
            if self.HTML:
                if not ll:
                    ll = self.sas._io.submit(code)
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                if not self.sas.batch:
                    self.sas._render_html_or_log(ll)
                else:
                    return ll
            else:
                if not ll:
                    ll = self.sas._io.submit(code, "text")
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                if not self.sas.batch:
                    print(ll['LST'])
                else:
                    return ll

    def info(self):
        """
        Display the column info on a SAS data object

        :return: Pandas data frame
        """
        lastlog = len(self.sas._io._log)
        if self.results.casefold() != 'pandas':
            logger.error("The info method only works with Pandas results")
            return None
        info_code = """
        data work._statsInfo ;
            do rows=0 by 1 while( not last ) ;
                set {0}.'{1}'n {2} end=last;
                array chrs _character_ ;
                array nums _numeric_ ;
                array ccounts(999) _temporary_ ;
                array ncounts(999) _temporary_ ;
                do over chrs;
                    ccounts(_i_) + missing(chrs) ;
                end;
                do over nums;
                    ncounts(_i_) + missing(nums);
                end;
            end ;
            length Variable $32 type $8. ;
            Do over chrs;
                Type = 'char';
                Variable = vname(chrs) ;
                N = rows;
                Nmiss = ccounts(_i_) ;
                Output ;
            end ;
            Do over nums;
                Type = 'numeric';
                Variable = vname(nums) ;
                N = rows;
                Nmiss = ncounts(_i_) ;
                if variable ^= 'rows' then output;
            end ;
            stop;
            keep Variable N NMISS Type ;
        run;
        """
        if self.sas.nosub:
            print(info_code.format(self.libref, self.table, self._dsopts()))
            return None
        df = self._returnPD(info_code.format(self.libref, self.table.replace("'", "''"), self._dsopts()), '_statsInfo')
        df = df.iloc[:, :]
        df.index.name = None
        df.name = None
        self.sas._lastlog = self.sas._io._log[lastlog:]
        return df

    def describe(self):
        """
        display descriptive statistics for the table; summary statistics.

        :return:
        """
        return self.means()

    def means(self):
        """
        display descriptive statistics for the table; summary statistics. This is an alias for 'describe'

        :return:
        """
        lastlog = len(self.sas._io._log)
        dsopts = self._dsopts().partition(';\n\tformat')

        code  = "proc means data=" + self.libref + ".'" + self.table.replace("'", "''") + "'n " + dsopts[0] + " stackodsoutput n nmiss median mean std min p25 p50 p75 max;"
        code += dsopts[1]+dsopts[2]+"run;"

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()

        if self.results.upper() == 'PANDAS':
            code = "proc means data=%s.'%s'n %s stackodsoutput n nmiss median mean std min p25 p50 p75 max; %s ods output Summary=work._summary; run;" % (
                self.libref, self.table.replace("'", "''"), dsopts[0], dsopts[1]+dsopts[2])
            df = self._returnPD(code, '_summary')
            self.sas._lastlog = self.sas._io._log[lastlog:]
            return df
        else:
            if self.HTML:
               if not ll:
                  ll = self.sas._io.submit(code)
                  self.sas._lastlog = self.sas._io._log[lastlog:]
               if not self.sas.batch:
                  self.sas._render_html_or_log(ll)
               else:
                  return ll
            else:
               if not ll:
                  ll = self.sas._io.submit(code, "text")
                  self.sas._lastlog = self.sas._io._log[lastlog:]
               if not self.sas.batch:
                  print(ll['LST'])
               else:
                  return ll

    def impute(self, vars: dict, replace: bool = False, prefix: str = 'imp_', out: 'SASdata' = None) -> 'SASdata':
        """
        Imputes missing values for a SASdata object.

        :param vars: a dictionary in the form of {'varname':'impute type'} or {'impute type':'[var1, var2]'}
        :param replace:
        :param prefix:
        :param out:
        :return: 'SASdata'
        """
        lastlog = len(self.sas._io._log)
        outstr = ''
        if out:
            if isinstance(out, str):
                fn = out.partition('.')
                if fn[1] == '.':
                    out_libref = fn[0]
                    out_table = fn[2].strip()
                else:
                    out_libref = ''
                    out_table = fn[0].strip()
            else:
                out_libref = out.libref
                out_table = out.table
            outstr = "out=%s.'%s'n" % (out_libref, out_table.replace("'", "''"))

        else:
            out_table = self.table
            out_libref = self.libref

        # get list of variables and types
        varcode  = 'data _null_; d = open("' + self.libref + ".'" + self.table.replace("'", "''") + "'n " + '");\n'
        varcode += "nvars = attrn(d, 'NVARS');\n"
        varcode += "put 'VARNUMS=' nvars 'VARNUMS_END=';\n"
        varcode += "put 'VARLIST=';\n"
        varcode += "do i = 1 to nvars; var = varname(d, i); put %upcase('var=') var %upcase('varEND='); end;\n"
        varcode += "put 'TYPELIST=';\n"
        varcode += "do i = 1 to nvars; var = vartype(d, i); put %upcase('type=') var %upcase('typeEND='); end;\n"
        varcode += "put 'END_ALL_VARS_AND_TYPES=';\n"
        varcode += "run;"

        ll = self.sas._io.submit(varcode, "text")

        l2 = ll['LOG'].rpartition("VARNUMS=")[2].partition("VARNUMS_END=")
        nvars = int(float(l2[0].strip()))

        varlist = []
        log = ll['LOG'].rpartition('TYPELIST=')[0].rpartition('VARLIST=')

        for vari in range(log[2].count('VAR=')):
           log = log[2].partition('VAR=')[2].partition('VAREND=')
           varlist.append(log[0].strip().upper())

        typelist = []
        log = ll['LOG'].rpartition('END_ALL_VARS_AND_TYPES=')[0].rpartition('TYPELIST=')

        for typei in range(log[2].count('VAR=')):
           log = log[2].partition('TYPE=')[2].partition('TYPEEND=')
           typelist.append(log[0].strip().upper())

        varListType = dict(zip(varlist, typelist))

        # process vars dictionary to generate code
        ## setup default statements
        sql = "proc sql;\n  select\n"
        sqlsel = ' %s(%s),\n'
        sqlinto = ' into\n'
        if len(out_libref)>0 :
            ds1 = "data " + out_libref + ".'" + out_table.replace("'", "''") + "'n " + "; set " + self.libref + ".'" + self.table.replace("'", "''") +"'n " + self._dsopts() + ";\n"
        else:
            ds1 = "data '"                    + out_table.replace("'", "''") + "'n " + "; set " + self.libref + ".'" + self.table.replace("'", "''") +"'n " + self._dsopts() + ";\n"
        dsmiss = 'if missing({0}) then {1} = {2};\n'
        if replace:
            dsmiss = prefix+'{1} = {0}; if missing({0}) then %s{1} = {2};\n' % prefix

        modesql = ''
        modeq = "proc sql outobs=1;\n  select %s, count(*) as freq into :imp_mode_%s, :imp_mode_freq\n"
        modeq += "  from %s where %s is not null group by %s order by freq desc, %s;\nquit;\n"

        # pop the values key because it needs special treatment
        contantValues = vars.pop('value', None)
        if contantValues is not None:
            if not all(isinstance(x, tuple) for x in contantValues):
                raise SyntaxError("The elements in the 'value' key must be tuples")
            for t in contantValues:
                if varListType.get(t[0].upper()) == "N":
                    ds1 += dsmiss.format((t[0], t[0], t[1]))
                else:
                    ds1 += dsmiss.format(t[0], t[0], '"' + str(t[1]) + '"')
        for key, values in vars.items():
            if key.lower() in ['midrange', 'random']:
                for v in values:
                    sql += sqlsel % ('max', v)
                    sql += sqlsel % ('min', v)
                    sqlinto += ' :imp_max_' + v + ',\n'
                    sqlinto += ' :imp_min_' + v + ',\n'
                    if key.lower() == 'midrange':
                        ds1 += dsmiss.format(v, v, '(&imp_min_' + v + '.' + ' + ' + '&imp_max_' + v + '.' + ') / 2')
                    elif key.lower() == 'random':
                        # random * (max - min) + min
                        ds1 += dsmiss.format(v, v, '(&imp_max_' + v + '.' + ' - ' + '&imp_min_' + v + '.' + ') * ranuni(0)' + '+ &imp_min_' + v + '.')
                    else:
                        raise SyntaxError("This should not happen!!!!")
            else:
                for v in values:
                    sql += sqlsel % (key, v)
                    sqlinto += ' :imp_' + v + ',\n'
                    if key.lower == 'mode':
                        modesql += modeq % (v, v, self.libref + ".'" + self.table.replace("'", "''") + "'n " + self._dsopts() , v, v, v)
                    if varListType.get(v.upper()) == "N":
                        ds1 += dsmiss.format(v, v, '&imp_' + v + '.')
                    else:
                        ds1 += dsmiss.format(v, v, '"&imp_' + v + '."')

        if len(sql) > 20:
            sql = sql.rstrip(', \n') + '\n' + sqlinto.rstrip(', \n') + '\n  from ' + self.libref + ".'" + self.table.replace("'", "''") + "'n " + self._dsopts() + ';\nquit;\n'
        else:
            sql = ''
        ds1 += 'run;\n'

        if self.sas.nosub:
            print(modesql + sql + ds1)
            return None
        ll  = self.sas._io.submit(modesql + sql + ds1)
        ret = self.sas.sasdata(out_table, libref=out_libref, results=self.results, dsopts=self._dsopts())
        self.sas._lastlog = self.sas._io._log[lastlog:]
        return ret

    def sort(self, by: str, out: object = '', **kwargs) -> 'SASdata':
        """
        Sort the SAS Data Set

        :param by: REQUIRED variable to sort by (BY <DESCENDING> variable-1 <<DESCENDING> variable-2 ...>;)
        :param out: OPTIONAL takes either a string 'libref.table' or 'table' which will go to WORK or USER
            if assigned or a sas data object'' will sort in place if allowed
        :param kwargs:
        :return: SASdata object if out= not specified, or a new SASdata object for out= when specified

        :Example:

        #. wkcars.sort('type')
        #. wkcars2 = sas.sasdata('cars2')
        #. wkcars.sort('cylinders', wkcars2)
        #. cars2=cars.sort('DESCENDING origin', out='foobar')
        #. cars.sort('type').head()
        #. stat_results = stat.reg(model='horsepower = Cylinders EngineSize', by='type', data=wkcars.sort('type'))
        #. stat_results2 = stat.reg(model='horsepower = Cylinders EngineSize', by='type', data=wkcars.sort('type','work.cars'))
        """
        lastlog = len(self.sas._io._log)
        outstr = ''
        options = ''
        if out:
            if isinstance(out, str):
                fn = out.partition('.')
                if fn[1] == '.':
                    libref = fn[0]
                    table  = fn[2].strip()
                    outstr = "out=%s.'%s'n" % (libref, table.replace("'", "''"))
                else:
                    libref = ''
                    table  = fn[0].strip()
                    outstr = "out='" + table.replace("'", "''") + "'n "
            else:
                libref = out.libref
                table  = out.table
                outstr = "out=%s.'%s'n" % (out.libref, out.table.replace("'", "''"))

        if 'options' in kwargs:
            options = kwargs['options']

        code = "proc sort data=%s.'%s'n %s %s %s ;\n" % (self.libref, self.table.replace("'", "''"), self._dsopts(), outstr, options)
        code += "by %s;" % by
        code += "run\n;"
        runcode = True
        if self.sas.nosub:
            print(code)
            runcode = False

        ll = self._is_valid()
        if ll:
            runcode = False
        self.sas._lastlog = self.sas._io._log[lastlog:]
        if runcode:
            ll = self.sas._io.submit(code, "text")
            self.sas._lastlog = self.sas._io._log[lastlog:]
            elog = []
            for line in ll['LOG'].splitlines():
                if line[self.sas.logoffset:].startswith('ERROR'):
                    elog.append(line)
            if len(elog):
                raise RuntimeError("\n".join(elog))
        if out:
            if not isinstance(out, str):
                return out
            else:
                ret = self.sas.sasdata(table, libref, self.results)
                self.sas._lastlog = self.sas._io._log[lastlog:]
                return ret
        else:
            return self

    def add_vars(self, vars: dict, out: object = None, **kwargs):
        """
        Copy table to itesf, or to 'out=' table and add any vars if you want

        :param vars: REQUIRED dictionayr of variable names (keys) and assignment statement (values)
               to maintain variable order use collections.OrderedDict Assignment statements must be valid
               SAS assignment expressions.
        :param out: OPTIONAL takes a SASdata Object you create ahead of time. If not specified, replaces the existing table
               and the current SAS data object still refers to the replacement table.
        :param kwargs:
        :return: SAS Log showing what happened

        :Example:

        #. cars   = sas.sasdata('cars', 'sashelp')
        #. wkcars = sas.sasdata('cars')
        #. cars.add_vars({'PW_ratio': 'weight / horsepower', 'Overhang' : 'length - wheelbase'}, wkcars)
        #. wkcars.head()
        """
        lastlog = len(self.sas._io._log)

        if out is not None:
           if not isinstance(out, SASdata):
              logger.error("out= needs to be a SASdata object")
              return None
           else:
              outtab = out.libref + ".'" + out.table.replace("'", "''") + "'n " + out._dsopts()
        else:
           outtab = self.libref + ".'" + self.table.replace("'", "''") + "'n " + self._dsopts()

        code  = "data "+outtab+"; set " + self.libref + ".'" + self.table.replace("'", "''") + "'n " + self._dsopts() + ";\n"
        for key in vars.keys():
           code += key+" = "+vars[key]+";\n"
        code += "; run;"

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()
        if not ll:
            ll = self.sas._io.submit(code, "text")
        self.sas._lastlog = self.sas._io._log[lastlog:]
        if not self.sas.batch:
            print(ll['LOG'])
        else:
            return ll

    def assessModel(self, target: str, prediction: str, nominal: bool = True, event: str = '', **kwargs):
        """
        This method will calculate assessment measures using the SAS AA_Model_Eval Macro used for SAS Enterprise Miner.
        Not all datasets can be assessed. This is designed for scored data that includes a target and prediction columns
        TODO: add code example of build, score, and then assess

        :param target: string that represents the target variable in the data
        :param prediction: string that represents the numeric prediction column in the data. For nominal targets this should a probability between (0,1).
        :param nominal: boolean to indicate if the Target Variable is nominal because the assessment measures are different.
        :param event: string which indicates which value of the nominal target variable is the event vs non-event
        :param kwargs:
        :return: SAS result object
        """
        lastlog = len(self.sas._io._log)
        # submit autocall macro
        self.sas._io.submit("%aamodel;")
        objtype = "datastep"
        objname = '{s:{c}^{n}}'.format(s=self.table[:3], n=3,
                                       c='_') + self.sas._objcnt()  # translate to a libname so needs to be less than 8
        code = "%macro proccall(d);\n"

        # build parameters
        score_table = str(self.libref + ".'" + self.table.replace("'", "''") + "'n " )
        binstats = str(objname + '.' + "ASSESSMENTSTATISTICS")
        out = str(objname + '.' + "ASSESSMENTBINSTATISTICS")
        level = 'interval'
        # var = 'P_' + target
        if nominal:
            level = 'class'
            # the user didn't specify the event for a nominal Give them the possible choices
            try:
                if len(event) < 1:
                    raise Exception(event)
            except Exception:
                logger.warning("No event was specified for a nominal target. Here are possible options:\n")
                event_code = "proc hpdmdb data=%s.'%s'n %s classout=work._DMDBCLASSTARGET(keep=name nraw craw level frequency nmisspercent);" % (
                    self.libref, self.table.replace("'", "''"), self._dsopts())
                event_code += "\nclass %s ; \nrun;" % target
                event_code += "data _null_; set work._DMDBCLASSTARGET; where ^(NRAW eq . and CRAW eq '') and lowcase(name)=lowcase('%s');" % target
                ec = self.sas._io.submit(event_code)
                self.sas.HTML(ec['LST'])
                # TODO: Finish output of the list of nominals variables

        if nominal:
            code += "%%aa_model_eval(DATA=%s%s, TARGET=%s, VAR=%s, level=%s, BINSTATS=%s, bins=100, out=%s,  EVENT=%s);" \
                    % (score_table, self._dsopts(), target, prediction, level, binstats, out, event)
        else:
            code += "%%aa_model_eval(DATA=%s%s, TARGET=%s, VAR=%s, level=%s, BINSTATS=%s, bins=100, out=%s);" \
                    % (score_table, self._dsopts(), target, prediction, level, binstats, out)
        rename_char = """
        data {0};
            set {0};
            if level in ("INTERVAL", "INT") then do;
                rename  _sse_ = SumSquaredError
                        _div_ = Divsor
                        _ASE_ = AverageSquaredError
                        _RASE_ = RootAverageSquaredError
                        _MEANP_ = MeanPredictionValue
                        _STDP_ = StandardDeviationPrediction
                        _CVP_ = CoefficientVariationPrediction;
            end;
            else do;
                rename  CR = MaxClassificationRate
                        KSCut = KSCutOff
                        CRDEPTH =  MaxClassificationDepth
                        MDepth = MedianClassificationDepth
                        MCut  = MedianEventDetectionCutOff
                        CCut = ClassificationCutOff
                        _misc_ = MisClassificationRate;
            end;
        run;
        """
        code += rename_char.format(binstats)
        if nominal:
            # TODO: add graphics code here to return to the SAS results object
            graphics ="""
            ODS PROCLABEL='ERRORPLOT' ;
            proc sgplot data={0};
                title "Error and Correct rate by Depth";
                series x=depth y=correct_rate;
                series x=depth y=error_rate;
                yaxis label="Percentage" grid;
            run;
            /* roc chart */
            ODS PROCLABEL='ROCPLOT' ;

            proc sgplot data={0};
                title "ROC Curve";
                series x=one_minus_specificity y=sensitivity;
                yaxis grid;
            run;
            /* Lift and Cumulative Lift */
            ODS PROCLABEL='LIFTPLOT' ;
            proc sgplot data={0};
                Title "Lift and Cumulative Lift";
                series x=depth y=c_lift;
                series x=depth y=lift;
                yaxis grid;
            run;
            """
            code += graphics.format(out)
        code += "run; quit; %mend;\n"
        code += "%%mangobj1(%s,%s,'%s'n);" % (objname, objtype, self.table.replace("'", "''"))
        code += "%%mangobj2(%s,%s,'%s'n);" % (objname, objtype, self.table.replace("'", "''"))

        if self.sas.nosub:
            print(code)
            return

        ll   = self.sas._io.submit(code, 'text')
        obj1 = sp2.SASProcCommons._objectmethods(self, objname)
        ret  = sp2.SASresults(obj1, self.sas, objname, self.sas.nosub, ll['LOG'])

        self.sas._lastlog = self.sas._io._log[lastlog:]
        return ret

    def to_csv(self, file: str, opts: dict = None) -> str:
        """
        This method will export a SAS Data Set to a file in CSV format.

        :param file: the OS filesystem path of the file to be created (exported from this SAS Data Set)
        :param opts: a dictionary containing any of the following Proc Export options(delimiter, putnames)

            - delimiter is a single character
            - putnames is a bool  [True | False]

            .. code-block:: python

                             {'delimiter' : '~',
                              'putnames'  : True
                             }
        :return:
        """
        lastlog = len(self.sas._io._log)
        opts = opts if opts is not None else {}
        ll = self._is_valid()
        self.sas._lastlog = self.sas._io._log[lastlog:]
        if ll:
            if not self.sas.batch:
                print(ll['LOG'])
            else:
                return ll
        else:
            csv = self.sas.write_csv(file, self.table, self.libref, self.dsopts, opts)
            self.sas._lastlog = self.sas._io._log[lastlog:]
            return csv

    def score(self, file: str = '', code: str = '', out: 'SASdata' = None) -> 'SASdata':
        """
        This method is meant to update a SAS Data object with a model score file.

        :param file: a file reference to the SAS score code
        :param code: a string of the valid SAS score code
        :param out: Where to the write the file. Defaults to update in place
        :return: The Scored SAS Data object.
        """
        lastlog = len(self.sas._io._log)
        if out is not None:
            outTable = out.table
            outLibref = out.libref
        else:
            outTable = self.table
            outLibref = self.libref
        codestr = code
        code = "data %s.'%s'n %s;" % (outLibref, outTable.replace("'", "''"), self._dsopts())
        code += "set %s.'%s'n %s;" % (self.libref, self.table.replace("'", "''"), self._dsopts())
        if len(file)>0:
            code += '%%include "%s";' % file
        else:
            code += "%s;" %codestr
        code += "run;"

        if self.sas.nosub:
            print(code)
            return None

        ll = self._is_valid()
        if not ll:
            html = self.HTML
            self.HTML = 1
            ll = self.sas._io.submit(code)
            self.HTML = html

        self.sas._lastlog = self.sas._io._log[lastlog:]
        if not self.sas.batch:
            self.sas.DISPLAY(self.sas.HTML(ll['LST']))
        else:
            return ll

    def to_pq(self, parquet_file_path: str,
                    pa_parquet_kwargs = None,
                    pa_pandas_kwargs  = None,
                    partitioned       = False,
                    partition_size_mb = 128,
                    chunk_size_mb     = 4,
                    coerce_timestamp_errors = True,
                    static_columns:list     = None,
                    rowsep: str = '\x01', colsep: str = '\x02',
                    rowrep: str = ' ',    colrep: str = ' ',
                    **kwargs) -> None:
       """
       This method exports the SAS Data Set to a Parquet file. This is an alias for sasdata2parquet.

       :param parquet_file_path: path of the parquet file to create
       :param pa_parquet_kwargs: Additional parameters to pass to pyarrow.parquet.ParquetWriter (default is {"compression": 'snappy', "flavor": "spark", "write_statistics": False}).
       :param pa_pandas_kwargs: Additional parameters to pass to pyarrow.Table.from_pandas (default is {}).
       :param partitioned: Boolean indicating whether the parquet file should be written in partitions (default is False).
       :param partition_size_mb: The size in MB of each partition in memory (default is 128).
       :param chunk_size_mb: The chunk size in MB at which the stream is processed (default is 4).
       :param coerce_timestamp_errors: Whether to coerce errors when converting timestamps (default is True).
       :param static_columns: List of tuples (name, value) representing static columns that will be added to the parquet file (default is None).
       :param rowsep: the row seperator character to use; defaults to '\x01'
       :param colsep: the column seperator character to use; defaults to '\x02'
       :param rowrep: the char to convert to for any embedded rowsep chars, defaults to  ' '
       :param colrep: the char to convert to for any embedded colsep chars, defaults to  ' '

       Two new kwargs args as of V5.100.0 are for dealing with SAS dates and datetimes that are out of range of Pandats Timestamps. These values will
       be converted to NaT in the dataframe. The new feature is to specify a Timestamp value (str(Timestamp)) for the high value and/or low value
       to use to replace Nat's with in the dataframe. This works for both SAS datetime and date values.

       :param tsmin: str(Timestamp) used to replace SAS datetime and dates that are earlier than supported by Pandas Timestamp; pandas.Timestamp.min
       :param tsmax: str(Timestamp) used to replace SAS datetime and dates that are later   than supported by Pandas Timestamp; pandas.Timestamp.max

       :param kwargs: a dictionary. These vary per access method, and are generally NOT needed.
                      They are either access method specific parms or specific pandas parms.
                      See the specific sasdata2dataframe* method in the access method for valid possibilities.

       These two options are for advanced usage. They override how saspy imports data. For more info
       see https://sassoftware.github.io/saspy/advanced-topics.html#advanced-sd2df-and-df2sd-techniques

       :param dtype: this is the parameter to Pandas read_csv, overriding what saspy generates and uses
       :param my_fmts: bool, if True, overrides the formats saspy would use, using those on the data set or in dsopts=

       :return: None
       """
       lastlog = len(self.sas._io._log)

       parquet_kwargs = pa_parquet_kwargs if pa_parquet_kwargs is not None else {"compression": 'snappy',
                                                                                 "flavor":"spark",
                                                                                 "write_statistics":False
                                                                                 }
       pandas_kwargs  = pa_pandas_kwargs if pa_pandas_kwargs  is not None  else {}

       ll = self._is_valid()
       self.sas._lastlog = self.sas._io._log[lastlog:]
       if ll:
          print(ll['LOG'])
          return None
       else:
          self.sas.sasdata2parquet(parquet_file_path = parquet_file_path,
                                   table  = self.table,
                                   libref = self.libref,
                                   dsopts = self.dsopts,
                                   pa_parquet_kwargs = parquet_kwargs,
                                   pa_pandas_kwargs  = pandas_kwargs,
                                   partitioned = partitioned,
                                   partition_size_mb = partition_size_mb,
                                   chunk_size_mb = chunk_size_mb,
                                   coerce_timestamp_errors=coerce_timestamp_errors,
                                   static_columns = static_columns,
                                   rowsep = rowsep,
                                   colsep = colsep,
                                   rowrep = rowrep,
                                   colrep = colrep,
                                   **kwargs)
          self.sas._lastlog = self.sas._io._log[lastlog:]
          return None

    def to_frame(self, **kwargs) -> 'pandas.DataFrame':
        """
        This is just an alias for to_df()

        :param kwargs:
        :return: Pandas data frame
        :rtype: 'pd.DataFrame'
        """
        return self.to_df(**kwargs)

    def to_df(self, method: str = 'MEMORY', **kwargs) -> 'pandas.DataFrame':
        """
        Export this SAS Data Set to a Pandas Data Frame

        :param method: defaults to MEMORY; As of V3.7.0 all 3 of these now stream directly into read_csv() with no disk I/O\
                       and have much improved performance. MEM, the default, is now as fast as the others.

           - MEMORY the original method. Streams the data over and builds the dataframe on the fly in memory
           - CSV    uses an intermediary Proc Export csv file and pandas read_csv() to import it; faster for large data
           - DISK   uses the original (MEMORY) method, but persists to disk and uses pandas read to import.   \
                    this has better support than CSV for embedded delimiters (commas), nulls, CR/LF that CSV  \
                    has problems with

        For the MEMORY and DISK methods the following 4 parameters are also available, depending upon access method

        :param rowsep: the row seperator character to use; defaults to hex(1)
        :param colsep: the column seperator character to use; defaults to hex(2)
        :param rowrep: the char to convert to for any embedded rowsep chars, defaults to  ' '
        :param colrep: the char to convert to for any embedded colsep chars, defaults to  ' '


        Two new kwargs args as of V5.100.0 are for dealing with SAS dates and datetimes that are out of range of Pandats Timestamps. These values will
        be converted to NaT in the dataframe. The new feature is to specify a Timestamp value (str(Timestamp)) for the high value and/or low value
        to use to replace Nat's with in the dataframe. This works for both SAS datetime and date values.

        :param tsmin: str(Timestamp) used to replace SAS datetime and dates that are earlier than supported by Pandas Timestamp; pandas.Timestamp.min
        :param tsmax: str(Timestamp) used to replace SAS datetime and dates that are later   than supported by Pandas Timestamp; pandas.Timestamp.max

        These vary per access method, and are generally NOT needed. They are either access method specific parms or specific \
        pandas parms. See the specific sasdata2dataframe* method in the access method for valid possibilities.

        :param kwargs: a dictionary. These vary per access method, and are generally NOT needed.
                       They are either access method specific parms or specific pandas parms.
                       See the specific sasdata2dataframe* method in the access method for valid possibilities.

        :return: Pandas data frame
        """
        lastlog = len(self.sas._io._log)
        ll = self._is_valid()
        self.sas._lastlog = self.sas._io._log[lastlog:]
        if ll:
            print(ll['LOG'])
            return None
        else:
            if self.sas.sascfg.pandas:
               raise type(self.sas.sascfg.pandas)(self.sas.sascfg.pandas.msg)
            df = self.sas.sasdata2dataframe(self.table, self.libref, self.dsopts, method, **kwargs)
            self.sas._lastlog = self.sas._io._log[lastlog:]
            return df

    def to_df_CSV(self, tempfile: str=None, tempkeep: bool=False, opts: dict = None, **kwargs) -> 'pandas.DataFrame':
        """
        This is an alias for 'to_df' specifying method='CSV'.

        :param tempfile: [deprecated except for Local IOM] [optional] an OS path for a file to use for the local CSV file; default it a temporary file that's cleaned up
        :param tempkeep: [deprecated except for Local IOM] if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it
        :param opts: a dictionary containing any of the following Proc Export options(delimiter, putnames)

            - delimiter is a single character
            - putnames is a bool  [True | False]

            .. code-block:: python

                             {'delimiter' : '~',
                              'putnames'  : True
                             }

        Two new kwargs args as of V5.100.0 are for dealing with SAS dates and datetimes that are out of range of Pandats Timestamps. These values will
        be converted to NaT in the dataframe. The new feature is to specify a Timestamp value (str(Timestamp)) for the high value and/or low value
        to use to replace Nat's with in the dataframe. This works for both SAS datetime and date values.

        :param tsmin: str(Timestamp) used to replace SAS datetime and dates that are earlier than supported by Pandas Timestamp; pandas.Timestamp.min
        :param tsmax: str(Timestamp) used to replace SAS datetime and dates that are later   than supported by Pandas Timestamp; pandas.Timestamp.max

        These vary per access method, and are generally NOT needed. They are either access method specific parms or specific \
        pandas parms. See the specific sasdata2dataframe* method in the access method for valid possibilities.

        :param kwargs: a dictionary. These vary per access method, and are generally NOT needed.
                       They are either access method specific parms or specific pandas parms.
                       See the specific sasdata2dataframe* method in the access method for valid possibilities.

        :return: Pandas data frame
        :rtype: 'pd.DataFrame'
        """
        opts   =   opts if   opts is not None else {}
        return self.to_df(method='CSV', tempfile=tempfile, tempkeep=tempkeep, opts=opts, **kwargs)

    def to_df_DISK(self, rowsep: str = '\x01', colsep: str = '\x02',
                   rowrep: str = ' ',    colrep: str = ' ', **kwargs) -> 'pandas.DataFrame':
        """
        This is an alias for 'to_df' specifying method='DISK'.

        :param rowsep: the row seperator character to use; defaults to hex(1)
        :param colsep: the column seperator character to use; defaults to hex(2)
        :param rowrep: the char to convert to for any embedded rowsep chars, defaults to  ' '
        :param colrep: the char to convert to for any embedded colsep chars, defaults to  ' '
        :param kwargs: a dictionary. These vary per access method, and are generally NOT needed.
                       They are either access method specific parms or specific pandas parms.
                       See the specific sasdata2dataframe* method in the access method for valid possibilities.

        Two new kwargs args as of V5.100.0 are for dealing with SAS dates and datetimes that are out of range of Pandats Timestamps. These values will
        be converted to NaT in the dataframe. The new feature is to specify a Timestamp value (str(Timestamp)) for the high value and/or low value
        to use to replace Nat's with in the dataframe. This works for both SAS datetime and date values.

        :param tsmin: str(Timestamp) used to replace SAS datetime and dates that are earlier than supported by Pandas Timestamp; pandas.Timestamp.min
        :param tsmax: str(Timestamp) used to replace SAS datetime and dates that are later   than supported by Pandas Timestamp; pandas.Timestamp.max

        These vary per access method, and are generally NOT needed. They are either access method specific parms or specific \
        pandas parms. See the specific sasdata2dataframe* method in the access method for valid possibilities.

        :param kwargs: a dictionary. These vary per access method, and are generally NOT needed.
                       They are either access method specific parms or specific pandas parms.
                       See the specific sasdata2dataframe* method in the access method for valid possibilities.

        :return: Pandas data frame
        :rtype: 'pd.DataFrame'
        """
        return self.to_df(method='DISK', rowsep=rowsep, colsep=colsep, rowrep=rowrep, colrep=colrep, **kwargs)

    def to_json(self, pretty: bool = False, sastag: bool = False, **kwargs) -> str:
        """
        Export this SAS Data Set to a JSON Object
        PROC JSON documentation: http://go.documentation.sas.com/?docsetId=proc&docsetVersion=9.4&docsetTarget=p06hstivs0b3hsn1cb4zclxukkut.htm&locale=en

        :param pretty: boolean False return JSON on one line True returns formatted JSON
        :param sastag: include SAS meta tags
        :param kwargs:
        :return: JSON str
        """
        lastlog = len(self.sas._io._log)
        code = "filename file1 temp;\n"
        code += "proc json out=file1"
        if pretty:
            code += " pretty "
        if not sastag:
            code += " nosastags "
        code +=";\n  export %s.'%s'n %s;\n run;" % (self.libref, self.table.replace("'", "''"), self._dsopts())

        if self.sas.nosub:
            print(code)
            return None

        ll = self._is_valid()
        self.sas._lastlog = self.sas._io._log[lastlog:]
        runcode = True
        if ll:
            runcode = False
        if runcode:
            ll = self.sas._io.submit(code, "text")
            self.sas._lastlog = self.sas._io._log[lastlog:]
            elog = []
            fpath=''
            for line in ll['LOG'].splitlines():
                if line[self.sas.logoffset:].startswith('JSONFilePath:'):
                    fpath = line[14:]
                if line[self.sas.logoffset:].startswith('ERROR'):
                    elog.append(line)
            if len(elog):
                raise RuntimeError("\n".join(elog))
            if len(fpath):
                with open(fpath, 'r') as myfile:
                    json_str = myfile.read()
                return json_str


    def heatmap(self, x: str, y: str, options: str = '', title: str = '',
                label: str = '') -> object:
        """
        Documentation link: http://support.sas.com/documentation/cdl/en/grstatproc/67909/HTML/default/viewer.htm#n0w12m4cn1j5c6n12ak64u1rys4w.htm

        :param x: x variable
        :param y: y variable
        :param options: display options (string)
        :param title: graph title
        :param label:
        :return:
        """
        lastlog = len(self.sas._io._log)
        code = "proc sgplot data=%s.'%s'n %s;" % (self.libref, self.table.replace("'", "''"), self._dsopts())
        if len(options):
            code += "\n\theatmap x='%s'n y='%s'n / %s;" % (x.replace("'", "''"), y.replace("'", "''"), options)
        else:
            code += "\n\theatmap x='%s'n y='%s'n;" % (x.replace("'", "''"), y.replace("'", "''"))

        if len(label) > 0:
            code += " LegendLABEL='" + label + "'"
        code += ";\n"
        if len(title) > 0:
            code += "\ttitle '%s';\n" % title
        code += "run;\ntitle;"

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()
        if not ll:
            html = self.HTML
            self.HTML = 1
            ll = self.sas._io.submit(code)
            self.HTML = html

        self.sas._lastlog = self.sas._io._log[lastlog:]
        if not self.sas.batch:
            self.sas._render_html_or_log(ll)
        else:
            return ll

    def hist(self, var: str, title: str = '',
             label: str = '') -> object:
        """
        This method requires a numeric column (use the contents method to see column types) and generates a histogram.

        :param var: the NUMERIC variable (column) you want to plot
        :param title: an optional Title for the chart
        :param label: LegendLABEL= value for sgplot
        :return:
        """
        lastlog = len(self.sas._io._log)
        code = "proc sgplot data=" + self.libref + ".'" + self.table.replace("'", "''") + "'n " + self._dsopts()
        code += ";\n\thistogram '" + var.replace("'", "''") + "'n / scale=count"
        if len(label) > 0:
            code += " LegendLABEL='" + label + "'"
        code += ";\n"
        if len(title) > 0:
            code += '\ttitle "' + title + '";\n'
        code += "\tdensity '" + var.replace("'", "''") + "'n;\nrun;\n" + "title;"

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()
        if not ll:
            html = self.HTML
            self.HTML = 1
            ll = self.sas._io.submit(code)
            self.HTML = html

        self.sas._lastlog = self.sas._io._log[lastlog:]
        if not self.sas.batch:
            self.sas._render_html_or_log(ll)
        else:
            return ll

    def top(self, var: str, n: int = 10, order: str = 'freq', title: str = '') -> object:
        """
        Return the most commonly occuring items (levels)

        :param var: the CHAR variable (column) you want to count
        :param n: the top N to be displayed (defaults to 10)
        :param order: default to most common use order='data' to get then in alphbetic order
        :param title: an optional Title for the chart
        :return: Data Table
        """
        lastlog = len(self.sas._io._log)
        code = "proc freq data=%s.'%s'n %s order=%s noprint;" % (self.libref, self.table.replace("'", "''"), self._dsopts(), order)
        code += "\n\ttables '%s'n / out=tmpFreqOut;" % var.replace("'", "''")
        code += "\nrun;"
        if len(title) > 0:
            code += '\ttitle "' + title + '";\n'
        code += "proc print data=tmpFreqOut(obs=%s); \nrun;" % n
        code += 'title;'

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()
        if self.results.upper() == 'PANDAS':
            code = "proc freq data=%s.'%s'n %s order=%s noprint;" % (self.libref, self.table.replace("'", "''"), self._dsopts(), order)
            code += "\n\ttables '%s'n / out=work._tmpFreqOut;" % var.replace("'", "''")
            code += "\nrun;"
            code += "\ndata work._tmpFreqOut; set work._tmpFreqOut(obs=%s); run;" % n

            df = self._returnPD(code, '_tmpFreqOut')
            self.sas._lastlog = self.sas._io._log[lastlog:]
            return df
        else:
            if self.HTML:
                if not ll:
                    ll = self.sas._io.submit(code)
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                if not self.sas.batch:
                    self.sas._render_html_or_log(ll)
                else:
                    return ll
            else:
                if not ll:
                    ll = self.sas._io.submit(code, "text")
                    self.sas._lastlog = self.sas._io._log[lastlog:]
                if not self.sas.batch:
                    print(ll['LST'])
                else:
                    return ll

    def bar(self, var: str, title: str = '', label: str = '') -> object:
        """
        This method requires a character column (use the contents method to see column types)
        and generates a bar chart.

        :param var: the CHAR variable (column) you want to plot
        :param title: an optional title for the chart
        :param label: LegendLABEL= value for sgplot
        :return: graphic plot
        """
        lastlog = len(self.sas._io._log)
        code = "proc sgplot data=" + self.libref + ".'" + self.table.replace("'", "''") + "'n " + self._dsopts()
        code += ";\n\tvbar '" + var.replace("'", "''") + "'n"
        if len(label) > 0:
            code += " / LegendLABEL='" + label + "'"
        code += ";\n"
        if len(title) > 0:
            code += '\ttitle "' + title + '";\n'
        code += 'run;\ntitle;'

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()
        if not ll:
            html = self.HTML
            self.HTML = 1
            ll = self.sas._io.submit(code)
            self.HTML = html

        self.sas._lastlog = self.sas._io._log[lastlog:]
        if not self.sas.batch:
            self.sas._render_html_or_log(ll)
        else:
            return ll

    def series(self, x: str, y: list, title: str = '') -> object:
        """
        This method plots a series of x,y coordinates. You can provide a list of y columns for multiple line plots.

        :param x: the x axis variable; generally a time or continuous variable.
        :param y: the y axis variable(s), you can specify a single column or a list of columns
        :param title: an optional Title for the chart
        :return: graph object
        """
        lastlog = len(self.sas._io._log)

        code = "proc sgplot data=" + self.libref + ".'" + self.table.replace("'", "''") + "'n " + self._dsopts() + ";\n"
        if len(title) > 0:
            code += '\ttitle "' + title + '";\n'

        if isinstance(y, list):
            num = len(y)
        else:
            num = 1
            y = [y]

        for i in range(num):
            code += "\tseries x='" + x.replace("'", "''") + "'n y='" + str(y[i]).replace("'", "''") + "'n;\n"

        code += 'run;\n' + 'title;'

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()
        if not ll:
            html = self.HTML
            self.HTML = 1
            ll = self.sas._io.submit(code)
            self.HTML = html

        self.sas._lastlog = self.sas._io._log[lastlog:]
        if not self.sas.batch:
            self.sas._render_html_or_log(ll)
        else:
            return ll

    def scatter(self, x: str, y: list, title: str = '') -> object:
        """
        This method plots a scatter of x,y coordinates. You can provide a list of y columns for multiple line plots.

        :param x: the x axis variable; generally a time or continuous variable.
        :param y: the y axis variable(s), you can specify a single column or a list of columns
        :param title: an optional Title for the chart
        :return: graph object
        """
        lastlog = len(self.sas._io._log)

        code = "proc sgplot data=" + self.libref + ".'" + self.table.replace("'", "''") + "'n " + self._dsopts() + ";\n"
        if len(title) > 0:
            code += '\ttitle "' + title + '";\n'

        if isinstance(y, list):
            num = len(y)
        else:
            num = 1
            y = [y]

        for i in range(num):
            code += "\tscatter x='" + x.replace("'", "''") + "'n y='" + y[i].replace("'", "''") + "'n;\n"

        code += 'run;\n' + 'title;'

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()
        if not ll:
            html = self.HTML
            self.HTML = 1
            ll = self.sas._io.submit(code)
            self.HTML = html

        self.sas._lastlog = self.sas._io._log[lastlog:]
        if not self.sas.batch:
            self.sas._render_html_or_log(ll)
        else:
            return ll

    def modify(self, formats: dict=None, informats: dict=None, label: str=None,
              renamevars: dict=None, labelvars: dict=None):
       """
       Modify a table, setting formats, informats or changing the data set name itself or renaming variables or adding labels to variables

       :param formats: dict of variable names and formats to assign
       :param informats: dict of variable names and informats to assign
       :param label: string of the label to assign to the data set; if it requires outer quotes, provide them
       :param renamevars: dict of variable names and new names tr rename the variables
       :param labelvars: dict of variable names and labels to assign to them; if any lables require outer quotes, provide them
       :return: SASLOG for this step
       """
       lastlog = len(self.sas._io._log)
       code  = "proc datasets dd="+self.libref+" nolist; modify '"+self.table.replace("'", "''")+"'n "

       if label is not None:
          code += "(label="+label+")"
       code += ";\n"

       if formats is not None:
          code += "format"
          for var in formats:
             code += " '"+var.replace("'", "''")+"'n "+formats[var]
          code += ";\n"

       if informats is not None:
          code += "informat"
          for var in informats:
             code += " '"+var.replace("'", "''")+"'n "+informats[var]
          code += ";\n"

       if renamevars is not None:
          code += "rename"
          for var in renamevars:
             code += " '"+var.replace("'", "''")+"'n = '"+renamevars[var].replace("'", "''")+"'n"
          code += ";\n"

       if labelvars is not None:
          code += "label"
          for var in labelvars:
             code += " '"+var.replace("'", "''")+"'n = "+labelvars[var]
          code += ";\n"

       code += ";run;quit;"

       if self.sas.nosub:
          print(code)
          return

       ll = self.sas._io.submit(code, results='text')
       self.sas._lastlog = self.sas._io._log[lastlog:]
       if not self.sas.batch:
          print(ll['LOG'])
       else:
          return ll['LOG']

    def rename(self, name: str=None):
       """
       Rename this data set

       :param name: new name for this data set
       :return: SASLOG for this step
       """
       lastlog = len(self.sas._io._log)
       code  = "proc datasets dd="+self.libref+" nolist;\n"
       code += "change '"+self.table.replace("'", "''")+"'n = '"+name.replace("'", "''")+"'n;\nrun;quit;"

       if self.sas.nosub:
          print(code)
          return

       if self.sas.exist(name, self.libref):
          self.sas._lastlog = self.sas._io._log[lastlog:]
          failmsg = "Data set with new name already exists. Rename failed."
          if not self.sas.batch:
             logger.error(failmsg)
             return None
          else:
             return failmsg

       ll = self.sas._io.submit(code, results='text')

       if not self.sas.exist(name, self.libref):
          failmsg = "New named data set doesn't exist. Rename must have failed.\n"
       else:
          failmsg = ""
          self.table = name

       self.sas._lastlog = self.sas._io._log[lastlog:]
       if not self.sas.batch:
          print(failmsg+ll['LOG'])
          return None
       else:
          return failmsg+ll['LOG']

    def delete(self, quiet=False):
       """
       Delete this data set; the SASdata object is still available

       :return: SASLOG for this step
       """
       lastlog = len(self.sas._io._log)
       code  = "proc delete data="+self.libref + ".'" + self.table.replace("'", "''") + "'n;run;"

       if self.sas.nosub:
          print(code)
          return

       ll = self.sas._io.submit(code, results='text')

       if self.sas.exist(self.table, self.libref):
          ll['LOG'] = "Data set still exists. Delete must have failed.\n"+ll['LOG']

       self.sas._lastlog = self.sas._io._log[lastlog:]

       if not self.sas.batch:
          if not quiet:
             print(ll['LOG'])
          return None
       else:
          return ll['LOG']

    def append(self, data, force: bool=False):
       """
       Append 'data' to this SAS Data Set. data can either be another SASdataobject or
       a Pandas DataFrame, in which case dataframe2sasdata(data) will be run for you to
       load the data into a SAS data Set which will then be appended to this data set.

       :param data: Either a SASdata object or a Pandas DataFrame
       :param force: boolean to force appended even if anomolies exist which could cause dropping or truncating
       :return: SASLOG for this step
       """
       lastlog = len(self.sas._io._log)
       new = None

       if not self.sas.sascfg.pandas:
          if type(data) is pandas.core.frame.DataFrame:
             new = 'df'
       else:
          new = 'no pandas'

       if type(data) is type(self):
          new = 'sd'

       if new not in ['df','sd']:
          failmsg = "The data parameter passed in must be either a SASdata object or a Pandas DataFrame. No data was appended."
          if not self.sas.batch:
             logger.error(failmsg)
             return None
          else:
             return failmsg

       if new == 'df':
          tmp = True
          new = self.sas.df2sd(data, '_temp_df')
          if type(new) is not type(self):
             failmsg = "df2sd on input data failed. Check SASLOG for errors."
             if not self.sas.batch:
                logger.error(failmsg)
                return None
             else:
                return failmsg
       else:
          tmp = False
          new = data

       if self.sas.nosub:
          print(code)
          return

       if not self.sas.exist(new.table, new.libref):
          self.sas._lastlog = self.sas._io._log[lastlog:]
          failmsg = "Data set to be appended doesn't exist. No data was appended."
          if not self.sas.batch:
             logger.error(failmsg)
             return None
          else:
             return failmsg

       code  = "proc append base="+self.libref+".'"+self.table.replace("'", "''")+"'n\n"
       code += "            data="+ new.libref+".'"+ new.table.replace("'", "''")+"'n"+new._dsopts()
       if force:
          code += "\n   force"
       code += ";\nrun;"

       ll = self.sas._io.submit(code, results='text')
       self.sas._lastlog = self.sas._io._log[lastlog:]

       if tmp:
          new.delete(quiet=True)

       if not self.sas.batch:
          print(ll['LOG'])
          return None
       else:
          return ll['LOG']

