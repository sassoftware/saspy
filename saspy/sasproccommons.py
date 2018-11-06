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
import warnings
import re

from functools import wraps
from saspy.sasdata import SASdata
from saspy.sasresults import SASresults
# from pdb import set_trace as bp

class Codegen(object):
    """
    Class to generate code for submission to the SAS system.
    """
    def __init__(self, key, args):
        self._key = key
        self._args = args

    @property
    def key(self):
        return self._key

    @property
    def codestmt(self):
        args = self._args
        if self._key in ['freq', 'weight'] and len(args.split()) > 1:
            raise SyntaxError('ERROR in code submission. {} can only have one variable and you submitted: {}'.format(self._key, args))
        if isinstance(self._args, (list, tuple)):
            args = " ".join(self._args)
            if len(self._args) < 1:
                raise SyntaxError("The {} list has no members".format(self._key))

        elif isinstance(self._args, bool):
            if self._args == False:
                return ''
            if self._key in ['level', 'estimate', 'irregular', 'slope', 'autotune']:
                args = ''
            elif self._key == 'partition':
                return "partition fraction(test=0 validation=.30 seed=9878);\n"
        elif isinstance(self._args, dict):
            pass

        if self._key == 'stmtpassthrough':
            return "{0} ;\n".format(args)

        return "{0} {1};\n".format(self._key, args)

    @property
    def debug(self):
        if isinstance(self._args, str):
            return "{0} statement,length: {1},{2}".format(
                self._key, self._args, len(self._args))
        elif isinstance(self._args, (list, tuple)):
            return "list:{}".format(self._args)

    @classmethod
    def new(cls, key, args):
        return cls(key, args)


