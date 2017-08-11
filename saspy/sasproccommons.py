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
# from pdb import set_trace as bp


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
        # Set ODS graphic generation to True by default
        ODSGraphics = args.get('ODSGraphics', True)

        # The different SAS products vary slightly in plotting and out methods.
        # this block sets the options correctly for plotting and output statements
        if self.sasproduct.lower() == 'stat' and not ('ODSGraphics' in args.keys() or ODSGraphics == False) :
            outmeth = ''
            plot = 'plot=all'
        if self.sasproduct.lower() == 'qc':
            outmeth = ''
            plot = ''
        if self.sasproduct.lower() == 'ets' and not ('ODSGraphics' in args.keys() or ODSGraphics == False) :
            outmeth = 'out'
            plot = 'plot=all'
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
            code += "proc %s data=%s.%s%s %s %s=%s %s ;\n" % (
                objtype, data.libref, data.table, data._dsopts(), plot, outmeth, outstr, procopts)
        else:
            code += "proc %s data=%s.%s%s %s %s ;\n" % (objtype, data.libref, data.table, data._dsopts(), plot, procopts)
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
        if 'assess' in args:
            self.logger.debug("assess statement,length: %s,%s", args['assess'], len(args['assess']))
            code += "assess %s;\n" % (args['assess'])
        if 'autoreg' in args:
            self.logger.debug("autoreg statement,length: %s,%s", args['autoreg'], len(args['autoreg']))
            code += "autoreg %s;\n" % (args['autoreg'])
        if 'bayes' in args:
            self.logger.debug("bayes statement,length: %s,%s", args['bayes'], len(args['bayes']))
            code += "bayes %s;\n" % (args['bayes'])
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
            if isinstance(args['cls'], str):
                self.logger.debug("class statement,length: %s,%s", args['cls'], len(args['cls']))
                code += "class %s;\n" % (args['cls'])
            elif isinstance(args['cls'], list):
                code += "class %s;\n" % (' '.join(args['cls']))
        if 'code' in args:
            self.logger.debug("code statement,length: %s,%s", args['code'], len(args['code']))
            code += "code file='%s';\n" % (args['code'])
        # The save statement is used by few procs but it doesn't have a consistent pattern
        # Here we case it correctly or throw an error.
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
                raise SyntaxError("ERROR in code submission. FREQ can only have one variable and you submitted: %s",
                                  args['freq'])
        if 'forecast' in args:
            self.logger.debug("forecast statement,length: %s,%s", args['forecast'], len(args['forecast']))
            code += "forecast %s;\n" % (args['forecast'])
        # handle a string or list of strings
        if 'hidden' in args:
            if isinstance(args['hidden'], (str, int)):
                self.logger.debug("hidden statement,length: %s,%s", str(args['hidden']), len(str(args['hidden'])))
                code += "hidden %s;\n" % (str(args['hidden']))
            else:
                for item in args['hidden']:
                    code += "hidden %s;\n" % item
        if 'id' in args:
            self.logger.debug("id statement,length: %s,%s", args['id'], len(args['id']))
            code += "id %s;\n" % (args['id'])
        if 'histogram' in args:
            self.logger.debug("histogram statement,length: %s,%s", args['histogram'], len(args['histogram']))
            code += "histogram %s;\n" % (args['histogram'])
        if 'hazardratio' in args:
            self.logger.debug("hazardratio statement,length: %s,%s", args['hazardratio'], len(args['hazardratio']))
            code += "hazardratio %s;\n" % (args['id'])
        if 'identify' in args:
            self.logger.debug("identify statement,length: %s,%s", args['identify'], len(args['identify']))
            code += "identify %s;\n" % (args['identify'])
        if 'impute' in args:
            self.logger.debug("impute statement,length: %s,%s", args['impute'], len(args['impute']))
            if not (isinstance(args['impute'], dict) or isinstance(args['impute'], str)):
                raise SyntaxError("IMPUTE must be a dictionary: %s" % str(type(args['impute'])))
            if isinstance(args['impute'], dict):
                usedVars = []
                tup_code = ''
                contantValues = args['impute'].pop('value', None)
                if contantValues is not None:
                    if not all(isinstance(x, tuple) for x in contantValues):
                        raise SyntaxError("The elements in the 'value' key must be tuples")
                    for t in contantValues:
                        tup_code += "impute %s / value = %s;\n" % (t[0], t[1])
                        usedVars.append(t[0])
                meth_code = ''
                for key, values in args['impute'].items():
                    for v in values:
                        meth_code += 'impute %s / method = %s;\n' % (v, key)
                        usedVars.append(v)
                code += '\ninput ' + ' '.join(list(set(usedVars))) + ';\n' + tup_code + meth_code + 'run;'
            elif isinstance(args['impute'], str):
                code += "impute %s;\n" % (args['impute'])
        if 'input' in args:
            if isinstance(args['input'], str):
                self.logger.debug("input statement,length: %s,%s", args['input'], len(args['input']))
                code += "input %s;\n" % (args['input'])
            elif isinstance(args['input'], dict):
                try:
                    # fix var type names for HPNEURAL
                    nomstr = 'nominal'
                    intstr = 'interval'
                    if objtype.casefold() =='hpneural':
                        nomstr = 'nom'
                        intstr = 'int'
                    if 'interval' in args['input'].keys():
                        if isinstance(args['input']['interval'], str):
                            code += "input %s /level=%s;\n" % (args['input']['interval'], intstr)
                        if isinstance(args['input']['interval'], list):
                            code += "input %s /level=%s;\n" % (" ".join(args['input']['interval']), intstr )
                    if 'nominal' in args['input'].keys():
                        if isinstance(args['input']['nominal'], str):
                            code += "input %s /level=%s;\n" % (args['input']['nominal'], nomstr)
                        if isinstance(args['input']['nominal'], list):
                            code += "input %s /level=%s;\n" % (" ".join(args['input']['nominal']), nomstr)
                except:
                    raise SyntaxError("Proper Keys not found for INPUT dictionary: %s" % args['input'].keys())
            elif isinstance(args['input'], list):
                if len(args['input']) == 1:
                    code += "input %s;\n" % str(args['input'][0])
                elif len(args['input']) > 1:
                    code += "input %s;\n" % " ".join(args['input'])
                else:
                    raise SyntaxError("The input list has no members")
            else:
                raise SyntaxError("INPUT is in an unknown format: %s" % str(args['input']))
        if 'inset' in args:
            self.logger.debug("inset statement,length: %s,%s", args['inset'], len(args['inset']))
            code += "inset %s;\n" % (args['inset'])
        if 'intervals' in args:
            self.logger.debug("intervals statement,length: %s,%s", args['intervals'], len(args['intervals']))
            code += "intervals %s;\n" % (args['intervals'])
        if 'irregular' in args:
            if isinstance(args['irregular'], str):
                self.logger.debug("irregular statement,length: %s,%s", args['irregular'], len(args['irregular']))
                code += "irregular %s;\n" % (args['irregular'])
            elif isinstance(args['irregular'], bool) and args['irregular']:
                code += "irregular;\n"
            else:
                raise SyntaxError("irregular is in an unknown format: %s" % str(args['irregular']))
        if 'level' in args:
            if isinstance(args['level'], str):
                self.logger.debug("level statement,length: %s,%s", args['level'], len(args['level']))
                code += "level %s;\n" % (args['level'])
            elif isinstance(args['level'], bool) and args['level']:
                code += "level;\n"
            else:
                raise SyntaxError("level is in an unknown format: %s" % str(args['level']))
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
            if isinstance(args['estimate'], str):
                self.logger.debug("estimate statement,length: %s,%s", args['estimate'], len(args['estimate']))
                code += "estimate %s;\n" % (args['estimate'])
            elif isinstance(args['estimate'], bool) and args['estimate']:
                code += "estimate;\n"
            else:
                raise SyntaxError("estimate is in an unknown format: %s" % str(args['estimate']))
        if 'lsmeans' in args:
            self.logger.debug("lsmeans statement,length: %s,%s", args['lsmeans'], len(args['lsmeans']))
            code += "lsmeans %s;\n" % (args['lsmeans'])
        if 'lsmestimate' in args:
            self.logger.debug("lsmestimate statement,length: %s,%s", args['lsmestimate'], len(args['lsmestimate']))
            code += "lsmestimate %s;\n" % (args['lsmestimate'])
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
        if 'paired' in args:
            if isinstance(args['paired'], str):
                self.logger.debug("paired statement,length: %s,%s", args['paired'], len(args['paired']))
                code += "paired %s;\n" % (args['paired'])
            elif isinstance(args['paired'], list):
                if len(args['paired']) == 1:
                    code += "paired %s;\n" % str(args['paired'][0])
                elif len(args['paired']) > 1:
                    code += "paired %s;\n" % " ".join(args['paired'])
                else:
                    raise SyntaxError("The paired list has no members")
            else:
                raise SyntaxError("paired is in an unknown format: %s" % str(args['paired']))
        if 'parms' in args:
            self.logger.debug("parms statement,length: %s,%s", args['parms'], len(args['parms']))
            code += "parms %s;\n" % (args['parms'])
        if 'partial' in args:
            self.logger.debug("partial statement,length: %s,%s", args['partial'], len(args['partial']))
            code += "partial %s;\n" % (args['partial'])
        if 'pathdiagram' in args:
            self.logger.debug("pathdiagram statement,length: %s,%s", args['pathdiagram'], len(args['pathdiagram']))
            code += "pathdiagram %s;\n" % (args['pathdiagram'])
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
        if 'priors' in args:
            if isinstance(args['priors'], str):
                self.logger.debug("priors statement,length: %s,%s", args['priors'], len(args['priors']))
                code += "priors %s;\n" % (args['priors'])
            elif isinstance(args['priors'], list):
                if len(args['priors']) == 1:
                    code += "priors %s;\n" % str(args['priors'][0])
                elif len(args['priors']) > 1:
                    code += "priors %s;\n" % " ".join(args['priors'])
                else:
                    raise SyntaxError("The priors list has no members")
            else:
                raise SyntaxError("priors is in an unknown format: %s" % str(args['priors']))
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
        if 'selection' in args:
            if isinstance(args['selection'], str):
                if args['selection'].lower().strip() in ['none', 'forward', 'backward', 'stepwise', 'forwardswap',
                                                     'lar', 'lasso']:
                    self.logger.debug("selection statement,length: %s,%s", args['selection'], len(args['selection']))
                    code += "selection method=%s;\n" % (args['selection'])
            if isinstance(args['selection'], dict):
                if bool(args['selection']): # is the dictionary empty
                    m = args['selection'].pop('method', '')
                    me = args['selection'].pop('maxeffects', None)
                    if me is not None:
                        if int(me) > 0 and m != 'backward':
                            args['selection']['maxeffects'] = me
                    d = args['selection'].pop('details', '')
                    dstr = ''
                    if len(d) > 0:
                        dstr = 'details = %s' % d  
                    code += "selection method=%s (%s)  %s;"  % (m, ' '.join('{}={}'.format(key, val) for key, val in args['selection'].items()), dstr)
        if 'slope' in args:
            if isinstance(args['slope'], str):
                self.logger.debug("slope statement,length: %s,%s", args['slope'], len(args['slope']))
                code += "slope %s;\n" % (args['slope'])
            elif isinstance(args['slope'], bool) and args['slope']:
                code += "slope;\n"
            else:
                raise SyntaxError("slope is in an unknown format: %s" % str(args['slope']))
        if 'splinereg' in args:
            self.logger.debug("splinereg statement,length: %s,%s", args['splinereg'], len(args['splinereg']))
            code += "splinereg %s;\n" % (args['splinereg'])
        if 'splineseason' in args:
            self.logger.debug("splineseason statement,length: %s,%s", args['splineseason'], len(args['splineseason']))
            code += "splineseason %s;\n" % (args['splineseason'])
        if 'store' in args:
            self.logger.debug("store statement,length: %s,%s", args['store'], len(args['store']))
            code += "store %s;\n" % (args['store'])
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
        if 'target' in args:
            self.logger.debug("target statement,length: %s,%s", args['target'], len(args['target']))
            # make sure target is a single variable extra split to account for level= option
            if isinstance(args['target'], str):
                if len(args['target'].split('/')[0].split()) == 1:
                    code += "target %s;\n" % (args['target'])
                else:
                    raise SyntaxError(
                        "ERROR in code submission. TARGET can only have one variable and you submitted: %s" % args[
                            'target'])
            elif isinstance(args['target'], list):
                if len(args['target']) == 1:
                    code += "target %s;\n" % str(args['input'][0])
                else:
                    raise SyntaxError("The target list must have exactly one member")
            elif isinstance(args['target'], dict):
                try:
                    # check there there is only one target:
                    length=0
                    try:
                        length += len([args['target']['nominal'], args['target']['interval'] ])
                    except KeyError:
                        try:
                            length += len([args['target']['nominal']])
                        except KeyError:
                            try:
                                length += len([args['target']['interval']])
                            except KeyError:
                                raise
                    if length  == 1:
                        # fix var type names for HPNEURAL
                        nomstr = 'nominal'
                        intstr = 'interval'
                        targOpts = ''
                        try:
                            targOpts = ' '.join('{}={}'.format(key, val) for key, val in args['target']['targOpts'].items())
                        except:
                            pass
                        if objtype.casefold() == 'hpneural':
                            nomstr = 'nom'
                            intstr = 'int'
                        if 'interval' in args['target'].keys():
                            if isinstance(args['target']['interval'], str):
                                code += "target %s /level=%s %s;\n" % (args['target']['interval'], intstr, targOpts)
                            if isinstance(args['target']['interval'], list):
                                code += "target %s /level=%s %s;\n" % (" ".join(args['target']['interval']), intstr, targOpts)
                        if 'nominal' in args['target'].keys():
                            if isinstance(args['target']['nominal'], str):
                                code += "target %s /level=%s;\n" % (args['target']['nominal'], nomstr)
                            if isinstance(args['target']['nominal'], list):
                                code += "target %s /level=%s;\n" % (" ".join(args['target']['nominal']), nomstr)
                    else:
                        raise SyntaxError
                except SyntaxError:
                    print("SyntaxError: TARGET can only have one variable")
                except KeyError:
                    print("KeyError: Proper keys not found for TARGET dictionary: %s" % args['target'].keys())
            else:
                raise SyntaxError("TARGET is in an unknown format: %s" % str(args['target']))
        if 'train' in args:
            if isinstance(args['train'], dict):
                try:
                    if all (k in args['train'] for k in ("numtries", "maxiter")):
                        code += "train numtries=%s maxiter=%s;\n" % (args['train']["numtries"], args['train']["maxiter"])
                except:
                    raise SyntaxError("Proper Keys not found for TRAIN dictionary: %s" % args['train'].keys())
            else:
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
                raise SyntaxError("ERROR in code submission. WEIGHT can only have one variable and you submitted: %s",
                                  args['weight'])
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
        if 'score' in args:
            if isinstance(args['score'], str):
                code += "score %s;\n" % args['score']
            else:
                scoreds = args['score']
                if objtype.upper() == "HP4SCORE":
                   f = scoreds.get('file')
                   d = scoreds.get('out')
                   o = d.libref+'.'+d.table
                   code += "score file='"+f+"' out="+o+";\n"
                elif objtype.upper() == 'TPSPLINE':
                   code += "score data=%s.%s out=%s.%s;\n" % (data.libref, data.table, scoreds.libref, scoreds.table)
                else:
                   code += "score out=%s.%s;\n" % (scoreds.libref, scoreds.table)
        # save statement must be after input and target for TREEBOOST
        if 'save' in args:
            #self.logger.debug("save statement,length: %s,%s", args['save'], len(args['save']))
            if objtype=="hpforest":
                code += "save file='%s';\n" % (args['save'])
            elif objtype=="treeboost":
                if isinstance(args['save'], bool):
                    libref=objname
                    code += "save fit=%s.%s importance=%s.%s model=%s.%s nodestats=%s.%s rules=%s.%s;\n" % \
                            (libref, "fit", libref, "importance", libref, "model",
                             libref, "nodestats", libref, "rules" )
                elif isinstance(args['save'], dict):
                    code += "save %s ;"  % ' '.join('{}={}'.format(key, val) for key, val in args['save'].items())
                else:
                    raise SyntaxError("SAVE statement object type is not recognized, must be a bool or dict. You provided: %s" % str(type(save)))
            else:
                raise SyntaxError("SAVE statement is not recognized for this procedure: %s" % str(objtype))

        # passthrough facility for procedures with special circumstances
        if 'stmtpassthrough' in args:
            code += str(args['stmtpassthrough'])

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


    def _charlist(self, data) -> list:
        """
        Private method to return the variables in a SAS Data set that are of type char

        :param data: SAS Data object to process
        :return: list of character variables
        :rtype: list
        """
        # Get list of character variables to add to nominal list
        char_string = """
        data _null_; file LOG;
          d = open('{0}.{1}');
          nvars = attrn(d, 'NVARS');
          put 'VARLIST=';
          do i = 1 to nvars;
             vart = vartype(d, i);
             var  = varname(d, i);
             if vart eq 'C' then
                put var; end;
          put 'VARLISTend=';
        run;
        """
        # ignore teach_me_SAS mode to run contents
        nosub = self.sas.nosub
        self.sas.nosub = False
        ll = self.sas.submit(char_string.format(data.libref, data.table + data._dsopts()))
        self.sas.nosub = nosub
        l2 = ll['LOG'].partition("VARLIST=\n")
        l2 = l2[2].rpartition("VARLISTend=\n")
        charlist1 = l2[0].split("\n")
        del charlist1[len(charlist1) - 1]
        charlist1 = [x.casefold() for x in charlist1]
        return charlist1

    def _processNominals(self, kwargs, data):
        nom = kwargs.pop('nominals', None)
        inputs = kwargs.pop('input', None)
        tgt = kwargs.pop('target', None)
        targOpts = kwargs.pop('targOpts', None)

        # get char variables and nominals list if it exists
        if nom is None:
            dsnom = SASProcCommons._charlist(self, data)
        elif isinstance(nom, list):
            nom = [x.casefold() for x in nom]
            dsnom = list(set(SASProcCommons._charlist(self, data)) | set(nom))
        else:
            raise SyntaxWarning('nominals must be list type. You gave %s.' % str(type(nom)))
        if tgt is not None:
            # what object type is target
            if isinstance(tgt, str):
                # if there is special character do nothing
                if len([word for word in tgt if any(letter in word for letter in '/\:;.%')]) != 0:
                    kwargs['target'] = tgt
                else:
                    # turn str into list and search for nominals
                    tgt_list = tgt.casefold().split()
                    nom_target = list(set(tgt_list).intersection(dsnom))
                    int_target = list(set(tgt_list).difference(dsnom))
                    if (nom_target is not None and len(nom_target) > 0) and (
                            int_target is not None and len(int_target) > 0):
                        kwargs['target'] = {'nominal' : nom_target,
                                            'interval': int_target}
                    elif nom_target is not None and len(nom_target) > 0:
                        kwargs['target'] = {'nominal': nom_target}
                    elif int_target is not None and len(int_target) > 0:
                        kwargs['target'] = {'interval': int_target}
            elif isinstance(tgt, list):
                tgt_list = tgt
                tgt_list = [x.casefold() for x in tgt_list]
                nom_target = list(set(tgt_list).intersection(dsnom))
                int_target = list(set(tgt_list).difference(dsnom))
                if (nom_target is not None and len(nom_target) > 0) and (
                        int_target is not None and len(int_target) > 0):
                    kwargs['target'] = {'nominal' : nom_target,
                                        'interval': int_target}
                elif nom_target is not None and len(nom_target) > 0:
                    kwargs['target'] = {'nominal': nom_target}
                elif int_target is not None and len(int_target) > 0:
                    kwargs['target'] = {'interval': int_target}
            elif isinstance(tgt, dict):
                # are the keys valid
                # TODO: make comparison case insensitive casefold()
                if any(key in tgt.keys() for key in ['nominal', 'interval']):
                    kwargs['target'] = tgt
            else:
                raise SyntaxError("Target must be a string, list, or dictionary you provided: %s" % str(type(tgt)))
        if targOpts is not None:
            kwargs['target']['targOpts'] = targOpts
        if inputs is not None:
            # what object type is input
            if isinstance(inputs, str):
                # if there is only one word or special character do nothing
                if len(inputs.split()) == 1 or len(
                        [word for word in inputs if any(letter in word for letter in '-/\\:;.%')]) != 0:
                    kwargs['input'] = inputs
                else:
                    # turn str into list and search for nominals
                    inputs_list = inputs.casefold().split()
                    nom_input = list(set(inputs_list).intersection(dsnom))
                    int_input = list(set(inputs_list).difference(dsnom))
                    if (nom_input is not None and len(nom_input) > 0) and (
                            int_input is not None and len(int_input) > 0):
                        kwargs['input'] = {'nominal' : nom_input,
                                           'interval': int_input}
                    elif nom_input is not None and len(nom_input) > 0:
                        kwargs['input'] = {'nominal': nom_input}
                    elif int_input is not None and len(int_input) > 0:
                        kwargs['input'] = {'interval': int_input}
            elif isinstance(inputs, list):
                inputs_list = inputs
                inputs_list = [x.casefold() for x in inputs_list]
                nom_input = list(set(inputs_list).intersection(dsnom))
                int_input = list(set(inputs_list).difference(dsnom))
                if (nom_input is not None and len(nom_input) > 0) and (int_input is not None and len(int_input) > 0):
                    kwargs['input'] = {'nominal' : nom_input,
                                       'interval': int_input}
                elif nom_input is not None and len(nom_input) > 0:
                    kwargs['input'] = {'nominal': nom_input}
                elif int_input is not None and len(int_input) > 0:
                    kwargs['input'] = {'interval': int_input}
            elif isinstance(inputs, dict):
                # are the keys valid
                # TODO: make comparison case insensitive casefold()
                if any(key in inputs.keys() for key in ['nominal', 'interval']):
                    kwargs['input'] = inputs
            else:
                raise SyntaxError("input must be a string, list, or dictionary you provided: %s" % str(type(inputs)))
        return kwargs

    def _target_stmt(self, stmt: object) -> tuple:
        """
        takes the target key from kwargs and processes it to aid in the generation of a model statement
        :param stmt: str, list, or dict that contains the model information.
        :return: tuple of strings one for the class statement one for the model statements
        """
        # make sure target is a single variable extra split to account for level= option
        code = ''
        cls  = ''
        if isinstance(stmt, str):
            if len(stmt.split('/')[0].split()) == 1:
                code += "%s" % (stmt)
            else:
                raise SyntaxError(
                    "ERROR in code submission. TARGET can only have one variable and you submitted: %s" % stmt)
        elif isinstance(stmt, list):
            if len(stmt) == 1:
                code += "%s" % str(stmt[0])
            else:
                raise SyntaxError("The target list must have exactly one member")
        elif isinstance(stmt, dict):
            try:
                # check there there is only one target:
                length = 0
                try:
                    length += len([stmt['nominal'], stmt['interval']])
                except KeyError:
                    try:
                        length += len([stmt['nominal']])
                    except KeyError:
                        try:
                            length += len([stmt['interval']])
                        except KeyError:
                            raise
                if length  == 1:
                    if 'interval' in stmt.keys():
                        if isinstance(stmt['interval'], str):
                            code += "%s" % stmt['interval']
                        if isinstance(stmt['interval'], list):
                            code += "%s" % " ".join(stmt['interval'])
                    if 'nominal' in stmt.keys():
                        if isinstance(stmt['nominal'], str):
                            code += "%s" % stmt['nominal']
                            cls  += "%s" % stmt['nominal']

                        if isinstance(stmt['nominal'], list):
                            code += "%s" % " ".join(stmt['nominal'])
                            cls  += "%s" % " ".join(stmt['nominal'])
                else:
                    raise SyntaxError
            except SyntaxError:
                print("SyntaxError: TARGET can only have one variable")
            except KeyError:
                print("KeyError: Proper keys not found for TARGET dictionary: %s" % stmt.keys())
        else:
            raise SyntaxError("TARGET is in an unknown format: %s" % str(stmt))
        return (code, cls)

    def _input_stmt(self, stmt: object) -> tuple:
        """
        takes the input key from kwargs and processes it to aid in the generation of a model statement
        :param stmt: str, list, or dict that contains the model information.
        :return: tuple of strings one for the class statement one for the model statements
        """
        code = ''
        cls  = ''
        if isinstance(stmt, str):
            code += "%s " % (stmt)
        elif isinstance(stmt, dict):
            try:
                if 'interval' in stmt.keys():
                    if isinstance(stmt['interval'], str):
                        code += "%s " % stmt['interval']
                    if isinstance(stmt['interval'], list):
                        code += "%s " % " ".join(stmt['interval'])
                if 'nominal' in stmt.keys():
                    if isinstance(stmt['nominal'], str):
                        code += "%s " % stmt['nominal']
                        cls += "%s " % stmt['nominal']
                    if isinstance(stmt['nominal'], list):
                        code += "%s " % " ".join(stmt['nominal'])
                        cls += "%s " % " ".join(stmt['nominal'])
            except:
                raise SyntaxError("Proper Keys not found for INPUT dictionary: %s" % stmt.keys())
        elif isinstance(stmt, list):
            if len(stmt) == 1:
                code += "%s" % str(stmt[0])
            elif len(stmt) > 1:
                code += "%s" % " ".join(stmt)
            else:
                raise SyntaxError("The input list has no members")
        else:
            raise SyntaxError("INPUT is in an unknown format: %s" % str(stmt))
        return (code, cls)

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
        objtype = procname.lower()
        if 'model' not in kwargs.keys():
            kwargs = SASProcCommons._processNominals(self, kwargs, data)
            if 'model' in required_set:
                tcls_str = ''
                icls_str = ''
                t_str, tcls_str = SASProcCommons._target_stmt(self, kwargs['target'])
                i_str, icls_str = SASProcCommons._input_stmt(self, kwargs['input'])

                kwargs['model'] = str(t_str + ' = ' + i_str )
                kwargs['cls'] = str(tcls_str + " " + icls_str)
        verifiedKwargs = SASProcCommons._stmt_check(self, required_set, legal_set, kwargs)
        obj1 = []
        nosub = False
        objname = ''
        log = ''
        if len(verifiedKwargs):
            objname = procname[:3].lower() + self.sas._objcnt()  # translate to a libname so needs to be less than 8
            code = SASProcCommons._makeProcCallMacro(self, objtype, objname, data, verifiedKwargs)
            self.logger.debug(procname + " macro submission: " + str(code))
            if not self.sas.nosub:
                ll = self.sas.submit(code, "text")
                log = ll['LOG']
                error = SASProcCommons._errorLog(log)
                isinstance(error, str)
                if len(error) > 1:
                    RuntimeWarning("ERRORS found in SAS log: \n%s" % error)
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
            RuntimeWarning("Error in code submission")
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
                if not stmt.get('score'): # till we handle either/or required. proc can be called more than one way w/ diff requirements
                   raise SyntaxError("You are missing %d required statements:\n%s" % (len(missing_set), str(missing_set)))

        # legal statements
        legalSet = legal
        if len(legalSet):
            if len(reqSet):
                totSet = legalSet | reqSet
            else:
                totSet = legalSet
            generalSet = set(['ODSGraphics', 'stmtpassthrough', 'targOpts'])
            extraSet = set(stmt.keys() - generalSet).difference(totSet)  # find keys not in legal or required sets
            if extraSet:
                for item in extraSet:
                    stmt.pop(item, None)
                SyntaxWarning("The following %d statements are invalid and will be ignored:\nextraSet " % len(extraSet))
        return stmt
