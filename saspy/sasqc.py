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
import os
from saspy.sasresults import SASresults

# create logger
logger = logging.getLogger('')
logger.setLevel(logging.WARN)

class SASqc:
    def __init__(self, session, *args, **kwargs):
        """Submit an initial set of macros to prepare the SAS system"""
        self.sas = session
        macro_path = os.path.dirname(os.path.realpath(__file__))
        code = "options pagesize=max; %include '" + macro_path + '/' + "libname_gen.sas'; "
        self.sas._asubmit(code, "text")

        logger.debug("Initialization of SAS Macro: " + str(self.sas._getlog()))

    def _objectmethods(self, obj: str, *args):
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
        logger.debug("Object Method macro call: " + str(code))
        res = self.sas.submit(code, "text")
        meth = res['LOG'].splitlines()
        logger.debug('SAS Log: ' + res['LOG'])
        objlist = meth[meth.index('startparse9878') + 1:meth.index('endparse9878')]
        logger.debug("PROC attr list: " + str(objlist))
        return objlist

    def _makeProcCallMacro(self, objtype: str, objname: str, data: object =None, args: dict =None):
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
        code += "proc %s data=%s.%s plots=all;\n" % (objtype, data.libref, data.table)
        logger.debug("args value: " + str(args))
        logger.debug("args type: " + str(type(args)))
        # this list is largely alphabetical but there are exceptions in order to
        # satisfy the order needs of the statements for the procedure
        # as an example... http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_glm_syntax.htm#statug.glm.glmpostable

        if 'by' in args:
            logger.debug("by statement,length: %s,%s", args['by'], len(args['by']))
            code += "by %s;\n" % (args['by'])

        if 'cdfplot' in args:
            logger.debug("cdfplot statement,length: %s,%s", args['cdfplot'], len(args['cdfplot']))
            code += "cdfplot %s;\n" % (args['cdfplot'])

        if 'class' in args:
            logger.debug("class statement,length: %s,%s", args['class'], len(args['class']))
            code += "class %s;\n" % (args['class'])

        if 'comphist' in args:
            logger.debug("comphistogram statement,length: %s,%s", args['comphist'], len(args['comphist']))
            code += "comphist %s;\n" % (args['comphist'])

        if 'freq' in args:
            logger.debug("freq statement,length: %s,%s", args['freq'], len(args['freq']))
            code += "freq %s;\n" % (args['freq'])

        if 'histogram' in args:
            logger.debug("histogram statement,length: %s,%s", args['histogram'], len(args['histogram']))
            code += "histogram %s;\n" % (args['histogram'])

        if 'id' in args:
            logger.debug("id statement,length: %s,%s", args['id'], len(args['id']))
            code += "id %s;\n" % (args['id'])

        if 'inset' in args:
            logger.debug("inset statement,length: %s,%s", args['inset'], len(args['inset']))
            code += "inset %s;\n" % (args['inset'])

        if 'intervals' in args:
            logger.debug("intervals statement,length: %s,%s", args['intervals'], len(args['intervals']))
            code += "intervals %s;\n" % (args['intervals'])

        if 'output' in args:
            logger.debug("output statement,length: %s,%s", args['output'], len(args['output']))
            # TODO: If output and proc capability must have a 'var' statement
            code += "output %s;\n" % (args['output'])

        if 'ppplot' in args:
            logger.debug("ppplot statement,length: %s,%s", args['ppplot'], len(args['ppplot']))
            code += "ppplot %s;\n" % (args['ppplot'])

        if 'probplot' in args:
            logger.debug("probplot statement,length: %s,%s", args['probplot'], len(args['probplot']))
            code += "probplot %s;\n" % (args['probplot'])

        if 'qqplot' in args:
            logger.debug("qqplot statement,length: %s,%s", args['qqplot'], len(args['qqplot']))
            code += "qqplot %s;\n" % (args['qqplot'])

        if 'spec' in args:
            logger.debug("spec statement,length: %s,%s", args['spec'], len(args['spec']))
            code += "spec %s;\n" % (args['spec'])

        if 'var' in args:
            logger.debug("var statement,length: %s,%s", args['var'], len(args['var']))
            code += "var %s;\n" % (args['var'])

        if 'weight' in args:
            logger.debug("weight statement,length: %s,%s", args['weight'], len(args['weight']))
            code += "weight %s;\n" % (args['weight'])

        if 'xchart' in args:
            logger.debug("xchart statement,length: %s,%s", args['xchart'], len(args['xchart']))
            code += "xchart %s;\n" % (args['xchart'])

        if 'out' in args:
            outds = args['out']
            outstr = outds.libref+'.'+outds.table
            code += "output out=%s;\n" % (outstr)

        code += "run; quit; %mend;\n"
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype, data.table)
        logger.debug("Proc code submission: " + str(code))
        return code

    def _stmt_check(self, req: set, legal: set, stmt: dict):
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
                print("Key: " + k + ", Value: " + v)
        # required statements
        req_set = req
        if len(req_set):
            missing_set = req_set.difference(set(stmt.keys()))
            if missing_set:
                msg  = "You are missing %d required statements:" % (len(missing_set))
                msg += "\n"+str(missing_set)
                print(msg)
                return msg

        # legal statements
        legal_set = legal
        if len(legal_set):
            extra_set = set(stmt.keys()).difference(legal_set | req_set)  # find keys not in legal or required sets
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
            objname='qc'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
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

    def cusum(self, **kwargs):
        """
        Python method to call the CUSUM procedure
        required_set = {}
        legal_set = {'by','xchart'}
        Documentation link:
        http://support.sas.com/documentation/cdl/en/qcug/68161/HTML/default/viewer.htm#qcug_cusum_sect001.htm
        """
        required_set = {}
        legal_set = {'by','xchart'}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return self._run_proc("CUSUM", required_set, legal_set, **kwargs)

    def macontrol(self, **kwargs):
        """
        Python method to call the MACONTROL procedure

        Documentation link:
        http://support.sas.com/documentation/cdl/en/qcug/68161/HTML/default/viewer.htm#qcug_macontrol_toc.htm
        """
        required_set = {}
        legal_set = {}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return self._run_proc("MACONTROL", required_set, legal_set, **kwargs)

    def capability(self, **kwargs):
        """
        Python method to call the CUSUM procedure
        required_set = {}
        legal_set = {'cdfplot', 'comphist', 'histogram', 'inset', 'intervals', 'output', 'ppplot', 'probplot',
                     'qqplot', 'freq', 'weight', 'id', 'by', 'spec'}
        Documentation link:
        http://support.sas.com/documentation/cdl/en/qcug/68161/HTML/default/viewer.htm#qcug_capability_sect001.htm
        """
        required_set = {}
        legal_set = {'cdfplot', 'comphist', 'histogram', 'inset', 'intervals', 'output', 'ppplot', 'probplot',
                     'qqplot', 'freq', 'weight', 'id', 'by', 'spec', 'out'}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return self._run_proc("CAPABILITY", required_set, legal_set, **kwargs)

    def shewhart(self, **kwargs):
        """
        Python method to call the SHEWHART procedure\n
        Documentation link:
        http://support.sas.com/documentation/cdl/en/qcug/68161/HTML/default/viewer.htm#qcug_shewhart_toc.htm
        """
        required_set = {}
        legal_set = {}
        logger.debug("kwargs type: " + str(type(kwargs)))
        return self._run_proc("SHEWHART", required_set, legal_set, **kwargs)

