from IPython.core.display import HTML
import IPython.display as id
import time
import logging
import os
import re

# create logger
logger = logging.getLogger('')
logger.setLevel(logging.WARN)


class SASets:
    def __init__(self, session, *args, **kwargs):
        '''Submit an initial set of macros to prepare the SAS system'''
        self.sas=session
        logger.debug("Initalization of SAS Macro: " + str(self.sas.saslog()))

    def _objectmethods(self,obj,*args):
        code  ="%listdata("
        code +=obj
        code +=");"
        logger.debug("Object Method macro call: " + str(code))
        res=self.sas.submit(code,"text")
        meth=res['LOG'].splitlines()
        for i in range(len(meth)):
           meth[i] = meth[i].lstrip().rstrip()
        logger.debug('SAS Log: ' + str(meth))
        objlist=meth[meth.index('startparse9878')+1:meth.index('endparse9878')]
        logger.debug("PROC attr list: " + str(objlist))
        return objlist

    def _makeProccallMacro(self, objtype, objname, data=None, args=''):
        #by='', corr='',
        #                   crosscorr='', decomp='', id='', season='', trend='', var='',
        #                   crossvar='', identify='', estimate='', outlier='', forecast='', 
        #                   autoreg='', blockseason='', cycle='', deplag='', irregular='', 
        #                   level='', model='', nloptions='', performance='', randomreg='', 
        #                   slope='', splinereg='', splineseason='', fcmport='', outarrays='', 
        #                   outscalars='', prog_stmts=''):
        code  = "%macro proccall(d);\n"
        code += "proc %s data=%s.%s plots=all;\n" % (objtype, data.libref, data.table)
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
            if len(req_set):
               tot_set = legal_set | req_set
            else:
               tot_set = legal_set
            extra_set=set(stmt.keys()).difference(tot_set)
            if extra_set:
                print ("The following %d statements are invalid and will be ignored: "% len(extra_set))
                for key in range(0,len(extra_set)):
                    print (key)
                    kwargs.pop(extra_set.pop())
        return True

    def timeseries(self, **kwargs):
        '''Python method to call the TIMESERIES procedure
        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeseries_overview.htm
        '''
        required_set={'id'}
        legal_set={ 'by', 'corr', 'crosscorr', 'decomp', 'id', 'season', 'trend', 'var', 'crossvar'}
        data=kwargs.pop('data',None)
        logger.debug("kwargs type: " + str(type(kwargs)))
        chk= self._stmt_check(required_set, legal_set,kwargs)
        if chk:
            objtype='timeseries'
            objname='ts1'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
            code=self._makeProccallMacro(objtype, objname, data, kwargs)
            logger.debug("TIMESERIES macro submission: " + str(code))
            self.sas._asubmit(code,"text")
            try:
                obj1=self._objectmethods(objname)
                logger.debug(obj1)
            except Exception:
                obj1=[]

            return (SAS_results(obj1, self.sas, objname))
        else:
            Print("Error in code submission")

    def arima(self, **kwargs):
        '''Python method to call the ARIMA procedure
        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_arima_overview.htm
        '''
        required_set={'identify'}
        legal_set={ 'by', 'identify', 'estimate', 'outlier', 'forecast'}
        data=kwargs.pop('data',None)
        chk= self._stmt_check(required_set,legal_set,kwargs)
        objtype='arima'
        objname='arm'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, data, kwargs)
        logger.debug("ARIMA macro submission: " + str(code))
        self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]
        return (SAS_results(obj1, self.sas, objname))
        
    def ucm(self, **kwargs):
        '''Python method to call the UCM procedure
        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_ucm_overview.htm
        '''
        required_set={'model'}
        legal_set={ 'autoreg','blockseason','by','cycle','deplag','estimate','forecast','id','irregular'
                    'level','model','nloptions','performance','outlier','randomreg','season','slope'
                    'splinereg','splineseason'}
        data=kwargs.pop('data',None)
        chk= self._stmt_check(required_set,legal_set,kwargs)
        objtype='ucm'
        objname='ucm'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, data, kwargs)
        logger.debug("UCM macro submission: " + str(code))
        self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]
        return (SAS_results(obj1, self.sas, objname))    
    
    def esm(self, **kwargs):
        '''Python method to call the ESM procedure
        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_esm_overview.htm
        '''
        required_set={}
        legal_set={ 'by', 'id', 'forecast'}
        data=kwargs.pop('data',None)
        chk= self._stmt_check(required_set,legal_set,kwargs)
        objtype='esm'
        objname='esm'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, data, kwargs)
        logger.debug("ESM macro submission: " + str(code))
        self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]        
        return (SAS_results(obj1, self.sas, objname))
    def timeid(self, **kwargs):
        '''Python method to call the TIMEID procedure
        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeid_overview.htm
        '''
        required_set={}
        legal_set={ 'by', 'id'}
        data=kwargs.pop('data',None)
        chk= self._stmt_check(required_set,legal_set,kwargs)
        objtype='timeid'
        objname='tid'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, data, kwargs)
        logger.debug("TIMEID macro submission: " + str(code))
        self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]        
        return (SAS_results(obj1, self.sas, objname))
        
    def timedata(self, **kwargs):
        '''Python method to call the TIMEDATA procedure
        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timedata_overview.htm
        '''
        required_set={}
        legal_set={ 'by', 'id', 'fcmport','outarrays','outscalars', 'var', 'prog_stmts'}
        data=kwargs.pop('data',None)
        chk= self._stmt_check(required_set,legal_set,kwargs)
        objtype='timedata'
        objname='tda'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, data, kwargs)
        logger.debug("TIMEDATA macro submission: " + str(code))
        self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]                
        return (SAS_results(obj1, self.sas, objname))
    

from collections import namedtuple

class SAS_results(object):
    '''Return results from a SAS Model object'''
    def __init__(self,attrs, session, objname):

        self._attrs = attrs
        self._name = objname
        self.sas=session

    def __dir__(self):
        '''Overload dir method to return the attributes'''
        return self._attrs

    def __getattr__(self, attr):
        if attr.startswith('_'):
            return getattr(self, attr)
        if attr.upper() in self._attrs:
            #print(attr.upper())
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
             #raise AttributeError
             print("Result named "+attr+" not found. Valid results are:"+str(self._attrs))
             return
        return HTML(data)

    def _go_run_code(self, attr):
        #print(self._name, attr)
        code = '%%getdata(%s, %s);' % (self._name, attr)
        res=self.sas.submit(code)
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

