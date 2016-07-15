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
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sas = session
        logging.debug("Initialization of SAS Macro: " + self.sas.saslog())

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
        plot = ''
        outmeth = ''
        procopts = ''
        if self.sasproduct.lower() == 'stat':
            outmeth = ''
            plot = 'plot=all'
        if self.sasproduct.lower() == 'qc':
            outmeth = ''
            plot = ''
        if self.sasproduct.lower() == 'ets':
            outmeth = 'out'
            plot = 'plots=all'
        if self.sasproduct.lower() == 'em':
            outmeth = ''
            plot = ''
        if self.sasproduct.lower() == 'dmml':
            outmeth = 'out'
            plot = ''
        self.logger.debug("product caller: " + self.sasproduct.lower())
        code = "%macro proccall(d);\n"
        # resolve issues withe Proc options, out= and plots=
        # The procopts statement should be in every procedure as a way to pass arbitrary options to the procedures
        if 'procopts' in args:
            self.logger.debug("procopts statement,length: %s,%s", args['procopts'], len(args['procopts']))
            procopts = args['procopts']
        if 'outmeth' in args:
            outmeth = args['outmeth']
        if 'plot' in args:
            plot = args['plot']
        if len(outmeth) and 'out' in args:
            outds = args['out']
            outstr = outds.libref + '.' + outds.table
            code += "proc %s data=%s.%s %s %s=%s %s ;\n" % (objtype, data.libref, data.table, plot, outmeth, outstr, procopts)
        else:
            code += "proc %s data=%s.%s %s %s ;\n" % (objtype, data.libref, data.table, plot, procopts)
        self.logger.debug("args value: " + str(args))
        self.logger.debug("args type: " + str(type(args)))

        # this list is largely alphabetical but there are exceptions in order to
        # satisfy the order needs of the statements for the procedure
        # as an example... http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_glm_syntax.htm#statug.glm.glmpostable
        if 'absorb' in args:
            self.logger.debug("absorb statement,length: %s,%s", args['absorb'], len(args['absorb']))
            code += "absorb %s;\n" % (args['absorb'])
        if 'add' in args:
            self.logger.debug("add statement,length: %s,%s", args['add'], len(args['add']))
            code += "add %s;\n" % (args['add'])
        # only three valid values logistic, mlp, mlp direct
        if 'architecture' in args:
            self.logger.debug("architecture statement,length: %s,%s", args['architecture'], len(args['architecture']))
            if args['architecture'].lower().strip() in ['logistic', 'mlp', 'mlp direct']:
                code += "architecture %s;\n" % (args['architecture'])
            else:
                print("ERROR in code submission. ARCHITECTURE can only have one of these")
                print("values -- ['logistic', 'mlp', 'mlp direct'] you submitted: %s", args['architecture'])
        if 'autoreg' in args:
            self.logger.debug("autoreg statement,length: %s,%s", args['autoreg'], len(args['autoreg']))
            code += "autoreg %s;\n" % (args['autoreg'])
        if 'blockseason' in args:
            self.logger.debug("blockseason statement,length: %s,%s", args['blockseason'], len(args['blockseason']))
            code += "blockseason %s;\n" % (args['blockseason'])
        if 'by' in args:
            self.logger.debug("by statement,length: %s,%s", args['by'], len(args['by']))
            code += "by %s;\n" % (args['by'])
        if 'cdfplot' in args:
            self.logger.debug("cdfplot statement,length: %s,%s", args['cdfplot'], len(args['cdfplot']))
            code += "cdfplot %s;\n" % (args['cdfplot'])
        if 'cls' in args:
            self.logger.debug("class statement,length: %s,%s", args['cls'], len(args['cls']))
            code += "class %s;\n" % (args['cls'])
            #   if 'class' in args:
            #       self.logger.debug("class statement,length: %s,%s", args['class'], len(args['class']))
            #       code += "class %s;\n" % (args['class'])
        if 'comphist' in args:
            self.logger.debug("comphistogram statement,length: %s,%s", args['comphist'], len(args['comphist']))
            code += "comphist %s;\n" % (args['comphist'])
        # contrast moved
        if 'corr' in args:
            self.logger.debug("corr statement,length: %s,%s", args['corr'], len(args['corr']))
            code += "corr %s;\n" % (args['corr'])
        if 'crosscorr' in args:
            self.logger.debug("crosscorr statement,length: %s,%s", args['crosscorr'], len(args['crosscorr']))
            code += "crosscorr %s;\n" % (args['crosscorr'])
        if 'crossvar' in args:
            self.logger.debug("crossvar statement,length: %s,%s", args['crossvar'], len(args['crossvar']))
            code += "crossvar %s;\n" % (args['crossvar'])
        if 'cycle' in args:
            self.logger.debug("cycle statement,length: %s,%s", args['cycle'], len(args['cycle']))
            code += "cycle %s;\n" % (args['cycle'])
        if 'decomp' in args:
            self.logger.debug("decomp statement,length: %s,%s", args['decomp'], len(args['decomp']))
            code += "decomp %s;\n" % (args['decomp'])
        if 'deplag' in args:
            self.logger.debug("deplag statement,length: %s,%s", args['deplag'], len(args['deplag']))
            code += "deplag %s;\n" % (args['deplag'])
        if 'effect' in args:
            self.logger.debug("effect statement,length: %s,%s", args['effect'], len(args['effect']))
            code += "effect %s;\n" % (args['effect'])
        # estimate moved
        if 'fcmport' in args:
            self.logger.debug("fcmport statement,length: %s,%s", args['fcmport'], len(args['fcmport']))
            code += "fcmport %s;\n" % (args['fcmport'])
        if 'freq' in args:
            # add check to make sure it is only one variable
            self.logger.debug("freq statement,length: %s,%s", args['freq'], len(args['freq']))
            # check to make sure it is only one variable
            if len(args['freq'].split()) == 1:
                code += "freq %s;\n" % (args['freq'])
            else:
                raise SyntaxError("ERROR in code submission. FREQ can only have one variable and you submitted: %s", args['freq'])
        if 'forecast' in args:
            self.logger.debug("forecast statement,length: %s,%s", args['forecast'], len(args['forecast']))
            code += "forecast %s;\n" % (args['forecast'])
        # handle a string or list of strings
        if 'hidden' in args:
            if isinstance(args['hidden'], (str,int)):
                self.logger.debug("hidden statement,length: %s,%s", str(args['hidden']), len(str(args['hidden'])))
                code +=  "hidden %s;\n" % (str(args['hidden']))
            else:
                for item in args['hidden']:
                    code += "hidden %s;\n" % item
        if 'histogram' in args:
            self.logger.debug("histogram statement,length: %s,%s", args['histogram'], len(args['histogram']))
            code += "histogram %s;\n" % (args['histogram'])
        if 'id' in args:
            self.logger.debug("id statement,length: %s,%s", args['id'], len(args['id']))
            code += "id %s;\n" % (args['id'])
        if 'identify' in args:
            self.logger.debug("identify statement,length: %s,%s", args['identify'], len(args['identify']))
            code += "identify %s;\n" % (args['identify'])
        if 'input' in args:
            if isinstance(args['input'], str):
                self.logger.debug("input statement,length: %s,%s", args['input'], len(args['input']))
                code += "input %s;\n" % (args['input'])
            else:
                for item in args['input']:
                    code += "input %s;\n" % item
        if 'inset' in args:
            self.logger.debug("inset statement,length: %s,%s", args['inset'], len(args['inset']))
            code += "inset %s;\n" % (args['inset'])
        if 'intervals' in args:
            self.logger.debug("intervals statement,length: %s,%s", args['intervals'], len(args['intervals']))
            code += "intervals %s;\n" % (args['intervals'])
        if 'irregular' in args:
            self.logger.debug("irregular statement,length: %s,%s", args['irregular'], len(args['irregular']))
            code += "irregular %s;\n" % (args['irregular'])
        if 'level' in args:
            self.logger.debug("level statement,length: %s,%s", args['level'], len(args['level']))
            code += "level %s;\n" % (args['level'])
        # lsmeans moved
        # manova moved
        # means moved
        if 'model' in args:
            self.logger.debug("model statement,length: %s,%s", args['model'], len(args['model']))
            code += "model %s;\n" % (args['model'])
        if 'contrast' in args:
            self.logger.debug("contrast statement,length: %s,%s", args['contrast'], len(args['contrast']))
            code += "contrast %s;\n" % (args['contrast'])
        if 'estimate' in args:
            self.logger.debug("estimate statement,length: %s,%s", args['estimate'], len(args['estimate']))
            code += "estimate %s;\n" % (args['estimate'])
        if 'lsmeans' in args:
            self.logger.debug("lsmeans statement,length: %s,%s", args['lsmeans'], len(args['lsmeans']))
            code += "lsmeans %s;\n" % (args['lsmeans'])
        if 'test' in args:
            self.logger.debug("test statement,length: %s,%s", args['test'], len(args['test']))
            code += "test %s;\n" % (args['test'])
        if 'manova' in args:
            self.logger.debug("manova statement,length: %s,%s", args['manova'], len(args['manova']))
            code += "manova %s;\n" % (args['manova'])
        if 'means' in args:
            self.logger.debug("means statement,length: %s,%s", args['means'], len(args['means']))
            code += "means %s;\n" % (args['means'])
        if 'nloptions' in args:
            self.logger.debug("nloptions statement,length: %s,%s", args['nloptions'], len(args['nloptions']))
            code += "nloptions %s;\n" % (args['nloptions'])
        if 'oddsratio' in args:
            self.logger.debug("oddsratio statement,length: %s,%s", args['oddsratio'], len(args['oddsratio']))
            code += "oddsratio %s;\n" % (args['oddsratio'])
        if 'outarrays' in args:
            self.logger.debug("outarrays statement,length: %s,%s", args['outarrays'], len(args['outarrays']))
            code += "outarrays %s;\n" % (args['outarrays'])
        if 'outscalars' in args:
            self.logger.debug("outscalars statement,length: %s,%s", args['outscalars'], len(args['outscalars']))
            code += "outscalars %s;\n" % (args['outscalars'])
        if 'outlier' in args:
            self.logger.debug("outlier statement,length: %s,%s", args['outlier'], len(args['outlier']))
            code += "outlier %s;\n" % (args['outlier'])
        if 'parms' in args:
            self.logger.debug("parms statement,length: %s,%s", args['parms'], len(args['parms']))
            code += "parms %s;\n" % (args['parms'])
        if 'performance' in args:
            self.logger.debug("performance statement,length: %s,%s", args['performance'], len(args['performance']))
            code += "performance %s;\n" % (args['performance'])
        if 'ppplot' in args:
            self.logger.debug("ppplot statement,length: %s,%s", args['ppplot'], len(args['ppplot']))
            code += "ppplot %s;\n" % (args['ppplot'])
        if 'prior' in args:
            # TODO: check that distribution is in the list
            self.logger.debug("prior statement,length: %s,%s", args['prior'], len(args['prior']))
            code += "prior %s;\n" % (args['prior'])
        if 'prog_stmts' in args:
            self.logger.debug("prog_stmts statement,length: %s,%s", args['prog_stmts'], len(args['prog_stmts']))
            code += " %s;\n" % (args['prog_stmts'])
        if 'probplot' in args:
            self.logger.debug("probplot statement,length: %s,%s", args['probplot'], len(args['probplot']))
            code += "probplot %s;\n" % (args['probplot'])
        if 'qqplot' in args:
            self.logger.debug("qqplot statement,length: %s,%s", args['qqplot'], len(args['qqplot']))
            code += "qqplot %s;\n" % (args['qqplot'])
        if 'random' in args:
            self.logger.debug("random statement,length: %s,%s", args['random'], len(args['random']))
            code += "random %s;\n" % (args['random'])
        if 'randomreg' in args:
            self.logger.debug("randomreg statement,length: %s,%s", args['randomreg'], len(args['randomreg']))
            code += "randomreg %s;\n" % (args['randomreg'])
        if 'repeated' in args:
            self.logger.debug("repeated statement,length: %s,%s", args['repeated'], len(args['repeated']))
            code += "repeated %s;\n" % (args['repeated'])
        if 'roc' in args:
            self.logger.debug("roc statement,length: %s,%s", args['roc'], len(args['roc']))
            code += "roc %s;\n" % (args['roc'])
        if 'season' in args:
            self.logger.debug("season statement,length: %s,%s", args['season'], len(args['season']))
            code += "season %s;\n" % (args['season'])
        if 'slope' in args:
            self.logger.debug("slope statement,length: %s,%s", args['slope'], len(args['slope']))
            code += "slope %s;\n" % (args['slope'])
        if 'splinereg' in args:
            self.logger.debug("splinereg statement,length: %s,%s", args['splinereg'], len(args['splinereg']))
            code += "splinereg %s;\n" % (args['splinereg'])
        if 'splineseason' in args:
            self.logger.debug("splineseason statement,length: %s,%s", args['splineseason'], len(args['splineseason']))
            code += "splineseason %s;\n" % (args['splineseason'])
        if 'trend' in args:
            self.logger.debug("trend statement,length: %s,%s", args['trend'], len(args['trend']))
            code += "trend %s;\n" % (args['trend'])
        if 'slice' in args:
            self.logger.debug("slice statement,length: %s,%s", args['slice'], len(args['slice']))
            code += "slice %s;\n" % (args['slice'])
        if 'spec' in args:
            self.logger.debug("spec statement,length: %s,%s", args['spec'], len(args['spec']))
            code += "spec %s;\n" % (args['spec'])
        if 'strata' in args:
            self.logger.debug("strata statement,length: %s,%s", args['strata'], len(args['strata']))
            code += "strata %s;\n" % (args['strata'])
        if 'score' in args:
            scoreds = args['score']
            code += "score out=%s.%s;\n" % (scoreds.libref, scoreds.table)
        if 'target' in args:
            self.logger.debug("target statement,length: %s,%s", args['target'], len(args['target']))
            # make sure target is a single variable extra split to account for level= option
            if len(args['target'].split('/')[0].split()) == 1:
                code += "target %s;\n" % (args['target'])
            else:
                raise SyntaxError("ERROR in code submission. TARGET can only have one variable and you submitted: %s" % args['target'])
        if 'train' in args:
            self.logger.debug("train statement,length: %s,%s", args['train'], len(args['train']))
            code += "train %s;\n" % (args['train'])
        # test moved
        if 'var' in args:
            self.logger.debug("var statement,length: %s,%s", args['var'], len(args['var']))
            code += "var %s;\n" % (args['var'])
        if 'weight' in args:
            self.logger.debug("weight statement,length: %s,%s", args['weight'], len(args['weight']))
            # check to make sure it is only one variable
            if len(args['weight'].split()) == 1:
                code += "weight %s;\n" % (args['weight'])
            else:
                raise SyntaxError("ERROR in code submission. WEIGHT can only have one variable and you submitted: %s", args['weight'])
        if 'grow' in args:
            self.logger.debug("grow statement,length: %s,%s", args['grow'], len(args['grow']))
            code += "grow %s;\n" % (args['grow'])
        if 'prune' in args:
            self.logger.debug("prune statement,length: %s,%s", args['prune'], len(args['prune']))
            code += "prune %s;\n" % (args['prune'])
        if 'rules' in args:
            self.logger.debug("rules statement,length: %s,%s", args['rules'], len(args['rules']))
            code += "rules %s;\n" % (args['rules'])
        if 'partition' in args:
            self.logger.debug("partition statement,length: %s,%s", args['partition'], len(args['partition']))
            code += "partition %s;\n" % (args['partition'])
        if 'out' in args and not len(outmeth):
            outds = args['out']
            outstr = outds.libref + '.' + outds.table
            code += "output out=%s;\n" % outstr
        if 'xchart' in args:
            self.logger.debug("xchart statement,length: %s,%s", args['xchart'], len(args['xchart']))
            code += "xchart %s;\n" % (args['xchart'])

        code += "run; quit; %mend;\n"
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype, data.table)
        self.logger.debug("Proc code submission: " + str(code))
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
        self.logger.debug("Object Method macro call: " + str(code))
        res = self.sas.submit(code, "text")
        meth = res['LOG'].splitlines()
        for i in range(len(meth)):
            meth[i] = meth[i].lstrip().rstrip()
        self.logger.debug('SAS Log: ' + res['LOG'])
        objlist = meth[meth.index('startparse9878') + 1:meth.index('endparse9878')]
        self.logger.debug("PROC attr list: " + str(objlist))
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
        verifiedKwargs = SASProcCommons._stmt_check(self, required_set, legal_set, kwargs)
        print(verifiedKwargs)
        obj1 = []
        nosub = False
        objname = ''
        log = ''
        if len(verifiedKwargs):
            objtype = procname.lower()
            objname = procname[:3].lower() + self.sas._objcnt()  # translate to a libname so needs to be less than 8
            code = SASProcCommons._makeProcCallMacro(self, objtype, objname, data, verifiedKwargs)
            self.logger.debug(procname + " macro submission: " + str(code))
            if not self.sas.nosub:
                ll = self.sas.submit(code, "text")
                log = ll['LOG']
                error = SASProcCommons._errorLog(log)
                isinstance(error, str)
                if len(error) > 1:
                    print("SubmissionError: ERRORS found in SAS log: \n%s" % error)
                    return SASresults(obj1, self.sas, objname, nosub, log)
                try:
                    obj1 = SASProcCommons._objectmethods(self, objname)
                    self.logger.debug(obj1)
                except Exception:
                    pass
            else:
                print(code)
                nosub = True
        else:
            print("Error in code submission")

        return SASresults(obj1, self.sas, objname, nosub, log)

    @staticmethod
    def _stmt_check(self, req: set, legal: set, stmt: dict) -> dict:
        """
        This method checks to make sure that the proc has all required statements and removes any statements
        aren't valid. Missing required statements is an error. Extra statements are not.
        :param req: set
        :param legal: set
        :param stmt: dict
        :return: dictonary of verified statements
        """
        # debug the argument list
        if self.logger.level == 10:
            for k, v in stmt.items():
                if type(v) is str:
                    print("Key: " + k + ", Value: " + v)
                else:
                    print("Key: " + k + ", Value: " + str(type(v)))

        # required statements
        reqSet = req
        if len(reqSet):
            missing_set = reqSet.difference(set(stmt.keys()))
            if missing_set:
                raise SyntaxError("You are missing %d required statements:\n%s" % (len(missing_set), str(missing_set)))

        # legal statements
        legalSet = legal
        if len(legalSet):
            if len(reqSet):
                totSet = legalSet | reqSet
            else:
                totSet = legalSet
            extraSet = set(stmt.keys()).difference(totSet)  # find keys not in legal or required sets
            if extraSet:
                for item in extraSet:
                    stmt.pop(item, None)
                print("The following %d statements are invalid and will be ignored: " % len(extraSet))
                print(extraSet)
        return stmt
