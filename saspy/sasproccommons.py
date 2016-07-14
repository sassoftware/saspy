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
from saspy.sasresults import SASresults


class SASProcCommons:
    def __init__(self, session, *args, **kwargs):
        self.sas = session

    @staticmethod
    def _errorLog(log):
        if isinstance(log, str):
            lines = re.split(r'[\n]\s*', log)
            i = 0
            elog = []
            for line in lines:
                i += 1
                e = []
                if line.startswith('ERROR'):
                    e = lines[(max(i - 1, 0)):(min(i + 0, len(lines)))]
                elog = elog + e
            return "\n".join(elog)
        else:
            print("log is not a string but type:%s" % (str(type(log))))

    def _makeProcCallMacro(self, objtype: str, objname: str, data: object = None, args: dict = None) -> str:
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
        code = "%macro proccall(d);\n"
        # TODO: resolve issues withe Proc options, out= and plots=
        # The procopts statement should be in every procedure as a way to pass arbitrary options to the procedures
        if 'procopts' in args:
            logging.debug("procopts statement,length: %s,%s", args['procopts'], len(args['procopts']))
            code += "proc %s data=%s.%s %s;\n" % (objtype, data.libref, data.table, args['procopts'])
        else:
            code += "proc %s data=%s.%s ;\n" % (objtype, data.libref, data.table)
        logging.debug("args value: " + str(args))
        logging.debug("args type: " + str(type(args)))

        # this list is largely alphabetical but there are exceptions in order to
        # satisfy the order needs of the statements for the procedure
        # as an example... http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_glm_syntax.htm#statug.glm.glmpostable
        if 'absorb' in args:
            logging.debug("absorb statement,length: %s,%s", args['absorb'], len(args['absorb']))
            code += "absorb %s;\n" % (args['absorb'])
        if 'add' in args:
            logging.debug("add statement,length: %s,%s", args['add'], len(args['add']))
            code += "add %s;\n" % (args['add'])
        # Todo: only three valid values logistic, mlp, mlp direct
        if 'architecture' in args:
            logging.debug("architecture statement,length: %s,%s", args['architecture'], len(args['architecture']))
            code += "architecture %s;\n" % (args['architecture'])
        if 'autoreg' in args:
            logger.debug("autoreg statement,length: %s,%s", args['autoreg'], len(args['autoreg']))
            code += "autoreg %s;\n" % (args['autoreg'])
        if 'blockseason' in args:
            logger.debug("blockseason statement,length: %s,%s", args['blockseason'], len(args['blockseason']))
            code += "blockseason %s;\n" % (args['blockseason'])
        if 'by' in args:
            logging.debug("by statement,length: %s,%s", args['by'], len(args['by']))
            code += "by %s;\n" % (args['by'])
        if 'cdfplot' in args:
            logger.debug("cdfplot statement,length: %s,%s", args['cdfplot'], len(args['cdfplot']))
            code += "cdfplot %s;\n" % (args['cdfplot'])

        if 'cls' in args:
            logging.debug("class statement,length: %s,%s", args['cls'], len(args['cls']))
            code += "class %s;\n" % (args['cls'])
            #   if 'class' in args:
            #       logger.debug("class statement,length: %s,%s", args['class'], len(args['class']))
            #       code += "class %s;\n" % (args['class'])
        if 'comphist' in args:
            logger.debug("comphistogram statement,length: %s,%s", args['comphist'], len(args['comphist']))
            code += "comphist %s;\n" % (args['comphist'])

        # contrast moved
        if 'corr' in args:
            logger.debug("corr statement,length: %s,%s", args['corr'], len(args['corr']))
            code += "corr %s;\n" % (args['corr'])
        if 'crosscorr' in args:
            logger.debug("crosscorr statement,length: %s,%s", args['crosscorr'], len(args['crosscorr']))
            code += "crosscorr %s;\n" % (args['crosscorr'])
        if 'crossvar' in args:
            logger.debug("crossvar statement,length: %s,%s", args['crossvar'], len(args['crossvar']))
            code += "crossvar %s;\n" % (args['crossvar'])
        if 'cycle' in args:
            logger.debug("cycle statement,length: %s,%s", args['cycle'], len(args['cycle']))
            code += "cycle %s;\n" % (args['cycle'])
        if 'decomp' in args:
            logger.debug("decomp statement,length: %s,%s", args['decomp'], len(args['decomp']))
            code += "decomp %s;\n" % (args['decomp'])
        if 'deplag' in args:
            logger.debug("deplag statement,length: %s,%s", args['deplag'], len(args['deplag']))
            code += "deplag %s;\n" % (args['deplag'])
        if 'effect' in args:
            logging.debug("effect statement,length: %s,%s", args['effect'], len(args['effect']))
            code += "effect %s;\n" % (args['effect'])
        # estimate moved
        if 'fcmport' in args:
            logger.debug("fcmport statement,length: %s,%s", args['fcmport'], len(args['fcmport']))
            code += "fcmport %s;\n" % (args['fcmport'])
        if 'freq' in args:
            # TODO: add check to make sure it is only one variable
            logging.debug("freq statement,length: %s,%s", args['freq'], len(args['freq']))
            code += "freq %s;\n" % (args['freq'])
        if 'forecast' in args:
            logger.debug("forecast statement,length: %s,%s", args['forecast'], len(args['forecast']))
            code += "forecast %s;\n" % (args['forecast'])
        # TODO: make a dictionary?
        if 'hidden' in args:
            logging.debug("hidden statement,length: %s,%s", args['hidden'], len(args['hidden']))
            code += "hidden %s;\n" % (args['hidden'])
        if 'histogram' in args:
            logger.debug("histogram statement,length: %s,%s", args['histogram'], len(args['histogram']))
            code += "histogram %s;\n" % (args['histogram'])
        if 'id' in args:
            logging.debug("id statement,length: %s,%s", args['id'], len(args['id']))
            code += "id %s;\n" % (args['id'])
        if 'identify' in args:
            logger.debug("identify statement,length: %s,%s", args['identify'], len(args['identify']))
            code += "identify %s;\n" % (args['identify'])
        if 'input' in args:
            logging.debug("input statement,length: %s,%s", args['input'], len(args['input']))
            code += "input %s;\n" % (args['input'])
        if 'inset' in args:
            logger.debug("inset statement,length: %s,%s", args['inset'], len(args['inset']))
            code += "inset %s;\n" % (args['inset'])
        if 'intervals' in args:
            logger.debug("intervals statement,length: %s,%s", args['intervals'], len(args['intervals']))
            code += "intervals %s;\n" % (args['intervals'])
        if 'irregular' in args:
            logger.debug("irregular statement,length: %s,%s", args['irregular'], len(args['irregular']))
            code += "irregular %s;\n" % (args['irregular'])
        if 'level' in args:
            logger.debug("level statement,length: %s,%s", args['level'], len(args['level']))
            code += "level %s;\n" % (args['level'])
        # lsmeans moved
        # manova moved
        # means moved
        if 'model' in args:
            logging.debug("model statement,length: %s,%s", args['model'], len(args['model']))
            code += "model %s;\n" % (args['model'])
        if 'contrast' in args:
            logging.debug("contrast statement,length: %s,%s", args['contrast'], len(args['contrast']))
            code += "contrast %s;\n" % (args['contrast'])
        if 'estimate' in args:
            logging.debug("estimate statement,length: %s,%s", args['estimate'], len(args['estimate']))
            code += "estimate %s;\n" % (args['estimate'])
        if 'lsmeans' in args:
            logging.debug("lsmeans statement,length: %s,%s", args['lsmeans'], len(args['lsmeans']))
            code += "lsmeans %s;\n" % (args['lsmeans'])
        if 'test' in args:
            logging.debug("test statement,length: %s,%s", args['test'], len(args['test']))
            code += "test %s;\n" % (args['test'])
        if 'manova' in args:
            logging.debug("manova statement,length: %s,%s", args['manova'], len(args['manova']))
            code += "manova %s;\n" % (args['manova'])
        if 'means' in args:
            logging.debug("means statement,length: %s,%s", args['means'], len(args['means']))
            code += "means %s;\n" % (args['means'])
        if 'nloptions' in args:
            logger.debug("nloptions statement,length: %s,%s", args['nloptions'], len(args['nloptions']))
            code += "nloptions %s;\n" % (args['nloptions'])
        if 'oddsratio' in args:
            logging.debug("oddsratio statement,length: %s,%s", args['oddsratio'], len(args['oddsratio']))
            code += "oddsratio %s;\n" % (args['oddsratio'])
        if 'outarrays' in args:
            logger.debug("outarrays statement,length: %s,%s", args['outarrays'], len(args['outarrays']))
            code += "outarrays %s;\n" % (args['outarrays'])
        if 'outscalars' in args:
            logger.debug("outscalars statement,length: %s,%s", args['outscalars'], len(args['outscalars']))
            code += "outscalars %s;\n" % (args['outscalars'])
        if 'outlier' in args:
            logger.debug("outlier statement,length: %s,%s", args['outlier'], len(args['outlier']))
            code += "outlier %s;\n" % (args['outlier'])
        if 'parms' in args:
            logging.debug("parms statement,length: %s,%s", args['parms'], len(args['parms']))
            code += "parms %s;\n" % (args['parms'])
        if 'performance' in args:
            logger.debug("performance statement,length: %s,%s", args['performance'], len(args['performance']))
            code += "performance %s;\n" % (args['performance'])
        if 'ppplot' in args:
            logger.debug("ppplot statement,length: %s,%s", args['ppplot'], len(args['ppplot']))
            code += "ppplot %s;\n" % (args['ppplot'])
        if 'prior' in args:
            # TODO: check that distrbution is in the list
            logging.debug("prior statement,length: %s,%s", args['prior'], len(args['prior']))
            code += "prior %s;\n" % (args['prior'])
        if 'prog_stmts' in args:
            logger.debug("prog_stmts statement,length: %s,%s", args['prog_stmts'], len(args['prog_stmts']))
            code += " %s;\n" % (args['prog_stmts'])
        if 'probplot' in args:
            logger.debug("probplot statement,length: %s,%s", args['probplot'], len(args['probplot']))
            code += "probplot %s;\n" % (args['probplot'])
        if 'qqplot' in args:
            logger.debug("qqplot statement,length: %s,%s", args['qqplot'], len(args['qqplot']))
            code += "qqplot %s;\n" % (args['qqplot'])
        if 'random' in args:
            logging.debug("random statement,length: %s,%s", args['random'], len(args['random']))
            code += "random %s;\n" % (args['random'])
        if 'randomreg' in args:
            logger.debug("randomreg statement,length: %s,%s", args['randomreg'], len(args['randomreg']))
            code += "randomreg %s;\n" % (args['randomreg'])
        if 'repeated' in args:
            logging.debug("repeated statement,length: %s,%s", args['repeated'], len(args['repeated']))
            code += "repeated %s;\n" % (args['repeated'])
        if 'roc' in args:
            logging.debug("roc statement,length: %s,%s", args['roc'], len(args['roc']))
            code += "roc %s;\n" % (args['roc'])
        if 'season' in args:
            logger.debug("season statement,length: %s,%s", args['season'], len(args['season']))
            code += "season %s;\n" % (args['season'])
        if 'slope' in args:
            logger.debug("slope statement,length: %s,%s", args['slope'], len(args['slope']))
            code += "slope %s;\n" % (args['slope'])
        if 'splinereg' in args:
            logger.debug("splinereg statement,length: %s,%s", args['splinereg'], len(args['splinereg']))
            code += "splinereg %s;\n" % (args['splinereg'])
        if 'splineseason' in args:
            logger.debug("splineseason statement,length: %s,%s", args['splineseason'], len(args['splineseason']))
            code += "splineseason %s;\n" % (args['splineseason'])
        if 'trend' in args:
            logger.debug("trend statement,length: %s,%s", args['trend'], len(args['trend']))
            code += "trend %s;\n" % (args['trend'])
        if 'slice' in args:
            logging.debug("slice statement,length: %s,%s", args['slice'], len(args['slice']))
            code += "slice %s;\n" % (args['slice'])
        if 'spec' in args:
            logger.debug("spec statement,length: %s,%s", args['spec'], len(args['spec']))
            code += "spec %s;\n" % (args['spec'])
        if 'strata' in args:
            logging.debug("strata statement,length: %s,%s", args['strata'], len(args['strata']))
            code += "strata %s;\n" % (args['strata'])
        if 'score' in args:
            scoreds = args['score']
            code += "score out=%s.%s;\n" % (scoreds.libref, scoreds.table)
        # TODO: make sure target is a single variable
        if 'target' in args:
            logging.debug("target statement,length: %s,%s", args['target'], len(args['target']))
            code += "target %s;\n" % (args['target'])
        if 'train' in args:
            logging.debug("train statement,length: %s,%s", args['train'], len(args['train']))
            code += "train %s;\n" % (args['train'])
        # test moved
        if 'var' in args:
            logging.debug("var statement,length: %s,%s", args['var'], len(args['var']))
            code += "var %s;\n" % (args['var'])
        if 'weight' in args:
            # TODO: add check to make sure it is only one variable
            logging.debug("weight statement,length: %s,%s", args['weight'], len(args['weight']))
            code += "weight %s;\n" % (args['weight'])

        if 'grow' in args:
            logging.debug("grow statement,length: %s,%s", args['grow'], len(args['grow']))
            code += "grow %s;\n" % (args['grow'])
        if 'prune' in args:
            logging.debug("prune statement,length: %s,%s", args['prune'], len(args['prune']))
            code += "prune %s;\n" % (args['prune'])
        if 'rules' in args:
            logging.debug("rules statement,length: %s,%s", args['rules'], len(args['rules']))
            code += "rules %s;\n" % (args['rules'])
        if 'partition' in args:
            logging.debug("partition statement,length: %s,%s", args['partition'], len(args['partition']))
            code += "partition %s;\n" % (args['partition'])
        if 'out' in args:
            outds = args['out']
            outstr = outds.libref + '.' + outds.table
            code += "output out=%s;\n" % outstr
        if 'xchart' in args:
            logger.debug("xchart statement,length: %s,%s", args['xchart'], len(args['xchart']))
            code += "xchart %s;\n" % (args['xchart'])

        code += "run; quit; %mend;\n"
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype, data.table)
        logging.debug("Proc code submission: " + str(code))
        return code

    def _objectmethods(self, obj: str, *args) -> list:
        """
        This method parses the SAS log for artifacts (tables and graphics) that were created
        from the procedure method call

        :param obj: str -- proc object
        :param args: list likely none
        :return: list -- the tables and graphs available for tab complete
        """
        code = "%listdata("
        code += obj
        code += ");"
        logging.debug("Object Method macro call: " + str(code))
        res = self.sas.submit(code, "text")
        meth = res['LOG'].splitlines()
        for i in range(len(meth)):
            meth[i] = meth[i].lstrip().rstrip()
        logging.debug('SAS Log: ' + res['LOG'])
        objlist = meth[meth.index('startparse9878') + 1:meth.index('endparse9878')]
        logging.debug("PROC attr list: " + str(objlist))
        return objlist

    def _run_proc(self, procname: str, required_set: set, legal_set: set, **kwargs: dict):
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
        data = kwargs.pop('data', None)
        log = SASProcCommons._stmt_check(self, required_set, legal_set, kwargs)
        obj1 = []
        nosub = False
        objname = ''
        if not log:
            objtype = procname.lower()
            objname = procname[:3].lower() + self.sas._objcnt()  # translate to a libname so needs to be less than 8
            code = SASProcCommons._makeProcCallMacro(self, objtype, objname, data, kwargs)
            logging.debug(procname + " macro submission: " + str(code))
            if not self.sas.nosub:
                ll = self.sas.submit(code, "text")
                error = SASProcCommons._errorLog(ll['LOG'])
                isinstance(error, str)
                if len(error) > 1:
                    raise SyntaxError("ERROR in submission: \n%s" % error)
                log = ll['LOG']
                try:
                    obj1 = SASProcCommons._objectmethods(self, objname)
                    logging.debug(obj1)
                except Exception:
                    pass
            else:
                print(code)
                log = ''
                nosub = True
        else:
            print("Error in code submission")

        return SASresults(obj1, self.sas, objname, nosub, log)

    @staticmethod
    def _stmt_check(self, req: set, legal: set, stmt: dict) -> bool:
        """
        This method checks to make sure that the proc has all required statements and removes any statements
        aren't valid. Missing required statements is an error. Extra statements are not.
        :param req: set
        :param legal: set
        :param stmt: dict
        :return: binary
        """
        # debug the argument list
        if logging.getLogger().getEffectiveLevel() == 10:
            for k, v in stmt.items():
                if type(v) is str:
                    print("Key: " + k + ", Value: " + v)
                else:
                    print("Key: " + k + ", Value: " + str(type(v)))

        # required statements
        req_set = req
        if len(req_set):
            missing_set = req_set.difference(set(stmt.keys()))
            if missing_set:
                msg = "You are missing %d required statements:" % (len(missing_set))
                msg += "\n" + str(missing_set)
                print(msg)
                return msg

        # legal statements
        legal_set = legal
        if len(legal_set):
            if len(req_set):
                tot_set = legal_set | req_set
            else:
                tot_set = legal_set
            extra_set = set(stmt.keys()).difference(tot_set)  # find keys not in legal or required sets
            if extra_set:
                print("The following %d statements are invalid and will be ignored: " % len(extra_set))
                print(extra_set)
        return None
