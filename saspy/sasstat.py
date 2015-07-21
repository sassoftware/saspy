from IPython.core.display import HTML
from SAS import pysas34 as sas
import time
import logging

# create logger
logger = logging.getLogger('')
logger.setLevel(logging.WARN)


class sasstat:
    def __init__(self, *args, **kwargs):
        '''Submit an initial set of macros to prepare the SAS system'''
        code="options pagesize=max; %include '/root/jared/metis/saspy_pip/saspy/libname_gen.sas'; "
        sas._submit(code,"text")
        logger.debug("Initalization of SAS Macro: " + str(sas._getlog()))

    def __flushlst__(self):
        lst = b'hi'
        while(len(lst) > 0):
           lst = saspid.stdout.read1(4096)
           continue

    def _objectmethods(self,obj,*args):
        self.obj=obj
        clear=sas.getlog(1)
        code  ="%listdata("
        code +=self.obj
        code +=");"
        logger.debug("Object Method macro call: " + str(code))
        sas.submit(code,"text")
        meth=sas.getlog().splitlines()
        logger.debug('SAS Log: ' + str(meth))
        objlist=meth[meth.index('startparse9878')+1:meth.index('endparse9878')]
        logger.debug("PROC attr list: " + str(objlist))
        return objlist

    def hpsplit(self, model='', data=None, **kwargs):
        self.model=model
        self.data=data
        self.objtype='hps'
        self.objname='hps1' #how to give this a better name -- translate to a libname so needs to be less than 8
        code  = "%macro proccall(d);\n"
        code += "proc hpsplit data="
        code += self.data.libref
        code += "."
        code += self.data.table
        code += " plots=all ;"
        if len(model):
            code += "model "+self.model+";"
        code += "run; "
        code += "%mend;\n"
        code += "%mangobj("
        code += self.objname
        code += ","
        code += self.objtype
        code += ","
        code += self.data.table
        code += ");"

        logger.debug("HPSPLIT macro submission: " + str(code))
        sas._submit(code,"text")
        #time.sleep(5)
        try:
            obj1=self._objectmethods(self.objname)
            #print("in try block")
        except Exception:
            #print("Exception Block:", sys.exc_info()[0])
            obj1=[]

        return (Results(obj1,self.objname))

    def _makeProccallMacro(self):
        code  = "%macro proccall(d);\n"
        code += "proc %s data=%s.%s plots(unpack)=all;\n" % (self.objtype, self.data.libref, self.data.table)
        if len(model):
            code += "model %s;" % (self.model)
        if len(self.cls):
            code += "class %s;" % (self.cls)
        code += "run; quit; %mend;\n"
        code += "%mangobj(%s,%s,%s);" % (self.objname, self.objtype,self.data.table)
        logger.debug("Proc code submission: " + str(code))
        return (code)


    def reg(self, model='', data=None, **kwargs):
        self.model=model
        self.data=data
        self.objtype='reg'
        self.objname='reg1' #how to give this a better name
        code=_makeProccallMacro()
        #logger.debug("REG macro submission: " + str(code))
        sas._submit(code,"text")
        #time.sleep(.2)
        try:
            obj1=self._objectmethods(self.objname)
            #print(obj1)
        except Exception:
            obj1=[]
        return (Results(obj1,self.objname))

    def reg2(self, model='', data=None, **kwargs):
        self.model=model
        self.data=data
        self.objtype='reg'
        self.objname='reg1' #how to give this a better name
        code  = "%macro proccall(d);\n"
        code += "proc reg plots(unpack)=all data="
        code += self.data.libref
        code += "."
        code += self.data.table
        code += ";"
        if len(model):
            code += "model "+self.model+";"
        code += "run; quit;"
        code += "%mend;\n"
        code += "%mangobj("
        code += self.objname
        code += ","
        code += self.objtype
        code += ","
        code += self.data.table
        code += ");"

        logger.debug("REG macro submission: " + str(code))
        sas._submit(code,"text")
        #time.sleep(.2)
        try:
            obj1=self._objectmethods(self.objname)
            #print(obj1)
        except Exception:
            obj1=[]
        return (Results(obj1,self.objname))


    def glm(self, model='', data=None, **kwargs):
        self.model=model
        self.data=data
        self.cls=kwargs.get('cls', '')
        self.objtype='glm'
        self.objname='glm1' #how to give this a better name
        code  = "%macro proccall(d);\n"
        code += "proc glm plots(unpack)=all data="
        code += self.data.libref
        code += "."
        code += self.data.table
        code += ";"
        if len(self.cls):
            code += "class %s;" % (self.cls)
        if len(model):
            code += "model "+self.model+";"
        code += "run; quit;"
        code += "%mend;\n"
        code += "%mangobj("
        code += self.objname
        code += ","
        code += self.objtype
        code += ","
        code += self.data.table
        code += ");"

        logger.debug("GLM macro submission: " + str(code))
        sas._submit(code,"text")
        try:
            obj1=self._objectmethods(self.objname)
        except Exception:
            obj1=[]
        return (Results(obj1,self.objname))

from collections import namedtuple

class Results(object):
    '''Return results from a SAS Model object'''
    def __init__(self, attrs, objname):

        self._attrs = attrs
        self._name = objname
        #logger.debug("attributes passed to Results: "+ self._attrs,self._name)

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
        sas._submit(code)
        return sas._getlst()

