from IPython.core.display import HTML
import IPython.display as id
#from saspy import pysas34 as sas
import time
import logging
import os

# create logger
logger = logging.getLogger('')
logger.setLevel(logging.WARN)


class SAS_stat:
    def __init__(self, session, *args, **kwargs):
        '''Submit an initial set of macros to prepare the SAS system'''
        self.sas=session
        macro_path=os.path.dirname(os.path.realpath(__file__))
        code="options pagesize=max; %include '" + macro_path + '/' + "libname_gen.sas'; "
        self.sas._asubmit(code,"text")

        logger.debug("Initalization of SAS Macro: " + str(self.sas._getlog()))

    def _objectmethods(self,obj,*args):
        code  ="%listdata("
        code +=obj
        code +=");"
        logger.debug("Object Method macro call: " + str(code))
        res=self.sas.submit(code,"text")
        meth=res['LOG'].splitlines()
        logger.debug('SAS Log: ' + res['LOG'])
        objlist=meth[meth.index('startparse9878')+1:meth.index('endparse9878')]
        logger.debug("PROC attr list: " + str(objlist))
        return objlist

    def _makeProccallMacro(self,objtype,objname,data=None, args=''):
        code  = "%macro proccall(d);\n"
        code += "proc %s data=%s.%s plots=all;\n" % (objtype, data.libref, data.table)
        logger.debug("args value: " + str(args))
        logger.debug("args type: " + str(type(args)))
        #this list is largly alphabetical but there are exceptions in order to 
        #satisfy the order needs of the statements for the procedure
        # as an example... http://support.sas.com/documentation/cdl/en/statug/68162/HTML/default/viewer.htm#statug_glm_syntax.htm#statug.glm.glmpostable


        if 'absorb' in args:
            logger.debug("absorb statement,length: %s,%s", args['absorb'], len(args['absorb']))
            code += "absorb %s;\n" % (args['absorb'])
        if 'add' in args:
            logger.debug("add statement,length: %s,%s", args['add'], len(args['add']))
            code += "add %s;\n" % (args['add'])
        if 'by' in args:
            logger.debug("by statement,length: %s,%s", args['by'], len(args['by']))
            code += "by %s;\n" % (args['by'])
        if 'cls' in args:
            logger.debug("class statement,length: %s,%s", args['cls'], len(args['cls']))
            code += "class %s;\n" % (args['cls'])
        #contrast moved
        if 'effect' in args:
            logger.debug("effect statement,length: %s,%s", args['effect'], len(args['effect']))
            code += "effect %s;\n" % (args['effect'])
        #estimate moved
        if 'freq' in args:
            #add check to make sure it is only one variable
            logger.debug("freq statement,length: %s,%s", args['freq'], len(args['freq']))
            code += "freq %s;\n" % (args['freq'])
        if 'id' in args:
            logger.debug("id statement,length: %s,%s", args['id'], len(args['id']))
            code += "id %s;\n" % (args['id'])
        #lsmeans moved
        #manova moved
        #means moved
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
            #check that distrbution is in the list
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
        if 'score' in args:
            logger.debug("score statement,length: %s,%s", args['score'], len(args['score']))
            code += "score %s;\n" % (args['score'])
        if 'slice' in args:
            logger.debug("slice statement,length: %s,%s", args['slice'], len(args['slice']))
            code += "slice %s;\n" % (args['slice'])
        if 'strata' in args:
            logger.debug("strata statement,length: %s,%s", args['strata'], len(args['strata']))
            code += "strata %s;\n" % (args['strata'])
        #test moved
        if 'var' in args:
            logger.debug("var statement,length: %s,%s", args['var'], len(args['var']))
            code += "var %s;\n" % (args['var'])
        if 'weight' in args:
            #add check to make sure it is only one variable
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
        '''
        if 'foobar' in args:
            logger.debug("foobar statement,length: %s,%s", args['foobar'], len(args['foobar']))
            code += "foobar %s;\n" % (args['foobar'])
        '''
        code += "run; quit; %mend;\n"
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype,data.table)
        logger.debug("Proc code submission: " + str(code))
        return (code)
        
    def _stmt_check(self, req:set ,legal:set,stmt:dict):
        # debug the argument list
        if (logging.getLogger().getEffectiveLevel()==10):
            for k,v in stmt.items():
                print ("Key: " +k+", Value: " + v)
        #required statements
        req_set=req
        if (len(req_set)):
            missing_set=req_set.difference(set(stmt.keys()))
            if missing_set:
                print ("You are missing %d required statements:" % (len(missing_set)))
                print (missing_set)
                return False

        #legal statments
        legal_set=legal
        if (len(legal_set)):
            extra_set=set(stmt.keys()).difference(legal_set|req_set) # find keys not in legal or required sets
            if extra_set:
                print ("The following %d statements are invalid and will be ignored: "% len(extra_set))
                for key in range(0,len(extra_set)):
                    print (key)
                    stmt.pop(extra_set.pop())
        return True


    def hpsplit(self, **kwargs):
        '''
        Python method to call the HPSPLIT procedure\n
        Documentation link: 
        http://support.sas.com/documentation/cdl/en/stathpug/68163/HTML/default/viewer.htm#stathpug_hpsplit_overview.htm
        '''
        required_set={}
        legal_set={'cls','code','grow','id','model',
                   'partition','performance','prune','rules'}
        data=kwargs.pop('data',None)
        logger.debug("kwargs type: " + str(type(kwargs)))
        chk= self._stmt_check(required_set, legal_set,kwargs)
        if chk:
            objtype='hpsplit'
            objname='hps'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
            code=self._makeProccallMacro(objtype, objname, data, kwargs)
            logger.debug("HPSPLIT macro submission: " + str(code))
            self.sas._asubmit(code,"text")
            try:
                obj1=self._objectmethods(objname)
                logger.debug(obj1)
            except Exception:
                obj1=[]

            return (SAS_results(obj1, self.sas, objname))
        else:
            print("Error in code submission")


        if self.sas.nosub:
           print(code)
           return (SAS_results([], self, objname, True))

        res = self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            #print("Exception Block:", sys.exc_info()[0])
            obj1=[]

        return (SAS_results(obj1, self, objname))
    def reg(self, **kwargs):
        required_set={'model'}
        legal_set={'add','by','code','id','var'
                   'lsmeans','model','random','repeated',
                   'slice','test','weight'}

        data=kwargs.pop('data',None)
        logger.debug("kwargs type: " + str(type(kwargs)))
        chk= self._stmt_check(required_set, legal_set,kwargs)
        if chk:
            objtype='reg'
            objname=objtype+self.sas._objcnt() #translate to a libname so needs to be less than 8
            code=self._makeProccallMacro(objtype, objname, data, kwargs)
            logger.debug("REG macro submission: " + str(code))
            self.sas._asubmit(code,"text")
            try:
                obj1=self._objectmethods(objname)
                logger.debug(obj1)
            except Exception:
                obj1=[]

            return (SAS_results(obj1, self.sas, objname))
        else:
            print("Error in code submission")

        if self.sas.nosub:
           print(code)
           return (SAS_results([], self, objname, True))

        res = self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]
        return (SAS_results(obj1, self, objname))
    def mixed(self, **kwargs):
        required_set={'model'}
        legal_set={'by','cls','code','contrast','estimate','id',
                   'lsmeans','model','random','repeated',
                   'slice','weight'}

        data=kwargs.pop('data',None)
        logger.debug("kwargs type: " + str(type(kwargs)))
        chk= self._stmt_check(required_set, legal_set,kwargs)
        if chk:
            objtype='mixed'
            objname='mix'+self.sas._objcnt()
            code=self._makeProccallMacro(objtype, objname, data, kwargs)
            logger.debug("Mixed Macro submission: " + str(code))
            self.sas._asubmit(code,"text")
            try:
                obj1=self._objectmethods(objname)
                logger.debug(obj1)
            except Exception:
                obj1=[]

            return (SAS_results(obj1, self.sas, objname))
        else:
            print("Error in code submission")
        if self.sas.nosub:
           print(code)
           return (SAS_results([], self, objname, True))

        res = self.sas._asubmit(code, "text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]
        return (SAS_results(obj1, self, objname))
    def glm(self, **kwargs):
        required_set={'model'}
        legal_set={'absorb','by','cls','contrast','estimate','freq','id',
                   'lsmeans','manova','means', 'model','random','repeated',
                   'test','weight'}

        data=kwargs.pop('data',None)
        logger.debug("kwargs type: " + str(type(kwargs)))
        chk= self._stmt_check(required_set, legal_set,kwargs)
        if chk:
            objtype='glm'
            objname=objtype+self.sas._objcnt() #translate to a libname so needs to be less than 8
            code=self._makeProccallMacro(objtype, objname, data, kwargs)
            logger.debug("GLM macro submission: " + str(code))
            self.sas._asubmit(code,"text")
            try:
                obj1=self._objectmethods(objname)
                logger.debug(obj1)
            except Exception:
                obj1=[]

            return (SAS_results(obj1, self.sas, objname))
        else:
            print("Error in code submission")

        if self.sas.nosub:
           print(code)
           return (SAS_results([], self, objname, True))

        res = self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]
        return (SAS_results(obj1, self, objname))
    def logistic(self, **kwargs):

        required_set={'model'}
        '''
        The PROC LOGISTIC and MODEL statements are required. 
        The CLASS and EFFECT statements (if specified) must 
        precede the MODEL statement, and the CONTRAST, EXACT, 
        and ROC statements (if specified) must follow the MODEL 
        statement.
        '''
        legal_set={'by','cls','contrast','effect','effectplot','estimate',
                   'exact','freq','lsmeans','oddsratio','roc','score','slice',
                   'store','strata','units','weight'}

        data=kwargs.pop('data',None)
        logger.debug("kwargs type: " + str(type(kwargs)))
        chk= self._stmt_check(required_set, legal_set,kwargs)
        logger.debug("chk value: " + str(chk))
        if chk:
            objtype='logistic'
            objname='log'+self.sas._objcnt() #translate to a libname so needs to be less than 8
            code=self._makeProccallMacro(objtype, objname, data, kwargs)
            logger.debug("LOGISTIC macro submission: " + str(code))
            self.sas._asubmit(code,"text")
            try:
                obj1=self._objectmethods(objname)
                logger.debug(obj1)
            except Exception:
                obj1=[]

            return (SAS_results(obj1, self.sas, objname))
        else:
            print("Error in code submission")


        if self.sas.nosub:
           print(code)
           return (SAS_results([], self, objname, True))

        res = self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]
        return (SAS_results(obj1, self, objname))

