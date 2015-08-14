from IPython.core.display import HTML
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

    def _makeProccallMacro(self,objtype,objname,kwargs):
        data=kwargs.get('data','')
        model=kwargs.get('model','')
        cls=kwargs.get('cls','')
        means=kwargs.get('means','')
        by =kwargs.get('by', '')
        est=kwargs.get('estimate','')
        weight=kwargs.get('weight','')
        lsmeans=kwargs.get('lsmeans','')

        code  = "%macro proccall(d);\n"
        if objtype == 'hpsplit':
           code += "proc %s data=%s.%s plots=all;\n" % (objtype, data.libref, data.table)
        else:
           code += "proc %s data=%s.%s plots(unpack)=all;\n" % (objtype, data.libref, data.table)
        #logger.debug("cls stuff: " +str(hasattr(self,'cls')) + ' ' + str(len(self.cls)))
        if len(cls):
            #logger.debug("cls stuff: " +str(hasattr(self,'cls')) + ' ' + str(len(self.cls)))
            code += "class %s;" % (cls)
        if len(model):
            code += "model %s;" % (model)
        if len(means):
            code += "means %s;" % (cls)
        code += "run; quit; %mend;\n"
        code += "%%mangobj(%s,%s,%s);" % (objname, objtype,data.table)
        logger.debug("Proc code submission: " + str(code))
        return (code)

    def hpsplit(self, **kwargs):
        '''Python method to call the HPSPLIT procedure\nDocumentation link: http://support.sas.com/documentation/cdl/en/stathpug/68163/HTML/default/viewer.htm#stathpug_hpsplit_overview.htm'''
        objtype='hpsplit'
        objname='hps'+self.sas._objcnt()  #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("HPSPLIT macro submission: " + str(code))
        self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            #print("Exception Block:", sys.exc_info()[0])
            obj1=[]

        return (SAS_results(obj1, self.sas, objname))

    def reg(self, **kwargs):
        objtype='reg'
        objname=objtype+self.sas._objcnt() #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("REG macro submission: " + str(code))
        self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]
        return (SAS_results(obj1, self.sas, objname))
    
    
    def mixed(self, **kwargs):
        objtype='mixed'
        objname='mix'+self.sas._objcnt()
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("Mixed Macro submission: " + str(code))
        self.sas._asubmit(code, "text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]
        return (SAS_results(obj1, self.sas, objname))



    def glm(self, **kwargs):
        objtype='glm'
        objname=objtype+self.sas._objcnt() #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("GLM macro submission: " + str(code))
        self.sas._asubmit(code,"text")
        try:
            obj1=self._objectmethods(objname)
            logger.debug(obj1)
        except Exception:
            obj1=[]
        return (SAS_results(obj1, self.sas, objname))

    def logistic(self, **kwargs):
        objtype='logistic'
        objname='log'+self.sas._objcnt() #translate to a libname so needs to be less than 8
        code=self._makeProccallMacro(objtype, objname, kwargs)
        logger.debug("LOGISTIC macro submission: " + str(code))
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
             raise AttributeError
        return HTML(data)

    def _go_run_code(self, attr):
        #print(self._name, attr)
        code = '%%getdata(%s, %s);' % (self._name, attr)
        #print (code)
        res=self.sas.submit(code)
        return res['LST']

    def sasdata(self, table):
        x=self.sas.sasdata(table,'_'+self._name)
        return (x)


