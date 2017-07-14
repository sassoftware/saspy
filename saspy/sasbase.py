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
#
#
# This module is designed to connect to SAS from python, providing a natural python style interface.
# it provides base functionality, data access and processing, and includes analytics and ODS results.
# There is a configuration file named sascfg.py in the saspy package used to configure connections
# to SAS. Currently supported methods are STDIO, connecting to a local (same machine) Linux SAS using
# stdio methods (fork, exec, and pipes). The is also support for running STDIO over SSH, which can 
# connect to a remote linux SAS via passwordless ssh. The ssh method cannot currently support interrupt
# handling, as the local STDIO method can. An interrupt on this method can only terminate the SAS process;
# you'll be prompted to terminate or wait for completion. The third method is HTTP, which can connect
# to SAS Viya via the Compute Service, a restful micro service in the Viya system.
#
# Each of these connection methods (access methods) are handled by their own IO module. This main
# module determines which IO module to use based upon the configuration chosen at runtime. More
# IO modules can be seamlessly plugged in, if needed, in the future.
#
# The expected use is to simply import this package and establish a SAS session, then use the methods:
#
# import saspy
# sas = saspy.SASsession()
# sas.[have_at_it]()
#

import os
import sys
import re
# from pdb import set_trace as bp
import logging

try:
   import pandas as pd
except ImportError:
   pass

try:
   import saspy.sascfg_personal as SAScfg
except ImportError:
   import saspy.sascfg as SAScfg

try:
    import saspy.sasiostdio as sasiostdio
except:
    pass

import saspy.sasioiom   as sasioiom
#import saspy.sasiohttp  as sasiohttp
from saspy.sasstat import *
from saspy.sasets import *
from saspy.sasml import *
from saspy.sasqc import *
from saspy.sasutil import *
from saspy.sasresults import *

try:
    from IPython.display import HTML
    from IPython.display import display as DISPLAY
except ImportError:
    pass


class SASconfig:
    """
    This object is not intended to be used directly. Instantiate a SASsession object instead
    """

    def __init__(self, **kwargs):
        configs = []
        self._kernel = kwargs.get('kernel', None)
        self.valid = True
        self.mode = ''

        # GET Config options
        try:
            self.cfgopts = getattr(SAScfg, "SAS_config_options")
        except:
            self.cfgopts = {}

        # GET Config names
        configs = getattr(SAScfg, "SAS_config_names")

        cfgname = kwargs.get('cfgname', '')

        if len(cfgname) == 0:
            if len(configs) == 0:
                print("No SAS Configuration names found in saspy.sascfg")
                self.valid = False
                return
            else:
                if len(configs) == 1:
                    cfgname = configs[0]
                    if self._kernel is None:
                        print("Using SAS Config named: " + cfgname)
                else:
                    cfgname = self._prompt(
                        "Please enter the name of the SAS Config you wish to run. Available Configs are: " +
                        str(configs) + " ")

        while cfgname not in configs:
            cfgname = self._prompt(
                "The SAS Config name specified was not found. Please enter the SAS Config you wish to use. Available Configs are: " +
                str(configs) + " ")

        self.name = cfgname
        cfg = getattr(SAScfg, cfgname)

        ip           = cfg.get('ip', '')
        ssh          = cfg.get('ssh', '')
        path         = cfg.get('saspath', '')
        java         = cfg.get('java', '')
        self.results = cfg.get('results', None)

        if len(java) > 0:
            self.mode = 'IOM'
        elif len(ip) > 0:
            self.mode = 'HTTP'
        elif len(ssh) > 0:
            self.mode = 'SSH'
        elif len(path) > 0:
            self.mode = 'STDIO'
        else:
            self.valid = False

    def _prompt(self, prompt, pw=False):
        if self._kernel is None:
            if not pw:
                try:
                    return input(prompt)
                except KeyboardInterrupt:
                    return ''
            else:
                try:
                    return getpass.getpass(prompt)
                except KeyboardInterrupt:
                    return ''
        else:
            try:
                return self._kernel._input_request(prompt, self._kernel._parent_ident, self._kernel._parent_header,
                                                   password=pw)
            except KeyboardInterrupt:
                return ''


