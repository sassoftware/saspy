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


class SASml:
    def __init__(self, session, *args, **kwargs):
        """
        Submit an initial set of macros to prepare the SAS system
        """
        self.sas=session
        logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

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
        res=self.sas.submit(code,"text")
        meth = res['LOG'].splitlines()
        for i in range(len(meth)):
           meth[i] = meth[i].lstrip().rstrip()
        logger.debug('SAS Log: ' + res['LOG'])
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
        code += "proc %s data=%s.%s ;\n" % (objtype, data.libref, data.table)
        logger.debug("args value: " + str(args))
        logger.debug("args type: " + str(type(args)))
        # this list is largely alphabetical but there are exceptions in order to
        # satisfy the order needs of the statements for the procedure
        # as an example... http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_glm_syntax.htm#statug.glm.glmpostable

        if 'absorb' in args:
            logger.debug("absorb statement,length: %s,%s", args['absorb'], len(args['absorb']))
            code += "absorb %s;\n" % (args['absorb'])
        if 'add' in args:
            logger.debug("add statement,length: %s,%s", args['add'], len(args['add']))
            code += "add %s;\n" % (args['add'])
        # Todo: only three valid values logistic, mlp, mlp direct
        if 'architecture' in args:
            logger.debug("architecture statement,length: %s,%s", args['architecture'], len(args['architecture']))
            code += "architecture %s;\n" % (args['architecture'])
        if 'by' in args:
            logger.debug("by statement,length: %s,%s", args['by'], len(args['by']))
            code += "by %s;\n" % (args['by'])
        if 'cls' in args:
            logger.debug("class statement,length: %s,%s", args['cls'], len(args['cls']))
            code += "class %s;\n" % (args['cls'])
        # contrast moved
        if 'effect' in args:
            logger.debug("effect statement,length: %s,%s", args['effect'], len(args['effect']))
            code += "effect %s;\n" % (args['effect'])
        # estimate moved
        if 'freq' in args:
            # TODO: add check to make sure it is only one variable
            logger.debug("freq statement,length: %s,%s", args['freq'], len(args['freq']))
            code += "freq %s;\n" % (args['freq'])
        # TODO: make a dictonary?
        if 'hidden' in args:
            logger.debug("hidden statement,length: %s,%s", args['hidden'], len(args['hidden']))
            code += "hidden %s;\n" % (args['hidden'])
        if 'id' in args:
            logger.debug("id statement,length: %s,%s", args['id'], len(args['id']))
            code += "id %s;\n" % (args['id'])
        if 'input' in args:
            logger.debug("input statement,length: %s,%s", args['input'], len(args['input']))
            code += "input %s;\n" % (args['input'])
        # lsmeans moved
        # manova moved
        # means moved
        if 'model' in args:
            logger.debug("model statement,length: %s,%s", args['model'], len(args['model']))
            code += "model %s;\n" % (args['model'])
        if 'contrast' in args:
            logger.debug("contrast statement,length: %s,%s", args['contrast'], len(args['contrast']))
            code += "contrast %s;\n" % (args['contrast'])
        if 'estimate' in args:
            logger.debug("estimate statement,length: %s,%s", args['estimate'], len(args['estimate']))
            code += "estimate %s;\n" % (args['estimate'])
        if 'lsmeans' in args:
            logger.debug("lsmeans statement,length: %s,%s", args['lsmeans'], len(args['lsmeans']))
            code += "lsmeans %s;\n" % (args['lsmeans'])
        if 'test' in args:
            logger.debug("test statement,length: %s,%s", args['test'], len(args['test']))
            code += "test %s;\n" % (args['test'])
        if 'manova' in args:
            logger.debug("manova statement,length: %s,%s", args['manova'], len(args['manova']))
            code += "manova %s;\n" % (args['manova'])
        if 'means' in args:
            logger.debug("means statement,length: %s,%s", args['means'], len(args['means']))
            code += "means %s;\n" % (args['means'])
        if 'oddsratio' in args:
            logger.debug("oddsratio statement,length: %s,%s", args['oddsratio'], len(args['oddsratio']))
            code += "oddsratio %s;\n" % (args['oddsratio'])
        if 'parms' in args:
            logger.debug("parms statement,length: %s,%s", args['parms'], len(args['parms']))
            code += "parms %s;\n" % (args['parms'])
        if 'prior' in args:
            # TODO: check that distrbution is in the list
            logger.debug("prior statement,length: %s,%s", args['prior'], len(args['prior']))
            code += "prior %s;\n" % (args['prior'])
        if 'random' in args:
            logger.debug("random statement,length: %s,%s", args['random'], len(args['random']))
            code += "random %s;\n" % (args['random'])
        if 'repeated' in args:
            logger.debug("repeated statement,length: %s,%s", args['repeated'], len(args['repeated']))
            code += "repeated %s;\n" % (args['repeated'])
        if 'roc' in args:
            logger.debug("roc statement,length: %s,%s", args['roc'], len(args['roc']))
            code += "roc %s;\n" % (args['roc'])
        if 'slice' in args:
            logger.debug("slice statement,length: %s,%s", args['slice'], len(args['slice']))
            code += "slice %s;\n" % (args['slice'])
        if 'strata' in args:
            logger.debug("strata statement,length: %s,%s", args['strata'], len(args['strata']))
            code += "strata %s;\n" % (args['strata'])
        if 'score' in args:
            scoreds = args['score']
            code += "score out=%s.%s;\n" % (scoreds.libref, scoreds.table)
        # TODO: make sure target is a single variable
        if 'target' in args:
            logger.debug("target statement,length: %s,%s", args['target'], len(args['target']))
            code += "target %s;\n" % (args['target'])
        if 'train' in args:
            logger.debug("train statement,length: %s,%s", args['train'], len(args['train']))
            code += "train %s;\n" % (args['train'])
        # test moved
        if 'var' in args:
            logger.debug("var statement,length: %s,%s", args['var'], len(args['var']))
            code += "var %s;\n" % (args['var'])
        if 'weight' in args:
            # TODO: add check to make sure it is only one variable
            logger.debug("weight statement,length: %s,%s", args['weight'], len(args['weight']))
            code += "weight %s;\n" % (args['weight'])

        if 'grow' in args:
            logger.debug("grow statement,length: %s,%s", args['grow'], len(args['grow']))
            code += "grow %s;\n" % (args['grow'])
        if 'prune' in args:
            logger.debug("prune statement,length: %s,%s", args['prune'], len(args['prune']))
            code += "prune %s;\n" % (args['prune'])
        if 'rules' in args:
            logger.debug("rules statement,length: %s,%s", args['rules'], len(args['rules']))
            code += "rules %s;\n" % (args['rules'])
        if 'partition' in args:
            logger.debug("partition statement,length: %s,%s", args['partition'], len(args['partition']))
            code += "partition %s;\n" % (args['partition'])
        if 'out' in args:
            outds = args['out']
            outstr = outds.libref+'.'+outds.table
            code += "output out=%s;\n" % (outstr)

        code += "run; quit; %mend;\n"
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype,data.table)
        logger.debug("Proc code submission: " + str(code))
        return code

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
        data=kwargs.pop('data',None)
        log = self._stmt_check(required_set, legal_set, kwargs)
        obj1=[]; nosub=False; objname='';
        if not log:
            objtype=procname.lower()
            objname='ml'+self.sas._objcnt()  # translate to a libname so needs to be less than 8
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

    def forest(self, **kwargs: dict) -> object:
        """
        Python method to call the HPFOREST procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target'}
        legal_set= {'freq', 'input', 'id', 'target', 'save', 'score'}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return self._run_proc("HPFOREST", required_set, legal_set, **kwargs)

    def cluster(self, **kwargs: dict) -> object:
        """
        Python method to call the HPCLUS procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input'}
        legal_set= {'freq', 'input', 'id', 'score'}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return self._run_proc("HPCLUS", required_set, legal_set, **kwargs)

    def neural(self, **kwargs: dict) -> object:
        """
        Python method to call the HPNEURAL procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        required_set = {'input', 'target', 'train'}
        legal_set= {'freq', 'input', 'id', 'target', 'save', 'score',
                    'architecture', 'weight', 'hidden', 'partition', 'train'}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return self._run_proc("HPNEURAL", required_set, legal_set, **kwargs)
    def svm(self, **kwargs: dict) -> object:
        """
        Python method to call the HPFOREST procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        pass

    def bnet(self, **kwargs: dict) -> object:
        """
        Python method to call the HPFOREST procedure

        Documentation link:
        https://support.sas.com/documentation/solutions/miner/emhp/14.1/emhpprcref.pdf
        :param kwargs: dict
        :return: SAS result object
        """
        pass


