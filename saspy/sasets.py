from IPython.core.display import HTML
#from saspy import pysas34 as sas
import time
import logging

# create logger
logger = logging.getLogger('')
logger.setLevel(logging.WARN)


class SAS_ets:
    def __init__(self, session, *args, **kwargs):
        '''Submit an initial set of macros to prepare the SAS system'''
        self.sas=session
        code="options pagesize=max; %include '/root/jared/metis/saspy_pip/saspy/libname_gen.sas'; "
        self.sas._submit(code,"text")

        logger.debug("Initalization of SAS Macro: " + str(self.sas._getlog()))

    def _objectmethods(self,obj,*args):
        clear=self.sas._getlog(1)
        code  ="%listdata("
        code +=obj
        code +=");"
        logger.debug("Object Method macro call: " + str(code))
        self.sas._submit(code,"text")
        meth=self.sas._getlog().splitlines()
        logger.debug('SAS Log: ' + str(meth))
        objlist=meth[meth.index('startparse9878')+1:meth.index('endparse9878')]
        logger.debug("PROC attr list: " + str(objlist))
        return objlist

    def _makeProccallMacro(self, objtype, objname, data='', by='', corr='',
                           crosscorr='', decomp='', id='', season='', trend='', var='',
                           crossvar='', identify='', estimate='', outlier='', forecast'', 
                           autoreg='', blockseason='', cycle='', deplag='', irregular='', 
                           level='', model='', nloptions='', performance='', randomreg='', 
                           slope='', splinereg='', splineseason='', fcmport='', outarrays='', 
                           outscalars='', prog_stmts=''):
        code  = "%macro proccall(d);\n"
        code += "proc %s data=%s.%s plots=all;\n" % (objtype, data.libref, data.table)
        if by:
            logger.debug("by statement,length: %s,%s", by, len(by))
            code += "by %s;" % (by, )
        if corr:
            logger.debug("corr statement,length: %s,%s", corr, len(corr))
            code += "corr %s;" % (corr, )
        if crosscorr:
            logger.debug("crosscorr statement,length: %s,%s", crosscorr, len(crosscorr))
            code += "crosscorr %s;" % (crosscorr, )
        if decomp:
            logger.debug("decomp statement,length: %s,%s", decomp, len(decomp))
            code += "decomp %s;" % (decomp, )
        if id:
            logger.debug("id statement,length: %s,%s", id, len(id))
            code += "id %s;" % (id, )
        if season:
            logger.debug("season statement,length: %s,%s", season, len(season))
            code += "season %s;" % (season, )
        if trend:
            logger.debug("trend statement,length: %s,%s", trend, len(trend))
            code += "trend %s;" % (trend, )
        if var:
            logger.debug("var statement,length: %s,%s", var, len(var))
            code += "var %s;" % (var, )
        if crossvar:
            logger.debug("crossvar statement,length: %s,%s", crossvar, len(crossvar))
            code += "crossvar %s;" % (crossvar, )
        if identify:
            logger.debug("identify statement,length: %s,%s", identify, len(identify))
            code += "identify %s;" % (identify, )
        if estimate:
            logger.debug("estimate statement,length: %s,%s", estimate, len(estimate))
            code += "estimate %s;" % (estimate, )
        if outlier:
            logger.debug("outlier statement,length: %s,%s", outlier, len(outlier))
            code += "outlier %s;" % (outlier, )
        if forecast:
            logger.debug("forecast statement,length: %s,%s", forecast, len(forecast))
            code += "forecast %s;" % (forecast, )
        if autoreg:
            logger.debug("autoreg statement,length: %s,%s", autoreg, len(autoreg))
            code += "autoreg %s;" % (autoreg, )
        if blockseason:
            logger.debug("blockseason statement,length: %s,%s", blockseason, len(blockseason))
            code += "blockseason %s;" % (blockseason, )
        if cycle:
            logger.debug("cycle statement,length: %s,%s", cycle, len(cycle))
            code += "cycle %s;" % (cycle, )
        if deplag:
            logger.debug("deplag statement,length: %s,%s", deplag, len(deplag))
            code += "deplag %s;" % (deplag, )
        if irregular:
            logger.debug("irregular statement,length: %s,%s", irregular, len(irregular))
            code += "irregular %s;" % (irregular, )
        if level:
            logger.debug("level statement,length: %s,%s", level, len(level))
            code += "level %s;" % (level, )
        if model:
            logger.debug("model statement,length: %s,%s", model, len(model))
            code += "model %s;" % (model, )
        if nloptions:
            logger.debug("nloptions statement,length: %s,%s", nloptions, len(nloptions))
            code += "nloptions %s;" % (nloptions, )
        if performance:
            logger.debug("performance statement,length: %s,%s", performance, len(performance))
            code += "performance %s;" % (performance, )
        if randomreg:
            logger.debug("randomreg statement,length: %s,%s", randomreg, len(randomreg))
            code += "randomreg %s;" % (randomreg, )
        if slope:
            logger.debug("slope statement,length: %s,%s", slope, len(slope))
            code += "slope %s;" % (slope, )
        if splinereg:
            logger.debug("splinereg statement,length: %s,%s", splinereg, len(splinereg))
            code += "splinereg %s;" % (splinereg, )
        if splineseason:
            logger.debug("splineseason statement,length: %s,%s", splineseason, len(splineseason))
            code += "splineseason %s;" % (splineseason, )
        if fcmport:
            logger.debug("fcmport statement,length: %s,%s", fcmport, len(fcmport))
            code += "fcmport %s;" % (fcmport, )
        if outarrays:
            logger.debug("outarrays statement,length: %s,%s", outarrays, len(outarrays))
            code += "outarrays %s;" % (outarrays, )
        if outscalars:
            logger.debug("outscalars statement,length: %s,%s", outscalars, len(outscalars))
            code += "outscalars %s;" % (outscalars, )
        if prog_stmts:
            logger.debug("prog_stmts statement,length: %s,%s", prog_stmts, len(prog_stmts))
            code += " %s;" % (prog_stmts, )
        code += "run; quit; %mend;\n"
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype,data.table)
        logger.debug("Proc code submission: " + str(code))
        return (code)
        
    def timeseries(self, **kwargs):
        '''Python method to call the TIMESERIES procedure
        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_timeseries_overview.htm
        '''
        objtype='timeseries'
        objname='ts1'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("TIMESERIES macro submission: " + str(code))
        self.sas._submit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]

        return (SAS_results(obj1, self.sas, objname))

    def arima(self, **kwargs):
        '''Python method to call the ARIMA procedure
        Documentation link: http://support.sas.com/documentation/cdl//en/etsug/68148/HTML/default/viewer.htm#etsug_arima_overview.htm
        '''
        objtype='arima'
        objname='arm'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("ARIMA macro submission: " + str(code))
        self.sas._submit(code,"text")
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
        objtype='ucm'
        objname='ucm'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("UCM macro submission: " + str(code))
        self.sas._submit(code,"text")
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
        objtype='esm'
        objname='esm'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("ESM macro submission: " + str(code))
        self.sas._submit(code,"text")
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
        objtype='tid'
        objname='tid'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("TIMEID macro submission: " + str(code))
        self.sas._submit(code,"text")
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
        objtype='tda'
        objname='tda'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("TIMEDATA macro submission: " + str(code))
        self.sas._submit(code,"text")
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
             raise AttributeError
        return HTML(data)

    def _go_run_code(self, attr):
        #print(self._name, attr)
        code = '%%getdata(%s, %s);' % (self._name, attr)
        #print (code)
        self.sas._submit(code)
        return self.sas._getlst()

    def sasdata(self, table):
        x=self.sas.sasdata(table,'_'+self._name)
        return (x)