class SASsession():
    """
    **Overview**

    The SASsession object is the main object to instantiate and provides access to the rest of the functionality.
    Most of these parameters will be configured in the sascfg.py configuration file.

    Common parms for all access methods are:

    :param cfgname: value in SAS_config_names List of the sascfg.py file
    :param kernel: None - internal use when running the SAS_kernel notebook
    :param results: Type of tabular results to return. default is 'Pandas', other options are 'HTML or 'TEXT'
    :return: 'SASsession'
    :rtype: 'SASsession'

    And each access method has its own set of parameters.

    **STDIO**

    :param saspath: overrides saspath Dict entry of cfgname in sascfg.py file
    :param options: overrides options Dict entry of cfgname in sascfg.py file
    :param encoding: This is the python encoding value that matches the SAS session encoding

    **STDIO over SSH**

    and for running STDIO over passwordless ssh, add these required parameters

    :param ssh: full path of the ssh command; /usr/bin/ssh for instance
    :param host: host name of the remote machine

    **IOM**

    and for the IOM IO module to connect to SAS9 via Java IOM

    :param java: the path to the java executable to use
    :param iomhost: for remote IOM case, not local Windows] the resolvable host name, or ip to the IOM server to connect to
    :param iomport: for remote IOM case, not local Windows] the port IOM is listening on
    :param omruser: user id for remote IOM access
    :param omrpw: pw for user for remote IOM access
    :param encoding: This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
    :param classpath: classpath to IOM client jars and saspyiom client jar.

    **Compute Service**

    and for the HTTP IO module to connect to SAS Viya

    :param ip: host address
    :param port: port; the code Defaults this to 80 (the Compute Services default port)
    :param context: context name defined on the compute service
    :param options: SAS options to include in the start up command line
    :param user: user name to authenticate with
    :param pw: password to authenticate with
    :param encoding: This is the python encoding value that matches the SAS session encoding

    """

    # def __init__(self, cfgname: str ='', kernel: 'SAS_kernel' =None, saspath :str ='', options: list =[]) -> 'SASsession':
    def __init__(self, **kwargs) -> 'SASsession':
        self._loaded_macros = False
        self._obj_cnt       = 0
        self.nosub          = False
        self.sascfg         = SASconfig(**kwargs)
        self.batch          = False
        self.results        = kwargs.get('results', self.sascfg.results)
        if not self.results:
           self.results     = 'Pandas'
        self.workpath       = ''
        self.sasver         = ''
        self.sascei         = ''

        if not self.sascfg.valid:
            return

        if self.sascfg.mode in ['STDIO', 'SSH', '']:
            if os.name != 'nt':
                self._io = sasiostdio.SASsessionSTDIO(sascfgname=self.sascfg.name, sb=self, **kwargs)
            else:
                print(
                    "Cannot use STDIO I/O module on Windows. No SASsession established. Choose an IOM SASconfig definition")
        elif self.sascfg.mode == 'IOM':
            self._io = sasioiom.SASsessionIOM(sascfgname=self.sascfg.name, sb=self, **kwargs)
        '''
        elif self.sascfg.mode == 'HTTP':
            self._io = sasiohttp.SASsessionHTTP(sascfgname=self.sascfg.name, sb=self, **kwargs)
        '''

        try:
           if self._io:
             ll = self.submit('libname work list;')
             self.workpath = ll['LOG'].partition('Physical Name=')[2].partition('\n')[0].strip()
             win = self.workpath.count('\\')
             lnx = self.workpath.count('/')
             if (win > lnx):
                self.workpath += '\\'
             else:
                self.workpath += '/'
             ll = self.submit('%put SYSV=&sysvlong4;')
             self.sasver = ll['LOG'].rpartition('SYSV=')[2].partition('\n')[0].strip()
             ll = self.submit('proc options option=encoding;run;')
             self.sascei = ll['LOG'].rpartition('ENCODING=')[2].partition(' ')[0].strip()

        except (AttributeError):
           self._io = None

    def __repr__(self):
        """
        display info about this object ...

        :return: output
        """
        x  = "Access Method         = %s\n" % self.sascfg.mode
        x += "SAS Config name       = %s\n" % self.sascfg.name
        x += "WORK Path             = %s\n" % self.workpath    
        x += "SAS Version           = %s\n" % self.sasver        
        x += "SASPy Version         = %s\n" % sys.modules['saspy'].__version__
        x += "Teach me SAS          = %s\n" % str(self.nosub)  
        x += "Batch                 = %s\n" % str(self.batch)    
        x += "Results               = %s\n" % self.results     
        x += "SAS Session Encoding  = %s\n" % self.sascei     
        x += "Python Encoding value = %s\n" % self._io.sascfg.encoding     
        return(x)                 

    def __del__(self):
        if self._io:
           return self._io.__del__()

    def _objcnt(self):
        self._obj_cnt += 1
        return '%04d' % self._obj_cnt

    def _startsas(self):
        return self._io._startsas()

    def _endsas(self):
        return self._io._endsas()

    def _getlog(self, **kwargs):
        return self._io._getlog(**kwargs)

    def _getlst(self, **kwargs):
        return self._io._getlst(**kwargs)

    def _getlsttxt(self, **kwargs):
        return self._io._getlsttxt(**kwargs)

    def _asubmit(self, code, result):
        if results == '':
            if self.results.upper() == 'PANDAS':
                results = 'HTML'
            else:
                results = self.results

        return self._io._asubmit(code, result)

    def submit(self, code: str, results: str = '', prompt: dict = []) -> dict:
        '''
        This method is used to submit any SAS code. It returns the Log and Listing as a python dictionary.

        - code    - the SAS statements you want to execute
        - results - format of results, HTLML and TEXT is the alternative
        - prompt  - dict of names:flags to prompt for; create marco variables (used in submitted code), then keep or delete 
                    the keys which are the names of the macro variables. The boolean flag is to either hide what you type and delete the macros,
                    or show what you type and keep the macros (they will still be available later).

            for example (what you type for pw will not be displayed, user and dsname will):

            .. code-block:: python

                results_dict = sas.submit(
                             """
                             libname tera teradata server=teracop1 user=&user pw=&pw;
                             proc print data=tera.&dsname (obs=10); run;
                             """ ,
                             prompt = {'user': False, 'pw': True, 'dsname': False}
                             )

            Returns - a Dict containing two keys:values, [LOG, LST]. LOG is text and LST is 'results' (HTML or TEXT)

        NOTE: to view HTML results in the ipykernel, issue: from IPython.display import HTML  and use HTML() instead of print()

        i.e,: results = sas.submit("data a; x=1; run; proc print;run')
                      print(results['LOG'])
                      HTML(results['LST'])
        '''
        if self.nosub:
            return dict(LOG=code, LST='')

        if results == '':
            if self.results.upper() == 'PANDAS':
                results = 'HTML'
            else:
                results = self.results

        return self._io.submit(code, results, prompt)

    def saslog(self) -> str:
        """
        This method is used to get the current, full contents of the SASLOG

        :return: SAS log
        :rtype: str
        """
        return self._io.saslog()

    def teach_me_SAS(self, nosub: bool):
        '''
        nosub - bool. True means don't submit the code, print it out so I can see what the SAS code would be.
            False means run normally - submit the code.
        '''
        self.nosub = nosub

    def set_batch(self, batch: bool) -> bool:
        """
        This method sets the batch attribute for the SASsession object; it stays in effect until changed.
        For methods that just display results like SASdata object methods (head, tail, hist, series, etc.)
        and SASresult object results, you can set 'batch' to true to get the results back directly so you
        can write them to files or whatever you want to do with them.

        This is intended for use in python batch scripts so you can still get ODS XML5 results
        and save them to files, which you couldn't otherwise do for these methods.
        When running interactively, the expectation is that you want to have the results directly rendered,
        but you can run this way too; get the objects display them yourself and/or write them to somewhere.

        When `set_batch ==True`, you get the same dictionary returned as from the `SASsession.submit()` method.

        :param batch: bool
        :rtype: bool
        :return: True = return dict([LOG, LST]. False = display LST to screen.
        """
        self.batch = batch

    def set_results(self, results: str) -> str:
        """
        This method set the results attribute for the SASsession object; it stays in effect till changed

        :param results: set the default result type for this SASdata object. ``'Pandas' or 'HTML' or 'TEXT'``.
        :return: string of the return type
        :rtype: str
        """
        self.results = results

    def exist(self, table: str, libref: str = "") -> bool:
        """
        Does the SAS data set currently exist

        :param table: the name of the SAS Data Set
        :param libref: the libref for the Data Set, defaults to WORK, or USER if assigned
        :return: Boolean True it the Data Set exists and False if it does not
        :rtype: bool
        """
        return self._io.exist(table, libref)

    def sasets(self) -> 'SASets':
        """
        This methods creates a SASets object which you can use to run various analytics.
        See the sasets.py module.
        :return: sasets object
        """
        if not self._loaded_macros:
            self._loadmacros()
            self._loaded_macros = True
        return SASets(self)

    def sasstat(self) -> 'SASstat':
        """
        This methods creates a SASstat object which you can use to run various analytics.
        See the sasstat.py module.

        :return: sasstat object
        """
        if not self._loaded_macros:
            self._loadmacros()
            self._loaded_macros = True

        return SASstat(self)

    def sasml(self) -> 'SASml':
        """
        This methods creates a SASML object which you can use to run various analytics. See the sasml.py module.

        :return: sasml object
        """
        if not self._loaded_macros:
            self._loadmacros()
            self._loaded_macros = True


        return SASml(self)

    def sasqc(self) -> 'SASqc':
        """
        This methods creates a SASqc object which you can use to run various analytics. See the sasqc.py module.

        :return: sasqc object
        """
        if not self._loaded_macros:
            self._loadmacros()
            self._loaded_macros = True

        return SASqc(self)

    def sasutil(self) -> 'SASutil':
        '''
        This methods creates a SASutil object which you can use to run various analytics.
        See the sasutil.py module.

        :return: sasutil object
        '''
        if not self._loaded_macros:
            self._loadmacros()
            self._loaded_macros = True

        return SASutil(self)

    def _loadmacros(self):
        """
        Load the SAS macros at the start of the session

        :return:
        """
        macro_path = os.path.dirname(os.path.realpath(__file__))
        fd = os.open(macro_path + '/' + 'libname_gen.sas', os.O_RDONLY)
        code = b'options nosource;\n'
        code += os.read(fd, 32767)
        code += b'\noptions source;'

        self._io._asubmit(code.decode(), results='text')
        os.close(fd)

    def sasdata(self, table: str, libref: str = '', results: str = '', dsopts: dict = {}) -> 'SASdata':
        """
        Method to define an existing SAS dataset so that it can be accessed via SASPy

        :param table:   the name of the SAS Data Set
        :param libref:  the libref for the Data Set, defaults to WORK, or USER if assigned
        :param results: format of results, SASsession.results is default, Pandas, HTML and TEXT are the valid options
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a numbers - either string or int
            - first obs is a numbers - either string or int

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                             }

        :return: SASdata object
        """
        if results == '':
            results = self.results
        sd = SASdata(self, libref, table, results, dsopts)
        if not self.exist(sd.table, sd.libref):
            if not self.batch:
                print(
                    "Table " + sd.libref + '.' + sd.table + " does not exist. This SASdata object will not be useful until the data set is created.")
        return sd

    def saslib(self, libref: str, engine: str = ' ', path: str = '',
               options: str = ' ', prompt: dict = []) -> str:
        """

        :param libref:  the libref for be assigned
        :param engine:  the engine name used to access the SAS Library (engine defaults to BASE, per SAS)
        :param path:    path to the library (for engines that take a path parameter)
        :param options: other engine or engine supervisor options
        :return: SAS log
        """
        code = "libname " + libref + " " + engine + " "
        if len(path) > 0:
            code += " '" + path + "' "
        code += options + ";"

        if self.nosub:
            print(code)
        else:
            ll = self._io.submit(code, "text", prompt)
            if self.batch:
                return ll['LOG'].rsplit(";*\';*\";*/;\n")[0]
            else:
                print(ll['LOG'].rsplit(";*\';*\";*/;\n")[0])

    def datasets(self, libref: str = '') -> str:
        """
        This method is used to query a libref. The results show information about the libref including members.

        :param libref: the libref to query
        :return:
        """
        code = "proc datasets"
        if libref:
            code += " dd=" + libref
        code += "; quit;"

        if self.nosub:
            print(code)
        else:
            ll = self._io.submit(code, "text")
            if self.batch:
                return ll['LOG'].rsplit(";*\';*\";*/;\n")[0]
            else:
                print(ll['LOG'].rsplit(";*\';*\";*/;\n")[0])

    def read_csv(self, file: str, table: str = '_csv', libref: str = '', results: str = '', opts: dict ={}) -> 'SASdata':
        """
        :param file: either the OS filesystem path of the file, or HTTP://... for a url accessible file
        :param table: the name of the SAS Data Set to create
        :param libref: the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
        :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives
        :param opts: a dictionary containing any of the following Proc Import options(datarow, delimiter, getnames, guessingrows)
        :return: SASdata object
        """
        if results == '':
            results = self.results

        self._io.read_csv(file, table, libref, self.nosub, opts)

        if self.exist(table, libref):
            return SASdata(self, libref, table, results)
        else:
            return None

    def write_csv(self, file: str, table: str, libref: str = '',
                  dsopts: dict = {}, opts: dict ={}) -> str:
        """

        :param file: the OS filesystem path of the file to be created (exported from the SAS Data Set)
        :param table: the name of the SAS Data Set you want to export to a CSV file
        :param libref: the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs)
        :param opts: a dictionary containing any of the following Proc Export options(delimiter, putnames)

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a numbers - either string or int
            - first obs is a numbers - either string or int

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                             }
        :return: SAS log
        """
        log = self._io.write_csv(file, table, libref, self.nosub, dsopts, opts)
        if not self.batch:
            print(log)
        else:
            return log

    def df2sd(self, df: 'pd.DataFrame', table: str = '_df', libref: str = '',
              results: str = '') -> 'SASdata':
        """
        This is an alias for 'dataframe2sasdata'. Why type all that?

        :param df: :class:`pandas.DataFrame` Pandas Data Frame to import to a SAS Data Set
        :param table: the name of the SAS Data Set to create
        :param libref: the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
        :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives
        :return: SASdata object
        """
        return self.dataframe2sasdata(df, table, libref, results)

    def dataframe2sasdata(self, df: 'pd.DataFrame', table: str = '_df', libref: str = '',
                          results: str = '') -> 'SASdata':
        """
        This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.

        :param df: Pandas Data Frame to import to a SAS Data Set
        :param table: the name of the SAS Data Set to create
        :param libref: the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
        :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives
        :return: SASdata object
        """
        if results == '':
            results = self.results
        if self.nosub:
            print("too complicated to show the code, read the source :), sorry.")
            return None
        else:
            self._io.dataframe2sasdata(df, table, libref)

        if self.exist(table, libref):
            return SASdata(self, libref, table, results)
        else:
            return None

    def sd2df(self, table: str, libref: str = '', dsopts: dict = {}, **kwargs) -> 'pd.DataFrame':
        """
        This is an alias for 'sasdata2dataframe'. Why type all that?
        SASdata object that refers to the Sas Data Set you want to export to a Pandas Data Frame

        :param table: the name of the SAS Data Set you want to export to a Pandas Data Frame
        :param libref: the libref for the SAS Data Set.
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a numbers - either string or int
            - first obs is a numbers - either string or int

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                             }
        :param kwargs: dictionary
        :return: Pandas data frame
        """
        return self.sasdata2dataframe(table, libref, dsopts, **kwargs)

    def sasdata2dataframe(self, table: str, libref: str = '', dsopts: dict = {},
                          **kwargs) -> 'pd.DataFrame':
        """
        This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
        SASdata object that refers to the Sas Data Set you want to export to a Pandas Data Frame

        :param table: the name of the SAS Data Set you want to export to a Pandas Data Frame
        :param libref: the libref for the SAS Data Set.
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a numbers - either string or int
            - first obs is a numbers - either string or int

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                             }

        :param kwargs: dictionary
        :return: Pandas data frame
        """

        if self.exist(table, libref) == 0:
            print('The SAS Data Set ' + libref + '.' + table + ' does not exist')
            return None

        if self.nosub:
            print("too complicated to show the code, read the source :), sorry.")
            return None
        else:
            return self._io.sasdata2dataframe(table, libref, dsopts, **kwargs)

    def _dsopts(self, dsopts):
        """
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a numbers - either string or int
            - first obs is a numbers - either string or int

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                             }
        :return: str
        """
        opts = ''

        if len(dsopts):
            for key in dsopts:
                if len(str(dsopts[key])):
                    if key == 'where':
                        opts += 'where=(' + dsopts[key] + ') '
                    elif key == 'drop':
                        opts += 'drop='
                        if isinstance(dsopts[key], list):
                            for var in dsopts[key]:
                                opts += var + ' '
                        else:
                            opts += dsopts[key] + ' '
                    elif key == 'keep':
                        opts += 'keep='
                        if isinstance(dsopts[key], list):
                            for var in dsopts[key]:
                                opts += var + ' '
                        else:
                            opts += dsopts[key] + ' '
                    elif key == 'obs':
                        opts += 'obs=' + str(dsopts[key]) + ' '
                    elif key == 'firstobs':
                        opts += 'firstobs=' + str(dsopts[key]) + ' '
            if len(opts):
                opts = '(' + opts + ')'
        return opts


    def _impopts(self, opts):
        """
        :param opts: a dictionary containing any of the following Proc Import options(datarow, delimiter, getnames, guessingrows):

            - datarow      is a number
            - delimiter    is a character
            - getnames     is a boolean
            - guessingrows is a numbers or the string 'MAX'

            .. code-block:: python

                             {'datarow'     : 2
                              'delimiter'   : ',''
                              'getnames'    : True
                              'guessingrows': 20
                             }
        :return: str
        """
        optstr = ''

        if len(opts):
            for key in opts:
                if len(str(opts[key])):
                    if key     == 'datarow':
                        optstr += 'datarow=' + str(opts[key]) + ';'
                    elif key   == 'delimiter':
                        optstr += 'delimiter='
                        optstr += "'"+'%02x' % ord(opts[key].encode(self._io.sascfg.encoding))+"'x; "
                    elif key   == 'getnames':
                        optstr += 'getnames='
                        if opts[key]:
                           optstr += 'YES; '
                        else:
                           optstr += 'NO; '
                    elif key   == 'guessingrows':
                        optstr += 'guessingrows='
                        if opts[key] == 'MAX':
                           optstr += 'MAX; '
                        else:
                           optstr += str(opts[key])+'; '
        return optstr


    def _expopts(self, opts):
        """
        :param opts: a dictionary containing any of the following Proc Export options(delimiter, putnames):

            - delimiter    is a character
            - putnames     is a boolean

            .. code-block:: python

                             {'delimiter'   : ',''
                              'putnames'    : True
                             }
        :return: str
        """
        optstr = ''

        if len(opts):
            for key in opts:
                if len(str(opts[key])):
                    if key     == 'delimiter':
                        optstr += 'delimiter='
                        optstr += "'"+'%02x' % ord(opts[key].encode(self._io.sascfg.encoding))+"'x; "
                    elif key   == 'putnames':
                        optstr += 'putnames='
                        if opts[key]:
                           optstr += 'YES; '
                        else:
                           optstr += 'NO; '
        return optstr


