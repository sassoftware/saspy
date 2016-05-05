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
# stdio methods (fork, exec, and pipes). The is also support for running STDIO over ssh, which can 
# connect to a remote linux SAS via passwordless ssh. The ssh method cannot currently support interupt
# handling, as the local STDIO method can. An interupt on this method will terminate the SAS process; 
# you'll be prompted to terminate or wait for completion. The third method is HTTP, which can connect
# to SAS Viya via the Compute Servie, a restfull micro service in the Viay system.
#
# Each of these connection methods (access methods) are handled by their own IO module. This main
# module determines which IO module to use based upon the configuration chosen at runtime. More
# IO modules can be seemlessly plugged in, if needed, in the future.
#
# The expected use is to simply import this package and establish a SAS session, then use the methods:
#
# import saspy
# sas = saspy.SASsession()
# sas.[have_at_it]()
#

import fcntl
import os
import signal
import subprocess
from time import sleep
import saspy.sascfg as sascfg
import saspy.sasiostdio as sasiostdio
import saspy.sasiohttp  as sasiohttp
from saspy.sasstat import *
from saspy.sasets  import *

try:
   from IPython.display import HTML
except ImportError:
   pass

class SASconfig:
   '''
   This object is not intended to be used directly. Instantiate a SASsession object instead 
   '''
   def __init__(self, **kwargs):
      configs       = []
      self._kernel  = kwargs.get('kernel', None)
      self.valid    = True
      self.mode     = ''

      # GET Config options
      try:
         self.cfgopts = getattr(sascfg, "SAS_config_options")
      except:
         self.cfgopts = {}

      # GET Config names
      configs = getattr(sascfg, "SAS_config_names")

      cfgname = kwargs.get('cfgname', '')

      if len(cfgname) == 0:
         if len(configs) == 0:
            print("No SAS Configuration names found in saspy.sascfg")
            self.valid = False
            return
         else:
            if len(configs) == 1:
               cfgname = configs[0]
               if kernel == None:
                  print("Using SAS Config named: "+cfgname)
            else:
               cfgname = self._prompt("Please enter the name of the SAS Config you wish to run. Available Configs are: " +
                                      str(configs)+" ")

      while cfgname not in configs:
         cfgname = self._prompt(
             "The SAS Config name specified was not found. Please enter the SAS Config you wish to use. Available Configs are: " +
              str(configs)+" ")

      self.name = cfgname
      cfg       = getattr(sascfg, cfgname) 

      ip   = cfg.get('ip', '')
      ssh  = cfg.get('ssh', '')
      path = cfg.get('saspath', '')

      if len(ip) > 0:
         self.mode = 'HTTP'
      else:
         if len(ssh) > 0:
            self.mode = 'SSH'
         else:
            if len(path) > 0:
               self.mode = 'STDIO'
            else:
               self.valid = False

   def _prompt(self, prompt, pw=False):
      if self._kernel is None:
          if not pw:
              try:
                 return input(prompt)
              except (KeyboardInterrupt):
                 return ''
          else:
              try:
                 return getpass.getpass(prompt)
              except (KeyboardInterrupt):
                 return ''
      else:
          try:
             return self._kernel._input_request(prompt, self._kernel._parent_ident, self._kernel._parent_header,
                                                password=pw)
          except (KeyboardInterrupt):
             return ''
                   
