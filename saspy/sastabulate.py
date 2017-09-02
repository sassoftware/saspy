import logging
from saspy.sasresults import SASresults
try:
    from IPython.display import HTML
    from IPython.display import display as DISPLAY
except ImportError:
    pass

class TabulationItem:
    def __init__(self, key, **kwargs):
        self.key = key
        self.child = None
        self.label = kwargs.get('label', None)
        # for chainable cloning
        self._args = [key]
        self._kwargs = ['label', 'child']
        
    def with_(self, **kwargs):
        # clone with settable properties, merge new properties
        copy = self.__class__(*self._args, **{k:self.__getattribute__(k) for k in self._kwargs})
        for key, value in kwargs.items():
            copy.__setattr__(key, value)
        return copy
        
    def __or__(self, other):
        if isinstance(other, TabulationItem):
            return Grouping([self, other])
        if type(other)==Grouping:
            return other.add(self, True)
    
    def __mul__(self, other):
        if self.child:
            self.child = self.child.__mul__(other)
        else:
            # always clone for composition purposes
            return self.with_(child = other)
        return self
    
    # override for entities needing to add top-level entries
    def _gather(self, collected):
        pass

    
class Class(TabulationItem):
    def __init__(self, key, **kwargs):
        super().__init__(key, **kwargs)
        self.all = kwargs.get('all', None)
        self._kwargs += ['all']
                
    def __str__(self):
        code = self.key
        if self.label != None:
            code += "='%s'" % self.label
        if self.all:
            code = "(%s ALL='%s')" % (code, self.all)
        if self.child:
            code += " * %s" % str(self.child)
        return code
    
    def _gather(self, collected):
        collected['classes'].add(self.key)
        if (self.child):
            self.child._gather(collected)

    
class Var(TabulationItem):                       
    def __str__(self):
        code = self.key
        if self.label != None:
            code += "='%s'" % self.label
        if self.child:
            code += " * %s" % str(self.child)
        return code
    
    def __mul__(self, other):
        if isinstance(other, Class):
            raise SyntaxError('A Class variable cannot be a descendent of a Var')
        return super().__mul__(other)
    
    def _gather(self, collected):
        collected['vars'].add(self.key)
        if (self.child):
            self.child._gather(collected)
    
class Statistic(TabulationItem):
    def __init__(self, key, **kwargs):
        super().__init__(key, **kwargs)
        self.format = kwargs.get('format', None)
        self._kwargs += ['format']
                        
    def __str__(self):
        code = self.key
        if self.label != None:
            code += "='%s'" % self.label
        if self.format:
            code += "*f=%s" % self.format
        return code
    
    def __mul__(self, other):
        raise SyntaxError("Statistics cannot have further descendents")

        
class Grouping:
    def __init__(self, items, **kwargs):
        self.items = items
        self.child = None
    
    def __or__(self, other):
        if type(other)==Grouping:
            return other.add_all(self.items, True)
        return self.add(other)
    
    def __mul__(self, other):
        if self.child:
            self.child.__mul__(other)
        else:
            self.child = other
        return self
    
    def __str__(self):
        code = ' '.join([str(item) for item in self.items])
        if self.child:
            code = '(%s) * %s' % (code, str(self.child))
        return '(%s)' % code
    
    def add(self, other, prepend=False):
        if prepend:
            self.items.insert(0, other)
        else:
            self.items.append(other)
        return self
    
    def add_all(self, others, prepend=False):
        if prepend:
            self.items = others.concat(self.items)
        else:
            self.items = self.items.concat(others)
        return self
    
    def _gather(self, collected):
        for item in self.items:
            item._gather(collected)
        if (self.child):
            self.child._gather(collected)
        
# distribute arg(as key) from value(as list, None, or False)
def build_kwargs(key, value, n):
    if value==False:
        kwargs = [dict(label='') for i in range(n)]
    elif value and isinstance(value, str):
        kwargs = [{key:value} for i in range(n)]
    elif value and len(value)==n:
        kwargs = [{key:value[i]} for i in range(n)]
    else:
        kwargs = [dict() for i in range(n)]
    return kwargs

class Tabulate:
    """
    Adds tabulation functions to a SAS dataset
    """
    def __init__(self, session, data):
        self.data = data
        self.sas = session
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
        self.sasproduct = 'base'

    @staticmethod
    def as_class(*args, **kwargs):
        return Class(*args, **kwargs)

    @staticmethod
    def classes(*args, labels=[]):
        label_kwargs = build_kwargs('label', labels, len(args))
        return [Class(args[i], **label_kwargs[i]) for i in range(len(args))]

    @staticmethod
    def as_var(*args, **kwargs):
        return Var(*args, **kwargs)

    @staticmethod
    def vars(*args, labels=[]):
        label_kwargs = build_kwargs('label', labels, len(args))
        return [Var(args[i], **label_kwargs[i]) for i in range(len(args))]

    @staticmethod
    def stat(*args, **kwargs):
        return Statistic(*args, **kwargs)

    @staticmethod
    def stats(*args, labels=[], formats=[]):
        label_kwargs = build_kwargs('label', labels, len(args))
        format_kwargs = build_kwargs('format', formats, len(args))
        return [Statistic(args[i], **label_kwargs[i], **format_kwargs[i]) for i in range(len(args))]

    def table(self, **kwargs: dict) -> 'SASresults':
        """
        Generates and executes a PROC TABULATE statement 

        :param left: the query for the left side of the table
        :param top: the query for the top of the table
        :return:
        """

        left = kwargs.pop('left', None)
        top = kwargs.pop('top', None)
        sets = dict(classes=set(), vars=set())
        left._gather(sets)
        top._gather(sets)

        table = '%s, %s' % (str(left), str(top))
        proc_kwargs = dict(
            cls   = ' '.join(sets['classes']),
            var   = ' '.join(sets['vars']),
            table = table
        )

        code = "proc tabulate data=%s.%s %s;\n" % (self.data.libref, self.data.table, self.data._dsopts())
        code += "  class %s;\n" % proc_kwargs['cls']
        code += "  var %s;\n" % proc_kwargs['var']
        code += "  table %s;\n" % proc_kwargs['table']
        code += "run;"

        if self.sas.nosub:
            print(code)
            return

        ll = self.data._is_valid()
        if not ll:
            html = self.data.HTML
            self.data.HTML = 1
            ll = self.sas._io.submit(code)
            self.data.HTML = html
        if not self.sas.batch:
            DISPLAY(HTML(ll['LST']))
            check, errorMsg = self.data._checkLogForError(ll['LOG'])
            if not check:
                raise ValueError("Internal code execution failed: " + errorMsg)
        else:
            return ll
        