class SASProcCommons:
    def __init__(self, session, *args, **kwargs):
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.sas = session
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

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
            raise SyntaxError("log is not a string but type:%s" % (str(type(log))))

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
        if self.sasproduct.lower() == 'stat' and not ('ODSGraphics' in args.keys() or ODSGraphics == False):
            outmeth = ''
            plot = 'plot=all'
        if self.sasproduct.lower() == 'qc':
            outmeth = ''
            plot = ''
        if self.sasproduct.lower() == 'ets' and not ('ODSGraphics' in args.keys() or ODSGraphics == False):
            outmeth = 'out'
            plot = 'plot=all'
        if self.sasproduct.lower() == 'em':
            outmeth = ''
            plot = ''
        if self.sasproduct.lower() == 'vddml':
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
            code += "proc %s data=%s.%s%s %s %s ;\n" % (
            objtype, data.libref, data.table, data._dsopts(), plot, procopts)
        self.logger.debug("args value: " + str(args))
        self.logger.debug("args type: " + str(type(args)))

        # this list is largely alphabetical but there are exceptions in order to
        # satisfy the order needs of the statements for the procedures
        # as an example...
        # http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_glm_syntax.htm#statug.glm.glmpostable

        for key, value in args.items():
            gen = Codegen.new(key, value)
            code += gen.codestmt
            if gen.debug is not None:
                debug_code += gen.debug

        # only three valid values logistic, mlp, mlp direct
        if 'architecture' in args:
            self.logger.debug("architecture statement,length: %s,%s", args['architecture'], len(args['architecture']))
            if self.sasproduct.lower() == 'vddml':
                if args['architecture'].lower().strip() in ['glim', 'mlp', 'mlp direct']:
                    code += "architecture %s;\n" % (args['architecture'])
                else:
                    print("ERROR in code submission. ARCHITECTURE can only have one of these")
                    print("values -- ['glim', 'mlp', 'mlp direct'] you submitted: %s", args['architecture'])
            else:
                if args['architecture'].lower().strip() in ['logistic', 'mlp', 'mlp direct']:
                    code += "architecture %s;\n" % (args['architecture'])
                else:
                    print("ERROR in code submission. ARCHITECTURE can only have one of these")
                    print("values -- ['logistic', 'mlp', 'mlp direct'] you submitted: %s", args['architecture'])

        if 'autotune' in args:
            if isinstance(args['autotune'], bool):
                if args['autotune'] == True:
                    code += 'autotune;\n'
            elif isinstance(args['autotune'], str):
                self.logger.debug("autotune statement,length: %s,%s", args['autotune'], len(args['autotune']))
                code += "autotune %s;\n" % (args['autotune'])
            elif isinstance(args['autotune'], dict):
                try:
                    nomstr = 'nominal'
                    intstr = 'interval'
                    if 'interval' in args['autotune'].keys():
                        if isinstance(args['autotune']['interval'], str):
                            code += "input %s /level=%s;\n" % (args['autotune']['interval'], intstr)
                        if isinstance(args['autotune']['interval'], list):
                            code += "input %s /level=%s;\n" % (" ".join(args['autotune']['interval']), intstr)
                    if 'nominal' in args['autotune'].keys():
                        if isinstance(args['autotune']['nominal'], str):
                            code += "input %s /level=%s;\n" % (args['autotune']['nominal'], nomstr)
                        if isinstance(args['autotune']['nominal'], list):
                            code += "input %s /level=%s;\n" % (" ".join(args['autotune']['nominal']), nomstr)
                except:
                    raise SyntaxError("Proper Keys not found for AUTOTUNE dictionary: %s" % args['autotune'].keys())
            elif isinstance(args['autotune'], list):
                if len(args['autotune']) == 1:
                    code += "autotune %s;\n" % str(args['autotune'][0])
                elif len(args['autotune']) > 1:
                    code += "autotune %s;\n" % " ".join(args['autotune'])
                else:
                    raise SyntaxError("The autotune list has no members")
            else:
                raise SyntaxError("AUTOTUNE is in an unknown format: %s" % str(args['input']))

        if 'code' in args:
            self.logger.debug("code statement,length: %s,%s", args['code'], len(args['code']))
            code += "code file='%s';\n" % (args['code'])
        # The save statement is used by few procs but it doesn't have a consistent pattern
        # Here we case it correctly or throw an error.
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
                    if objtype.casefold() == 'hpneural':
                        nomstr = 'nom'
                        intstr = 'int'
                    if 'interval' in args['input'].keys():
                        if isinstance(args['input']['interval'], str):
                            code += "input %s /level=%s;\n" % (args['input']['interval'], intstr)
                        if isinstance(args['input']['interval'], list):
                            code += "input %s /level=%s;\n" % (" ".join(args['input']['interval']), intstr)
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
        if 'prior' in args:
            # TODO: check that distribution is in the list
            self.logger.debug("prior statement,length: %s,%s", args['prior'], len(args['prior']))
            code += "prior %s;\n" % (args['prior'])
        if 'selection' in args:
            if isinstance(args['selection'], str):
                if args['selection'].lower().strip() in ['none', 'forward', 'backward', 'stepwise', 'forwardswap',
                                                         'lar', 'lasso']:
                    self.logger.debug("selection statement,length: %s,%s", args['selection'], len(args['selection']))
                    code += "selection method=%s;\n" % (args['selection'])
            if isinstance(args['selection'], dict):
                if bool(args['selection']):  # is the dictionary empty
                    m = args['selection'].pop('method', '')
                    me = args['selection'].pop('maxeffects', None)
                    if me is not None:
                        if int(me) > 0 and m != 'backward':
                            args['selection']['maxeffects'] = me
                    d = args['selection'].pop('details', '')
                    dstr = ''
                    if len(d) > 0:
                        dstr = 'details = %s' % d
                    code += "selection method=%s (%s)  %s;" % (
                    m, ' '.join('{}={}'.format(key, val) for key, val in args['selection'].items()), dstr)
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
                    # check that there is only one target:
                    length = 0
                    try:
                        length += len([args['target']['nominal'], args['target']['interval']])
                    except KeyError:
                        try:
                            length += len([args['target']['nominal']])
                        except KeyError:
                            try:
                                length += len([args['target']['interval']])
                            except KeyError:
                                raise
                    if length == 1:
                        # fix var type names for HPNEURAL
                        nomstr = 'nominal'
                        intstr = 'interval'
                        targOpts = ''
                        try:
                            targOpts = ' '.join(
                                '{}={}'.format(key, val) for key, val in args['target']['targOpts'].items())
                        except:
                            pass
                        if objtype.casefold() == 'hpneural':
                            nomstr = 'nom'
                            intstr = 'int'
                        if 'interval' in args['target'].keys():
                            if isinstance(args['target']['interval'], str):
                                code += "target %s /level=%s %s;\n" % (args['target']['interval'], intstr, targOpts)
                            if isinstance(args['target']['interval'], list):
                                code += "target %s /level=%s %s;\n" % (
                                " ".join(args['target']['interval']), intstr, targOpts)
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
                    if all(k in args['train'] for k in ("numtries", "maxiter")):
                        code += "train numtries=%s maxiter=%s;\n" % (
                        args['train']["numtries"], args['train']["maxiter"])
                except:
                    raise SyntaxError("Proper Keys not found for TRAIN dictionary: %s" % args['train'].keys())
            else:
                self.logger.debug("train statement,length: %s,%s", args['train'], len(args['train']))
                code += "train %s;\n" % (args['train'])
        # test moved
        if 'partition' in args:
            if isinstance(args['partition'], str):
                self.logger.debug("partition statement,length: %s,%s", args['partition'], len(args['partition']))
                code += "partition %s;\n" % (args['partition'])
            elif isinstance(args['partition'], bool) and args['partition'] == True:
                code += "partition fraction(test=0 validation=.30 seed=9878);\n"
            elif isinstance(args['partition'], dict):
                if args['partition'].keys() in ['rolevar']:
                    pass
                elif args['partition'].keys() in ['fraction']:
                    pass
                else:
                    raise SyntaxWarning("invalid key for partition statement")

        if 'out' in args and not len(outmeth):
            if not isinstance(args['out'], dict):
                outds = args['out']
                outstr = outds.libref + '.' + outds.table
                code += "output out=%s;\n" % outstr
            else:
                t = args['out'].pop("table", None)
                l = args['out'].pop("libref", None)
                d = args['out'].pop("data", None)
                if t and l:
                    outstr = l + '.' + t
                elif d:
                    outstr = d.libref + '.' + d.table
                else:
                    raise SyntaxError(
                        "OUT statement is not in a recognized form either {'libname':'foo', 'table':'bar'} or {'data':'sasdataobject'}  %s" % str(
                            objtype))

                varlist = ' '.join('{}={}'.format(key, val) for key, val in args['out'].items())
                code += "output out=%s %s;\n" % (outstr, varlist)
        if 'score' in args:
            if isinstance(args['score'], str):
                code += "score %s;\n" % args['score']
            else:
                scoreds = args['score']
                if objtype.upper() == 'HP4SCORE':
                    f = scoreds.get('file')
                    d = scoreds.get('out')
                    o = d.libref + '.' + d.table
                    code += "score file='" + f + "' out=" + o + ";\n"
                elif objtype.upper() == 'TPSPLINE':
                    code += "score data=%s.%s out=%s.%s;\n" % (data.libref, data.table, scoreds.libref, scoreds.table)
                else:
                    code += "score out=%s.%s;\n" % (scoreds.libref, scoreds.table)
        # save statement must be after input and target for TREEBOOST
        if 'save' in args:
            if objtype == 'hpforest':
                code += "save file='%s';\n" % (args['save'])
            elif objtype == 'treeboost':
                if isinstance(args['save'], bool):
                    libref = objname
                    code += 'save fit=%s.%s importance=%s.%s model=%s.%s nodestats=%s.%s rules=%s.%s;\n' % \
                            (libref, "fit", libref, "importance", libref, "model",
                             libref, "nodestats", libref, "rules")
                elif isinstance(args['save'], dict):
                    code += 'save %s ;' % ' '.join('{} = {}'.format(key, val) for key, val in args['save'].items())
                else:
                    raise SyntaxError('SAVE statement object type is not recognized,'
                                      'must be a bool or dict. You provided: %s' % str(type(save)))
            else:
                raise SyntaxError('SAVE statement is not recognized for this procedure: %s' % str(objtype))
        if 'savestate' in args:
            if isinstance(args['savestate'], str):
                self.logger.debug('savestate statement,length: %s,%s', args['savestate'], len(args['savestate']))
                code += 'savestate %s;\n' % (args['savestate'])
            # TODO test if savestate is a SASData Object
            elif isinstance(args['savestate'], SASdata):
                code += 'savestate rstore={}.{};\n'.format(args['savestate'].libref, args['savestate'].table)
        # passthrough facility for procedures with special circumstances
        code += "run; quit; %mend;\n"
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype, data.table)
        if self.logger.level == 10:
            print("Proc code submission: " + str(code))
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
        cls = ''
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
                if length == 1:
                    if 'interval' in stmt.keys():
                        if isinstance(stmt['interval'], str):
                            code += "%s" % stmt['interval']
                        if isinstance(stmt['interval'], list):
                            code += "%s" % " ".join(stmt['interval'])
                    if 'nominal' in stmt.keys():
                        if isinstance(stmt['nominal'], str):
                            code += "%s" % stmt['nominal']
                            cls += "%s" % stmt['nominal']

                        if isinstance(stmt['nominal'], list):
                            code += "%s" % " ".join(stmt['nominal'])
                            cls += "%s" % " ".join(stmt['nominal'])
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
        cls = ''
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

    def _convert_model_to_target(self):
        target = kwargs['model'].split('=', maxsplit=1)[0].split()[0]
        input_list = kwargs['model'].split('=', maxsplit=1)[1].split('/')[0].split()
        if len(kwargs['model'].split('=', maxsplit=1)[1].split('/')[1]) > 0:
            warnings.warn("\nThe options after the '/' '{}' will be ignored.".format(
                kwargs['model'].split('=', maxsplit=1)[1].split('/')[1]))
        if len(kwargs['cls']) > 0:
            cls = kwargs['cls'].split()
            inputs = {'nominal' : cls,
                      'interval': list(set(input_list).difference(cls))}
        else:
            inputs = {'intveral': input_list}

        kwargs['target'] = target
        kwargs['input'] = inputs
        return True

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
        if required_set is None:
            required_set = {}
        objtype = procname.lower()
        if {'model'}.intersection(required_set) and 'target' in kwargs.keys() and 'model' not in kwargs.keys():
            kwargs = SASProcCommons._processNominals(self, kwargs, data)
            t_str, tcls_str = SASProcCommons._target_stmt(self, kwargs['target'])
            i_str, icls_str = SASProcCommons._input_stmt(self, kwargs['input'])
            kwargs['model'] = str(t_str + ' = ' + i_str)
            if len(icls_str) > 0:
                kwargs['cls'] = str(tcls_str + " " + icls_str)
            legal_set.add('cls')
            drop_target = kwargs.pop('target', None)
            drop_input = kwargs.pop('input', None)
            self.logger.debug(drop_target)
            self.logger.debug(drop_input)

        elif {'target'}.intersection(required_set) and 'model' in kwargs.keys() and 'target' not in kwargs.keys():
            SASProcCommons._convert_model_to_target(self)

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
        :return: dictionary of verified statements
        """
        # debug the argument list
        if self.logger.level == 10:
            for k, v in stmt.items():
                print("Key: " + k + ", Value: " + str(v) + ", Type: " + str(type(v)))

        # required statements
        reqSet = req
        if len(reqSet):
            self.logger.debug("reqSet: {}".format(reqSet))
            missing_set = reqSet.difference(set(stmt.keys()))
            if missing_set:
                if not stmt.get(
                        'score'):  # till we handle either/or required. proc can be called more than one way w/ diff requirements
                    raise SyntaxError(
                        "You are missing %d required statements:\n%s" % (len(missing_set), str(missing_set)))

        # legal statements
        legalSet = legal
        if len(legalSet):
            self.logger.debug("legalSet: {}".format(legalSet))
            if len(reqSet):
                totSet = legalSet | reqSet
            else:
                totSet = legalSet
            generalSet = {'ODSGraphics', 'stmtpassthrough', 'targOpts', 'procopts'}
            extraSet = set(stmt.keys() - generalSet).difference(totSet)  # find keys not in legal or required sets
            if extraSet:
                self.logger.debug("extraSet: {}".format(extraSet))
                for item in extraSet:
                    stmt.pop(item, None)
                warnings.warn(
                    "The following {} statements are invalid and will be ignored:\n{}".format(len(extraSet), extraSet))
        self.logger.debug("stmt: {}".format(stmt))
        return stmt

class procDecorator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        if sys.version_info[0] < 3 or (sys.version_info[0] >= 3 and sys.version_info[1] < 4):
            warnings.warn('Python 3.4+ is required to get correct tab complete and docstring '
                          'information for methods')

    def proc_decorator(req_set):
        """
        Decorator that provides the wrapped function with an attribute 'actual_kwargs'
        containing just those keyword arguments actually passed in to the function.
        """

        def decorator(func):
            @wraps(func)
            def inner(self, *args, **kwargs):
                inner.proc_decorator = kwargs
                self.logger.debug("processing proc:{}".format(func.__name__))
                self.logger.debug(req_set)
                self.logger.debug("kwargs type: " + str(type(kwargs)))
                if func.__name__.lower() in ['hplogistic', 'hpreg']:
                    kwargs['ODSGraphics'] = kwargs.get('ODSGraphics', False)
                legal_set = set(kwargs.keys())
                self.logger.debug(legal_set)
                return SASProcCommons._run_proc(self, func.__name__.lower(), req_set, legal_set, **kwargs)
            return inner
        return decorator

    def doc_convert(ls):
        generic_terms = ['procopts', 'stmtpassthrough']
        ls_list = list(ls)
        doc_list = []
        doc_markup = []
        for i in [j for j in ls_list if j not in generic_terms]:
            doc_mstr = ''.join([':parm ', i, ': The {} variable can only be a string type.'.format(i)])
            doc_str = ': str = None,'

            if i.lower() in ['target', 'input']:
                doc_mstr = ''.join([':parm ', i,
                                    ': The {} variable can be a string, list or dict type. It refers to the dependent, y, or label variable.'.format(
                                        i)])
                doc_str = ': [str, list, dict] = None,'
            if i.lower() == 'score':
                doc_str = ": [str, bool, 'SASdata' ] = True,"
            if i.lower() in ['cls']:
                doc_mstr = ''.join([':parm ', i,
                                    ': The {} variable can be a string or list type. It refers to the categorical, or nominal variables.'.format(
                                        i)])
                doc_str = ': [str, list] = None,'

            doc_list.append(''.join([i, doc_str, '\n']))
            doc_markup.append(''.join([doc_mstr, '\n']))
        doc_list.sort()
        doc_markup.sort()
        # add procopts and stmtpassthrough last for each proc
        for j in generic_terms:
            doc_list.append(''.join([j, doc_str, '\n']))
            doc_mstr = ''.join([':parm ', j,
                                ': The {} variable is a generic option available for advanced use. It can only be a string type.'.format(
                                    j)])
            doc_markup.append(''.join([doc_mstr, '\n']))

        doc_list.insert(0, ''.join(["data: 'SASData' = None,", '\n']))
        doc_markup.insert(0, ''.join([':param data: SASData object This parameter is required', '\n']))
        doc_markup.append(''.join([':return: SAS Result Object', '\n']))
        return (''.join(doc_list), ''.join(doc_markup))