class SASsession:
   '''
   The SASsession object is the main object to instantiate and provides access to the rest of the functionality.
   cfgname - value in SAS_config_names List of the sascfg.py file
   kernel  - None - internal use when running the SAS_kernel notebook
   saspath - overrides saspath Dict entry of cfgname in sascfg.py file
   options - overrides options Dict entry of cfgname in sascfg.py file

   and for running over passwordless ssh
   ssh     - full path of the ssh command; /usr/bin/ssh for instance
   host    - host name of the remote machine
   '''
   #def __init__(self, cfgname: str ='', kernel: '<SAS_kernel object>' =None, saspath :str ='', options: list ='') -> '<SASsession object>':
   def __init__(self, **kwargs) -> '<SASsession object>':
      self.loaded_macros = False
      self._obj_cnt      = 0
      self.nosub         = False
      self.sascfg        = SASconfig(**kwargs)

      if not self.sascfg.valid:
         return

      if self.sascfg.mode in ['STDIO', 'SSH', '']:
         self.io = sasiostdio.SASsessionSTDIO(**kwargs, sascfgname=self.sascfg.name)
      else:
         if self.sascfg.mode == 'HTTP':
            self.io = sasiohttp.SASsessionHTTP(**kwargs, sascfgname=self.sascfg.name)

   def __del__(self):
      return self.io.__del__()

   def _objcnt(self):
       self._obj_cnt += 1
       return '%04d' % self._obj_cnt

   def _startsas(self):
      return self.io._startsas()

   def _endsas(self):
      return self.io._endsas()

   def _getlog(self, **kwargs):
      return self.io._getlog(**kwargs)

   def _getlst(self, **kwargs):
      return self.io._getlst(**kwargs)

   def _getlsttxt(self, **kwargs):
      return self.io._getlsttxt(**kwargs)

   def _asubmit(self, code, result): 
      return self.io._asubmit(code, result)

   def submit(self, code: str, results: str ="html", prompt: list = []) -> dict:
      '''
      This method is used to submit any SAS code. It returns the Log and Listing as a python dictionary.
      code    - the SAS statements you want to execute 
      results - format of results, HTML is default, TEXT is the alternative
      prompt  - list of names to prompt for; create marco variables (used in submitted code), then delete

      Returns - a Dict containing two keys:values, [LOG, LST]. LOG is text and LST is 'results' (HTML or TEXT)

      NOTE: to view HTML results in the ipykernel, issue: from IPython.display import HTML  and use HTML() instead of print()
      i.e,: results = sas.submit("data a; x=1; run; proc print;run')
            print(results['LOG'])
            HTML(results['LST']) 
      '''
      return self.io.submit(code, results, prompt)

   def saslog(self):
      '''
      this method is used to get the current, full contents of the SASLOG
      '''
      return self.io.saslog()

   def teach_me_SAS(self, nosub: bool):
      '''
      nosub - bool. True means don't submit the code, print it out so I can see what the SAS code would be.
                    False means run normally - submit the code.
      '''
      self.nosub = nosub

   def exist(self, table: str, libref: str ="work") -> bool:
      '''
      table  - the name of the SAS Data Set
      libref - the libref for the Data Set, defaults to WORK

      Returns True it the Data Set exists and False if it does not
      '''
      code  = "data _null_; e = exist('"
      code += libref+"."+table+"');\n" 
      code += "te='TABLE_EXISTS='; put te e;run;"
   
      ll = self.io.submit(code, "text")

      l2 = ll['LOG'].rpartition("TABLE_EXISTS= ")
      l2 = l2[2].partition("\n")
      exists = int(l2[0])
   
      return exists
   
   def sasstat(self) -> '<SASstat object>':
      '''
      This methods creates a SASstat object which you can use to run various analytics. See the sasstat.py module.
      '''
      if not self.loaded_macros:
         self._loadmacros()
         loaded_marcos = True

      return SASstat(self)

   def sasets(self) -> '<SASets object>':
      '''
      This methods creates a SASets object which you can use to run various analytics. See the sasets.py module.
      '''
      if not self.loaded_macros:
         self._loadmacros()
         loaded_marcos = True

      return SASets(self)

   def _loadmacros(self):
      macro_path=os.path.dirname(os.path.realpath(__file__))
      fd = os.open(macro_path+'/'+'libname_gen.sas', os.O_RDONLY)
      code = os.read(fd, 32767)
      self.io._asubmit(code.decode(), results='text')

   def sasdata(self, table: str, libref: str ="work", results: str ='HTML')  -> '<SASdata object>':
      '''
      This method creates a SASdata object for the SAS Data Set you specify
      table   - the name of the SAS Data Set
      libref  - the libref for the Data Set, defaults to WORK
      results - format of results, HTML is default, TEXT is the alternative
      '''
      if self.exist(table, libref):
         return SASdata(self, libref, table, results)
      else:
         return None
   
   def saslib(self, libref: str, engine: str =' ', path: str ='', options: str =' ') -> 'The LOG showing the assignment of the libref':
      '''
      This method is used to assign a libref. The libref is then available to be used in the SAS session.
      libref  - the libref for be assigned
      engine  - the engine name used to access the SAS Library (engine defaults to BASE, per SAS)
      path    - path to the library (for engines that take a path parameter)
      options - other engine or engine supervisor options
      '''
      code  = "libname "+libref+" "+engine+" "
      if len(path) > 0:
         code += " '"+path+"' "
      code += options+";"

      if self.nosub:
         print(code)
      else:
         ll = self.io.submit(code, "text")
         print(ll['LOG'].rsplit(";*\';*\";*/;\n")[0]) 

   def read_csv(self, file: str, table: str, libref: str ="work", results: str ='HTML') -> '<SASdata object>':
      '''
      This method will import a csv file into a SAS Data Set and return the SASdata object referring to it.
      file    - eithe the OS filesystem path of the file, or HTTP://... for a url accessible file
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK
      results - format of results, HTML is default, TEXT is the alternative
      '''
      code  = "filename x "
   
      if file.startswith(("http","HTTP")):
         code += "url "
   
      code += "\""+file+"\";\n"
      code += "proc import datafile=x out="
      code += libref+"."+table
      code += " dbms=csv replace; run;"
   
      if self.nosub:
         print(code)
      else:
         ll = self.io.submit(code, "text")
         if self.exist(table, libref):
            return SASdata(self, libref, table, results)
         else:
            return None
   
   def df2sd(self, df: '<Pandas Data Frame object>', table: str ='a', libref: str ="work", results: str ='HTML') -> '<SASdata object>':
      '''
      This is an alias for 'dataframe2sasdata'. Why type all that?
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK
      results - format of results, HTML is default, TEXT is the alternative
      '''
      return self.dataframe2sasdata(df, table, libref, results)
   
   def dataframe2sasdata(self, df: '<Pandas Data Frame object>', table: str ='a', libref: str ="work", results: str ='HTML') -> '<SASdata object>':
      '''
      This method imports a Pandas Data Frame to a SAS Data Set, returning the SASdata object for the new Data Set.
      df      - Pandas Data Frame to import to a SAS Data Set
      table   - the name of the SAS Data Set to create
      libref  - the libref for the SAS Data Set being created. Defaults to WORK
      results - format of results, HTML is default, TEXT is the alternative
      '''
      self.io.dataframe2sasdata(df, table, libref, results)

      if self.exist(table, libref):
         return SASdata(self, libref, table, results)
      else:
         return None
   
   def sd2df(self, sd: '<SASdata object>') -> '<Pandas Data Frame object>':
      '''
      This is an alias for 'sasdata2dataframe'. Why type all that?
      sd      - SASdata object that refers to the Sas Data Set you want to export to a Pandas Data Frame
      '''
      return self.sasdata2dataframe(sd)
   
   def sasdata2dataframe(self, sd: '<SASdata object>') -> '<Pandas Data Frame object>':
      '''
      This method exports the SAS Data Set to a Pandas Data Frame, returning the Data Frame object.
      sd      - SASdata object that refers to the Sas Data Set you want to export to a Pandas Data Frame
      '''
      if sd == None:
         print('The SAS_data object is not valid; it is \'None\'')
         return None                            
      if sd == None or self.exist(sd.table, sd.libref) == 0:
         print('The SAS Data Set '+sd.libref|'.'+sd.table+' does not exist')
         return None                            
   
      return self.io.sasdata2dataframe(sd)
   
