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
# There is a sample configuration file named sascfg in the saspy package showing how to configure connections
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
import getpass
import tempfile

from saspy.sasioiom  import SASsessionIOM
from saspy.sasets    import SASets
from saspy.sasml     import SASml
from saspy.sasqc     import SASqc
from saspy.sasstat   import SASstat
from saspy.sasutil   import SASutil
from saspy.sasViyaML import SASViyaML
from saspy.sasdata   import SASdata

try:
    import pandas as pd
except ImportError:
    pass

try:
   import saspy.sascfg_personal as SAScfg
except ImportError:
   try:
      import sascfg_personal as SAScfg
   except ImportError:
      import saspy.sascfg as SAScfg

if os.name != 'nt':
    from saspy.sasiostdio import SASsessionSTDIO

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
        self._kernel = kwargs.get('kernel', None)
        self.valid   = True
        self.mode    = ''
        configs      = []

        cfgfile = kwargs.get('cfgfile', None)
        if cfgfile:
            tempdir = tempfile.TemporaryDirectory()
            try:
                fdin = open(cfgfile)
            except:
                print("Couldn't open cfgfile " + cfgfile)
                cfgfile = None

            if cfgfile:
                f1 = fdin.read()
                fdout = open(tempdir.name + os.sep + "sascfgfile.py", 'w')
                fdout.write(f1)
                fdout.close()
                fdin.close()
                sys.path.append(tempdir.name)
                import sascfgfile as SAScfg
                tempdir.cleanup()
                sys.path.remove(tempdir.name)

        if not cfgfile:
            try:
                import saspy.sascfg_personal as SAScfg
            except ImportError:
                try:
                    import sascfg_personal as SAScfg
                except ImportError:
                    import saspy.sascfg as SAScfg

        self.SAScfg = SAScfg

        # GET Config options
        try:
            self.cfgopts = getattr(SAScfg, "SAS_config_options")
        except:
            self.cfgopts = {}

        # in lock down mode, don't allow runtime overrides of option values from the config file.
        lock = self.cfgopts.get('lock_down', True)

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
            if cfgname is None:
                raise KeyboardInterrupt

        self.name = cfgname
        cfg = getattr(SAScfg, cfgname)

        ip            = cfg.get('ip', '')
        ssh           = cfg.get('ssh', '')
        path          = cfg.get('saspath', '')
        java          = cfg.get('java', '')
        self.results  = cfg.get('results', None)
        self.autoexec = cfg.get('autoexec', None)

        inautoexec = kwargs.get('autoexec', None)
        if inautoexec:
            if lock and self.autoexec:
                print("Parameter 'autoexec' passed to SAS_session was ignored due to configuration restriction.")
            else:
                self.autoexec = inautoexec

        if len(java)   > 0:
            self.mode  = 'IOM'
        elif len(ip)   > 0:
            self.mode  = 'HTTP'
        elif len(ssh)  > 0:
            self.mode  = 'SSH'
        elif len(path) > 0:
            self.mode  = 'STDIO'
        else:
            print("Configuration Definition " + cfgname + " is not valid. Failed to create a SASsession.")
            self.valid = False

    def _prompt(self, prompt, pw=False):
        if self._kernel is None:
            if not pw:
                try:
                    return input(prompt)
                except KeyboardInterrupt:
                    return None
            else:
                try:
                    return getpass.getpass(prompt)
                except KeyboardInterrupt:
                    return None
        else:
            try:
                return self._kernel._input_request(prompt, self._kernel._parent_ident, self._kernel._parent_header,
                                                   password=pw)
            except KeyboardInterrupt:
                return None