class SASdata:
    def __init__(self, sassession, libref, table, results='', dsopts={}):
        """

        :param sassession:
        :param table: the name of the SAS Data Set
        :param libref: the libref for the SAS Data Set.
        :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a numbers - either string or int
            - first obs is a numbers - either string or int

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                             }
        end comment
        """
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

        self.table = table
        self.dsopts = dsopts
        self.results = results

    def __getitem__(self, key):

        print(key)
        print(type(key))
        #print(kwargs.keys())
        #print(kwargs.items())

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
        libref = 'work'
        if 'libref' in kwargs:
            libref = kwargs['libref']
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
        '''
        This method builds out data set options clause for this SASdata object: '(where= , keeep=, obs=, ...)'
        '''
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
        code = "proc sql;select count(*) into :lastobs from " + self.libref + '.' + self.table + self._dsopts() + ";%put lastobs=&lastobs tom;quit;"

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
            code = "proc contents data=%s.%s %s ;" % (self.libref, self.table, self._dsopts())
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
        code = "proc means data=" + self.libref + '.' + self.table + self._dsopts() + " stackodsoutput n nmiss median mean std min p25 p50 p75 max;run;"

        if self.sas.nosub:
            print(code)
            return

        ll = self._is_valid()

        if self.results.upper() == 'PANDAS':
            code = "proc means data=%s.%s %s stackodsoutput n nmiss median mean std min p25 p50 p75 max; ods output Summary=work._summary; run;" % (
                self.libref, self.table, self._dsopts())
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

    def impute(self, vars: dict, replace: bool = False, prefix: str = 'imp_', out: 'SASData' = None) -> 'SASdata':
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

        #code += "%%mangobj(%s,%s,%s);" % (objname, objtype, self.table)
        #code += "run; quit; %mend;\n"

        # Debug block

        #debug={'name': name,
        #       'score_table': score_table,
        #       'target': target,
        #       'var': var,
        #       'nominals': nominals,
        #       'level': level,
        #       'binstats': binstats,
        #       'out':out}
        #print(debug.items())

        if self.sas.nosub:
            print(code)
            return

        ll = self.sas.submit(code, 'text')
        obj1 = SASProcCommons._objectmethods(self, objname)
        return SASresults(obj1, self.sas, objname, self.sas.nosub, ll['LOG'])

    def to_csv(self, file: str, opts: dict ={}) -> str:
        """
        This method will export a SAS Data Set to a file in CSV format.

        :param file: the OS filesystem path of the file to be created (exported from this SAS Data Set)
        :return:
        """
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

    def to_frame(self, **kwargs) -> 'pd.DataFrame':
        """
        Export this SAS Data Set to a Pandas Data Frame

        :param kwargs:
        :return: Pandas data frame
        :rtype: 'pd.DataFrame'
        """
        return self.to_df(**kwargs)

    def to_df(self, **kwargs) -> 'pd.DataFrame':
        """
        Export this SAS Data Set to a Pandas Data Frame

        :param kwargs:
        :return: Pandas data frame
        """
        ll = self._is_valid()
        if ll:
            print(ll['LOG'])
            return None
        else:
            return self.sas.sasdata2dataframe(self.table, self.libref, self.dsopts, **kwargs)

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
        code += "\tdensity " + var + ';\nrun;\n' + 'title \"\";'

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
        code += 'title \"\";'

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
        code += ";\n\tvbar " + var + " ; "
        if len(label) > 0:
            code += " LegendLABEL='" + label + "'"
        code += ";\n"
        if len(title) > 0:
            code += '\ttitle "' + title + '";\n'
        code += 'title \"\";'
        code += 'run;'

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

        if type(y) == list:
            num = len(y)
        else:
            num = 1
            y = [y]

        for i in range(num):
            code += "\tseries x=" + x + " y=" + y[i] + ";\n"

        code += 'run;\n' + 'title \"\";'

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


if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(_getlog())
    print(_getlsttxt())

    endsas()