class SASdata:

    def __init__(self, sassession, libref, table, results="HTML"):

        self.sas =  sassession

        failed = 0 
        if results.upper() == "HTML":
           try:
              from IPython.display import HTML 
           except:
              failed = 1

           if failed:
              self.HTML = 0
           else:
              self.HTML = 1
        else:
           self.HTML = 0

        self.libref = libref 
        self.table  = table

    def set_results(self, results: str):
        '''
        This method set the results attribute for the SASdata object; it stays in effect till changed
        results - set the default result type for this SASdata object. 'HTML' = HTML. Anything else = 'TEXT'.
        '''
        if results.upper() == "HTML":
           self.HTML = 1
        else:
           self.HTML = 0

    def head(self, obs=5):
        '''
        display the first n rows of a table
        obs - the number of rows of the table that you want to display. The default is 5

        '''
        code  = "proc print data="
        code += self.libref
        code += "."
        code += self.table
        code += "(obs="
        code += str(obs)
        code += ");run;"
        
        if self.sas.nosub:
           print(code)
           return

        if self.HTML:
           ll = self.sas.io.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.io.submit(code, "text")
           print(ll['LST'])
   
    def tail(self, obs=5):
        '''
        display the last n rows of a table
        obs - the number of rows of the table that you want to display. The default is 5

        '''
        code  = "%put lastobs=%sysfunc(attrn(%sysfunc(open("
        code += self.libref
        code += "."
        code += self.table
        code += ")),NOBS)) tom;"

        ll = self.sas.submit(code, "text")

        lastobs = ll['LOG'].rpartition("lastobs=")
        lastobs = lastobs[2].partition(" tom")
        lastobs = int(lastobs[0])

        code  = "proc print data="
        code += self.libref
        code += "."
        code += self.table
        code += "(firstobs="
        code += str(lastobs-(obs-1))
        code += " obs="
        code += str(lastobs)
        code += ");run;"
        
        if self.sas.nosub:
           print(code)
           return

        if self.HTML:
           ll = self.sas.io.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.io.submit(code, "text")
           print(ll['LST'])
   
    def contents(self):
        '''
        display metadata about the table. size, number of rows, columns and their data type ...

        '''
        code  = "proc contents data="
        code += self.libref
        code += "."
        code += self.table
        code += ";run;"

        if self.sas.nosub:
           print(code)
           return

        if self.HTML:
           ll = self.sas.io.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.io.submit(code, "text")
           print(ll['LST'])
   
    def describe(self):
        '''
        display descriptive statistics for the table; summary statistics.

        '''
        return(self.means())

    def means(self):
        '''
        display descriptive statistics for the table; summary statistics. This is an alias for 'describe'

        '''
        code  = "proc means data="
        code += self.libref
        code += "."
        code += self.table
        code += " n mean std min p25 p50 p75 max;run;"
        
        if self.sas.nosub:
           print(code)
           return

        if self.HTML:
           ll = self.sas.io.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.io.submit(code, "text")
           print(ll['LST'])

    def to_csv(self, file: str) -> 'The LOG showing the results of the step':
        '''
        This method will export a SAS Data Set to a file in CCSV format.
        file    - the OS filesystem path of the file to be created (exported from this SAS Data Set)
        '''
        code  = "filename x \""+file+"\";\n"
        code += "proc export data="+self.libref+"."+self.table+" outfile=x"
        code += " dbms=csv replace; run;"

        if self.sas.nosub:
           print(code)
        else:
           ll = self.sas.io.submit(code, "text")
           return 0

    def to_df(self) -> '<Pandas Data Frame object>':
        '''
        Export this SAS Data Set to a Pandas Data Frame
        '''
        return self.sas.sasdata2dataframe(self)

    def hist(self, var: str, title: str ='', label: str ='') -> 'a histogram plot of the (numeric) variable you chose':
        '''
        This method requires a numeric column (use the contents method to see column types) and generates a histogram.
        var   - the NUMERIC variable (column) you want to plot
        title - an optional Title for the chart
        label - LegendLABEL= value for sgplot
        '''
        code  = "proc sgplot data="
        code += self.libref
        code += "."
        code += self.table
        code += ";\n\thistogram "+var+" / scale=count"
        if len(label) > 0:
           code += " LegendLABEL='"+label+"'"
        code += ";\n"
        if len(title) > 0:
           code += '\ttitle "'+title+'";\n'
        code += "\tdensity "+var+';\nrun;\n'+'title \"\";'
        
        if self.sas.nosub:
           print(code)
           return

        if self.HTML:
           ll = self.sas.io.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.io.submit(code, "text")
           print(ll['LST'])

    def series(self, x: str, y: list, title: str ='') -> 'a line plot of the x,y coordinates':
        '''
        This method plots a series of x,y coordinates. You can provide a list of y columns for multiple line plots.
        x     - the x axis variable; generally a time or continuous variable. 
        y     - the y axis variable(s), you can specify a single column or a list of columns 
        title - an optional Title for the chart
        '''
        code  = "proc sgplot data="
        code += self.libref
        code += "."
        code += self.table+";\n"
        if len(title) > 0:
           code += '\ttitle "'+title+'";\n'

        if type(y) == list:
           num = len(y)
        else:
           num = 1
           y = [y]

        for i in range(num):
           code += "\tseries x="+x+" y="+y[i]+";\n"
                                                      
        code += 'run;\n'+'title \"\";'
        
        if self.sas.nosub:
           print(code)
           return

        if self.HTML:
           ll = self.sas.io.submit(code)
           return HTML(ll['LST'])
        else:
           ll = self.sas.io.submit(code, "text")
           print(ll['LST'])