class SASsession():
    """
    **Overview**

    The SASsession object is the main object to instantiate and provides access to the rest of the functionality.
    Most of these parameters will be configured in the sascfg_personal.py configuration file.
    All of these parameters are documented more thoroughly in the configuration section of the saspy doc:
    https://sassoftware.github.io/saspy/install.html#configuration
    These are generally defined in the sascfg_personal.py file as opposed to being specified on the SASsession() invocation.

    Common parms for all access methods are:

    :param cfgname: the Configuration Definition to use - value in SAS_config_names List in the sascfg_personal.py file
    :param cfgfile: fully qualified file name of your sascfg_personal.py file, if it's not in the python search path
    :param kernel: None - internal use when running the SAS_kernel notebook
    :param results: Type of tabular results to return. default is 'Pandas', other options are 'HTML or 'TEXT'
    :param lrecl: An integer specifying the record length for transferring wide data sets from SAS to Data Frames.
    :param autoexec: A string of SAS code that will be submitted upon establishing a connection
    :return: 'SASsession'
    :rtype: 'SASsession'

    And each access method has its own set of parameters.

    **STDIO**

    :param saspath: overrides saspath Dict entry of cfgname in sascfg_personal.py file
    :param options: overrides options Dict entry of cfgname in sascfg_personal.py file
    :param encoding: This is the python encoding value that matches the SAS session encoding

    **STDIO over SSH**

    and for running STDIO over passwordless ssh, add these required parameters

    :param ssh: full path of the ssh command; /usr/bin/ssh for instance
    :param host: host name of the remote machine
    :param identity: (Optional) path to a .ppk identity file to be used on the ssh -i parameter

    :param port: (Optional) The ssh port of the remote machine normally 22 (equivalent to invoking ssh with the -p option)
    :param tunnel: (Optional) Certain methods of saspy require opening a local port and accepting data streamed from the SAS instance.

    **IOM**

    and for the IOM IO module to connect to SAS9 via Java IOM

    :param java: the path to the java executable to use
    :param iomhost: for remote IOM case, not local Windows] the resolvable host name, or ip to the IOM server to connect to
    :param iomport: for remote IOM case, not local Windows] the port IOM is listening on
    :param omruser: user id for remote IOM access
    :param omrpw: pw for user for remote IOM access
    :param encoding: This is the python encoding value that matches the SAS session encoding of the IOM server you are connecting to
    :param classpath: classpath to IOM client jars and saspyiom client jar.
    :param authkey: Key value for finding credentials in .authfile
    :param timeout: Timeout value for establishing connection to workspace server
    :param appserver: Appserver name of the workspace server to connect to
    :param sspi: Boolean for using IWA to connect to a workspace server configured to use IWA
    :param javaparms: for specifying java command line options if necessary

    """

    # def __init__(self, cfgname: str ='', kernel: 'SAS_kernel' =None, saspath :str ='', options: list =[]) -> 'SASsession':
    def __init__(self, **kwargs):
        self._loaded_macros    = False
        self._obj_cnt          = 0
        self.nosub             = False
        self.sascfg            = SASconfig(**kwargs)
        self.batch             = False
        self.results           = kwargs.get('results', self.sascfg.results)
        if not self.results:
            self.results       = 'Pandas'
        self.workpath          = ''
        self.sasver            = ''
        self.sascei            = ''
        self.SASpid            = None
        self.HTML_Style        = "HTMLBlue"
        self.sas_date_fmts     = sas_date_fmts
        self.sas_time_fmts     = sas_time_fmts
        self.sas_datetime_fmts = sas_datetime_fmts

        if not self.sascfg.valid:
            self._io = None
            return

        if self.sascfg.mode in ['STDIO', 'SSH', '']:
            if os.name != 'nt':
                self._io = SASsessionSTDIO(sascfgname=self.sascfg.name, sb=self, **kwargs)
            else:
                print("Cannot use STDIO I/O module on Windows. No "
                    "SASsession established. Choose an IOM SASconfig " 
                    "definition")
        elif self.sascfg.mode == 'IOM':
            self._io = SASsessionIOM(sascfgname=self.sascfg.name, sb=self, **kwargs)

        try:
            if self._io.pid:
                sysvars = """
                    %put WORKPATH=%sysfunc(pathname(work));
                    %put ENCODING=&SYSENCODING;
                    %put SYSVLONG=&SYSVLONG4;
                    %put SYSJOBID=&SYSJOBID;
                    %put SYSSCP=&SYSSCP;
                """
                res = self.submit(sysvars)['LOG']
                vlist         = res.rpartition('SYSSCP=')
                self.hostsep  = vlist[2].partition('\n')[0]
                vlist         = res.rpartition('SYSJOBID=')
                self.SASpid   = vlist[2].partition('\n')[0]
                vlist         = res.rpartition('SYSVLONG=')
                self.sasver   = vlist[2].partition('\n')[0]
                vlist         = res.rpartition('ENCODING=')
                self.sascei   = vlist[2].partition('\n')[0]
                vlist         = res.rpartition('WORKPATH=')
                self.workpath = vlist[2].partition('\n')[0]

                if self.hostsep == 'WIN':
                    self.hostsep = '\\'
                else:
                    self.hostsep = '/'
                self.workpath = self.workpath + self.hostsep

                if self.sascfg.autoexec:
                    self.submit(self.sascfg.autoexec)

        except (AttributeError):
            self._io = None

    def __repr__(self):
        """
        Display info about this object
        :return [str]:
        """
        if self._io is None:
            pyenc = ''
            if self.sascfg.cfgopts.get('verbose', True):
                print("This SASsession object is not valid\n")
        else:
           pyenc = self._io.sascfg.encoding

        x  = "Access Method         = %s\n" % self.sascfg.mode
        x += "SAS Config name       = %s\n" % self.sascfg.name
        x += "WORK Path             = %s\n" % self.workpath
        x += "SAS Version           = %s\n" % self.sasver
        x += "SASPy Version         = %s\n" % sys.modules['saspy'].__version__
        x += "Teach me SAS          = %s\n" % str(self.nosub)
        x += "Batch                 = %s\n" % str(self.batch)
        x += "Results               = %s\n" % self.results
        x += "SAS Session Encoding  = %s\n" % self.sascei
        x += "Python Encoding value = %s\n" % pyenc
        x += "SAS process Pid value = %s\n" % self.SASpid
        x += "\n"

        return x

    def __del__(self):
        if self._io:
            if self._io:
                return self._io.__del__()

    def _objcnt(self):
        self._obj_cnt += 1
        return '%04d' % self._obj_cnt

    def _startsas(self):
        return self._io._startsas()

    def _endsas(self):
        self.SASpid = None
        return self._io._endsas()

    def _getlog(self, **kwargs):
        return self._io._getlog(**kwargs)

    def _getlst(self, **kwargs):
        return self._io._getlst(**kwargs)

    def _getlsttxt(self, **kwargs):
        return self._io._getlsttxt(**kwargs)

    def _asubmit(self, code, results):
        if results == '':
            if self.results.upper() == 'PANDAS':
                results = 'HTML'
            else:
                results = self.results

        return self._io._asubmit(code, results)

    def submit(self, code: str, results: str = '', prompt: dict = None) -> dict:
        '''
        This method is used to submit any SAS code. It returns the Log and Listing as a python dictionary.

        - code    - the SAS statements you want to execute
        - results - format of results, HTLML and TEXT is the alternative
        - prompt  - dict of names:flags to prompt for; create macro variables (used in submitted code), then keep or delete
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

        prompt = prompt if prompt is not None else {}

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
        """
        nosub - bool. True means don't submit the code, print it out so I can see what the SAS code would be.
            False means run normally - submit the code.
        """
        self.nosub = nosub

    def set_batch(self, batch: bool):
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

    def set_results(self, results: str):
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
        """
        This methods creates a SASutil object which you can use to run various analytics.
        See the sasutil.py module.

        :return: sasutil object
        """
        if not self._loaded_macros:
            self._loadmacros()
            self._loaded_macros = True

        return SASutil(self)

    def sasviyaml(self) -> 'SASViyaML':
        """
        This methods creates a SASViyaML object which you can use to run various analytics.
        See the SASViyaML.py module.

        :return: SASViyaML object
        """
        if not self._loaded_macros:
            self._loadmacros()
            self._loaded_macros = True

        return SASViyaML(self)

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

    def sasdata(self, table: str, libref: str = '', results: str = '', dsopts: dict = None) -> 'SASdata':
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
            - format is a string or dictionary { var: format }

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                              'format'  : {'money': 'dollar10', 'time': 'tod5.'}
                             }

        :return: SASdata object
        """
        dsopts = dsopts if dsopts is not None else {}

        if results == '':
            results = self.results
        sd = SASdata(self, libref, table, results, dsopts)
        if not self.exist(sd.table, sd.libref):
            if not self.batch:
                print(
                    "Table " + sd.libref + '.' + sd.table + " does not exist. This SASdata object will not be useful until the data set is created.")
        return sd

    def saslib(self, libref: str, engine: str = ' ', path: str = '',
               options: str = ' ', prompt: dict = None) -> str:
        """

        :param libref:  the libref to be assigned
        :param engine:  the engine name used to access the SAS Library (engine defaults to BASE, per SAS)
        :param path:    path to the library (for engines that take a path parameter)
        :param options: other engine or engine supervisor options
        :return: SAS log
        """
        prompt = prompt if prompt is not None else {}

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

    def read_csv(self, file: str, table: str = '_csv', libref: str = '', results: str = '',
                 opts: dict = None) -> 'SASdata':
        """
        :param file: either the OS filesystem path of the file, or HTTP://... for a url accessible file
        :param table: the name of the SAS Data Set to create
        :param libref: the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
        :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives
        :param opts: a dictionary containing any of the following Proc Import options(datarow, delimiter, getnames, guessingrows)
        :return: SASdata object
        """
        opts = opts if opts is not None else {}

        if results == '':
            results = self.results

        self._io.read_csv(file, table, libref, self.nosub, opts)

        if self.exist(table, libref):
            return SASdata(self, libref, table, results)
        else:
            return None

    def write_csv(self, file: str, table: str, libref: str = '',
                  dsopts: dict = None, opts: dict = None) -> str:
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
            - format is a string or dictionary { var: format }

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                              'format'  : {'money': 'dollar10', 'time': 'tod5.'}
                             }
        :return: SAS log
        """
        dsopts = dsopts if dsopts is not None else {}
        opts = opts if opts is not None else {}

        log = self._io.write_csv(file, table, libref, self.nosub, dsopts, opts)
        if not self.batch:
            print(log)
        else:
            return log

    def df2sd(self, df: 'pd.DataFrame', table: str = '_df', libref: str = '',
              results: str = '', keep_outer_quotes: bool = False) -> 'SASdata':
        """
        This is an alias for 'dataframe2sasdata'. Why type all that?

        :param df: :class:`pandas.DataFrame` Pandas Data Frame to import to a SAS Data Set
        :param table: the name of the SAS Data Set to create
        :param libref: the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
        :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives
        :param keep_outer_quotes: the defualt is for SAS to strip outer quotes from delimitted data. This lets you keep them
        :return: SASdata object
        """
        return self.dataframe2sasdata(df, table, libref, results, keep_outer_quotes)

    def dataframe2sasdata(self, df: 'pd.DataFrame', table: str = '_df', libref: str = '',
                          results: str = '', keep_outer_quotes: bool = False) -> 'SASdata':
        """
        This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.

        :param df: Pandas Data Frame to import to a SAS Data Set
        :param table: the name of the SAS Data Set to create
        :param libref: the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
        :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives
        :param keep_outer_quotes: the defualt is for SAS to strip outer quotes from delimitted data. This lets you keep them
        :return: SASdata object
        """
        if results == '':
            results = self.results
        if self.nosub:
            print("too complicated to show the code, read the source :), sorry.")
            return None
        else:
            self._io.dataframe2sasdata(df, table, libref, keep_outer_quotes)

        if self.exist(table, libref):
            return SASdata(self, libref, table, results)
        else:
            return None

    def sd2df(self, table: str, libref: str = '', dsopts: dict = None, method: str = 'MEMORY',
              **kwargs) -> 'pd.DataFrame':
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
            - format is a string or dictionary { var: format }

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                              'format'  : {'money': 'dollar10', 'time': 'tod5.'}
                             }
        :param method: defaults to MEMORY; the original method. CSV is the other choice which uses an intermediary csv file; faster for large data
        :param kwargs: dictionary
        :return: Pandas data frame
        """
        dsopts = dsopts if dsopts is not None else {}
        return self.sasdata2dataframe(table, libref, dsopts, method, **kwargs)

    def sd2df_CSV(self, table: str, libref: str = '', dsopts: dict = None, tempfile: str = None, tempkeep: bool = False,
                  **kwargs) -> 'pd.DataFrame':
        """
        This is an alias for 'sasdata2dataframe' specifying method='CSV'. Why type all that?
        SASdata object that refers to the Sas Data Set you want to export to a Pandas Data Frame

        :param table: the name of the SAS Data Set you want to export to a Pandas Data Frame
        :param libref: the libref for the SAS Data Set.
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a numbers - either string or int
            - first obs is a numbers - either string or int
            - format is a string or dictionary { var: format }

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                              'format'  : {'money': 'dollar10', 'time': 'tod5.'}
                             }
        :param tempfile: [optional] an OS path for a file to use for the local CSV file; default it a temporary file that's cleaned up
        :param tempkeep: if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it
        :param kwargs: dictionary
        :return: Pandas data frame
        """
        dsopts = dsopts if dsopts is not None else {}
        return self.sasdata2dataframe(table, libref, dsopts, method='CSV', tempfile=tempfile, tempkeep=tempkeep,
                                      **kwargs)

    def sasdata2dataframe(self, table: str, libref: str = '', dsopts: dict = None, method: str = 'MEMORY',
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
            - format is a string or dictionary { var: format }

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                              'format'  : {'money': 'dollar10', 'time': 'tod5.'}
                             }

        :param method: defaults to MEMORY; the original method. CSV is the other choice which uses an intermediary csv file; faster for large data
        :param kwargs: dictionary
        :return: Pandas data frame
        """
        dsopts = dsopts if dsopts is not None else {}
        if self.exist(table, libref) == 0:
            print('The SAS Data Set ' + libref + '.' + table + ' does not exist')
            return None

        if self.nosub:
            print("too complicated to show the code, read the source :), sorry.")
            return None
        else:
            return self._io.sasdata2dataframe(table, libref, dsopts, method=method, **kwargs)

    def _dsopts(self, dsopts):
        """
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string or list of strings
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a numbers - either string or int
            - first obs is a numbers - either string or int
            - format is a string or dictionary { var: format }

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"'
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight'
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight']
                              'obs'      :  10
                              'firstobs' : '12'
                              'format'  : {'money': 'dollar10', 'time': 'tod5.'}
                             }
        :return: str
        """
        opts = ''
        fmat = ''
        if len(dsopts):
            for key in dsopts:
                if len(str(dsopts[key])):
                    if key == 'where':
                        if isinstance(dsopts[key], str):
                            opts += 'where=(' + dsopts[key] + ') '
                        elif isinstance(dsopts[key], list):
                            opts += 'where=(' + " and ".join(dsopts[key]) + ') '
                        else:
                            raise TypeError("Bad key type. {} must be a str or list type".format(key))

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

                    elif key == 'format':
                        if isinstance(dsopts[key], str):
                            fmat = 'format ' + dsopts[key] + ';'
                        elif isinstance(dsopts[key], dict):
                            fmat = 'format '
                            for k, v in dsopts[key].items():
                                fmat += ' '.join((k, v)) + ' '
                            fmat += ';'
                        else:
                            raise TypeError("Bad key type. {} must be a str or dict type".format(key))

            if len(opts):
                opts = '(' + opts + ')'
                if len(fmat) > 0:
                    opts += ';\n\t' + fmat
            elif len(fmat) > 0:
                opts = ';\n\t' + fmat
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
                    if key == 'datarow':
                        optstr += 'datarow=' + str(opts[key]) + ';'
                    elif key == 'delimiter':
                        optstr += 'delimiter='
                        optstr += "'" + '%02x' % ord(opts[key].encode(self._io.sascfg.encoding)) + "'x; "
                    elif key == 'getnames':
                        optstr += 'getnames='
                        if opts[key]:
                            optstr += 'YES; '
                        else:
                            optstr += 'NO; '
                    elif key == 'guessingrows':
                        optstr += 'guessingrows='
                        if opts[key] == 'MAX':
                            optstr += 'MAX; '
                        else:
                            optstr += str(opts[key]) + '; '
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
                    if key == 'delimiter':
                        optstr += 'delimiter='
                        optstr += "'" + '%02x' % ord(opts[key].encode(self._io.sascfg.encoding)) + "'x; "
                    elif key == 'putnames':
                        optstr += 'putnames='
                        if opts[key]:
                            optstr += 'YES; '
                        else:
                            optstr += 'NO; '
        return optstr

    def symput(self, name, value):
        """
        :param name:  name of the macro varable to set:
        :param value: python variable to use for the value to assign to the macro variable:

            - name    is a character
            - value   is a variable that can be resolved to a string

        """
        ll = self.submit("%let " + name + "=%NRBQUOTE(" + str(value) + ");\n")

    def symget(self, name):
        """
        :param name:  name of the macro varable to set:

            - name    is a character

        """
        ll = self.submit("%put " + name + "=&" + name + ";\n")

        l2 = ll['LOG'].rpartition(name + "=")
        l2 = l2[2].partition("\n")
        try:
            var = int(l2[0])
        except:
            try:
                var = float(l2[0])
            except:
                var = l2[0]

        return var

    def disconnect(self):
        """
        This method disconnects an IOM session to allow for reconnecting when switching networks
        See the Advanced topics section of the doc for details
        """
        if self.sascfg.mode != 'IOM':
            res = "This method is only available with the IOM access method"
        else:
            res = self._io.disconnect()
        return res

    def SYSINFO(self):
        """
        This method returns the SAS Automatic Macro Variable SYSINFO which
        contains return codes provided by some SAS procedures.
        """
        return self.symget("SYSINFO")

    def SYSERR(self):
        """
        This method returns the SAS Automatic Macro Variable SYSERR which
        contains a return code status set by some SAS procedures and the DATA step.
        """
        return self.symget("SYSERR")

    def SYSERRORTEXT(self):
        """
        This method returns the SAS Automatic Macro Variable SYSERRORTEXT which
        is the text of the last error message generated in the SAS log.
        """
        return self.symget("SYSERRORTEXT")

    def SYSWARNINGTEXT(self):
        """
        This method returns the SAS Automatic Macro Variable SYSWARNINGTEXT which
        is the text of the last warning message generated in the SAS log.
        """
        return self.symget("SYSWARNINGTEXT")

    def SYSFILRC(self):
        """
        This method returns the SAS Automatic Macro Variable SYSFILRC which
        identifies whether or not the last FILENAME statement executed correctly.
        """
        return self.symget("SYSFILRC")

    def SYSLIBRC(self):
        """
        This method returns the SAS Automatic Macro Variable SYSLIBRC which
        reports whether the last LIBNAME statement executed correctly.
        """
        return self.symget("SYSLIBRC")

    def assigned_librefs(self):
        """
        This method returns the list of currently assigned librefs
        """

        code = """
        data _null_; retain libref; retain cobs 1; 
           set sashelp.vlibnam end=last;
           if cobs EQ 1 then
              put "LIBREFSSTART";
           cobs = 2;
           if libref NE libname then
              put "LIBREF=" libname;
           libref = libname;
           if last then
              put "LIBREFSEND";
        run;
        """

        ll = self.submit(code, results='text')

        librefs = []
        log = ll['LOG'].rpartition('LIBREFSEND')[0].rpartition('LIBREFSSTART')
                                                                                  
        for i in range(log[2].count('LIBREF=')):                                    
           log = log[2].partition('LIBREF=')[2].partition('\n')                    
           librefs.append(log[0].strip())                                                         
                                                                                  
        return librefs


    def dirlist(self, path):
        """
        This method returns the directory list for the path specified where SAS is running
        """

        code = """
        data _null_;
         spd = '""" + path + """';
         rc  = filename('saspydir', spd);
         did = dopen('saspydir');

         if did > 0 then
            do;
               memcount = dnum(did);
               put 'MEMCOUNT=' memcount;
               do while (memcount > 0);
                  name = dread(did, memcount);
                  memcount = memcount - 1;

                  qname = spd || '"""+self.hostsep+"""' || name;

                  rc = filename('saspydq', qname);
                  dq = dopen('saspydq');
                  if dq NE 0 then
                     do;
                        dname = strip(name) || '"""+self.hostsep+"""';
                        put 'DIR=' dname;
                        rc = dclose(dq);
                     end;
                  else
                     put 'FILE=' name;
               end;

            put 'MEMEND';
            rc = dclose(did);
            end;
         else
            do;
               put 'MEMCOUNT=0';
               put 'MEMEND';
           end;

         rc = filename('saspydq');
         rc = filename('saspydir');
        run;
        """

        ll = self.submit(code, results='text')

        dirlist = []

        l2 = ll['LOG'].rpartition("MEMCOUNT=")[2].partition("\n")
        memcount = int(l2[0])

        l3 = l2[2].rpartition("MEMEND")[0]

        for row in l3.split(sep='\n'):
            i = row.partition('=')
            if i[0] in ['FILE', 'DIR']:
                dirlist.append(i[2])

        if memcount != len(dirlist):
            print("Some problem parsing list. Should be " + str(memcount) + " entries but got " + str(
                len(dirlist)) + " instead.")

        return dirlist


    def list_tables(self, libref, results: str = 'list'):
        """
        This method returns a list of tuples containing MEMNAME, MEMTYPE of members in the library of memtype data or view

        If you would like a Pandas dataframe returned instead of a list, specify results='pandas'
        """

        ll = self.submit("%put LIBREF_EXISTS=%sysfunc(libref("+libref+"));")

        exists = ll['LOG'].rsplit('LIBREF_EXISTS=')[2].split('\n')[0]

        if exists != '0':
           print('Libref provided is not assigned')
           return None

        code = """
        proc datasets dd=librefx nodetails nolist noprint;
           contents memtype=(data view) nodetails 
              dir out=work._saspy_lib_list(keep=memname memtype) data=_all_ noprint;
        run;
        
        proc sql;
           create table work._saspy_lib_list as select distinct * from work._saspy_lib_list;
        quit;
        """.replace('librefx', libref)

        ll  = self.submit(code, results='text')

        if results != 'list':
           res = self.sd2df('_saspy_lib_list', 'work')
           if res is None:
              res = pd.DataFrame.from_records([], ['MEMNAME', 'MEMTYPE'])
           return res
           
        code = """
        data _null_;
           set work._saspy_lib_list end=last curobs=first;
           if first EQ 1 then
              put 'MEMSTART';
           put 'MEMNAME=' memname;
           put 'MEMTYPE=' memtype;
           if last then
              put 'MEMEND';
        run;
        """

        ll  = self.submit(code, results='text')

        res = []
        log = ll['LOG'].rpartition('MEMEND')[0].rpartition('MEMSTART')
                                                                                  
        for i in range(log[2].count('MEMNAME')):                                    
           log = log[2].partition('MEMNAME=')[2].partition('\n')                    
           key = log[0]                                                           
           log = log[2].partition('MEMTYPE=')[2].partition('\n')                     
           val = log[0]                                                           
           res.append(tuple((key, val)))                                                         
                                                                                  
        return res


    def file_info(self, filepath,  results: str = 'dict', fileref: str = '_spfinfo'):
        """
        This method returns a dictionaty containing the file attributes for the file name provided

        If you would like a Pandas dataframe returned instead of a dictionary, specify results='pandas'
        """

        code  = "filename "+fileref+" '"+filepath+"';\n"
        code += "%put FILEREF_EXISTS=%sysfunc(fexist("+fileref+"));"

        ll = self.submit(code)

        exists = ll['LOG'].rsplit('FILEREF_EXISTS=')[2].split('\n')[0]

        if exists != '1':
           print('The filepath provided does not exist')
           ll = self.submit("filename "+fileref+" clear;")
           return None

        if results != 'dict':
           code="""
           proc delete data=work._SASPY_FILE_INFO;run;
           data work._SASPY_FILE_INFO;
              length infoname infoval $60;
              drop rc fid infonum i close;
              fid=fopen('filerefx');
              if fid then
                 do;
                    infonum=foptnum(fid);
                    do i=1 to infonum;
                       infoname=foptname(fid, i);
                       infoval=finfo(fid, infoname);
                       output;
                    end;
                 end;
              close=fclose(fid);
              rc = filename('filerefx');
           run;
           """.replace('filerefx', fileref)
   
           ll  = self.submit(code, results='text')
   
           res = self.sd2df('_SASPY_FILE_INFO', 'work')
           if res is None:
              res = pd.DataFrame.from_records([], ['infoname', 'infoval'])
           return res


        code="""
        data _null_;
           length infoname infoval $60;
           drop rc fid infonum i close;
           put 'INFOSTART';
           fid=fopen('filerefx');
           if fid then
              do;
                 infonum=foptnum(fid);
                 do i=1 to infonum;
                    infoname=foptname(fid, i);
                    infoval=finfo(fid, infoname);
                    put 'INFONAME=' infoname;
                    put 'INFOVAL=' infoval;
                 end;
              end; 
           put 'INFOEND';
           close=fclose(fid);
           rc = filename('filerefx');
        run;
        """.replace('filerefx', fileref)

        ll  = self.submit(code, results='text')

        res = {}
        log = ll['LOG'].rpartition('INFOEND')[0].rpartition('INFOSTART')
                                                                                  
        for i in range(log[2].count('INFONAME')):                                    
           log = log[2].partition('INFONAME=')[2].partition('\n')                    
           key = log[0]                                                           
           log = log[2].partition('INFOVAL=')[2].partition('\n')                     
           val = log[0]                                                           
           res[key] = val                                                         
                                                                                  
        return res

if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(_getlog())
    print(_getlsttxt())

    endsas()

sas_date_fmts = (
    'AFRDFDD', 'AFRDFDE', 'AFRDFDE', 'AFRDFDN', 'AFRDFDWN', 'AFRDFMN', 'AFRDFMY', 'AFRDFMY', 'AFRDFWDX', 'AFRDFWKX',
    'ANYDTDTE', 'B8601DA', 'B8601DA', 'B8601DJ', 'CATDFDD', 'CATDFDE', 'CATDFDE', 'CATDFDN', 'CATDFDWN', 'CATDFMN',
    'CATDFMY', 'CATDFMY', 'CATDFWDX', 'CATDFWKX', 'CRODFDD', 'CRODFDE', 'CRODFDE', 'CRODFDN', 'CRODFDWN', 'CRODFMN',
    'CRODFMY', 'CRODFMY', 'CRODFWDX', 'CRODFWKX', 'CSYDFDD', 'CSYDFDE', 'CSYDFDE', 'CSYDFDN', 'CSYDFDWN', 'CSYDFMN',
    'CSYDFMY', 'CSYDFMY', 'CSYDFWDX', 'CSYDFWKX', 'DANDFDD', 'DANDFDE', 'DANDFDE', 'DANDFDN', 'DANDFDWN', 'DANDFMN',
    'DANDFMY', 'DANDFMY', 'DANDFWDX', 'DANDFWKX', 'DATE', 'DATE', 'DAY', 'DDMMYY', 'DDMMYY', 'DDMMYYB', 'DDMMYYC',
    'DDMMYYD', 'DDMMYYN', 'DDMMYYP', 'DDMMYYS', 'DESDFDD', 'DESDFDE', 'DESDFDE', 'DESDFDN', 'DESDFDWN', 'DESDFMN',
    'DESDFMY', 'DESDFMY', 'DESDFWDX', 'DESDFWKX', 'DEUDFDD', 'DEUDFDE', 'DEUDFDE', 'DEUDFDN', 'DEUDFDWN', 'DEUDFMN',
    'DEUDFMY', 'DEUDFMY', 'DEUDFWDX', 'DEUDFWKX', 'DOWNAME', 'E8601DA', 'E8601DA', 'ENGDFDD', 'ENGDFDE', 'ENGDFDE',
    'ENGDFDN', 'ENGDFDWN', 'ENGDFMN', 'ENGDFMY', 'ENGDFMY', 'ENGDFWDX', 'ENGDFWKX', 'ESPDFDD', 'ESPDFDE', 'ESPDFDE',
    'ESPDFDN', 'ESPDFDWN', 'ESPDFMN', 'ESPDFMY', 'ESPDFMY', 'ESPDFWDX', 'ESPDFWKX', 'EURDFDD', 'EURDFDE', 'EURDFDE',
    'EURDFDN', 'EURDFDWN', 'EURDFMN', 'EURDFMY', 'EURDFMY', 'EURDFWDX', 'EURDFWKX', 'FINDFDD', 'FINDFDE', 'FINDFDE',
    'FINDFDN', 'FINDFDWN', 'FINDFMN', 'FINDFMY', 'FINDFMY', 'FINDFWDX', 'FINDFWKX', 'FRADFDD', 'FRADFDE', 'FRADFDE',
    'FRADFDN', 'FRADFDWN', 'FRADFMN', 'FRADFMY', 'FRADFMY', 'FRADFWDX', 'FRADFWKX', 'FRSDFDD', 'FRSDFDE', 'FRSDFDE',
    'FRSDFDN', 'FRSDFDWN', 'FRSDFMN', 'FRSDFMY', 'FRSDFMY', 'FRSDFWDX', 'FRSDFWKX', 'HUNDFDD', 'HUNDFDE', 'HUNDFDE',
    'HUNDFDN', 'HUNDFDWN', 'HUNDFMN', 'HUNDFMY', 'HUNDFMY', 'HUNDFWDX', 'HUNDFWKX', 'IS8601DA', 'IS8601DA', 'ITADFDD',
    'ITADFDE', 'ITADFDE', 'ITADFDN', 'ITADFDWN', 'ITADFMN', 'ITADFMY', 'ITADFMY', 'ITADFWDX', 'ITADFWKX', 'JDATEMD',
    'JDATEMDW', 'JDATEMNW', 'JDATEMON', 'JDATEQRW', 'JDATEQTR', 'JDATESEM', 'JDATESMW', 'JDATEWK', 'JDATEYDW', 'JDATEYM',
    'JDATEYMD', 'JDATEYMD', 'JDATEYMW', 'JNENGO', 'JNENGO', 'JNENGOW', 'JULDATE', 'JULDAY', 'JULIAN', 'JULIAN', 'MACDFDD',
    'MACDFDE', 'MACDFDE', 'MACDFDN', 'MACDFDWN', 'MACDFMN', 'MACDFMY', 'MACDFMY', 'MACDFWDX', 'MACDFWKX', 'MINGUO',
    'MINGUO', 'MMDDYY', 'MMDDYY', 'MMDDYYB', 'MMDDYYC', 'MMDDYYD', 'MMDDYYN', 'MMDDYYP', 'MMDDYYS', 'MMYY', 'MMYYC',
    'MMYYD', 'MMYYN', 'MMYYP', 'MMYYS', 'MONNAME', 'MONTH', 'MONYY', 'MONYY', 'ND8601DA', 'NENGO', 'NENGO', 'NLDATE',
    'NLDATE', 'NLDATEL', 'NLDATEM', 'NLDATEMD', 'NLDATEMDL', 'NLDATEMDM', 'NLDATEMDS', 'NLDATEMN', 'NLDATES', 'NLDATEW',
    'NLDATEW', 'NLDATEWN', 'NLDATEYM', 'NLDATEYML', 'NLDATEYMM', 'NLDATEYMS', 'NLDATEYQ', 'NLDATEYQL', 'NLDATEYQM',
    'NLDATEYQS', 'NLDATEYR', 'NLDATEYW', 'NLDDFDD', 'NLDDFDE', 'NLDDFDE', 'NLDDFDN', 'NLDDFDWN', 'NLDDFMN', 'NLDDFMY',
    'NLDDFMY', 'NLDDFWDX', 'NLDDFWKX', 'NORDFDD', 'NORDFDE', 'NORDFDE', 'NORDFDN', 'NORDFDWN', 'NORDFMN', 'NORDFMY',
    'NORDFMY', 'NORDFWDX', 'NORDFWKX', 'POLDFDD', 'POLDFDE', 'POLDFDE', 'POLDFDN', 'POLDFDWN', 'POLDFMN', 'POLDFMY',
    'POLDFMY', 'POLDFWDX', 'POLDFWKX', 'PTGDFDD', 'PTGDFDE', 'PTGDFDE', 'PTGDFDN', 'PTGDFDWN', 'PTGDFMN', 'PTGDFMY',
    'PTGDFMY', 'PTGDFWDX', 'PTGDFWKX', 'QTR', 'QTRR', 'RUSDFDD', 'RUSDFDE', 'RUSDFDE', 'RUSDFDN', 'RUSDFDWN', 'RUSDFMN',
    'RUSDFMY', 'RUSDFMY', 'RUSDFWDX', 'RUSDFWKX', 'SLODFDD', 'SLODFDE', 'SLODFDE', 'SLODFDN', 'SLODFDWN', 'SLODFMN',
    'SLODFMY', 'SLODFMY', 'SLODFWDX', 'SLODFWKX', 'SVEDFDD', 'SVEDFDE', 'SVEDFDE', 'SVEDFDN', 'SVEDFDWN', 'SVEDFMN',
    'SVEDFMY', 'SVEDFMY', 'SVEDFWDX', 'SVEDFWKX', 'WEEKDATE', 'WEEKDATX', 'WEEKDAY', 'WEEKU', 'WEEKU', 'WEEKV', 'WEEKV',
    'WEEKW', 'WEEKW', 'WORDDATE', 'WORDDATX', 'XYYMMDD', 'XYYMMDD', 'YEAR', 'YYMM', 'YYMMC', 'YYMMD', 'YYMMDD', 'YYMMDD',
    'YYMMDDB', 'YYMMDDC', 'YYMMDDD', 'YYMMDDN', 'YYMMDDP', 'YYMMDDS', 'YYMMN', 'YYMMN', 'YYMMP', 'YYMMS', 'YYMON', 'YYQ',
    'YYQ', 'YYQC', 'YYQD', 'YYQN', 'YYQP', 'YYQR', 'YYQRC', 'YYQRD', 'YYQRN', 'YYQRP', 'YYQRS', 'YYQS', 'YYQZ', 'YYQZ',
    'YYWEEKU', 'YYWEEKV', 'YYWEEKW',
)

sas_time_fmts = (
    'ANYDTTME', 'B8601LZ', 'B8601LZ', 'B8601TM', 'B8601TM', 'B8601TZ', 'B8601TZ', 'E8601LZ', 'E8601LZ', 'E8601TM',
    'E8601TM', 'E8601TZ', 'E8601TZ', 'HHMM', 'HOUR', 'IS8601LZ', 'IS8601LZ', 'IS8601TM', 'IS8601TM', 'IS8601TZ',
    'IS8601TZ', 'JTIMEH', 'JTIMEHM', 'JTIMEHMS', 'JTIMEHW', 'JTIMEMW', 'JTIMESW', 'MMSS', 'ND8601TM', 'ND8601TZ',
    'NLTIMAP', 'NLTIMAP', 'NLTIME', 'NLTIME', 'STIMER', 'TIME', 'TIMEAMPM', 'TOD',
)

sas_datetime_fmts = (
    'AFRDFDT', 'AFRDFDT', 'ANYDTDTM', 'B8601DN', 'B8601DN', 'B8601DT', 'B8601DT', 'B8601DZ', 'B8601DZ', 'CATDFDT',
    'CATDFDT', 'CRODFDT', 'CRODFDT', 'CSYDFDT', 'CSYDFDT', 'DANDFDT', 'DANDFDT', 'DATEAMPM', 'DATETIME', 'DATETIME',
    'DESDFDT', 'DESDFDT', 'DEUDFDT', 'DEUDFDT', 'DTDATE', 'DTMONYY', 'DTWKDATX', 'DTYEAR', 'DTYYQC', 'E8601DN',
    'E8601DN', 'E8601DT', 'E8601DT', 'E8601DZ', 'E8601DZ', 'ENGDFDT', 'ENGDFDT', 'ESPDFDT', 'ESPDFDT', 'EURDFDT',
    'EURDFDT', 'FINDFDT', 'FINDFDT', 'FRADFDT', 'FRADFDT', 'FRSDFDT', 'FRSDFDT', 'HUNDFDT', 'HUNDFDT', 'IS8601DN',
    'IS8601DN', 'IS8601DT', 'IS8601DT', 'IS8601DZ', 'IS8601DZ', 'ITADFDT', 'ITADFDT', 'JDATEYT', 'JDATEYTW', 'JNENGOT',
    'JNENGOTW', 'MACDFDT', 'MACDFDT', 'MDYAMPM', 'MDYAMPM', 'ND8601DN', 'ND8601DT', 'ND8601DZ', 'NLDATM', 'NLDATM',
    'NLDATMAP', 'NLDATMAP', 'NLDATMDT', 'NLDATML', 'NLDATMM', 'NLDATMMD', 'NLDATMMDL', 'NLDATMMDM', 'NLDATMMDS',
    'NLDATMMN', 'NLDATMS', 'NLDATMTM', 'NLDATMTZ', 'NLDATMW', 'NLDATMW', 'NLDATMWN', 'NLDATMWZ', 'NLDATMYM', 'NLDATMYML',
    'NLDATMYMM', 'NLDATMYMS', 'NLDATMYQ', 'NLDATMYQL', 'NLDATMYQM', 'NLDATMYQS', 'NLDATMYR', 'NLDATMYW', 'NLDATMZ',
    'NLDDFDT', 'NLDDFDT', 'NORDFDT', 'NORDFDT', 'POLDFDT', 'POLDFDT', 'PTGDFDT', 'PTGDFDT', 'RUSDFDT', 'RUSDFDT',
    'SLODFDT', 'SLODFDT', 'SVEDFDT', 'SVEDFDT', 'TWMDY', 'YMDDTTM',
)
