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

from collections import OrderedDict
from saspy.sasdata import SASdata
from saspy.sasresults import SASresults
# from pdb import set_trace as bp

class Codegen(object):
    """
    Class to generate code for submission to the SAS system.
    """
    def __init__(self, key, args, **kwargs):
        self._key = key
        self._args = args

    @property
    def key(self):
        return self._key

    @property
    def codestmt(self):
        args = self._args
        key = self._key
        if self._key in ['code', 'save'] and isinstance(self._args, str):
            args = "file = '{}'".format(args)
        if self._key in ['output', 'out'] and isinstance(self._args, str):
            if not len(self.outmeth):
                if bool(re.match(r'(\bout\W*=+)',args, flags=re.IGNORECASE)):
                    return "output {};\n".format(args)
                else:
                    return "output out= {};\n".format(args)
            return args
        if self._key in ['selection'] and isinstance(self._args, str):
            if self._args.lower().strip() in ['none', 'forward', 'backward', 'stepwise', 'forwardswap','lar', 'lasso']:
                if len(self._args.split()) == 1:
                    return "selection method={};\n".format(self._args)
                else:
                    raise SyntaxError("selection method: '{}' is not valid".format(self._args))
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
            elif self._key in ['save']:
                return "{0} {2}={1}.{2} {3}={1}.{3} {4}={1}.{4} {5}={1}.{5} {6}={1}.{6};\n"\
                    .format(self._key, self.objname, "fit", "importance", "model", "nodestats", "rules" )
            elif self._key in ['out', 'output']:
                if not len(self.outmeth):
                    return "output out={}.{};\n".format(self.objname, '_output')
                return '{}.{}'.format(self.objname, '_output')

        elif isinstance(self._args, dict):
            try:
                c = ''
                length = 0
                for k,v in self._args.items():
                    if k not in ['interval', 'nominal']:
                        raise KeyError
                    keystr = k
                    if self.objtype.casefold() == 'hpneural':
                        if keystr == 'interval':
                            keystr = 'int'
                        else:
                            keystr = 'nom'
                    if isinstance(v, str):
                        if self._key.casefold() == 'target':
                            length += len(v.split())
                        c += "{0} {1} /level={2};\n".format(self._key, self._args[k], keystr)
                    elif isinstance(self._args[k], (list, tuple)):
                        if self._key.casefold() == 'target':
                            length += len(v)
                        c += "{0} {1} /level={2};\n".format(self._key, " ".join(self._args[k]), keystr)

                if self._key.casefold() == 'target' and not length==1:
                    raise SyntaxError
                return c
            except SyntaxError:
                print("SyntaxError: TARGET can only have one variable")
            except KeyError:
                if self._key.casefold() == 'selection':
                    if bool(self._args):  # is the dictionary empty
                        m = self._args.pop('method', '')
                        me = self._args.pop('maxeffects', None)
                        if me is not None:
                            if int(me) > 0 and m != 'backward':
                                self._args['maxeffects'] = me
                        d = self._args.pop('details', '')
                        dstr = ''
                        if len(d) > 0:
                            dstr = 'details = %s' % d
                        return "selection method={} ({})  {}\n;".format(m, ' '.join('{}={}'.format(key, val) for key, val in self._args.items()), dstr)
                if self.objtype.lower() == 'hpneural' and self._key.casefold() == 'train' and all(k in self._args for k in ("numtries", "maxiter")):
                    return "train numtries={} maxiter={};\n".format(self._args['numtries'], self._args['maxiter'])
                if self.objtype.lower() == 'nnet' and self._key.casefold() == 'train':
                    return "{0} {1};\n".format(self._key, ' '.join('{}={}'.format(key, val) for key, val in self._args.items()))
                if self._key.casefold() == 'out' and not len(self.outmeth):
                    return "output out={}.{}\n;".format(self._args.libref, self._args.table)

                if self._key.casefold() == 'save' and self.objtype == 'treeboost':
                    return '{} %s ;\n'.format(self._key) % ' '.join('{} = {}'.format(key, val) for key, val in self._args.items())
                if self._key.casefold() == 'impute':
                    usedVars = []
                    tup_code = ''
                    contantValues = self._args.pop('value', None)
                    if contantValues is not None:
                        if not all(isinstance(x, tuple) for x in contantValues):
                            raise SyntaxError("The elements in the 'value' key must be tuples")
                        for t in contantValues:
                            tup_code += "impute %s / value = %s;\n" % (t[0], t[1])
                            usedVars.append(t[0])
                    meth_code = ''
                    for key, values in self._args.items():
                        for v in values:
                            meth_code += 'impute %s / method = %s;\n' % (v, key)
                            usedVars.append(v)
                    return '\ninput ' + ' '.join(list(set(usedVars))) + ';\n' + tup_code + meth_code + 'run;'

                print("KeyError: Proper keys not found for {} dictionary: {}".format(self._key, args))

        elif isinstance(self._args, SASdata):
            key = "{} =".format(self._key)
            args = "{}.{}".format(self._args.libref, self._args.table)
            if self._key in ['out','output']:
                return 'output out={}.{}\n;'.format(self._args.libref, self._args.table)
            if self._key == 'score':
                if self.objtype.casefold() == 'hp4score':
                    return "score out={}.{}\n;".format(self._args.libref, self._args.table)
                elif self.objtype.casefold() == 'tpspline':
                    return "score data={0}.{1} out={2}.{3}\n;".format(self.data.libref, self.data.table, self._args.libref, self._args.table)
                return "score out={}.{}\n;".format(self._args.libref, self._args.table)
            elif self._key == 'savestate':
                return "{} rstore = {}.{}\n;".format(key, self._args.libref, self._args.table)
            elif self._key in ['output', 'out']:
                if len(self.outmeth):
                    return "{} out = {};\n".format(self._key, args)
                return "{}.{}".format(self._args.libref, self._args.table)
        if self._key in ['stmtpassthrough', 'prog_stmts']:
            return "{0} ;\n".format(args)
        if self._key =='cls':
            key = 'class'
        return "{0} {1};\n".format(key, args)

    @property
    def debug(self):
        if isinstance(self._args, str):
            return "{0} statement,length: {1},{2}\n".format(
                self._key, self._args, len(self._args))
        elif isinstance(self._args, (list, tuple)):
            return "list:{}\n".format(self._args)

    @classmethod
    def new(cls, key, args):
        return cls(key, args)