if __name__ == "__main__":
    startsas()

    submit(sys.argv[1], "text")

    print(_getlog())
    print(_getlsttxt())

    endsas()

sas_dtdt_fmts = (    
'AFRDFDD','AFRDFDE','AFRDFDE','AFRDFDN','AFRDFDT','AFRDFDT','AFRDFDWN',
'AFRDFMN','AFRDFMY','AFRDFMY','AFRDFWDX','AFRDFWKX','ANYDTDTE','ANYDTDTM','ANYDTTME','B8601DA','B8601DA','B8601DJ','B8601DN','B8601DN',
'B8601DT','B8601DT','B8601DZ','B8601DZ','B8601LZ','B8601LZ','B8601TM','B8601TM','B8601TZ','B8601TZ','CATDFDD','CATDFDE','CATDFDE','CATDFDN',
'CATDFDT','CATDFDT','CATDFDWN','CATDFMN','CATDFMY','CATDFMY','CATDFWDX','CATDFWKX','CRODFDD','CRODFDE','CRODFDE','CRODFDN','CRODFDT',
'CRODFDT','CRODFDWN','CRODFMN','CRODFMY','CRODFMY','CRODFWDX','CRODFWKX','CSYDFDD','CSYDFDE','CSYDFDE','CSYDFDN','CSYDFDT','CSYDFDT',
'CSYDFDWN','CSYDFMN','CSYDFMY','CSYDFMY','CSYDFWDX','CSYDFWKX','DANDFDD','DANDFDE','DANDFDE','DANDFDN','DANDFDT','DANDFDT','DANDFDWN','DANDFMN',
'DANDFMY','DANDFMY','DANDFWDX','DANDFWKX','DATE','DATE','DATEAMPM','DATETIME','DATETIME','DAY','DDMMYY','DDMMYY','DDMMYYB','DDMMYYC',
'DDMMYYD','DDMMYYN','DDMMYYP','DDMMYYS','DESDFDD','DESDFDE','DESDFDE','DESDFDN','DESDFDT','DESDFDT','DESDFDWN','DESDFMN','DESDFMY','DESDFMY',
'DESDFWDX','DESDFWKX','DEUDFDD','DEUDFDE','DEUDFDE','DEUDFDN','DEUDFDT','DEUDFDT','DEUDFDWN','DEUDFMN','DEUDFMY','DEUDFMY','DEUDFWDX',
'DEUDFWKX','DOWNAME','DTDATE','DTMONYY','DTWKDATX','DTYEAR','DTYYQC','E8601DA','E8601DA','E8601DN','E8601DN','E8601DT','E8601DT','E8601DZ',
'E8601DZ','E8601LZ','E8601LZ','E8601TM','E8601TM','E8601TZ','E8601TZ','ENGDFDD','ENGDFDE','ENGDFDE','ENGDFDN','ENGDFDT','ENGDFDT','ENGDFDWN',
'ENGDFMN','ENGDFMY','ENGDFMY','ENGDFWDX','ENGDFWKX','ESPDFDD','ESPDFDE','ESPDFDE','ESPDFDN','ESPDFDT','ESPDFDT','ESPDFDWN','ESPDFMN',
'ESPDFMY','ESPDFMY','ESPDFWDX','ESPDFWKX','EURDFDD','EURDFDE','EURDFDE','EURDFDN','EURDFDT','EURDFDT','EURDFDWN','EURDFMN','EURDFMY',
'EURDFMY','EURDFWDX','EURDFWKX','FINDFDD','FINDFDE','FINDFDE','FINDFDN','FINDFDT','FINDFDT','FINDFDWN','FINDFMN','FINDFMY','FINDFMY',
'FINDFWDX','FINDFWKX','FRADFDD','FRADFDE','FRADFDE','FRADFDN','FRADFDT','FRADFDT','FRADFDWN','FRADFMN','FRADFMY','FRADFMY','FRADFWDX',
'FRADFWKX','FRSDFDD','FRSDFDE','FRSDFDE','FRSDFDN','FRSDFDT','FRSDFDT','FRSDFDWN','FRSDFMN','FRSDFMY','FRSDFMY','FRSDFWDX','FRSDFWKX','HHMM',
'HOUR','HUNDFDD','HUNDFDE','HUNDFDE','HUNDFDN','HUNDFDT','HUNDFDT','HUNDFDWN','HUNDFMN','HUNDFMY','HUNDFMY','HUNDFWDX','HUNDFWKX',
'IS8601DA','IS8601DA','IS8601DN','IS8601DN','IS8601DT','IS8601DT','IS8601DZ','IS8601DZ','IS8601LZ','IS8601LZ','IS8601TM','IS8601TM',
'IS8601TZ','IS8601TZ','ITADFDD','ITADFDE','ITADFDE','ITADFDN','ITADFDT','ITADFDT','ITADFDWN','ITADFMN','ITADFMY','ITADFMY','ITADFWDX',
'ITADFWKX','JDATEMD','JDATEMDW','JDATEMNW','JDATEMON','JDATEQRW','JDATEQTR','JDATESEM','JDATESMW','JDATEWK','JDATEYDW','JDATEYM','JDATEYMD',
'JDATEYMD','JDATEYMW','JDATEYT','JDATEYTW','JNENGO','JNENGO','JNENGOT','JNENGOTW','JNENGOW','JTIMEH','JTIMEHM','JTIMEHMS','JTIMEHW',
'JTIMEMW','JTIMESW','JULDATE','JULDAY','JULIAN','JULIAN','MACDFDD','MACDFDE','MACDFDE','MACDFDN','MACDFDT','MACDFDT','MACDFDWN','MACDFMN',
'MACDFMY','MACDFMY','MACDFWDX','MACDFWKX','MDYAMPM','MDYAMPM','MINGUO','MINGUO','MMDDYY','MMDDYY','MMDDYYB','MMDDYYC','MMDDYYD','MMDDYYN',
'MMDDYYP','MMDDYYS','MMSS','MMYY','MMYYC','MMYYD','MMYYN','MMYYP','MMYYS','MONNAME','MONTH','MONYY','MONYY','ND8601DA','ND8601DN','ND8601DT',
'ND8601DZ','ND8601TM','ND8601TZ','NENGO','NENGO','NLDATE','NLDATE','NLDATEL','NLDATEM','NLDATEMD','NLDATEMDL','NLDATEMDM','NLDATEMDS',
'NLDATEMN','NLDATES','NLDATEW','NLDATEW','NLDATEWN','NLDATEYM','NLDATEYML','NLDATEYMM','NLDATEYMS','NLDATEYQ','NLDATEYQL','NLDATEYQM',
'NLDATEYQS','NLDATEYR','NLDATEYW','NLDATM','NLDATM','NLDATMAP','NLDATMAP','NLDATMDT','NLDATML','NLDATMM','NLDATMMD','NLDATMMDL','NLDATMMDM',
'NLDATMMDS','NLDATMMN','NLDATMS','NLDATMTM','NLDATMTZ','NLDATMW','NLDATMW','NLDATMWN','NLDATMWZ','NLDATMYM','NLDATMYML','NLDATMYMM',
'NLDATMYMS','NLDATMYQ','NLDATMYQL','NLDATMYQM','NLDATMYQS','NLDATMYR','NLDATMYW','NLDATMZ','NLDDFDD','NLDDFDE','NLDDFDE','NLDDFDN','NLDDFDT',
'NLDDFDT','NLDDFDWN','NLDDFMN','NLDDFMY','NLDDFMY','NLDDFWDX','NLDDFWKX','NLTIMAP','NLTIMAP','NLTIME','NLTIME','NORDFDD','NORDFDE',
'NORDFDE','NORDFDN','NORDFDT','NORDFDT','NORDFDWN','NORDFMN','NORDFMY','NORDFMY','NORDFWDX','NORDFWKX','POLDFDD','POLDFDE','POLDFDE',
'POLDFDN','POLDFDT','POLDFDT','POLDFDWN','POLDFMN','POLDFMY','POLDFMY','POLDFWDX','POLDFWKX','PTGDFDD','PTGDFDE','PTGDFDE','PTGDFDN',
'PTGDFDT','PTGDFDT','PTGDFDWN','PTGDFMN','PTGDFMY','PTGDFMY','PTGDFWDX','PTGDFWKX','QTR','QTRR','RUSDFDD','RUSDFDE','RUSDFDE','RUSDFDN',
'RUSDFDT','RUSDFDT','RUSDFDWN','RUSDFMN','RUSDFMY','RUSDFMY','RUSDFWDX','RUSDFWKX','SLODFDD','SLODFDE','SLODFDE','SLODFDN','SLODFDT',
'SLODFDT','SLODFDWN','SLODFMN','SLODFMY','SLODFMY','SLODFWDX','SLODFWKX','STIMER','SVEDFDD','SVEDFDE','SVEDFDE','SVEDFDN','SVEDFDT',
'SVEDFDT','SVEDFDWN','SVEDFMN','SVEDFMY','SVEDFMY','SVEDFWDX','SVEDFWKX','TIME','TIME','TIMEAMPM','TOD','TWMDY','WEEKDATE','WEEKDATX',
'WEEKDAY','WEEKU','WEEKU','WEEKV','WEEKV','WEEKW','WEEKW','WORDDATE','WORDDATX','XYYMMDD','XYYMMDD','YEAR','YMDDTTM','YYMM','YYMMC',
'YYMMD','YYMMDD','YYMMDD','YYMMDDB','YYMMDDC','YYMMDDD','YYMMDDN','YYMMDDP','YYMMDDS','YYMMN','YYMMN','YYMMP','YYMMS','YYMON','YYQ',
'YYQ','YYQC','YYQD','YYQN','YYQP','YYQR','YYQRC','YYQRD','YYQRN','YYQRP','YYQRS','YYQS','YYQZ','YYQZ','YYWEEKU','YYWEEKV','YYWEEKW'
)

