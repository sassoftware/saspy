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

#so the doc will generate for df methods
try:
   import pandas
except Exception as e:
   pass

import os
import sys
import datetime
import getpass
import importlib
import re
import shutil
import tempfile
import typing

import logging
logger = logging.getLogger('saspy')

from saspy.sasiostdio    import SASsessionSTDIO
from saspy.sasioiom      import SASsessionIOM
from saspy.sasiohttp     import SASsessionHTTP
from saspy.sasiocom      import SASSessionCOM

from saspy.sasdata       import SASdata
from saspy.sasml         import SASml
from saspy.sasets        import SASets
from saspy.sasqc         import SASqc
from saspy.sasstat       import SASstat
from saspy.sasutil       import SASutil
from saspy.sasViyaML     import SASViyaML

from saspy.version       import __version__ as SASPy_CUR_VER

from saspy.sasexceptions import (SASIONotSupportedError, SASConfigNotValidError,
                                SASConfigNotFoundError, SASIOConnectionError)
_cfgfile_cnt = 0

try:
   from IPython.display import HTML
   from IPython.display import display as DISPLAY
except ImportError:
   def DISPLAY(x): print(x)
   def HTML(x):    return "IPython didn't import. Can't render HTML"

def zepDISPLAY(x):
   print(x)

def zepHTML(x):
   return("%html "+x)

def dbDISPLAY(x):
   displayHTML(x)

def dbHTML(x):
   return(x)

def list_configs() -> list:
   cfg   = []
   sp    = []
   sp[:] = sys.path
   sp[0] = os.path.abspath(sp[0])
   sp.insert(1, os.path.expanduser('~/.config/saspy'))
   sp.insert(0, __file__.rsplit(os.sep+'sasbase.py')[0])

   for dir in sp:
      f1 = dir+os.sep+'sascfg_personal.py'
      if os.path.isfile(f1):
         cfg.append(f1)

   if len(cfg) == 0:
      f1 =__file__.rsplit('sasbase.py')[0]+'sascfg.py'
      if os.path.isfile(f1):
         cfg.append(f1)

   return cfg

class SASconfig(object):
    """
    This object is not intended to be used directly. Instantiate a SASsession object instead
    """
    DOTCONFIG = '~/.config/saspy/'

    def __init__(self, **kwargs):
        self._kernel = kwargs.get('kernel', None)
        self.valid   = True
        self.mode    = ''
        self.origin  = ''
        configs      = []

        curver       = [int(i) for i in SASPy_CUR_VER.split('.')]
        self.curver  = curver[0]*1000000+curver[1]*1000+curver[2]*1

        try:
           import pandas
           self.pandas  = None
        except Exception as e:
           self.pandas  = e

        SAScfg = self._find_config(cfg_override=kwargs.get('cfgfile'))
        self.SAScfg = SAScfg

        # Get Config options. Fallback to empty dict.
        self.cfgopts = getattr(SAScfg, "SAS_config_options", {})

        # account for default ODS style
        try:
           outopts       = getattr(SAScfg, "SAS_output_options")
           self.odsstyle = outopts.get('style', 'HTMLBlue')
        except:
           self.odsstyle = 'HTMLBlue'

        # See if we don't want to allow prompting in this environment
        prompt = self.cfgopts.get('prompt', True)
        self.prompt = kwargs.get('prompt', prompt)

        # In lock down mode, don't allow runtime overrides of option values from the config file.
        lock = self.cfgopts.get('lock_down', True)

        # Get Config names. Fallback to empty list.
        configs = getattr(SAScfg, "SAS_config_names", [])

        cfgname = kwargs.get('cfgname', '')

        if len(cfgname) == 0:
            if len(configs) == 0:
                raise SASConfigNotValidError(cfgname, msg='No SAS_config_names found in saspy.sascfg')
            else:
                if len(configs) == 1:
                    cfgname = configs[0]
                    if self._kernel is None:
                        logger.info("Using SAS Config named: " + cfgname)
                else:
                    cfgname = self._prompt(
                        "Please enter the name of the SAS Config you wish to run. Available Configs are: " +
                        str(configs) + " ")

        while cfgname not in configs:
            cfgname = self._prompt(
                "The SAS Config name specified was not found. Please enter the SAS Config you wish to use. Available Configs are: " +
                str(configs) + " ")
            if cfgname is None:
                raise RuntimeError("No SAS Config name provided.")

        self.name = cfgname
        cfg = getattr(SAScfg, cfgname)

        ip            = cfg.get('ip')
        url           = cfg.get('url')
        ssh           = cfg.get('ssh')
        path          = cfg.get('saspath')
        java          = cfg.get('java')
        provider      = cfg.get('provider')
        self.display  = cfg.get('display',  '')
        self.results  = cfg.get('results')
        self.autoexec = cfg.get('autoexec')

        bcv           = kwargs.get('SAS_BCV', getattr(SAScfg, "SAS_BCV", SASPy_CUR_VER))
        try:
           bcv = [int(i) for i in bcv.split('.')]
           if len(bcv) != 3 or False in [i >= 0 and i <=999 for i in bcv]:
              raise
           self.bcv = bcv[0]*1000000+bcv[1]*1000+bcv[2]*1
        except:
           logger.warning("Value provided for SAS_BCV was not valid. Using default of '3.7.8'.")
           self.bcv = self.curver

        indisplay = kwargs.get('display', '')
        if len(indisplay) > 0:
           if lock and len(self.display):
              logger.warning("Parameter 'display' passed to SAS_session was ignored due to configuration restriction.")
           else:
              self.display = indisplay
        if self.display == '':
           self.display = 'jupyter'
        else:
           if self.display.lower() not in ['zeppelin', 'jupyter', 'databricks']:
              logger.warning("Invalid value specified for 'display'. Using the default of 'jupyter'")
              self.display = 'jupyter'

        if   self.display.lower() == 'zeppelin':
           self.DISPLAY = zepDISPLAY
           self.HTML    = zepHTML
        elif self.display.lower() == 'databricks':
           self.DISPLAY = dbDISPLAY
           self.HTML    = dbHTML
        else:
           self.DISPLAY = DISPLAY
           self.HTML    = HTML

        inautoexec = kwargs.get('autoexec', None)
        if inautoexec:
            if lock and self.autoexec is not None:
                logger.warning("Parameter 'autoexec' passed to SAS_session was ignored due to configuration restriction.")
            else:
                self.autoexec = inautoexec

        inurl = kwargs.get('url', None)
        if inurl:
           if lock and url is not None:
              logger.warning("Parameter 'url' passed to SAS_session was ignored due to configuration restriction.")
           else:
              url = inurl

        inip = kwargs.get('ip', None)
        if inip:
           if lock and ip is not None:
              logger.warning("Parameter 'ip' passed to SAS_session was ignored due to configuration restriction.")
           else:
              ip = inip

        inssh = kwargs.get('ssh', None)
        if inssh:
           if lock and ssh is not None:
              logger.warning("Parameter 'ssh' passed to SAS_session was ignored due to configuration restriction.")
           else:
              ssh = inssh

        insaspath = kwargs.get('saspath', None)
        if insaspath:
           if lock and path is not None:
              logger.warning("Parameter 'saspath' passed to SAS_session was ignored due to configuration restriction.")
           else:
              path = insaspath

        injava = kwargs.get('java', None)
        if injava:
           if lock and java is not None:
              logger.warning("Parameter 'java' passed to SAS_session was ignored due to configuration restriction.")
           else:
              java = injava

        inprov = kwargs.get('provider', None)
        if inprov:
           if lock and provider is not None:
              logger.warning("Parameter 'provider' passed to SAS_session was ignored due to configuration restriction.")
           else:
              provider = inprov

        if java is not None:
            self.mode = 'IOM'
        elif url is not None:
            self.mode = 'HTTP'
        elif ip is not None:
            self.mode = 'HTTP'
        elif ssh is not None:
            self.mode = 'SSH'
        elif provider is not None:
            self.mode = 'COM'
        elif path is not None:
            self.mode = 'STDIO'
        else:
            raise SASConfigNotValidError(cfgname)

    def _find_config(self, cfg_override: str=None):
        """
        Locate the user's preferred configuration file if possible, falling
        back through a hierarchy of configuration file locations. The hierarchy
        is as follows:
            1. If a `cfgfile` param is provided to `sas.SASsession()`, use this
               configuration or nothing else. If the configuration path is
               invalid, raise an exception.
            2. If no `cfgfile` param is provided, use existing behavior of global
               "personal" config in the saspy library path.
            3. If no global "personal" file found search for a "personal" config
               in the local scope (`sys.path[0]`). This is mainly to support a
               local project config that differs from a more general one.
            4. If no config file is found locally, search for a "personal"
               config in the user's $HOME/.config/saspy directory.
            5. Finally, fall back to the standard `sascfg.py` file in the
               library path, then further down the rest of the path.
        :option cfg_override: The provided `cfgfile` param to `sas.SASsession()`
        :return [module]:
        """
        if cfg_override is not None:
            # Option 1
            #
            # This is the config file override import method, which copies a
            # given config file to a temp location and imports. This method
            # can be significantly cleaner if using the builtin importlib
            # functions, but we must support Python versions <= 3.4 (all EOL).
            cfg_expand = os.path.expanduser(cfg_override)

            # Check file exists before proceeding
            if not os.path.exists(cfg_expand):
                raise SASConfigNotFoundError(cfg_expand)
            self.origin = cfg_expand

            global _cfgfile_cnt
            _cfgfile_cnt += 1
            tempdir       = tempfile.TemporaryDirectory()
            tempname      = "sascfg"+'%03d' % _cfgfile_cnt

            shutil.copyfile(cfg_expand, os.path.join(tempdir.name, tempname+'.py'))
            sys.path.append(tempdir.name)

            #import sascfgfile as SAScfg
            SAScfg = importlib.import_module(tempname)

            sys.path.remove(tempdir.name)
            tempdir.cleanup()

        else:
            # Options 2, 3, 4, 5
            # Insert saspy config folder behind any local configs but ahead of other
            # configurations on the system.
            cfg_path = os.path.expanduser(self.DOTCONFIG)
            sys.path.insert(1, cfg_path)

            mod_path = __file__.replace(os.sep+'sasbase.py', '')
            sys.path.insert(0, mod_path)

            try:
                # Option 2, 3, 4
                import sascfg_personal as SAScfg
            except ImportError:
                # Option 5
                import sascfg as SAScfg
            finally:
                sys.path.remove(cfg_path)
                sys.path.remove(mod_path)
            self.origin = SAScfg.__spec__.origin

        return SAScfg

    def _prompt(self, prompt, pw=False):
        if self.prompt:
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
                   return self._kernel._input_request(prompt, self._kernel._parent_ident, self._kernel._parent_header, password=pw)
               except Exception:
                   return self._kernel._input_request(prompt, self._kernel._parent_ident["shell"], self._kernel.get_parent("shell"),
                                                      password=pw)
               except KeyboardInterrupt:
                   return None
        else:
           return None