class SASProcCommons:
    def __init__(self, session, *args, **kwargs):
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
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

    def _makeProcCallMacro(self, objtype: str, objname: str, data: ['SASdata', str] = None, args: dict = None) -> str:
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
        procopts = args.pop('procopts', '')
        # Set ODS graphic generation to True by default
        ODSGraphics = args.get('ODSGraphics', True)

        # The different SAS products vary slightly in plotting and out methods.
        # this block sets the options correctly for plotting and output statements
        if self.sasproduct.lower() == 'stat' and not ('ODSGraphics' in args.keys() or ODSGraphics == False):
            plot = 'plot=all'
        if self.sasproduct.lower() == 'qc':
            pass
        if self.sasproduct.lower() == 'ets' and not ('ODSGraphics' in args.keys() or ODSGraphics == False):
            outmeth = 'out'
            plot = 'plot=all'
        if self.sasproduct.lower() == 'em':

            pass
        if self.sasproduct.lower() == 'vddml':
            outmeth = 'out'
        if self.sasproduct.lower() == 'util':
            outmeth = 'out'
            if objtype.lower() =='univariate' and not ('ODSGraphics' in args.keys() or ODSGraphics == False):
                plot = 'plot'
                outmeth = ''
        outds = args.pop('out', None)
        if outds == None:
            outds = args.pop('output', None)
        outcodegen = Codegen.new('out', outds)
        outcodegen.outmeth = outmeth
        outcodegen.objname = objname
        outstr = outcodegen.codestmt
        self.logger.debug("product caller: " + self.sasproduct.lower())
        debug_code= ''
        code = "%macro proccall(d);\n"
        # resolve issues withe Proc options, out= and plots=
        # The procopts statement should be in every procedure as a way to pass arbitrary options to the procedures
        if 'outmeth' in args:
            outmeth = args['outmeth']
        if 'plot' in args:
            plot = args['plot']
        if len(outmeth) and not outds == None:
            #outstr = outds.libref + '.' + outds.table
            code += "proc %s data=%s.%s%s %s %s=%s %s ;\n" % (
                objtype, data.libref, data.table, data._dsopts(), plot, outmeth, outstr, procopts)
        else:
            code += "proc %s data=%s.%s%s %s %s ;\n" % (
            objtype, data.libref, data.table, data._dsopts(), plot, procopts)
            if outds is not None:
                args['output'] = outds
        self.logger.debug("args value: " + str(args))
        self.logger.debug("args type: " + str(type(args)))

        # this list is largely alphabetical but there are exceptions in order to
        # satisfy the order needs of the statements for the procedures
        # as an example...
        # http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_glm_syntax.htm#statug.glm.glmpostable

        uoargs = {}
        orderedargs = {}
        keyorder = ['by', 'input', 'target', 'cls', 'model', 'output']
        for k, v in args.items():
            if k in keyorder:
                orderedargs[k] = v
            else:
                uoargs[k] = v
        orderedargs = OrderedDict(sorted(orderedargs.items(), key=lambda i: keyorder.index(i[0])))
        for k, v in uoargs.items():
            orderedargs[k] = v
            orderedargs.move_to_end(k)
        for key, value in orderedargs.items():
            gen = Codegen.new(key, value)
            gen.objtype = objtype
            gen.data = data
            gen.outmeth = outmeth
            gen.objname = objname
            code += gen.codestmt
            if gen.debug is not None:
                debug_code += gen.debug

        code += "run; quit; %mend;\n"
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype, data.table)
        if self.logger.level == 10:
            print("Proc code submission:\n " + str(code))
            print("\n\n\n" + debug_code)
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
        if isinstance(data, str):
            tempdata = data
            try:
                table = tempdata.split('.')[-1]
                lib = tempdata.split('.')[-2]
            except IndexError:
                lib = ''
            # check that the table exists
            assert self.sas.exist(table, lib), "The dataset does not exist. Check your spelling and/or libname assignment."
            data = self.sas.sasdata(table, lib)
        assert isinstance(data, SASdata), "Data must be a sasdata object. Wrong type or string conversion failed."

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