from collections import namedtuple

class SAS_results(object):
    '''Return results from a SAS Model object'''
    def __init__(self,attrs, session, objname, nosub=False):

        self._attrs = attrs
        self._name  = objname
        self.sas    = session
        self.nosub  = nosub

    def __dir__(self):
        '''Overload dir method to return the attributes'''
        return self._attrs

    def __getattr__(self, attr):
        if attr.startswith('_'):
            return getattr(self, attr)
        if attr.upper() in self._attrs:
            #print(attr.upper())
            if self.nosub:
                print('How did I get here? This SAS Result object was created in teach_me_SAS mode, so it has no results')
                return
            data = self._go_run_code(attr)
            '''
            if not attr.lower().endswith('plot'):
                libname, table = data.split()
                table_data = sasdata(libname, table)
                content = table_data.contents()
                # parse content
                headers = content[0]

                res = namedtuple('SAS Result', headers)
                results = [ res(x) for x in headers[1:] ]
            '''
 
        else:
            if self.nosub:
                print('This SAS Result object was created in teach_me_SAS mode, so it has no results')
                return
            else:
                raise AttributeError
        return HTML('<h1>'+attr+'</h1>'+data)

    def _go_run_code(self, attr):
        #print(self._name, attr)
        code = '%%getdata(%s, %s);' % (self._name, attr)
        #print (code)
        res = self.sas.submit(code)
        return res['LST']

    def sasdata(self, table):
        x=self.sas.sasdata(table,'_'+self._name)
        return (x)

    def ALL(self):
        '''
        This method shows all the results attributes for a given object
        '''
        for i in self._attrs:
            id.display(self.__getattr__(i))
