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
from saspy.sasresults import SASresults

# create logger
logger = logging.getLogger('')
logger.setLevel(logging.WARN)


class SASets:
    def __init__(self, session, *args, **kwargs):
        """Submit an initial set of macros to prepare the SAS system"""
        self.sas=session
        logger.debug("Initialization of SAS Macro: " + str(self.sas.saslog()))

    def _objectmethods(self, obj: str, *args) -> list:
        """
        This method parses the SAS log for artifacts (tables and graphics) that were created
        from the procedure method call

        :param obj: str -- proc object
        :param args: list likely none
        :return: list -- the tables and graphs available for tab complete
        """
        code  = "%listdata("
        code += obj
        code += ");"
        logger.debug("Object Method macro call: " + str(code))
        res = self.sas.submit(code,"text")
        meth = res['LOG'].splitlines()
        for i in range(len(meth)):
           meth[i] = meth[i].lstrip().rstrip()
        logger.debug('SAS Log: ' + str(meth))
        objlist = meth[meth.index('startparse9878')+1:meth.index('endparse9878')]
        logger.debug("PROC attr list: " + str(objlist))
        return objlist

    def _makeProcCallMacro(self, objtype: str, objname: str, data: object =None, args: dict =None) -> str:
        """
        This method generates the SAS code from the python objects and included data and arguments.
        The list of args in this method is largely alphabetical but there are exceptions in order to
        satisfy the order needs of the statements for the procedure. as an example...
        http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_glm_syntax.htm#statug.glm.glmpostable

        :param objtype: str -- proc name
        :param objname: str -- 3 digit code for proc
        :param data: sas dataset object
        :param args: dict --  proc arguments
        :return: str -- the SAS code needed to execute on the server
        """
        code  = "%macro proccall(d);\n"
        if 'out' in args:
            outds = args['out']
            code += "proc %s data=%s.%s out=%s.%s plot=all;\n" % (objtype, data.libref, data.table, outds.libref, outds.table)
        else:
            code += "proc %s data=%s.%s plot=all;\n" % (objtype, data.libref, data.table)
        logger.debug("args value: " + str(args))
        logger.debug("args type: " + str(type(args)))
        if 'by' in args:
            logger.debug("by statement,length: %s,%s", args['by'], len(args['by']))
            code += "by %s;\n" % (args['by'])
        if 'corr' in args:
            logger.debug("corr statement,length: %s,%s", args['corr'], len(args['corr']))
            code += "corr %s;\n" % (args['corr'])
        if 'crosscorr' in args:
            logger.debug("crosscorr statement,length: %s,%s", args['crosscorr'], len(args['crosscorr']))
            code += "crosscorr %s;\n" % (args['crosscorr'])
        if 'decomp' in args:
            logger.debug("decomp statement,length: %s,%s", args['decomp'], len(args['decomp']))
            code += "decomp %s;\n" % (args['decomp'])
        if 'id' in args:
            logger.debug("id statement,length: %s,%s", args['id'], len(args['id']))
            code += "id %s;\n" % (args['id'])
        if 'season' in args:
            logger.debug("season statement,length: %s,%s", args['season'], len(args['season']))
            code += "season %s;\n" % (args['season'])
        if 'trend' in args:
            logger.debug("trend statement,length: %s,%s", args['trend'], len(args['trend']))
            code += "trend %s;\n" % (args['trend'])
        if 'var' in args:
            logger.debug("var statement,length: %s,%s", args['var'], len(args['var']))
            code += "var %s;\n" % (args['var'])
        if 'crossvar' in args:
            logger.debug("crossvar statement,length: %s,%s", args['crossvar'], len(args['crossvar']))
            code += "crossvar %s;\n" % (args['crossvar'])
        if 'identify' in args:
            logger.debug("identify statement,length: %s,%s", args['identify'], len(args['identify']))
            code += "identify %s;\n" % (args['identify'])
        if 'estimate' in args:
            logger.debug("estimate statement,length: %s,%s", args['estimate'], len(args['estimate']))
            code += "estimate %s;\n" % (args['estimate'])
        if 'outlier' in args:
            logger.debug("outlier statement,length: %s,%s", args['outlier'], len(args['outlier']))
            code += "outlier %s;\n" % (args['outlier'])
        if 'forecast' in args:
            logger.debug("forecast statement,length: %s,%s", args['forecast'], len(args['forecast']))
            code += "forecast %s;\n" % (args['forecast'])
        if 'autoreg' in args:
            logger.debug("autoreg statement,length: %s,%s", args['autoreg'], len(args['autoreg']))
            code += "autoreg %s;\n" % (args['autoreg'])
        if 'blockseason' in args:
            logger.debug("blockseason statement,length: %s,%s", args['blockseason'], len(args['blockseason']))
            code += "blockseason %s;\n" % (args['blockseason'])
        if 'cycle' in args:
            logger.debug("cycle statement,length: %s,%s", args['cycle'], len(args['cycle']))
            code += "cycle %s;\n" % (args['cycle'])
        if 'deplag' in args:
            logger.debug("deplag statement,length: %s,%s", args['deplag'], len(args['deplag']))
            code += "deplag %s;\n" % (args['deplag'])
        if 'irregular' in args:
            logger.debug("irregular statement,length: %s,%s", args['irregular'], len(args['irregular']))
            code += "irregular %s;\n" % (args['irregular'])
        if 'level' in args:
            logger.debug("level statement,length: %s,%s", args['level'], len(args['level']))
            code += "level %s;\n" % (args['level'])
        if 'model' in args:
            logger.debug("model statement,length: %s,%s", args['model'], len(args['model']))
            code += "model %s;\n" % (args['model'])
        if 'nloptions' in args:
            logger.debug("nloptions statement,length: %s,%s", args['nloptions'], len(args['nloptions']))
            code += "nloptions %s;\n" % (args['nloptions'])
        if 'performance' in args:
            logger.debug("performance statement,length: %s,%s", args['performance'], len(args['performance']))
            code += "performance %s;\n" % (args['performance'])
        if 'randomreg' in args:
            logger.debug("randomreg statement,length: %s,%s", args['randomreg'], len(args['randomreg']))
            code += "randomreg %s;\n" % (args['randomreg'])
        if 'slope' in args:
            logger.debug("slope statement,length: %s,%s", args['slope'], len(args['slope']))
            code += "slope %s;\n" % (args['slope'])
        if 'splinereg' in args:
            logger.debug("splinereg statement,length: %s,%s", args['splinereg'], len(args['splinereg']))
            code += "splinereg %s;\n" % (args['splinereg'])
        if 'splineseason' in args:
            logger.debug("splineseason statement,length: %s,%s", args['splineseason'], len(args['splineseason']))
            code += "splineseason %s;\n" % (args['splineseason'])
        if 'fcmport' in args:
            logger.debug("fcmport statement,length: %s,%s", args['fcmport'], len(args['fcmport']))
            code += "fcmport %s;\n" % (args['fcmport'])
        if 'outarrays' in args:
            logger.debug("outarrays statement,length: %s,%s", args['outarrays'], len(args['outarrays']))
            code += "outarrays %s;\n" % (args['outarrays'])
        if 'outscalars' in args:
            logger.debug("outscalars statement,length: %s,%s", args['outscalars'], len(args['outscalars']))
            code += "outscalars %s;\n" % (args['outscalars'])
        if 'prog_stmts' in args:
            logger.debug("prog_stmts statement,length: %s,%s", args['prog_stmts'], len(args['prog_stmts']))
            code += " %s;\n" % (args['prog_stmts'])
        code += "run; quit; %mend;\n"
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype,data.table)
        logger.debug("Proc code submission: " + str(code))
        return code

    def _stmt_check(self, req:set, legal:set, stmt:dict) -> bool:
        """
        This method checks to make sure that the proc has all required statements and removes any statements
        aren't valid. Missing required statements is an error. Extra statements are not.
        :param req: set
        :param legal: set
        :param stmt: dict
        :return: binary
        """
        if logging.getLogger().getEffectiveLevel()==10:
            for k,v in stmt.items():
                print ("Key: " +k+", Value: " + v)

        # required statements
        req_set=req
        if len(req_set):
            missing_set=req_set.difference(set(stmt.keys()))
            if missing_set:
                msg  = "You are missing %d required statements:" % (len(missing_set))
                msg += "\n"+str(missing_set)
                print(msg)
                return msg

        # legal statements
        legal_set=legal
        if len(legal_set):
            if len(req_set):
               tot_set = legal_set | req_set
            else:
               tot_set = legal_set
            extra_set=set(stmt.keys()).difference(tot_set) # find keys not in legal or required sets
            if extra_set:
                print ("The following %d statements are invalid and will be ignored: "% len(extra_set))
                print(extra_set)
        return None

    def _run_proc(self, procname: str, required_set: set, legal_set: set, **kwargs: dict) -> object:
        """
        This internal method takes the options and statements from the PROC and generates
        the code needed to submit it to SAS. It then submits the code.
        :param self:
        :param procname: str
        :param required_set: set of options
        :param legal_set: set of valid options
        :param kwargs: dict (optional)
        :return: sas result object
        """
        data=kwargs.pop('data',None)
        log = self._stmt_check(required_set, legal_set, kwargs)
        obj1=[]; nosub=False; objname='';
        if not log:
            objtype=procname.lower()
            objname='ets'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
            code=self._makeProcCallMacro(objtype, objname, data, kwargs)
            logger.debug(procname+" macro submission: " + str(code))
            if not self.sas.nosub:
                ll = self.sas.submit(code,"text")
                log = ll['LOG']
                try:
                    obj1=self._objectmethods(objname)
                    logger.debug(obj1)
                except Exception:
                    pass
            else:
                print(code)
                log = ''
                nosub=True
        else:
            print("Error in code submission")

        return SASresults(obj1, self.sas, objname, nosub, log)


    def timeseries(self, **kwargs):
        """
        Python method to call the TIMESERIES procedure
        required_set={'id'}
        legal_set={ 'by', 'corr', 'crosscorr', 'decomp', 'id', 'season', 'trend', 'var', 'crossvar', 'out'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeseries_syntax.htm
        """
        required_set = {'id'}
        legal_set = { 'by', 'corr', 'crosscorr', 'decomp', 'id', 'season', 'trend', 'var', 'crossvar', 'out'}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return self._run_proc("TIMESERIES", required_set, legal_set, **kwargs)

    def arima(self, **kwargs):
        """
        Python method to call the ARIMA procedure
        required_set={'identify'}
        legal_set={ 'by', 'identify', 'estimate', 'outlier', 'forecast', 'out'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_arima_syntax.htm
        """
        required_set = {'identify'}
        legal_set = { 'by', 'identify', 'estimate', 'outlier', 'forecast', 'out'}
        return self._run_proc("ARIMA", required_set, legal_set, **kwargs)

    def ucm(self, **kwargs):
        """
        Python method to call the UCM procedure
        required_set={'model'}
        legal_set= {'autoreg', 'blockseason', 'by', 'cycle', 'deplag', 'estimate', 'forecast', 'id', 'irregular'
                    'level', 'model', 'nloptions', 'performance', 'out', 'outlier', 'randomreg', 'season', 'slope'
                    'splinereg', 'splineseason'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_ucm_syntax.htm
        """
        required_set = {'model'}
        legal_set = {'autoreg', 'blockseason', 'by', 'cycle', 'deplag', 'estimate', 'forecast', 'id', 'irregular'
                    'level', 'model', 'nloptions', 'performance', 'out', 'outlier', 'randomreg', 'season', 'slope'
                    'splinereg', 'splineseason'}
        return self._run_proc("UCM", required_set, legal_set, **kwargs)

    def esm(self, **kwargs):
        """
        Python method to call the ESM procedure
        required_set = {}
        legal_set = { 'by', 'id', 'forecast', 'out'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_esm_syntax.htm
        """
        required_set = {}
        legal_set = { 'by', 'id', 'forecast', 'out'}
        return self._run_proc("ESM", required_set, legal_set, **kwargs)

    def timeid(self, **kwargs):
        """
        Python method to call the TIMEID procedure
        required_set = {}
        legal_set = { 'by', 'id', 'out'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeid_syntax.htm
        """
        required_set = {}
        legal_set = { 'by', 'id', 'out'}
        return self._run_proc("TIMEID", required_set, legal_set, **kwargs)

    def timedata(self, **kwargs):
        """
        Python method to call the TIMEDATA procedure
        required_set = {}
        legal_set = {'by', 'id', 'fcmport', 'out', 'outarrays', 'outscalars', 'var', 'prog_stmts'}

        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timedata_syntax.htm
        """
        required_set = {}
        legal_set = {'by', 'id', 'fcmport', 'out', 'outarrays', 'outscalars', 'var', 'prog_stmts'}
        return self._run_proc("TIMEIDATA", required_set, legal_set, **kwargs)

