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
import re
import saspy as sp2
import pandas as pd

try:
    import pandas as pd
except ImportError:
    pass

try:
    from IPython.display import HTML
    from IPython.display import display as DISPLAY
except ImportError:
    pass

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
        - first obs is a numbers - either string or int
        - format is a string or dictionary { var: format }

        .. code-block:: python

                         {'where'    : 'msrp < 20000 and make = "Ford"',
                          'keep'     : 'msrp enginesize Cylinders Horsepower Weight',
                          'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight'],
                          'obs'      :  10,
                          'firstobs' : '12'
                          'format'  : {'money': 'dollar10', 'time': 'tod5.'}
                         }

    """

    def __init__(self, sassession, libref, table, results='', dsopts: dict=None):
        self.sas = sassession
        self.logger = logging.getLogger(__name__)

        if results == '':
            results = sassession.results

        failed = 0
        if results.upper() == "HTML":
            try:
                from IPython.display import HTML
            except:
                failed = 1

            if failed and not self.sas.batch:
                self.HTML = 0
            else:
                self.HTML = 1
        else:
            self.HTML = 0

        if len(libref):
            self.libref = libref
        else:
            if self.sas.exist(table, libref='user'):
                self.libref = 'USER'
            else:
                self.libref = 'WORK'

            # hack till the bug gets fixed
            if self.sas.sascfg.mode == 'HTTP':
                self.libref = 'WORK'

        self.table    = table
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
            if line.startswith('ERROR'):
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
        libref = kwargs.get('libref','work')
        ll = self.sas._io.submit(code)
        check, errorMsg = self._checkLogForError(ll['LOG'])
        if not check:
            raise ValueError("Internal code execution failed: " + errorMsg)
        if isinstance(tablename, str):
            pd = self.sas._io.sasdata2dataframe(tablename, libref)
            self.sas._io.submit("proc delete data=%s.%s; run;" % (libref, tablename))
        elif isinstance(tablename, list):
            pd = dict()
            for t in tablename:
                # strip leading '_' from names and capitalize for dictionary labels
                if self.sas.exist(t, libref):
                   pd[t.replace('_', '').capitalize()] = self.sas._io.sasdata2dataframe(t, libref)
                self.sas._io.submit("proc delete data=%s.%s; run;" % (libref, t))
        else:
            raise SyntaxError("The tablename must be a string or list %s was submitted" % str(type(tablename)))

        return pd

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
        topts = dict(self.dsopts)
        topts['obs'] = obs
        code = "proc print data=" + self.libref + '.' + self.table + self.sas._dsopts(topts) + ";run;"

        if self.sas.nosub:
            print(code)
            return

        if self.results.upper() == 'PANDAS':
            code = "data _head ; set %s.%s %s; run;" % (self.libref, self.table, self.sas._dsopts(topts))
            return self._returnPD(code, '_head')
        else:
            ll = self._is_valid()
            if self.HTML:
                if not ll:
                    ll = self.sas._io.submit(code)
                if not self.sas.batch:
                    DISPLAY(HTML(ll['LST']))
                else:
                    return ll
            else:
                if not ll:
                    ll = self.sas._io.submit(code, "text")
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
        code = "proc sql;select count(*) format best32. into :lastobs from " + self.libref + '.' + self.table + self._dsopts() + ";%put lastobs=&lastobs tom;quit;"

        nosub = self.sas.nosub
        self.sas.nosub = False

        le = self._is_valid()
        if not le:
            ll = self.sas.submit(code, "text")

            lastobs = ll['LOG'].rpartition("lastobs=")
            lastobs = lastobs[2].partition(" tom")
            lastobs = int(lastobs[0])
        else:
            lastobs = obs

        firstobs = lastobs - (obs - 1)
        if firstobs < 1:
            firstobs = 1

        topts = dict(self.dsopts)
        topts['obs'] = lastobs
        topts['firstobs'] = firstobs

        code = "proc print data=" + self.libref + '.' + self.table + self.sas._dsopts(topts) + ";run;"

        self.sas.nosub = nosub
        if self.sas.nosub:
            print(code)
            return

        if self.results.upper() == 'PANDAS':
            code = "data _tail ; set %s.%s %s; run;" % (self.libref, self.table, self.sas._dsopts(topts))
            return self._returnPD(code, '_tail')
        else:
            if self.HTML:
                if not le:
                    ll = self.sas._io.submit(code)
                else:
                    ll = le
                if not self.sas.batch:
                    DISPLAY(HTML(ll['LST']))
                else:
                    return ll
            else:
                if not le:
                    ll = self.sas._io.submit(code, "text")
                else:
                    ll = le
                if not self.sas.batch:
                    print(ll['LST'])
                else:
                    return ll

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
        # loop through for k folds cross-validation
        i = 1
        # initialize code string so that loops work
        code = ''
        # Make sure kfold was an integer
        try:
            k = int(kfold)
        except ValueError:
            print("Kfold must be an integer")
        if out is None:
            out_table = self.table
            out_libref = self.libref
        elif not isinstance(out, str):
            out_table = out.table
            out_libref = out.libref
        else:
            try:
                out_table = out.split('.')[1]
                out_libref = out.split('.')[0]
            except IndexError:
                out_table = out
                out_libref = 'work'
        while i <= k:
            # get the list of variables
            if k == 1:
                code += "proc hpsample data=%s.%s %s out=%s.%s %s samppct=%s seed=%s Partition;\n" % (
                    self.libref, self.table, self._dsopts(), out_libref, out_table, self._dsopts(), fraction * 100,
                    seed)
            else:
                seed += 1
                code += "proc hpsample data=%s.%s %s out=%s.%s %s samppct=%s seed=%s partition PARTINDNAME=_cvfold%s;\n" % (
                    self.libref, self.table, self._dsopts(), out_libref, out_table, self._dsopts(), fraction * 100,
                    seed, i)

            # Get variable info for stratified sampling
            if len(var) > 0:
                if i == 1:
                    num_string = """
                        data _null_; file LOG;
                          d = open('{0}.{1}');
                          nvars = attrn(d, 'NVARS'); 
                          put 'VARLIST=';
                          do i = 1 to nvars; 
                             vart = vartype(d, i);
                             var  = varname(d, i);
                             if vart eq 'N' then
                                put var; end;
                             put 'VARLISTend=';
                        run;
                        """
                    # ignore teach_me_SAS mode to run contents
                    nosub = self.sas.nosub
                    self.sas.nosub = False
                    ll = self.sas.submit(num_string.format(self.libref, self.table + self._dsopts()))
                    self.sas.nosub = nosub
                    l2 = ll['LOG'].partition("VARLIST=\n")
                    l2 = l2[2].rpartition("VARLISTend=\n")
                    numlist1 = l2[0].split("\n")

                    # check if var is in numlist1
                    if isinstance(var, str):
                        tlist = var.split()
                    elif isinstance(var, list):
                        tlist = var
                    else:
                        raise SyntaxError("var must be a string or list you submitted: %s" % str(type(var)))
                if set(numlist1).isdisjoint(tlist):
                    if isinstance(var, str):
                        code += "class _character_;\ntarget %s;\nvar _numeric_;\n" % var
                    else:
                        code += "class _character_;\ntarget %s;\nvar _numeric_;\n" % " ".join(var)
                else:
                    varlist = [x for x in numlist1 if x not in tlist]
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
                split_code += "\t%s.%s%s_train(drop=_Partind_ _cvfold:)\n" % (out_libref, out_table, j)
                split_code += "\t%s.%s%s_score(drop=_Partind_ _cvfold:)\n" % (out_libref, out_table, j)
            split_code += ';\n \tset %s.%s;\n' % (out_libref, out_table)
            for z in range(1, k + 1):
                split_code += "\tif _cvfold%s = 1 or _partind_ = 1 then output %s.%s%s_train;\n" % (z, out_libref, out_table, z)
                split_code += "\telse output %s.%s%s_score;\n" % (out_libref, out_table, z)
            split_code += 'run;'
        runcode = True
        if self.sas.nosub:
            print(code + '\n\n' + split_code)
            runcode = False
        ll = self._is_valid()
        if ll:
            runcode = False
        if runcode:
            ll = self.sas.submit(code + split_code, "text")
            elog = []
            for line in ll['LOG'].splitlines():
                if line.startswith('ERROR'):
                    elog.append(line)
            if len(elog):
                raise RuntimeError("\n".join(elog))
            if not singleOut:
                outTableList = []
                if k == 1:
                    return (self.sas.sasdata(out_table + str(k) + "_train", out_libref, dsopts=self._dsopts()),
                            self.sas.sasdata(out_table + str(k) + "_score", out_libref, dsopts=self._dsopts()))

                for j in range(1, k + 1):
                    outTableList.append((self.sas.sasdata(out_table + str(j) + "_train", out_libref, dsopts=self._dsopts()),
                                               self.sas.sasdata(out_table + str(j) + "_score", out_libref, dsopts=self._dsopts())))
                return outTableList
            if out:
                if not isinstance(out, str):
                    return out
                else:
                    return self.sas.sasdata(out_table, out_libref, self.results)
            else:
                return self

    def contents(self):
        """
        display metadata about the table. size, number of rows, columns and their data type ...

        :return: output
        """
        code = "proc contents data=" + self.libref + '.' + self.table + self._dsopts() + ";run;"

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()
        if self.results.upper() == 'PANDAS':
            code  = "proc contents data=%s.%s %s ;" % (self.libref, self.table, self._dsopts())
            code += "ods output Attributes=work._attributes;"
            code += "ods output EngineHost=work._EngineHost;"
            code += "ods output Variables=work._Variables;"
            code += "ods output Sortedby=work._Sortedby;"
            code += "run;"
            return self._returnPD(code, ['_attributes', '_EngineHost', '_Variables', '_Sortedby'])

        else:
            if self.HTML:
                if not ll:
                    ll = self.sas._io.submit(code)
                if not self.sas.batch:
                    DISPLAY(HTML(ll['LST']))
                else:
                    return ll
            else:
                if not ll:
                    ll = self.sas._io.submit(code, "text")
                if not self.sas.batch:
                    print(ll['LST'])
                else:
                    return ll

    def columnInfo(self):
        """
        display metadata about the table, size, number of rows, columns and their data type
        """
        code = "proc contents data=" + self.libref + '.' + self.table + ' ' + self._dsopts() + ";ods select Variables;run;"

        if self.sas.nosub:
            print(code)
            return

        if self.results.upper() == 'PANDAS':
            code = "proc contents data=%s.%s %s ;ods output Variables=work._variables ;run;" % (self.libref, self.table, self._dsopts())
            pd = self._returnPD(code, '_variables')
            pd['Type'] = pd['Type'].str.rstrip()
            return pd

        else:
            ll = self._is_valid()
            if self.HTML:
                if not ll:
                    ll = self.sas._io.submit(code)
                if not self.sas.batch:
                    DISPLAY(HTML(ll['LST']))
                else:
                    return ll
            else:
                if not ll:
                    ll = self.sas._io.submit(code, "text")
                if not self.sas.batch:
                    print(ll['LST'])
                else:
                    return ll

    def info(self):
        """
        Display the column info on a SAS data object

        :return: Pandas data frame
        """
        if self.results.casefold() != 'pandas':
            print("The info method only works with Pandas results")
            return None
        info_code = """
        data work._statsInfo ;
            do rows=0 by 1 while( not last ) ;
                set {0}.{1}{2} end=last;
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
        info_pd = self._returnPD(info_code.format(self.libref, self.table, self._dsopts()), '_statsInfo')
        info_pd = info_pd.iloc[:, :]
        info_pd.index.name = None
        info_pd.name = None
        return info_pd

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
        dsopts = self._dsopts().partition(';\n\tformat')

        code  = "proc means data=" + self.libref + '.' + self.table + dsopts[0] + " stackodsoutput n nmiss median mean std min p25 p50 p75 max;"
        code += dsopts[1]+dsopts[2]+"run;"

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()

        if self.results.upper() == 'PANDAS':
            code = "proc means data=%s.%s %s stackodsoutput n nmiss median mean std min p25 p50 p75 max; %s ods output Summary=work._summary; run;" % (
                self.libref, self.table, dsopts[0], dsopts[1]+dsopts[2])
            return self._returnPD(code, '_summary')
        else:
            if self.HTML:
               if not ll:
                  ll = self.sas._io.submit(code)
               if not self.sas.batch:
                  DISPLAY(HTML(ll['LST']))
               else:
                  return ll
            else:
               if not ll:
                  ll = self.sas._io.submit(code, "text")
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
        :return:
        """
        outstr = ''
        if out:
            if isinstance(out, str):
                fn = out.partition('.')
                if fn[1] == '.':
                    out_libref = fn[0]
                    out_table = fn[2]
                else:
                    out_libref = ''
                    out_table = fn[0]
            else:
                out_libref = out.libref
                out_table = out.table
            outstr = "out=%s.%s" % (out_libref, out_table)

        else:
            out_table = self.table
            out_libref = self.libref

        # get list of variables and types
        varcode = "data _null_; d = open('" + self.libref + "." + self.table + "');\n"
        varcode += "nvars = attrn(d, 'NVARS');\n"
        varcode += "vn='VARNUMS='; vl='VARLIST='; vt='VARTYPE=';\n"
        varcode += "put vn nvars; put vl;\n"
        varcode += "do i = 1 to nvars; var = varname(d, i); put var; end;\n"
        varcode += "put vt;\n"
        varcode += "do i = 1 to nvars; var = vartype(d, i); put var; end;\n"
        varcode += "run;"
        print(varcode)
        ll = self.sas._io.submit(varcode, "text")
        l2 = ll['LOG'].rpartition("VARNUMS= ")
        l2 = l2[2].partition("\n")
        nvars = int(float(l2[0]))
        l2 = l2[2].partition("\n")
        varlist = l2[2].upper().split("\n", nvars)
        del varlist[nvars]
        l2 = l2[2].partition("VARTYPE=")
        l2 = l2[2].partition("\n")
        vartype = l2[2].split("\n", nvars)
        del vartype[nvars]
        varListType = dict(zip(varlist, vartype))

        # process vars dictionary to generate code
        ## setup default statements
        sql = "proc sql;\n  select\n"
        sqlsel = ' %s(%s),\n'
        sqlinto = ' into\n'
        if len(out_libref)>0 :
            ds1 = "data " + out_libref + "." + out_table + "; set " + self.libref + "." + self.table + self._dsopts() + ";\n"
        else:
            ds1 = "data " + out_table + "; set " + self.libref + "." + self.table + self._dsopts() + ";\n"
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
                        modesql += modeq % (v, v, self.libref + "." + self.table + self._dsopts() , v, v, v)
                    if varListType.get(v.upper()) == "N":
                        ds1 += dsmiss.format(v, v, '&imp_' + v + '.')
                    else:
                        ds1 += dsmiss.format(v, v, '"&imp_' + v + '."')

        if len(sql) > 20:
            sql = sql.rstrip(', \n') + '\n' + sqlinto.rstrip(', \n') + '\n  from ' + self.libref + '.' + self.table + self._dsopts() + ';\nquit;\n'
        else:
            sql = ''
        ds1 += 'run;\n'

        if self.sas.nosub:
            print(modesql + sql + ds1)
            return None
        ll = self.sas.submit(modesql + sql + ds1)
        return self.sas.sasdata(out_table, libref=out_libref, results=self.results, dsopts=self._dsopts())

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
        outstr = ''
        options = ''
        if out:
            if isinstance(out, str):
                fn = out.partition('.')
                if fn[1] == '.':
                    libref = fn[0]
                    table = fn[2]
                    outstr = "out=%s.%s" % (libref, table)
                else:
                    libref = ''
                    table = fn[0]
                    outstr = "out=" + table
            else:
                libref = out.libref
                table = out.table
                outstr = "out=%s.%s" % (out.libref, out.table)

        if 'options' in kwargs:
            options = kwargs['options']

        code = "proc sort data=%s.%s%s %s %s ;\n" % (self.libref, self.table, self._dsopts(), outstr, options)
        code += "by %s;" % by
        code += "run\n;"
        runcode = True
        if self.sas.nosub:
            print(code)
            runcode = False

        ll = self._is_valid()
        if ll:
            runcode = False
        if runcode:
            ll = self.sas.submit(code, "text")
            elog = []
            for line in ll['LOG'].splitlines():
                if line.startswith('ERROR'):
                    elog.append(line)
            if len(elog):
                raise RuntimeError("\n".join(elog))
        if out:
            if not isinstance(out, str):
                return out
            else:
                return self.sas.sasdata(table, libref, self.results)
        else:
            return self

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
        # submit autocall macro
        self.sas.submit("%aamodel;")
        objtype = "datastep"
        objname = '{s:{c}^{n}}'.format(s=self.table[:3], n=3,
                                       c='_') + self.sas._objcnt()  # translate to a libname so needs to be less than 8
        code = "%macro proccall(d);\n"

        # build parameters
        score_table = str(self.libref + '.' + self.table)
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
                print("No event was specified for a nominal target. Here are possible options:\n")
                event_code = "proc hpdmdb data=%s.%s %s classout=work._DMDBCLASSTARGET(keep=name nraw craw level frequency nmisspercent);" % (
                    self.libref, self.table, self._dsopts())
                event_code += "\nclass %s ; \nrun;" % target
                event_code += "data _null_; set work._DMDBCLASSTARGET; where ^(NRAW eq . and CRAW eq '') and lowcase(name)=lowcase('%s');" % target
                ec = self.sas._io.submit(event_code)
                HTML(ec['LST'])
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
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype, self.table)

        if self.sas.nosub:
            print(code)
            return

        ll = self.sas.submit(code, 'text')
        obj1 = sp2.SASProcCommons._objectmethods(self, objname)
        return sp2.SASresults(obj1, self.sas, objname, self.sas.nosub, ll['LOG'])

    def to_csv(self, file: str, opts: dict = None) -> str:
        """
        This method will export a SAS Data Set to a file in CSV format.

        :param file: the OS filesystem path of the file to be created (exported from this SAS Data Set)
        :return:
        """
        opts = opts if opts is not None else {}
        ll = self._is_valid()
        if ll:
            if not self.sas.batch:
                print(ll['LOG'])
            else:
                return ll
        else:
            return self.sas.write_csv(file, self.table, self.libref, self.dsopts, opts)

    def score(self, file: str = '', code: str = '', out: 'SASdata' = None) -> 'SASdata':
        """
        This method is meant to update a SAS Data object with a model score file.

        :param file: a file reference to the SAS score code
        :param code: a string of the valid SAS score code
        :param out: Where to the write the file. Defaults to update in place
        :return: The Scored SAS Data object.
        """
        if out is not None:
            outTable = out.table
            outLibref = out.libref
        else:
            outTable = self.table
            outLibref = self.libref
        codestr = code
        code = "data %s.%s%s;" % (outLibref, outTable, self._dsopts())
        code += "set %s.%s%s;" % (self.libref, self.table, self._dsopts())
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
        if not self.sas.batch:
            DISPLAY(HTML(ll['LST']))
        else:
            return ll

    def to_frame(self, **kwargs) -> 'pd.DataFrame':
        """
        Export this SAS Data Set to a Pandas Data Frame

        :param kwargs:
        :return: Pandas data frame
        :rtype: 'pd.DataFrame'
        """
        return self.to_df(**kwargs)

    def to_df(self, method: str = 'MEMORY', **kwargs) -> 'pd.DataFrame':
        """
        Export this SAS Data Set to a Pandas Data Frame

        :param method: defaults to MEMORY; the original method. CSV is the other choice which uses an intermediary csv file; faster for large data
        :param kwargs:
        :return: Pandas data frame
        """
        ll = self._is_valid()
        if ll:
            print(ll['LOG'])
            return None
        else:
            return self.sas.sasdata2dataframe(self.table, self.libref, self.dsopts, method, **kwargs)

    def to_df_CSV(self, tempfile: str=None, tempkeep: bool=False, **kwargs) -> 'pd.DataFrame':
        """
        Export this SAS Data Set to a Pandas Data Frame via CSV file

        :param tempfile: [optional] an OS path for a file to use for the local CSV file; default it a temporary file that's cleaned up
        :param tempkeep: if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it
        :param kwargs:
        :return: Pandas data frame
        :rtype: 'pd.DataFrame'
        """
        return self.to_df(method='CSV', tempfile=tempfile, tempkeep=tempkeep, **kwargs)

    def to_json(self, pretty: bool = False, sastag: bool = False, **kwargs) -> str:
        """
        Export this SAS Data Set to a JSON Object
        PROC JSON documentation: http://go.documentation.sas.com/?docsetId=proc&docsetVersion=9.4&docsetTarget=p06hstivs0b3hsn1cb4zclxukkut.htm&locale=en

        :param pretty: boolean False return JSON on one line True returns formatted JSON
        :param sastag: include SAS meta tags
        :param kwargs:
        :return: JSON str
        """
        code = "filename file1 temp;"
        code += "proc json out=file1"
        if pretty:
            code += " pretty "
        if not sastag:
            code += " nosastags "
        code +=";\n export %s.%s %s;\n run;" % (self.libref, self.table, self._dsopts())

        if self.sas.nosub:
            print(code)
            return None

        ll = self._is_valid()
        runcode = True
        if ll:
            runcode = False
        if runcode:
            ll = self.sas.submit(code, "text")
            elog = []
            fpath=''
            for line in ll['LOG'].splitlines():
                if line.startswith('JSONFilePath:'):
                    fpath = line[14:]
                if line.startswith('ERROR'):
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
        code = "proc sgplot data=%s.%s %s;" % (self.libref, self.table, self._dsopts())
        if len(options):
            code += "\n\theatmap x=%s y=%s / %s;" % (x, y, options)
        else:
            code += "\n\theatmap x=%s y=%s;" % (x, y)

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
        if not self.sas.batch:
            DISPLAY(HTML(ll['LST']))
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
        code = "proc sgplot data=" + self.libref + '.' + self.table + self._dsopts()
        code += ";\n\thistogram " + var + " / scale=count"
        if len(label) > 0:
            code += " LegendLABEL='" + label + "'"
        code += ";\n"
        if len(title) > 0:
            code += '\ttitle "' + title + '";\n'
        code += "\tdensity " + var + ';\nrun;\n' + 'title;'

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()
        if not ll:
            html = self.HTML
            self.HTML = 1
            ll = self.sas._io.submit(code)
            self.HTML = html
        if not self.sas.batch:
            DISPLAY(HTML(ll['LST']))
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
        code = "proc freq data=%s.%s %s order=%s noprint;" % (self.libref, self.table, self._dsopts(), order)
        code += "\n\ttables %s / out=tmpFreqOut;" % var
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
            code = "proc freq data=%s.%s%s order=%s noprint;" % (self.libref, self.table, self._dsopts(), order)
            code += "\n\ttables %s / out=tmpFreqOut;" % var
            code += "\nrun;"
            code += "\ndata tmpFreqOut; set tmpFreqOut(obs=%s); run;" % n
            return self._returnPD(code, 'tmpFreqOut')
        else:
            if self.HTML:
                if not ll:
                    ll = self.sas._io.submit(code)
                if not self.sas.batch:
                    DISPLAY(HTML(ll['LST']))
                else:
                    return ll
            else:
                if not ll:
                    ll = self.sas._io.submit(code, "text")
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
        code = "proc sgplot data=" + self.libref + '.' + self.table + self._dsopts()
        code += ";\n\tvbar " + var
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
        if not self.sas.batch:
            DISPLAY(HTML(ll['LST']))
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

        code = "proc sgplot data=" + self.libref + '.' + self.table + self._dsopts() + ";\n"
        if len(title) > 0:
            code += '\ttitle "' + title + '";\n'

        if isinstance(y, list):
            num = len(y)
        else:
            num = 1
            y = [y]

        for i in range(num):
            code += "\tseries x=" + x + " y=" + str(y[i]) + ";\n"

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
        if not self.sas.batch:
            DISPLAY(HTML(ll['LST']))
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

        code = "proc sgplot data=" + self.libref + '.' + self.table + self._dsopts() + ";\n"
        if len(title) > 0:
            code += '\ttitle "' + title + '";\n'

        if isinstance(y, list):
            num = len(y)
        else:
            num = 1
            y = [y]

        for i in range(num):
            code += "\tscatter x=" + x + " y=" + y[i] + ";\n"

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
        if not self.sas.batch:
            DISPLAY(HTML(ll['LST']))
        else:
            return ll