class SASsession():
    """
    **Overview**

    The SASsession object is the main object to instantiate and provides access to the rest of the functionality.
    Most of these parameters will be configured in the sascfg_personal.py configuration file.
    All of these parameters are documented more thoroughly in the Configuration section of the saspy doc:
    https://sassoftware.github.io/saspy/configuration.html
    These are generally defined in the sascfg_personal.py file as opposed to being specified on the SASsession() invocation.

    Common parms for all access methods are:

    :param cfgname: the Configuration Definition to use - value in SAS_config_names List in the sascfg_personal.py file
    :param cfgfile: fully qualified file name of your sascfg_personal.py file, if it's not in the python search path
    :param kernel: None - internal use when running the SAS_kernel notebook
    :param results: Type of tabular results to return. default is 'Pandas', other options are 'HTML or 'TEXT'
    :param lrecl: An integer specifying the record length for transferring wide data sets from SAS to DataFrames.
    :param autoexec: A string of SAS code that will be submitted upon establishing a connection
    :param display: controls how to display html in different notebooks. default is jupyter.
           valid values are ['jupyter', 'zeppelin', 'databricks']
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
    :param rtunnel: (Optional) Certain methods of saspy require opening a remote port and accepting data streamed to the SAS instance.

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
    :param logbufsz: see issue 266 for details on this. not needed normally
    :param reconuri: the uri (token) for connecting back to the workspace server after you've disconnected. \
                     not needed unless connecting back from a different Python process.

    **HTTP**

    and for the HTTP Access Method to to connect to SAS in Viya

    :param url: The URL to Viya, of the form: http[s]://host.identifier[:port]
    :param verify: Flag to have http try to verify the certificate or not
    :param client_id: [for SSO Viya configurations] client_id to use for authenticating to Viya (defaults to 'SASPy')
    :param client_secret: [for SSO Viya configurations] client_secret to use for authenticating to Viya (defaults to '')
    :param authcode: [for SSO Viya configurations] one time authorization code acquired via the SASLogon oauth servide \
           where the url to get the code would be [url]/SASLogon/oauth/authorize?client_id=[client_id]i&response_type=code \
           so perhaps: https://SAS.Viya.sas.com/SASLogon/oauth/authorize?client_id=SASPy&response_type=code
    :param authkey: Key value for finding credentials in .authfile
    :param user: userid for connecting to Viya (Not valid if Viya is configured for SSO - Single Sign On)
    :param pw: password for connecting to Viya (Not valid if Viya is configured for SSO - Single Sign On)
    :param context: The Compute Server Context to connect to
    :param options: SAS options to include when connecting
    :param encoding: [deprecated] The Compute Service interface only works in UTF-8, regardless of the SAS encoding
    :param timeout: This is passed to the HTTPConnection (http.client) and has nothing to do with Viya or Compute
    :param inactive: This is Inactivity Timeout, in minutes, for the SAS Compute Session. It defaults to 120 minutes.
    :param ip: [deprecated] The resolvable host name, or IP address to the Viya (use url instead)
    :param port: [deprecated] The port to use to connect to Viya (use url instead)
    :param ssl: [deprecated] Boolean identifying whether to use HTTPS (ssl=True) or just HTTP (use url instead)
    :param authtoken: The SASLogon authorization token to use instead of acquiring one via user/pw or authcode or jwt. \
           Normally SASPy calls SASLogon to authenticate and get this token. But, if you do that yourself, you can pass it in.
    :param jwt: A JWT that can be used to acquire a SASLogon authorization token. This would be something like an Azure \
           token, where Azure and Viya have been set up to allow the JWT to be used to get a SASLogon token.


    **COM**

    and for IOM IO via COM

    :param iomhost: Resolvable host name or IP of the server
    :param iomport: Server port
    :param class_id: IOM workspace server class identifier
    :param provider: IOM provider
    :param authkey: Key value for finding credentials in .authfile
    :param encoding: This is the python encoding value that matches the SAS
                     session encoding of the IOM server
    :param omruser: User
    :param omrpw: Password


    **Common SASsession attributes**

    The values of the following attributes will be displayed if you submit a SASsession object.
    These can be referenced programmatically in you code. For the Booleans, you should use the provided methods to set them,
    or change their value. The others you should NOT change, for obvious reasons.

    - workpath - string containing the WORK libref?s filesystem path.
    - sasver - string of the SAS Version for the SAS server connected to
    - version - string of the saspy version you?re running
    - nosub - Boolean for current value of the teach_me_SAS() setting.
    - batch - Boolean for current value of the batch setting. use set_batch() to change value.
    - results - string showing current value of for session results setting. use set_results() to change value.
    - sascei - string for the SAS Session Encoding this SAS server is using
    - SASpid - The SAS processes id, or None if no SAS session connected

    Other attrritubes of the SASsession object that you may use for various purposes.

    - hostsep - simply a forward slash for linux systems and a backslash on windows clients; just for convenience
    - check_error_log - Boolean that identifies an ERROR has been found in the SASLOG. You should set this to False prior \
                 to running a saspy method that where you check it after. saspy does not reset it to False for you.
    - reconuri - the uri (token) for connecting back to the workspace server after you've disconnected. \
                 not needed unless connecting back from a different Python process; not the usual case.

    """
    # SAS Epoch: 1960-01-01
    SAS_EPOCH = datetime.datetime(1960, 1, 1)

    # def __init__(self, cfgname: str ='', kernel: 'SAS_kernel' =None, saspath :str ='', options: list =[]) -> 'SASsession':
    def __init__(self, **kwargs):
        self._loaded_macros    = False
        self._obj_cnt          = 0
        self.nosub             = False
        self.sascfg            = SASconfig(**kwargs)
        self.batch             = False
        self.results           = kwargs.get('results', self.sascfg.results)
        if not self.results:
           self.results        = 'Pandas'
        if self.sascfg.pandas and self.results.lower() == 'pandas':
           self.results        = 'HTML'
           logger.warning('Pandas module not available. Setting results to HTML')
        self.workpath          = ''
        self.sasver            = ''
        self.version           = sys.modules['saspy'].__version__
        self.sascei            = ''
        self.SASpid            = None
        self.HTML_Style        = self.sascfg.odsstyle
        self.sas_date_fmts     = sas_date_fmts
        self.sas_time_fmts     = sas_time_fmts
        self.sas_datetime_fmts = sas_datetime_fmts
        self.DISPLAY           = self.sascfg.DISPLAY
        self.HTML              = self.sascfg.HTML
        self.logoffset         = 0
        self.check_error_log   = False

        if not self.sascfg.valid:
            self._io = None
            return

        if self.sascfg.mode in ['STDIO', 'SSH', '']:
            if os.name != 'nt' or self.sascfg.mode == 'SSH':
                self._io = SASsessionSTDIO(sascfgname=self.sascfg.name, sb=self, **kwargs)
            else:
                raise SASIONotSupportedError(self.sascfg.mode, alts=['IOM'])
        elif self.sascfg.mode == 'IOM':
            self._io = SASsessionIOM(sascfgname=self.sascfg.name, sb=self, **kwargs)
        elif self.sascfg.mode == 'COM':
            self._io = SASSessionCOM(sascfgname=self.sascfg.name, sb=self, **kwargs)
        elif self.sascfg.mode == 'HTTP':
            self._io = SASsessionHTTP(sascfgname=self.sascfg.name, sb=self, **kwargs)

        # gather some session info
        sysvars  = "data _null_; length x $ 4096;"
        if self.sascfg.mode in ['STDIO', 'SSH', '']:
           sysvars += " file STDERR;"
        sysvars += """
               x = resolve('%sysfunc(pathname(work))');  put 'WORKPATH=' x 'WORKPATHEND=';
               x = resolve('&SYSENCODING');              put 'ENCODING=' x 'ENCODINGEND=';
               x = resolve('&SYSVLONG4');                put 'SYSVLONG=' x 'SYSVLONGEND=';
               x = resolve('&SYSJOBID');                 put 'SYSJOBID=' x 'SYSJOBIDEND=';
               x = resolve('&SYSSCP');                     put 'SYSSCP=' x 'SYSSCPEND=';
            run;
        """

        # Validating encoding is done next, so handle it not being set for
        # this one call
        enc = self._io.sascfg.encoding
        if enc == '':
           self._io.sascfg.encoding = 'utf_8'
        res = self._io.submit(sysvars, "text")['LOG']
        self._io.sascfg.encoding = enc

        vlist         = res.rpartition('SYSSCP=')
        self.hostsep  = vlist[2].partition(' SYSSCPEND=')[0]
        vlist         = res.rpartition('SYSJOBID=')
        self.SASpid   = vlist[2].partition(' SYSJOBIDEND=')[0]
        vlist         = res.rpartition('SYSVLONG=')
        self.sasver   = vlist[2].partition(' SYSVLONGEND=')[0]
        vlist         = res.rpartition('ENCODING=')
        self.sascei   = vlist[2].partition(' ENCODINGEND=')[0]
        vlist         = res.rpartition('WORKPATH=')
        self.workpath = vlist[2].rpartition('WORKPATHEND=')[0].strip().replace('\n','')

        # validate encoding
        if self.sascfg.mode != 'HTTP':
           failed = False
           try:
              self.pyenc = sas_encoding_mapping[self.sascei]
           except KeyError:
              logger.fatal("Invalid response from SAS on inital submission. printing the SASLOG as diagnostic")
              logger.fatal(self._io._log)
              failed = True
              pass

           if failed:
              raise SASIOConnectionError(res)

           if self.pyenc is not None:
              if self._io.sascfg.encoding != '':
                 if self._io.sascfg.encoding.lower() not in self.pyenc:
                    msg  = "The encoding value provided doesn't match the SAS session encoding.\n"
                    msg += "SAS encoding is "+self.sascei+". Specified encoding is "+self._io.sascfg.encoding+".\n"
                    msg += "Using encoding "+self.pyenc[1]+" instead to avoid transcoding problems.\n"
                    logging.info(msg)
                    msg  = "You can override this change, if you think you must, by changing the encoding attribute of the SASsession object, as follows.\n"
                    msg += """If you had 'sas = saspy.SASsession(), then submit: "sas._io.sascfg.encoding='override_encoding'" to change it.\n"""
                    logging.debug(msg)
                    self._io.sascfg.encoding = self.pyenc[1]
              else:
                 self._io.sascfg.encoding = self.pyenc[1]
                 if self._io.sascfg.verbose:
                    msg  = "No encoding value provided. Will try to determine the correct encoding.\n"
                    msg += "Setting encoding to "+self.pyenc[1]+" based upon the SAS session encoding value of "+self.sascei+".\n"
                    logging.info(msg)
           else:
              msg  = "The SAS session encoding for this session ("+self.sascei+") doesn't have a known Python equivalent encoding.\n"
              if self._io.sascfg.encoding == '':
                 self._io.sascfg.encoding  = 'utf_8'
                 msg += "Proceeding using the default encoding of 'utf_8', though you may encounter transcoding problems.\n"
              else:
                 msg += "Proceeding using the specified encoding of "+self._io.sascfg.encoding+", though you may encounter transcoding problems.\n"
              logger.warning(msg)
        else:
           self.pyenc = sas_encoding_mapping['utf-8']

        if self.hostsep == 'WIN':
            self.hostsep = '\\'
        else:
            self.hostsep = '/'
        self.workpath = self.workpath + self.hostsep

        if self.sascfg.autoexec:
            self._io.submit(self.sascfg.autoexec)

        # this is to support parsing the log to fring log records w/ 'ERROR' when diagnostic logging is enabled.
        # in thi scase the log can have prefix and/or suffix info so the 'regular' log data is in the middle, not left justified
        if self.sascfg.mode in ['STDIO', 'SSH', '']:
           ll = self._io.submit("""data _null_; file STDERR; put %upcase('col0REG=');
                               data _null_; put %upcase('col0LOG=');run;""", results='text')
           regoff = len(ll['LOG'].rpartition('COL0REG=')[0].rpartition('\n')[2])
           logoff = len(ll['LOG'].rpartition('COL0LOG=')[0].rpartition('\n')[2])

           if regoff == 0 and logoff > 0:
              self.logoffset = logoff

        self._lastlog = self._io._log


    def __repr__(self):
        """
        Display info about this object
        :return [str]:
        """
        if self._io is None:
            pyenc = ''
            if self.sascfg.cfgopts.get('verbose', True):
                logger.warning("This SASsession object is not valid\n")
        else:
           pyenc = self._io.sascfg.encoding

        x  = "Access Method         = %s\n" % self.sascfg.mode
        x += "SAS Config name       = %s\n" % self.sascfg.name
        x += "SAS Config file       = %s\n" % self.sascfg.origin
        x += "WORK Path             = %s\n" % self.workpath
        x += "SAS Version           = %s\n" % self.sasver
        x += "SASPy Version         = %s\n" % self.version
        x += "Teach me SAS          = %s\n" % str(self.nosub)
        x += "Batch                 = %s\n" % str(self.batch)
        x += "Results               = %s\n" % self.results
        x += "SAS Session Encoding  = %s\n" % self.sascei
        x += "Python Encoding value = %s\n" % pyenc
        x += "SAS process Pid value = %s\n" % self.SASpid
        x += "\n"

        return x

    def __del__(self):
        if getattr(self, '_io', None) is not None:
           return self._io.__del__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.endsas()

    def _objcnt(self):
        self._obj_cnt += 1
        return '%04d' % self._obj_cnt

    def _startsas(self):
        return self._io._startsas()

    def endsas(self):
        """
        This method terminates the SAS session, shutting down the SAS process.
        """
        return self._endsas()

    def _endsas(self):
        self.SASpid = None
        if self._io:
           return self._io._endsas()

    def _refresh_token(self):
       if self.sascfg.mode == 'HTTP':
          return self._io._refresh_token()
       else:
          print("This method is only valid in the HTTP Access Method")

    def _getlog(self, **kwargs):
        return self._io._getlog(**kwargs)

    def _getlst(self, **kwargs):
        return self._io._getlst(**kwargs)

    def _getlsttxt(self, **kwargs):
        return self._io._getlsttxt(**kwargs)

    def _asubmit(self, code, results=''):
        if results == '':
            if self.results.upper() == 'PANDAS':
                results = 'HTML'
            else:
                results = self.results

        return self._io._asubmit(code, results)

    def submitLOG(self, code, results: str = '', prompt: dict = None, printto=False, **kwargs):
        '''
        This method is a convenience wrapper around the submit() method. It executes the submit then prints the LOG that was returned.
        '''
        print(self.submit(code, results, prompt, printto, **kwargs)['LOG'])

    def submitLST(self, code, results: str = '', prompt: dict = None, method: str = None, printto=False, **kwargs):
        '''
        This method is a convenience wrapper around the submit() method. It executes the submit then renders the LST that was returned,
        as either HTML or TEXT, depending upon results. The method= parameter allows you to adjust what gets returned to suit your needs.

           - listorlog  - this is the default as of V3.6.5. returns the LST, unless it's empty, then it returns the LOG instead \
                          (one or the other). Useful in case there's an ERROR.
           - listonly   - this was the default, and returns the LST (will be empty if no output was produced by what you submitted)
           - listandlog - as you might guess, this returns both. The LST followed by the LOG
           - logandlist - as you might guess, this returns both. The LOG followed by the LST
        '''
        if method is None:
           method = 'listorlog'

        if method.lower() not in ['listonly', 'listorlog', 'listandlog', 'logandlist']:
           logger.warning("The specified method is not valid. Using the default: 'listorlog'")
           method = 'listorlog'

        if results == '':
           if self.results.upper() == 'PANDAS':
              results = 'HTML'
           else:
              results = self.results

        ll  = self.submit(code, results, prompt, printto, **kwargs)

        if results.upper() == 'HTML':
           if   method.lower() == 'listonly':
              self.DISPLAY(self.HTML(ll['LST']))
           elif method.lower() == 'listorlog':
              if len(ll['LST']) > 0:
                 self.DISPLAY(self.HTML(ll['LST']))
              else:
                 self.DISPLAY(self.HTML("<pre>"+ll['LOG']+"</pre>"))
           elif method.lower() == 'listandlog':
              self.DISPLAY(self.HTML(ll['LST']+"\n<pre>"+ll['LOG']+"</pre>"))
           else:
              self.DISPLAY(self.HTML("<pre>"+ll['LOG']+"\n</pre>"+ll['LST']))
        else:
           if   method.lower() == 'listonly':
              print(ll['LST'])
           elif method.lower() == 'listorlog':
              if len(ll['LST']) > 0:
                 print(ll['LST'])
              else:
                 print(ll['LOG'])
           elif method.lower() == 'listandlog':
              print(ll['LST']+"\n"+ll['LOG'])
           else:
              print(ll['LOG']+"\n"+ll['LST'])

    def submit(self, code: str, results: str = '', prompt: dict = None, printto=False, **kwargs) -> dict:
        '''
        This method is used to submit any SAS code. It returns the Log and Listing as a python dictionary.

        :param code:    the SAS statements you want to execute
        :param results: format of results. 'HTML' by default, alternatively 'TEXT'
        :param prompt:  dict of names and flags to prompt for; create macro variables (used in submitted code), then keep or delete \
                        the keys which are the names of the macro variables. The boolean flag is to either hide what you type and \
                        delete the macros, or show what you type and keep the macros (they will still be available later).

            for example (what you type for pw will not be displayed, user and dsname will):

            .. code-block:: python

                results_dict = sas.submit(
                             """
                             libname tera teradata server=teracop1 user=&user pw=&pw;
                             proc print data=tera.&dsname (obs=10); run;
                             """ ,
                             prompt = {'user': False, 'pw': True, 'dsname': False}
                             )

        :param printto: this option, when set to True, will cause saspy to issue a 'proc printto;run;' after the code that is being \
                        submitted. This will 'undo' any proc printto w/in the submitted code that redirected the LOG or LST, to return \
                        the LOG/LST back to saspy. This is explained in more detail in the doc: https://sassoftware.github.io/saspy/limitations.html

        **HTTP**

        These kwargs are available for the HTTP Access Method for cases where long running code is submitteds. It's been observed
        that HTTP Disconnect failures can be returned, even though subsequent calls still work, when submitting the request to see
        if the code has finished, so the LOG and LST can then be requested.
        To work around this issue, two parameters are available; one to have a delay between polling requests, and the other the
        number of disconnect errors to ignore before returning a failure. The defaults are to delay 0 seconds (so everything doesn't
        have a delay that slows down how things run), and 5 disconnect errors. If you submit code that runs for more then a few
        seconds, you can specify GETstatusDelay=n.n, the nunber of seconds (maybe 0.5 or 2, or 60 if you job runs for many minutes)
        to wait befor asking Compute if the code finished.

        :param GETstatusDelay: Number of seconds to sleep between HTTP calls to poll and see if the submitted code has finished
        :param GETstatusFailcnt: Number of disconnect failures to ignore before failing, when polling to see if the submitted code has finished


        :return: a Dict containing two keys:values, [LOG, LST]. LOG is text and LST is 'results' (HTML or TEXT)

        NOTE: to view HTML results in the ipykernel, issue: from IPython.display import HTML  and use HTML() instead of print()

        In Zeppelin, the html LST results can be displayed via print("%html "+ ll['LST']) to diplay as HTML.

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

        ll = self._io.submit(code, results, prompt, undo=printto, **kwargs)

        return ll

    def saslog(self) -> str:
        """
        This method is used to get the current, full contents of the SASLOG

        :return: SAS log
        :rtype: str
        """
        return self._io.saslog()

    def lastlog(self) -> str:
        """
        This method is used to get the LOG from the most recetly executed submit() method. That is either
        a user submitted submit() or internally submitted by any saspy method. This is just a convenience
        over the saslog() method, to just see the LOG for the last code that was submitted instead of the
        whole session.

        :return: SAS log (partial)
        :rtype: str
        """
        return self._lastlog

    def teach_me_SAS(self, nosub: bool):
        """
        :param nosub: bool. True means don't submit the code, print it out so I can see what the SAS code would be. \
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

        :param batch: bool   True = return dict([LOG, LST]. False = display LST to screen.
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

    def _render_html_or_log(self, ll):
        """
        This method renders the html lst if it's there else the log
        """
        if len(ll['LST']) > 0:
            self.DISPLAY(self.HTML(ll['LST']))
        else:
            self.DISPLAY(self.HTML("<pre> NO HTML TO RENDER. LOG IS:\n"+ll['LOG']+" </pre>"))

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
            - obs is a number - either string or int
            - first obs is a number - either string or int
            - format is a string or dictionary { var: format }
            - encoding is a string

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"' ,
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight' ,
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight'] ,
                              'obs'      :  10 ,
                              'firstobs' : '12' ,
                              'format'   : {'money': 'dollar10', 'time': 'tod5.'} ,
                              'encoding' : 'latin9'
                             }

        :return: SASdata object
        """
        lastlog = len(self._io._log)
        dsopts  = dsopts if dsopts is not None else {}

        if results == '':
            results = self.results
        sd = SASdata(self, libref, table, results, dsopts)
        if not self.exist(sd.table, sd.libref):
            if not self.batch:
                logger.warning("Table "+sd.libref+'.'+sd.table+" does not exist. This SASdata object will not be useful until the data set is created.")

        self._lastlog = self._io._log[lastlog:]
        return sd

    def lib_path(self, libref: str) -> list:
        """
        :param libref:  the libref to get the path from
        :return: list of paths for the libref (supports concatenated libraries); note that some librefs have no path, like database librefs.
        """

        if libref.upper() not in self.assigned_librefs():
           logger.warning("Libref {} is not assigned in this SAS session".format(libref))
           return []

        code = "data _null_; length x $ 4096;"
        if self.sascfg.mode in ['STDIO', 'SSH', '']:
           code += " file STDERR;"
        code += " x = resolve('%sysfunc(pathname({}))');  put 'LIBPATH=' x 'LIBPATHEND='; run;".format(libref)

        if self.nosub:
            print(code)
        else:
            ll = self._io.submit(code, "text")

        libpath = ll['LOG'].rpartition('LIBPATH=')[2].rpartition('LIBPATHEND=')[0].strip().replace('\n','')

        libpathlist = []
        if libpath.startswith('(') and libpath.endswith(')'):
           npaths = int(libpath.count("'")/2)
           for i in range(npaths):
              path = libpath.partition("'")[2].partition("'")
              libpathlist.append(path[0])
              libpath = path[2]
        else:
           libpathlist.append(libpath)

        return libpathlist

    def saslib(self, libref: str, engine: str = ' ', path: typing.Union[str, list] = '',
               options: str = ' ', prompt: dict = None) -> str:
        """

        :param libref:  the libref to be assigned
        :param engine:  the engine name used to access the SAS Library (engine defaults to BASE, per SAS)
        :param path:    path or list of paths to the library (for engines that take a path parameter)
        :param options: other engine or engine supervisor options
        :return: SAS log
        """
        prompt = prompt if prompt is not None else {}

        code = "libname " + libref + " " + engine + " "
        if type(path) == str and len(path) > 0:
            code += " '" + path + "' "
        if type(path) == list and len(path) > 0:
            code += "(" + ','.join("'" + p + "'" for p in path) + ")"
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
           if self.results.lower() == 'html':
              ll = self._io.submit(code, "html")
              if not self.batch:
                 self._render_html_or_log(ll)
              else:
                 return ll
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
        lastlog = len(self._io._log)
        opts    = opts if opts is not None else {}

        if results == '':
            results = self.results

        self._io.read_csv(file, table, libref, self.nosub, opts)

        if self.exist(table, libref):
            sd = SASdata(self, libref, table, results)
        else:
            sd =None

        self._lastlog = self._io._log[lastlog:]
        return sd

    def write_csv(self, file: str, table: str, libref: str = '',
                  dsopts: dict = None, opts: dict = None) -> str:
        """

        :param file: the OS filesystem path of the file to be created (exported from the SAS Data Set)
        :param table: the name of the SAS Data Set you want to export to a CSV file
        :param libref: the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs)

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a number - either string or int
            - first obs is a number - either string or int
            - format is a string or dictionary { var: format }
            - encoding is a string

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"' ,
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight' ,
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight'] ,
                              'obs'      :  10 ,
                              'firstobs' : '12' ,
                              'format'   : {'money': 'dollar10', 'time': 'tod5.'} ,
                              'encoding' : 'latin9'
                             }


        :param opts: a dictionary containing any of the following Proc Export options(delimiter, putnames)

            - delimiter is a single character
            - putnames is a bool  [True | False]

            .. code-block:: python

                             {'delimiter' : '~',
                              'putnames'  : True
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

    def upload(self, localfile: str, remotefile: str, overwrite: bool = True, permission: str = '', **kwargs):
        """
        This method uploads a local file to the SAS servers file system.

        :param localfile: path to the local file
        :param remotefile: path to remote file to create or overwrite. If a directory, the file will be
         created in that directory and be named the same as the local file's name
        :param overwrite: overwrite the output file if it exists?
        :param permission: permissions to set on the new file. See SAS Filename Statement Doc for syntax
        :return: dict with 2 keys {'Success' : bool, 'LOG' : str}
        """
        lastlog = len(self._io._log)
        if self.nosub:
            print("too complicated to show the code, read the source :), sorry.")
            return None
        else:
            log = self._io.upload(localfile, remotefile, overwrite, permission, **kwargs)

        self._lastlog = self._io._log[lastlog:]
        return log

    def download(self, localfile: str, remotefile: str, overwrite: bool = True, **kwargs):
        """
        This method downloads a remote file from the SAS servers file system.

        :param localfile: path to the local file to create or overwrite. If a directory, the file will be
         created in that directory and be named the same as the remote file's name
        :param remotefile: path to remote file
        :param overwrite: overwrite the output file if it exists?
        :return: dict with 2 keys {'Success' : bool, 'LOG' : str}
        """
        lastlog = len(self._io._log)
        if self.nosub:
            print("too complicated to show the code, read the source :), sorry.")
            return None
        else:
            log = self._io.download(localfile, remotefile, overwrite, **kwargs)

        self._lastlog = self._io._log[lastlog:]
        return log

    def df_char_lengths(self, df: 'pandas.DataFrame', encode_errors = None, char_lengths = None,
                        **kwargs) -> dict:
        """
        This is a utility method for df2sd, use to get the character columns lengths from a DataFrame to use to
        create a SAS data set. This can be called by the user and the returned dict can be passed in to df2sd via
        the char_lengths= option. For big DataFrames, this can take a long time, so this can be used to do it once,
        and then the dictionary returned can be provided to df2sd each time it's called to avoid recalculating this again.

        :param df: :class:`pandas.DataFrame` Pandas DataFrames to import to a SAS Data Set

        :param encode_errors: 'fail', 'replace' - default is to 'fail', other choice is to 'replace' \
                              invalid chars with the replacement char. This is only when calculating byte lengths, \
                              which is dependent upon the value of char_lengths=. When calculating char lengths, this \
                              parameter is ignored in this method (encoding is deferred to the data transfer step in df2sd).

        :param char_lengths: How to determine (and declare) lengths for CHAR variables in the output SAS data set \
                             SAS declares lenghts in bytes, not characters, so multibyte encodings require more bytes per character (BPC)

            - 'exact'  - the default if SAS is in a multibyte encoding. calculate the max number of bytes, in SAS encoding, \
                         required for the longest actual value. This is slowest but most accurate. For big data, this can \
                         take excessive time. If SAS is running in a single byte encoding then this defaults to '1' (see below), \
                         but you can override even that by explicitly specifying 'exact' when SAS is a single byte encoding.

            - 'safe'   - use char len of the longest values in the column, multiplied by max BPC of the SAS multibyte \
                         encoding. This is much faster, but could declare SAS Char variables longer than absolutely required \
                         for multibyte SAS encodings. If SAS is running in a single byte encoding then '1' (see below) is used. \
                         Norte that SAS has no fixed length multibyte encodings, so BPC is always between 1-2 or 1-4 for these. \
                         ASCII characters hex 00-7F use one btye in all of these, which other characters use more BPC; it's variable

            - [1|2|3|4]- this is 'safe' except the number (1 or 2 or 3 or 4) is the multiplier to use (BPC) instead of the \
                         default BPC of the SAS session encoding. For SAS single byte encodings, the valuse of 1 is the default \
                         used, since characters can only be 1 byte long so char len == byte len \
                         For UTF-8 SAS session, 4 is the BPC, so if you know you don't have many actual unicode characters \
                         you could specify 2 so the SAS column lengths are only twice the length as the longest value, instead \
                         of 4 times the, which would be much longer than actually needed. Or if you know you have no unicode \
                         chars (all the char data is actual only 1 byte), you could specify 1 since it only requires 1 BPC.

            - dictionary - a dictionary containing the names:lengths of a subset of the character columns. This will calculate \
                           the rest of them and return the full dictionary of columns. This way you can override some of them. \
                           Also, the column names are now case independent.

        :return: SASdata object
        """
        ret = {}
        if encode_errors is None:
           encode_errors = 'fail'

        if char_lengths and str(char_lengths) == 'exact':
           CnotB = False
        else:
           if char_lengths and str(char_lengths).strip() in ['1','2','3','4']:
              bpc = int(char_lengths)
           else:
              bpc = self.pyenc[0]

           CnotB = bpc == 1

        if type(char_lengths) is dict:
           chr_upper = {k.upper():v for k,v in char_lengths.items()}
           chr_keys  = chr_upper.keys()
        else:
           chr_upper = {}
           chr_keys  = chr_upper.keys()

        for name in df.columns:
           colname = str(name)
           col_up  = colname.upper()
           if col_up not in chr_keys:
              if df.dtypes[name].kind in ('O','S','U','V'):
                 if CnotB:  # calc max Chars not Bytes
                    col_l = df[name].astype(str).map(len).max() * bpc
                 else:
                    if encode_errors == 'fail':
                       try:
                          col_l = df[name].astype(str).apply(lambda x: len(x.encode(self._io.sascfg.encoding))).max()
                       except Exception as e:
                          msg  = "Transcoding error encountered.\n"
                          msg += "DataFrame contains characters that can't be transcoded into the SAS session encoding.\n"+str(e)
                          logger.error(msg)
                          return None
                    else:
                       col_l = df[name].astype(str).apply(lambda x: len(x.encode(self._io.sascfg.encoding, errors='replace'))).max()
                 if not col_l > 0:
                    col_l = 8
                 ret[colname] = col_l
           else:
              ret[colname] = chr_upper[col_up]
        return ret


    def df2sd(self, df: 'pandas.DataFrame', table: str = '_df', libref: str = '',
              results: str = '', keep_outer_quotes: bool = False,
                                 embedded_newlines: bool = True,
              LF: str = '\x01', CR: str = '\x02',
              colsep: str = '\x03', colrep: str = ' ',
              datetimes: dict={}, outfmts: dict={}, labels: dict={},
              outdsopts: dict={}, encode_errors = None, char_lengths = None,
              **kwargs) -> 'SASdata':
        """
        This is an alias for 'dataframe2sasdata'. Why type all that?

        Also note that DataFrame indexes (row label) are not transferred over as columns, as they aren't actualy in df.columns.
        You can simpley use df.reset_index() before this method and df.set_index() after to have the index be a column which
        is transferred over to the SAS data set. If you want to create a SAS index at the same time, use the outdsopts dict.

        :param df: :class:`pandas.DataFrame` Pandas DataFrame to import to a SAS Data Set
        :param table: the name of the SAS Data Set to create
        :param libref: the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
        :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives

        As of version 3.5.0, keep_outer_quotes is deprecated and embedded_newlines defaults to True

        :param keep_outer_quotes: the defualt is for SAS to strip outer quotes from delimitted data. This lets you keep them
        :param embedded_newlines: if any char columns have embedded CR or LF, set this to True to get them iported into the SAS data set

        colrep is new as of version 3.5.0

        :param LF: if embedded_newlines=True, the chacter to use for LF when transferring the data; defaults to hex(1)
        :param CR: if embedded_newlines=True, the chacter to use for CR when transferring the data; defaults to hex(2)
        :param colsep: the column separator character used for streaming the delimmited data to SAS defaults to hex(3)
        :param colrep: the char to convert to for any embedded colsep, LF, CR chars in the data; defaults to  ' '
        :param datetimes: dict with column names as keys and values of 'date' or 'time' to create SAS date or times instead of datetimes
        :param outfmts: dict with column names and SAS formats to assign to the new SAS data set
        :param labels: dict with column names and labels to assign to the new SAS data set
        :param outdsopts: a dictionary containing output data set options for the table being created \
                          for instance, compress=, encoding=, index=, outrep=, replace=, rename= ... \
                          the options will be generated simply as key=value, so if a value needs quotes or parentheses, provide them in the value

            .. code-block:: python

                             {'compress' : 'yes' ,
                              'encoding' : 'latin9' ,
                              'replace'  : 'NO' ,
                              'index'    : 'coli' ,
                              'rename'   : "(col1 = Column_one  col2 = 'Column Two'n)"
                             }

        :param encode_errors: 'fail', 'replace' or 'ignore' - default is to 'fail', other choice is to 'replace' \
                              invalid chars with the replacement char. 'ignore' doesn't try to transcode in python, so you \
                              get whatever happens in SAS based upon the data you send over. Note 'ignore' is only valid for IOM and HTTP
        :param char_lengths: How to determine (and declare) lengths for CHAR variables in the output SAS data set \
                             SAS declares lenghts in bytes, not characters, so multibyte encodings require more bytes per character (BPC)

            - 'exact'  - the default if SAS is in a multibyte encoding. calculate the max number of bytes, in SAS encoding, \
                         required for the longest actual value. This is slowest but most accurate. For big data, this can \
                         take excessive time. If SAS is running in a single byte encoding then this defaults to '1' (see below), \
                         but you can override even that by explicitly specifying 'exact' when SAS is a single byte encoding.

            - 'safe'   - use char len of the longest values in the column, multiplied by max BPC of the SAS multibyte \
                         encoding. This is much faster, but could declare SAS Char variables longer than absolutely required \
                         for multibyte SAS encodings. If SAS is running in a single byte encoding then '1' (see below) is used. \
                         Norte that SAS has no fixed length multibyte encodings, so BPC is always between 1-2 or 1-4 for these. \
                         ASCII characters hex 00-7F use one btye in all of these, which other characters use more BPC; it's variable

            - [1|2|3|4]- this is 'safe' except the number (1 or 2 or 3 or 4) is the multiplier to use (BPC) instead of the \
                         default BPC of the SAS session encoding. For SAS single byte encodings, the valuse of 1 is the default \
                         used, since characters can only be 1 byte long so char len == byte len \
                         For UTF-8 SAS session, 4 is the BPC, so if you know you don't have many actual unicode characters \
                         you could specify 2 so the SAS column lengths are only twice the length as the longest value, instead \
                         of 4 times the, which would be much longer than actually needed. Or if you know you have no unicode \
                         chars (all the char data is actual only 1 byte), you could specify 1 since it only requires 1 BPC.

            - dictionary - a dictionary containing the names:lengths of a the character columns you want to specify (all or some). \
                           This eliminates runmning the code to calculate the lengths (if you provide them all), and goes strainght
                           to transferring the data. If you only provide some columns, the others will be calculated still. \
                           This way you canoverride all or some of them. Also, the column names are now case independent.

        :return: SASdata object
        """
        return self.dataframe2sasdata(df, table, libref, results, keep_outer_quotes, embedded_newlines, LF, CR, colsep, colrep,
                                      datetimes, outfmts, labels, outdsopts, encode_errors, char_lengths, **kwargs)

    def dataframe2sasdata(self, df: 'pandas.DataFrame', table: str = '_df', libref: str = '',
                          results: str = '', keep_outer_quotes: bool = False,
                                             embedded_newlines: bool = True,
                          LF: str = '\x01', CR: str = '\x02',
                          colsep: str = '\x03', colrep: str = ' ',
                          datetimes: dict={}, outfmts: dict={}, labels: dict={},
                          outdsopts: dict={}, encode_errors = None, char_lengths = None, **kwargs) -> 'SASdata':
        """
        This method imports a Pandas DataFrame to a SAS Data Set, returning the SASdata object for the new Data Set.

        Also note that DataFrame indexes (row label) are not transferred over as columns, as they aren't actualy in df.columns.
        You can simpley use df.reset_index() before this method and df.set_index() after to have the index be a column which
        is transferred over to the SAS data set. If you want to create a SAS index at the same time, use the outdsopts dict.

        :param df: Pandas DataFrame to import to a SAS Data Set
        :param table: the name of the SAS Data Set to create
        :param libref: the libref for the SAS Data Set being created. Defaults to WORK, or USER if assigned
        :param results: format of results, SASsession.results is default, PANDAS, HTML or TEXT are the alternatives

        As of version 3.5.0, keep_outer_quotes is deprecated and embedded_newlines defaults to True

        :param keep_outer_quotes: the defualt is for SAS to strip outer quotes from delimitted data. This lets you keep them
        :param embedded_newlines: if any char columns have embedded CR or LF, set this to True to get them iported into the SAS data set

        colrep is new as of version 3.5.0

        :param LF: if embedded_newlines=True, the chacter to use for LF when transferring the data; defaults to hex(1)
        :param CR: if embedded_newlines=True, the chacter to use for CR when transferring the data; defaults to hex(2)
        :param colsep: the column separator character used for streaming the delimmited data to SAS defaults to hex(3)
        :param colrep: the char to convert to for any embedded colsep, LF, CR chars in the data; defaults to  ' '
        :param datetimes: dict with column names as keys and values of 'date' or 'time' to create SAS date or times instead of datetimes
        :param outfmts: dict with column names and SAS formats to assign to the new SAS data set
        :param labels: dict with column names and labels to assign to the new SAS data set
        :param outdsopts: a dictionary containing output data set options for the table being created \
                          for instance, compress=, encoding=, index=, outrep=, replace=, rename= ... \
                          the options will be generated simply as key=value, so if a value needs quotes or parentheses, provide them in the value

            .. code-block:: python

                             {'compress' : 'yes' ,
                              'encoding' : 'latin9' ,
                              'replace'  : 'NO' ,
                              'index'    : 'coli' ,
                              'rename'   : "(col1 = Column_one  col2 = 'Column Two'n)"
                             }

        :param encode_errors: 'fail', 'replace' or 'ignore' - default is to 'fail', other choice is to 'replace' \
                              invalid chars with the replacement char. 'ignore' doesn't try to transcode in python, so you \
                              get whatever happens in SAS based upon the data you send over. Note 'ignore' is only valid for IOM and HTTP
        :param char_lengths: How to determine (and declare) lengths for CHAR variables in the output SAS data set \
                             SAS declares lenghts in bytes, not characters, so multibyte encodings require more bytes per character (BPC)

            - 'exact'  - the default if SAS is in a multibyte encoding. calculate the max number of bytes, in SAS encoding, \
                         required for the longest actual value. This is slowest but most accurate. For big data, this can \
                         take excessive time. If SAS is running in a single byte encoding then this defaults to '1' (see below), \
                         but you can override even that by explicitly specifying 'exact' when SAS is a single byte encoding.

            - 'safe'   - use char len of the longest values in the column, multiplied by max BPC of the SAS multibyte \
                         encoding. This is much faster, but could declare SAS Char variables longer than absolutely required \
                         for multibyte SAS encodings. If SAS is running in a single byte encoding then '1' (see below) is used. \
                         Norte that SAS has no fixed length multibyte encodings, so BPC is always between 1-2 or 1-4 for these. \
                         ASCII characters hex 00-7F use one btye in all of these, which other characters use more BPC; it's variable

            - [1|2|3|4]- this is 'safe' except the number (1 or 2 or 3 or 4) is the multiplier to use (BPC) instead of the \
                         default BPC of the SAS session encoding. For SAS single byte encodings, the valuse of 1 is the default \
                         used, since characters can only be 1 byte long so char len == byte len \
                         For UTF-8 SAS session, 4 is the BPC, so if you know you don't have many actual unicode characters \
                         you could specify 2 so the SAS column lengths are only twice the length as the longest value, instead \
                         of 4 times the, which would be much longer than actually needed. Or if you know you have no unicode \
                         chars (all the char data is actual only 1 byte), you could specify 1 since it only requires 1 BPC.

            - dictionary - a dictionary containing the names:lengths of all of the character columns. This eliminates \
                           running the code to calculate the lengths, and goes strainght to transferring the data \


        :return: SASdata object
        """
        lastlog = len(self._io._log)
        if self.sascfg.pandas:
           raise type(self.sascfg.pandas)(self.sascfg.pandas.msg)

        if libref != '':
           if libref.upper() not in self.assigned_librefs():
              logger.error("The libref specified is not assigned in this SAS Session.")
              return None

        # support oringinal implementation of outencoding - should have done it as a ds option to begin with
        outencoding = kwargs.pop('outencoding', None)
        if outencoding:
           outdsopts['encoding'] = outencoding

        if results == '':
           results = self.results
        if self.nosub:
           print("too complicated to show the code, read the source :), sorry.")
           return None

        ncols = len(df.columns)

        if self.sascfg.mode != 'COM':
           if char_lengths and str(char_lengths) == 'exact':
              CnotB = False
           else:
              if char_lengths and str(char_lengths).strip() in ['1','2','3','4']:
                 bpc = int(char_lengths)
              else:
                 bpc = self.pyenc[0]
              CnotB = bpc == 1

           if type(char_lengths) is not dict or len(char_lengths) < len(df.columns):
              charlens = self.df_char_lengths(df, encode_errors, char_lengths)
           else:
              charlens = char_lengths

           #lrecl = sum(charlens.values()) + (ncols - len(charlens)) * 32 + ncols + 1
           #print("guess lrel = {}".format(str(lrecl)))

           rc = self._io.dataframe2sasdata(df, table, libref, keep_outer_quotes, embedded_newlines, LF, CR, colsep, colrep,
                                           datetimes, outfmts, labels, outdsopts, encode_errors, charlens, CnotB=CnotB, **kwargs)

        else:
           rc = self._io.dataframe2sasdata(df, table, libref, keep_outer_quotes, embedded_newlines, LF, CR, colsep, colrep,
                                           datetimes, outfmts, labels, outdsopts, encode_errors, char_lengths, **kwargs)

        if rc is None:
           if self.exist(table, libref):
              dsopts = {}
              if outencoding:
                 dsopts['encoding'] = outencoding
              sd = SASdata(self, libref, table, results, dsopts)
           else:
              sd = None
        else:
           sd = None

        self._lastlog = self._io._log[lastlog:]
        return sd

    def sd2df(self, table: str, libref: str = '', dsopts: dict = None,
              method: str = 'MEMORY', **kwargs) -> 'pandas.DataFrame':
        """
        This is an alias for 'sasdata2dataframe'. Why type all that?

        :param table: the name of the SAS Data Set you want to export to a Pandas DataFrame
        :param libref: the libref for the SAS Data Set.
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a number - either string or int
            - first obs is a number - either string or int
            - format is a string or dictionary { var: format }
            - encoding is a string

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"' ,
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight' ,
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight'] ,
                              'obs'      :  10 ,
                              'firstobs' : '12' ,
                              'format'   : {'money': 'dollar10', 'time': 'tod5.'} ,
                              'encoding' : 'latin9'
                             }


        :param method: defaults to MEMORY; As of V3.7.0 all 3 of these now stream directly into read_csv() with no disk I/O\
                       and have much improved performance. MEM, the default, is now as fast as the others.

           - MEMORY the original method. Streams the data over and builds the DataFrame on the fly in memory
           - CSV    uses an intermediary Proc Export csv file and pandas read_csv() to import it; faster for large data
           - DISK   uses the original (MEMORY) method, but persists to disk and uses pandas read to import. \
                    this has better support than CSV for embedded delimiters (commas), nulls, CR/LF that CSV \
                    has problems with


        For the CSV and DISK methods, the following 2 parameters are also available As of V3.7.0 all 3 of these now stream \
        directly into read_csv() with no disk I/O and have much improved performance. MEM, the default, is now as fast as the others.

        :param tempfile: [deprecated] [optional] an OS path for a file to use for the local file; default it a temporary file that's cleaned up
        :param tempkeep: [deprecated] if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it

        For the MEMORY and DISK methods, the following 4 parameters are also available, depending upon access method

        :param rowsep: the row separator character to use; defaults to hex(1)
        :param colsep: the column separator character to use; defaults to hex(2)
        :param rowrep: the char to convert to for any embedded rowsep chars, defaults to  ' '
        :param colrep: the char to convert to for any embedded colsep chars, defaults to  ' '


        :param kwargs: a dictionary. These vary per access method, and are generally NOT needed.
                       They are either access method specific parms or specific pandas parms.
                       See the specific sasdata2dataframe* method in the access method for valid possibilities.

        :return: Pandas DataFrame
        """
        dsopts = dsopts if dsopts is not None else {}
        return self.sasdata2dataframe(table, libref, dsopts, method, **kwargs)

    def sd2df_CSV(self, table: str, libref: str = '', dsopts: dict = None, tempfile: str = None,
                  tempkeep: bool = False, opts: dict = None, **kwargs) -> 'pandas.DataFrame':
        """
        This is an alias for 'sasdata2dataframe' specifying method='CSV'. Why type all that?

        :param table: the name of the SAS Data Set you want to export to a Pandas DataFrame
        :param libref: the libref for the SAS Data Set.
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a number - either string or int
            - first obs is a number - either string or int
            - format is a string or dictionary { var: format }
            - encoding is a string

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"' ,
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight' ,
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight'] ,
                              'obs'      :  10 ,
                              'firstobs' : '12' ,
                              'format'   : {'money': 'dollar10', 'time': 'tod5.'} ,
                              'encoding' : 'latin9'
                             }


        :param tempfile: [deprecated except for Local IOM] [optional] an OS path for a file to use for the local CSV file; default it a temporary file that's cleaned up
        :param tempkeep: [deprecated except for Local IOM] if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it

        :param opts: a dictionary containing any of the following Proc Export options(delimiter, putnames)

            - delimiter is a single character
            - putnames is a bool  [True | False]

            .. code-block:: python

                             {'delimiter' : '~',
                              'putnames'  : True
                             }

        :param kwargs: a dictionary. These vary per access method, and are generally NOT needed.
                       They are either access method specific parms or specific pandas parms.
                       See the specific sasdata2dataframe* method in the access method for valid possibilities.

        :return: Pandas DataFrame
        """
        dsopts = dsopts if dsopts is not None else {}
        opts   =   opts if   opts is not None else {}
        return self.sasdata2dataframe(table, libref, dsopts, method='CSV', tempfile=tempfile, tempkeep=tempkeep,
                                      opts=opts, **kwargs)

    def sd2df_DISK(self, table: str, libref: str = '', dsopts: dict = None, tempfile: str = None,
                  tempkeep: bool = False, rowsep: str = '\x01', colsep: str = '\x02',
                  rowrep: str = ' ', colrep: str = ' ', **kwargs) -> 'pandas.DataFrame':
        """
        This is an alias for 'sasdata2dataframe' specifying method='DISK'. Why type all that?

        :param table: the name of the SAS Data Set you want to export to a Pandas DataFrame
        :param libref: the libref for the SAS Data Set.
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a number - either string or int
            - first obs is a number - either string or int
            - format is a string or dictionary { var: format }
            - encoding is a string

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"' ,
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight' ,
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight'] ,
                              'obs'      :  10 ,
                              'firstobs' : '12' ,
                              'format'   : {'money': 'dollar10', 'time': 'tod5.'} ,
                              'encoding' : 'latin9'
                             }

        :param tempfile: [deprecated] [optional] an OS path for a file to use for the local file; default it a temporary file that's cleaned up
        :param tempkeep: [deprecated] if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it

        :param rowsep: the row separator character to use; defaults to hex(1)
        :param colsep: the column separator character to use; defaults to hex(2)
        :param rowrep: the char to convert to for any embedded rowsep chars, defaults to  ' '
        :param colrep: the char to convert to for any embedded colsep chars, defaults to  ' '


        :param kwargs: a dictionary. These vary per access method, and are generally NOT needed.
                       They are either access method specific parms or specific pandas parms.
                       See the specific sasdata2dataframe* method in the access method for valid possibilities.

        :return: Pandas DataFrame
        """
        dsopts = dsopts if dsopts is not None else {}
        return self.sasdata2dataframe(table, libref, dsopts, method='DISK', tempfile=tempfile, tempkeep=tempkeep,
                                      rowsep=rowsep, colsep=colsep, rowrep=rowrep, colrep=colrep, **kwargs)

    def sasdata2dataframe(self, table: str, libref: str = '', dsopts: dict = None,
                          method: str = 'MEMORY', **kwargs) -> 'pandas.DataFrame':
        """
        This method exports the SAS Data Set to a Pandas DataFrame, returning the DataFrame object.

        :param table: the name of the SAS Data Set you want to export to a Pandas DataFrame
        :param libref: the libref for the SAS Data Set.
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a number - either string or int
            - first obs is a number - either string or int
            - format is a string or dictionary { var: format }
            - encoding is a string

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"' ,
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight' ,
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight'] ,
                              'obs'      :  10 ,
                              'firstobs' : '12' ,
                              'format'   : {'money': 'dollar10', 'time': 'tod5.'} ,
                              'encoding' : 'latin9'
                             }

        :param method: defaults to MEMORY; As of V3.7.0 all 3 of these now stream directly into read_csv() with no disk I/O\
                       and have much improved performance. MEM, the default, is now as fast as the others.

           - MEMORY the original method. Streams the data over and builds the DataFrame on the fly in memory
           - CSV    uses an intermediary Proc Export csv file and pandas read_csv() to import it; faster for large data
           - DISK   uses the original (MEMORY) method, but persists to disk and uses pandas read to import.  \
                    this has better support than CSV for embedded delimiters (commas), nulls, CR/LF that CSV \
                    has problems with


        For the CSV and DISK methods, the following 2 parameters are also available As of V3.7.0 all 3 of these now stream \
        directly into read_csv() with no disk I/O and have much improved performance. MEM, the default, is now as fast as the others.

        :param tempfile: [deprecated except for Local IOM] [optional] an OS path for a file to use for the local file; default it a temporary file that's cleaned up
        :param tempkeep: [deprecated except for Local IOM] if you specify your own file to use with tempfile=, this controls whether it's cleaned up after using it

        For the MEMORY and DISK methods, the following 4 parameters are also available, depending upon access method

        :param rowsep: the row separator character to use; defaults to hex(1)
        :param colsep: the column separator character to use; defaults to hex(2)
        :param rowrep: the char to convert to for any embedded rowsep chars, defaults to  ' '
        :param colrep: the char to convert to for any embedded colsep chars, defaults to  ' '


        :param kwargs: a dictionary. These vary per access method, and are generally NOT needed.
                       They are either access method specific parms or specific pandas parms.
                       See the specific sasdata2dataframe* method in the access method for valid possibilities.

        :return: Pandas DataFrame
        """
        lastlog = len(self._io._log)
        if self.sascfg.pandas:
           raise type(self.sascfg.pandas)(self.sascfg.pandas.msg)

        if method.lower() not in ['memory', 'csv', 'disk']:
            logger.error("The specified method is not valid. Supported methods are MEMORY, CSV and DISK")
            return None

        dsopts = dsopts if dsopts is not None else {}
        if self.exist(table, libref) == 0:
            logger.error('The SAS Data Set ' + libref + '.' + table + ' does not exist')
            if self.sascfg.bcv < 3007009:
               return None
            else:
               raise FileNotFoundError('The SAS Data Set ' + libref + '.' + table + ' does not exist')

        if self.nosub:
            print("too complicated to show the code, read the source :), sorry.")
            df = None
        else:
            df = self._io.sasdata2dataframe(table, libref, dsopts, method=method, **kwargs)

        self._lastlog = self._io._log[lastlog:]
        return df

    def _dsopts(self, dsopts):
        """
        :param dsopts: a dictionary containing any of the following SAS data set options(where, drop, keep, obs, firstobs):

            - where is a string or list of strings
            - keep are strings or list of strings.
            - drop are strings or list of strings.
            - obs is a number - either string or int
            - first obs is a number - either string or int
            - format is a string or dictionary { var: format }
            - encoding is a string

            .. code-block:: python

                             {'where'    : 'msrp < 20000 and make = "Ford"' ,
                              'keep'     : 'msrp enginesize Cylinders Horsepower Weight' ,
                              'drop'     : ['msrp', 'enginesize', 'Cylinders', 'Horsepower', 'Weight'] ,
                              'obs'      :  10 ,
                              'firstobs' : '12' ,
                              'format'   : {'money': 'dollar10', 'time': 'tod5.'} ,
                              'encoding' : 'latin9'
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

                    elif key == 'encoding':
                        opts += 'encoding="' + str(dsopts[key]) + '" '

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
                    else:
                        opts += key+'='+str(dsopts[key]) + ' '

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
            - guessingrows is a number or the string 'MAX'

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

    def symput(self, name: str, value, quoting='NRBQUOTE'):
        """
        :param name:  name of the macro varable to set
        :param value: python variable, that can be resolved to a string, to use for the value to assign to the macro variable
        :param quoting: None for 'asis' macro definition. Or any of the special SAS quoting function like \
                        BQUOTE, NRBQUOTE, QUOTE, NRQUOTE, STR, NRSTR, SUPERQ, ...  default is NRBQUOTE

        """
        if quoting:
           ll = self._io.submit("%let " + name + "=%" + quoting.upper() + "(" + str(value) + ");\n", results='text')
        else:
           ll = self._io.submit("%let " + name + "=" + str(value) + ";\n", results='text')

    def symget(self, name: str, outtype=None):
        """
        :param name:    [required] name of the macro varable to get
        :param outtype: [optional] desired output type of the python variable; valid types are [int, float, str] \
                        provide an object of the type [1, 1.0, ' '] or a string of 'int', 'float' or 'str'

        """
        ll = self._io.submit("%put " + name + "BEGIN=&" + name + " "+ name+"END=;\n", results='text')
        l2 = ll['LOG'].rpartition(name + "BEGIN=")[2].rpartition(name+"END=")[0].strip().replace('\n','')

        if outtype is not None:
           if   outtype == 'int':
              outtype = 1
           elif outtype == 'float':
              outtype = 1.0

        if outtype is not None and type(outtype) not in [int, float, str]:
           logger.warning("invalid type specified. supported are [int, float, str], will return default type")
           outtype=None

        if outtype is not None:
           if   type(outtype) == int:
              var = int(l2)
           elif type(outtype) == float:
              var = float(l2)
           elif type(outtype) == str:
              var = l2
        else:
           try:
              var = int(l2)
           except:
              try:
                 var = float(l2)
              except:
                 var = l2

        return var

    def symexist(self, name: str):
        """
        :param name:    [required] name of the macro varable to check for existence

        :return: bool
        """
        ll = self._io.submit("%put " + name + "BEGIN=%symexist(" + name + ") "+ name+"END=;\n")
        l2 = ll['LOG'].rpartition(name + "BEGIN=")[2].rpartition(name+"END=")[0].strip().replace('\n','')

        var = int(l2)

        return bool(var)

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

    def assigned_librefs(self) -> list:
        """
        This method returns the list of currently assigned librefs
        """

        code = """
        data _null_; retain libref; retain cobs 1;
           set sashelp.vlibnam end=last;
           if cobs EQ 1 then
              put "LIBREFSSTART=";
           cobs = 2;
           if libref NE libname then
              put  %upcase("lib=") libname  %upcase('libEND=');
           libref = libname;
           if last then
              put "LIBREFSEND=";
        run;
        """

        if self.nosub:
            print(code)
            return None
        else:
           ll = self._io.submit(code, results='text')

        librefs = []
        log = ll['LOG'].rpartition('LIBREFSEND=')[0].rpartition('LIBREFSSTART=')

        for i in range(log[2].count('LIB=')):
           log = log[2].partition('LIB=')[2].partition(' LIBEND=')
           librefs.append(log[0])

        return librefs


    def dirlist(self, path) -> list:
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
               put 'MEMCOUNT=' memcount 'MEMCOUNTEND=';
               do while (memcount > 0);
                  name = dread(did, memcount);
                  memcount = memcount - 1;

                  qname = spd || '"""+self.hostsep+"""' || name;

                  rc = filename('saspydq', qname);
                  dq = dopen('saspydq');
                  if dq NE 0 then
                     do;
                        dname = strip(name) || '"""+self.hostsep+"""';
                        put %upcase('DIR_file=') dname %upcase('fileEND=');
                        rc = dclose(dq);
                     end;
                  else
                     put %upcase('file=') name %upcase('fileEND=');
               end;

            put 'MEMEND=';
            rc = dclose(did);
            end;
         else
            do;
               put 'MEMCOUNT=0 MEMCOUNTEND=';
               put 'MEMEND=';
           end;

         rc = filename('saspydq');
         rc = filename('saspydir');
        run;
        """

        if self.nosub:
            print(code)
            return None
        else:
           ll = self._io.submit(code, results='text')

        dirlist = []

        l2 = ll['LOG'].rpartition("MEMCOUNT=")[2].partition(" MEMCOUNTEND=")
        memcount = int(l2[0])

        dirlist = []
        log = ll['LOG'].rpartition('MEMEND=')[0].rpartition('MEMCOUNTEND=')

        for i in range(log[2].count('FILE=')):
           log = log[2].partition('FILE=')[2].partition(' FILEEND=')
           dirlist.append(log[0])

        if memcount != len(dirlist):
            logger.warning("Some problem parsing list. Should be "+str(memcount)+" entries but got "+str(len(dirlist))+" instead.")

        return dirlist


    def list_tables(self, libref: str='work', results: str = 'list') -> list:
        """
        This method returns a list of tuples containing MEMNAME, MEMTYPE of members in the library of memtype data or view

        If you would like a Pandas DataFrame returned instead of a list, specify results='pandas'
        """
        lastlog = len(self._io._log)

        if not self.nosub:
           ll = self._io.submit("%put LIBREF_EXISTS=%sysfunc(libref("+libref+")) LIB_EXT_END=;", results='text')
           try:
              exists = int(ll['LOG'].rpartition('LIBREF_EXISTS=')[2].rpartition('LIB_EXT_END=')[0])
           except:
              exists = 1

           if exists != 0:
              logger.error('Libref provided is not assigned')
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

        if self.nosub:
            print(code)
            return None
        else:
           ll = self._io.submit(code, results='text')

        if results != 'list':
           res = self.sd2df('_saspy_lib_list', 'work')
           ll = self._io.submit("proc delete data=work._saspy_lib_list;run;", results='text')
           self._lastlog = self._io._log[lastlog:]
           return res

        code = """
        data _null_;
           set work._saspy_lib_list end=last curobs=first;
           if first EQ 1 then
              put 'MEMSTART=';
           put %upcase('memNAME=') memname %upcase('memNAMEEND=');
           put %upcase('memTYPE=') memtype %upcase('memTYPEEND=');
           if last then
              put 'MEMEND=';
        run;
        proc delete data=work._saspy_lib_list;run;
        """

        ll  = self._io.submit(code, results='text')

        log = ll['LOG'].rpartition('MEMEND=')[0].rpartition('MEMSTART=')

        tablist = []
        for i in range(log[2].count('MEMNAME=')):
           log = log[2].partition('MEMNAME=')[2].partition(' MEMNAMEEND=')
           key = log[0]
           log = log[2].partition('MEMTYPE=')[2].partition(' MEMTYPEEND=')
           val = log[0]
           tablist.append(tuple((key, val)))

        self._lastlog = self._io._log[lastlog:]
        return tablist


    def file_info(self, filepath, results: str = 'dict', fileref: str = '_spfinfo', quiet: bool = False) -> dict:
        """
        This method returns a dictionary containing the file attributes for the file name provided

        If you would like a Pandas DataFrame returned instead of a dictionary, specify results='pandas'
        """
        lastlog = len(self._io._log)

        if not self.nosub:
           code  = "filename "+fileref+" '"+filepath+"';\n"
           code += "%put FILEREF_EXISTS=%sysfunc(fexist("+fileref+")) FILE_EXTEND=;"

           ll = self._io.submit(code, results='text')
           try:
              exists = int(ll['LOG'].rpartition('FILEREF_EXISTS=')[2].rpartition(' FILE_EXTEND=')[0])
           except:
              exists = 0

           if exists != 1:
              if not quiet:
                 logger.error('The filepath provided does not exist')
              ll = self._io.submit("filename "+fileref+" clear;", results='text')
              return None

        if results != 'dict':
           code="""
           proc delete data=work._SASPY_FILE_INFO;run;
           data work._SASPY_FILE_INFO;
              length infoname $256 infoval $4096;
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

           if self.nosub:
               print(code)
               return None
           else:
              ll  = self._io.submit(code, results='text')

           res = self.sd2df('_SASPY_FILE_INFO', 'work')
           ll  = self._io.submit("proc delete data=work._SASPY_FILE_INFO;run;", results='text')

           self._lastlog = self._io._log[lastlog:]
           return res


        code="""options nosource;
        data _null_;
           length infoname $256 infoval $4096;
        """
        if self.sascfg.mode in ['STDIO', 'SSH', '']:
           code +=" file STDERR; "
        code +="""
           drop rc fid infonum i close;
           put 'INFOSTART=';
           fid=fopen('filerefx');
           if fid then
              do;
                 infonum=foptnum(fid);
                 do i=1 to infonum;
                    infoname=foptname(fid, i);
                    infoval=finfo(fid, infoname);
                    put %upcase('infoNAME=') infoname %upcase('infoNAMEEND=');
                    put %upcase('infoVAL=') infoval %upcase('infoVALEND=');
                 end;
              end;
           put 'INFOEND=';
           close=fclose(fid);
           rc = filename('filerefx');
        run; options source;
        """.replace('filerefx', fileref)

        if self.nosub:
            print(code)
            return None
        else:
           ll  = self._io.submit(code, results='text')

        vi = len(ll['LOG'].rpartition('INFOEND=')[0].rpartition('\n')[2])

        res = {}
        log = ll['LOG'].rpartition('INFOEND=')[0].rpartition('INFOSTART=')

        if vi > 0:
           for i in range(log[2].count('INFONAME=')):
              log = log[2].partition('INFONAME=')[2].partition(' INFONAMEEND=')
              key = log[0]
              log = log[2].partition('INFOVAL=')[2].partition('INFOVALEND=')

              vx = log[0].split('\n')
              val = vx[0]
              for x in vx[1:]:
                 val += x[vi:]
              res[key] = val.strip()
        else:
           for i in range(log[2].count('INFONAME=')):
              log = log[2].partition('INFONAME=')[2].partition(' INFONAMEEND=')
              key = log[0]
              log = log[2].partition('INFOVAL=')[2].partition('INFOVALEND=')
              val = log[0].replace('\n', '').strip()
              res[key] = val

        self._lastlog = self._io._log[lastlog:]
        return res

    def file_delete(self, filepath, fileref: str = '_spfinfo', quiet: bool = False) -> dict:
        """
        This method deletes an external file or directory on the SAS server side

        :param filepath: path to the remote file to delete
        :param fileref: fileref to use on the generated filename stmt
        :param quiet: print any messages or not

        :return: dict with 2 keys {'Success' : bool, 'LOG' : str}
        """
        lastlog = len(self._io._log)

        code  = "data _null_;\n rc=filename('"+fileref+"', '"+filepath+"');\n"
        code += " if rc = 0 and fexist('"+fileref+"') then do;\n"
        code += "    rc = fdelete('"+fileref+"');\n"
        code += "    put 'FILEREF_EXISTS= ' rc 'FILE_EXTEND=';\n"
        code += " end; else do;\n"
        code += "    put 'FILEREF_EXISTS= -1 FILE_EXTEND=';\n"
        code += " end; run;\n"

        if self.nosub:
            print(code)
            return None
        else:
           ll = self._io.submit(code, results='text')

        try:
           exists = int(ll['LOG'].rpartition('FILEREF_EXISTS=')[2].rpartition(' FILE_EXTEND=')[0])
        except:
           exists = 1

        if exists != 0:
           if not quiet:
              logger.error('The filepath provided does not exist')

        self._lastlog = self._io._log[lastlog:]
        return {'Success' : not bool(exists), 'LOG' : ll['LOG']}

    def file_copy(self, source_path, dest_path, fileref: str = '_spfinf', quiet: bool = False) -> dict:
        """
        This method copies one external file to another on the SAS server side

        :param source_path: path to the remote source file to copy
        :param dest_path: path for the remote file write to
        :param fileref: fileref (first 7 chars of one) to use on the two generated filename stmts
        :param quiet: print any messages or not

        :return: dict with 2 keys {'Success' : bool, 'LOG' : str}
        """
        lastlog = len(self._io._log)

        code  = "filename {} '{}' recfm=n;\n".format(fileref[:7]+'s', source_path)
        code += "filename {} '{}' recfm=n;\n".format(fileref[:7]+'d', dest_path)
        code += "data _null_;\n"
        code += "   rc = fcopy('{}', '{}');\n".format(fileref[:7]+'s',fileref[:7]+'d')
        code += "   put 'FILEREF_EXISTS= ' rc 'FILE_EXTEND=';\n"
        code += "run;\n"
        code += "filename {} clear;\n".format(fileref[:7]+'s')
        code += "filename {} clear;\n".format(fileref[:7]+'d')

        if self.nosub:
            print(code)
            return None
        else:
           ll = self._io.submit(code, results='text')

        try:
           exists = int(ll['LOG'].rpartition('FILEREF_EXISTS=')[2].rpartition(' FILE_EXTEND=')[0])
        except:
           exists = 1

        if exists != 0:
           if not quiet:
              logger.warning('Non Zero return code. Check the SASLOG for messages')

        self._lastlog = self._io._log[lastlog:]
        return {'Success' : not bool(exists), 'LOG' : ll['LOG']}

    def cat(self, path) -> str:
       """
       Like Linux 'cat' - open and print the contents of a file
       """
       fd = open(path, 'r')
       dat = fd.read()
       fd.close()
       print(dat)


    def sil(self, life=None, rate=None, amount=None, payment=None, out: object = None, out_summary: object = None):
       """
       Alias for simple_interest_loan
       """
       return self.simple_interest_loan(life, rate, amount, payment, out, out_summary)

    def simple_interest_loan(self, life=None, rate=None, amount=None, payment=None, out: object = None, out_summary: object = None):
       """
       Calculate the amortization schedule of a simple interest load given 3 of the 4 variables
       You must specify 3 of the for variables, to solve for the 4th.

       :param life:    length of loan in months
       :param rate:    interest rate as a decimal percent: .03 is 3% apr
       :param amount:  amount of loan
       :param payment: monthly payment amount
       :return: SAS Lst showing the amortization schule calculated for the missing variable
       """
       vars = 0

       code  = "proc mortgage"
       if life is not None:
          code += " life="+str(life)
          vars += 1
       if rate is not None:
          code += " rate="+str(rate)
          vars += 1
       if amount is not None:
          code += " amount="+str(amount)
          vars += 1
       if payment is not None:
          code += " payment="+str(payment)
          vars += 1
       if out is not None:
          code += " out="+out.libref + ".'" + out.table.replace("'", "''") +"'n " + out._dsopts()
       if out_summary is not None:
          code += " outsum="+out_summary.libref + ".'" + out_summary.table.replace("'", "''")  +"'n " + out_summary._dsopts()
       code += "; run;"

       if vars != 3:
          logger.error("Must suply 3 of the 4 variables. Only "+str(vars)+" variables provided.")
          return None

       if self.nosub:
          print(code)
       else:
          if self.results.lower() == 'html':
             ll = self._io.submit(code, "html")
             if not self.batch:
                self._render_html_or_log(ll)
             else:
                return ll
          else:
             ll = self._io.submit(code, "text")
             if self.batch:
                return ll
             else:
                print(ll['LST'])

    def validvarname(self, df: 'pandas.DataFrame', version: str = "v7" )  -> 'pandas.DataFrame':
        """
        Creates a copy of a DataFrame with SAS compatible column names. The version= parameter allows
        you to choose the compatability setting to use.

        :param df:      a Pandas DataFrame whose column names you wish to make SAS compatible.
        :param version: select the validvarname version using SAS convention.

            - V7: ensures the following conditions are met:
                - up to 32 mixed case alphanumeric characters are allowed.
                - names must begin with alphabetic characters or an underscore.
                - non SAS characters are mapped to underscores.
                - any column name that is not unique when normalized is made unique by appending a counter (0,1,2,...) to the name.
            - V6:     like V7, but column names truncated to 8 characters.
            - upcase: like V7, but columns names will be uppercase.
            - any:    any characters are valid, but column names truncated to 32 characters.

        :return: a Pandas DataFrame whose column names are SAS compatible according to the selected version.
        """
        if version.lower() not in ['v6', 'v7', 'upcase', 'any']:
           logger.warning("The specified version is not valid. Using the default: 'V7'")
           version = 'v7'

        max_length = 8 if version.lower() == 'v6' else 32

        names = {}

        # normalize variable names
        for col_name in df.columns:
            new_name = col_name[:max_length]

            if version.lower() != 'any':
                new_name = re.sub(r'[^\d\w]+', r'_'  , new_name)
                new_name = re.sub(r'^(\d+)',   r'_\1', new_name)

            if version.lower() == 'upcase':
                new_name = new_name.upper()

            names[col_name] = new_name

        # serialize duplicates in normalized variable names
        for col_name in df.columns:
            duplicate_keys = [key for key in names.keys()
                                if names[key].upper() == names[col_name].upper() ]
            duplicate_count = len(duplicate_keys)-1
            if duplicate_count>0:
                count = 0
                padding = len(str(duplicate_count))
                for val in df.columns:
                    if val in duplicate_keys:
                        names[val] =  "{}{}".format(names[val][:max_length-padding], count)
                        count += 1

        return df.rename(columns=names)


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

sas_encoding_mapping = {
'arabic':      [1, 'iso8859_6', 'iso-8859-6', 'arabic'],
'big5':        [2, 'big5', 'big5-tw', 'csbig5'],
'cyrillic':    [1, 'iso8859_5', 'iso-8859-5', 'cyrillic'],
'ebcdic037':   [1, 'cp037', 'ibm037', 'ibm039'],
'ebcdic273':   [1, 'cp273', '273', 'ibm273', 'csibm273'],
'ebcdic500':   [1, 'cp500', 'ebcdic-cp-be', 'ebcdic-cp-ch', 'ibm500'],
'euc-cn':      [2, 'gb2312', 'chinese', 'csiso58gb231280', 'euc-cn', 'euccn', 'eucgb2312-cn', 'gb2312-1980', 'gb2312-80', 'iso-ir-58'],
'euc-jp':      [4, 'euc_jis_2004', 'jisx0213', 'eucjis2004'],
'euc-kr':      [4, 'euc_kr', 'euckr', 'korean', 'ksc5601', 'ks_c-5601', 'ks_c-5601-1987', 'ksx1001', 'ks_x-1001'],
'greek':       [1, 'iso8859_7', 'iso-8859-7', 'greek', 'greek8'],
'hebrew':      [1, 'iso8859_8', 'iso-8859-8', 'hebrew'],
'ibm-949':     [1, 'cp949', '949', 'ms949', 'uhc'],
'kz1048':      [1, 'kz1048', 'kz_1048', 'strk1048_2002', 'rk1048'],
'latin10':     [1, 'iso8859_16', 'iso-8859-16', 'latin10', 'l10'],
'latin1':      [1, 'latin_1', 'iso-8859-1', 'iso8859-1', '8859', 'cp819', 'latin', 'latin1', 'l1'],
'latin2':      [1, 'iso8859_2', 'iso-8859-2', 'latin2', 'l2'],
'latin3':      [1, 'iso8859_3', 'iso-8859-3', 'latin3', 'l3'],
'latin4':      [1, 'iso8859_4', 'iso-8859-4', 'latin4', 'l4'],
'latin5':      [1, 'iso8859_9', 'iso-8859-9', 'latin5', 'l5'],
'latin6':      [1, 'iso8859_10', 'iso-8859-10', 'latin6', 'l6'],
'latin7':      [1, 'iso8859_13', 'iso-8859-13', 'latin7', 'l7'],
'latin8':      [1, 'iso8859_14', 'iso-8859-14', 'latin8', 'l8'],
'latin9':      [1, 'iso8859_15', 'iso-8859-15', 'latin9', 'l9'],
'ms-932':      [2, 'cp932', '932', 'ms932', 'mskanji', 'ms-kanji'],
'msdos737':    [1, 'cp737'],
'msdos775':    [1, 'cp775', 'ibm775'],
'open_ed-1026':[1, 'cp1026', 'ibm1026'],
'open_ed-1047':[1, 'cp1047'],              # Though this isn't available in base python, it's 3rd party
'open_ed-1140':[1, 'cp1140', 'ibm1140'],
'open_ed-424': [1, 'cp424', 'ebcdic-cp-he', 'ibm424'],
'open_ed-875': [1, 'cp875'],
'pcoem437':    [1, 'cp437', '437', 'ibm437'],
'pcoem850':    [1, 'cp850', '850', 'ibm850'],
'pcoem852':    [1, 'cp852', '852', 'ibm852'],
'pcoem857':    [1, 'cp857', '857', 'ibm857'],
'pcoem858':    [1, 'cp858', '858', 'ibm858'],
'pcoem860':    [1, 'cp860', '860', 'ibm860'],
'pcoem862':    [1, 'cp862', '862', 'ibm862'],
'pcoem863':    [1, 'cp863'],
'pcoem864':    [1, 'cp864', 'ibm864'],
'pcoem865':    [1, 'cp865', '865', 'ibm865'],
'pcoem866':    [1, 'cp866', '866', 'ibm866'],
'pcoem869':    [1, 'cp869', '869', 'cp-gr', 'ibm869'],
'pcoem874':    [1, 'cp874'],
'shift-jis':   [2, 'shift_jis', 'csshiftjis', 'shiftjis', 'sjis', 's_jis'],
'thai':        [1, 'iso8859_11', 'so-8859-11', 'thai'],
'us-ascii':    [1, 'ascii', '646', 'us-ascii'],
'utf-8':       [4, 'utf_8', 'u8', 'utf', 'utf8', 'utf-8'],
'warabic':     [1, 'cp1256', 'windows-1256'],
'wbaltic':     [1, 'cp1257', 'windows-1257'],
'wcyrillic':   [1, 'cp1251', 'windows-1251'],
'wgreek':      [1, 'cp1253', 'windows-1253'],
'whebrew':     [1, 'cp1255', 'windows-1255'],
'wlatin1':     [1, 'cp1252', 'windows-1252'],
'wlatin2':     [1, 'cp1250', 'windows-1250'],
'wturkish':    [1, 'cp1254', 'windows-1254'],
'wvietnamese': [1, 'cp1258', 'windows-1258'],
'any':None,
'dec-cn':None,
'dec-jp':None,
'dec-tw':None,
'ebcdic1025':None,
'ebcdic1026':None,
'ebcdic1047':None,
'ebcdic1112':None,
'ebcdic1122':None,
'ebcdic1130':None,
'ebcdic1137':None,
'ebcdic1140':None,
'ebcdic1141':None,
'ebcdic1142':None,
'ebcdic1143':None,
'ebcdic1144':None,
'ebcdic1145':None,
'ebcdic1146':None,
'ebcdic1147':None,
'ebcdic1148':None,
'ebcdic1149':None,
'ebcdic1153':None,
'ebcdic1154':None,
'ebcdic1155':None,
'ebcdic1156':None,
'ebcdic1157':None,
'ebcdic1158':None,
'ebcdic1160':None,
'ebcdic1164':None,
'ebcdic275':None,
'ebcdic277':None,
'ebcdic278':None,
'ebcdic280':None,
'ebcdic284':None,
'ebcdic285':None,
'ebcdic297':None,
'ebcdic424':None,
'ebcdic425':None,
'ebcdic838':None,
'ebcdic870':None,
'ebcdic875':None,
'ebcdic905':None,
'ebcdic924':None,
'ebcdic-any':None,
'euc-tw':None,
'hp15-tw':None,
'ibm-930':None,
'ibm-933':None,
'ibm-935':None,
'ibm-937':None,
'ibm-939e':None,
'ibm-939':None,
'ibm-942':None,
'ibm-950':None,
'ms-936':None,
'ms-949':None,
'ms-950':None,
'msdos720':None,
'open_ed-037':None,
'open_ed-1025':None,
'open_ed-1112':None,
'open_ed-1122':None,
'open_ed-1130':None,
'open_ed-1137':None,
'open_ed-1141':None,
'open_ed-1142':None,
'open_ed-1143':None,
'open_ed-1144':None,
'open_ed-1145':None,
'open_ed-1146':None,
'open_ed-1147':None,
'open_ed-1148':None,
'open_ed-1149':None,
'open_ed-1153':None,
'open_ed-1154':None,
'open_ed-1155':None,
'open_ed-1156':None,
'open_ed-1157':None,
'open_ed-1158':None,
'open_ed-1160':None,
'open_ed-1164':None,
'open_ed-1166':None,
'open_ed-273':None,
'open_ed-275':None,
'open_ed-277':None,
'open_ed-278':None,
'open_ed-280':None,
'open_ed-284':None,
'open_ed-285':None,
'open_ed-297':None,
'open_ed-425':None,
'open_ed-500':None,
'open_ed-838':None,
'open_ed-870':None,
'open_ed-905':None,
'open_ed-924':None,
'open_ed-930':None,
'open_ed-933':None,
'open_ed-935':None,
'open_ed-937':None,
'open_ed-939e':None,
'open_ed-939':None,
'pc1098':None,
'pciscii806':None,
'pcoem1129':None,
'pcoem921':None,
'pcoem922':None,
'roman8':None
}

