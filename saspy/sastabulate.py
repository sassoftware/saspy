import logging
from typing import TYPE_CHECKING

try:
    import pandas as pd
except ImportError:
    pass
try:
    from IPython.display import HTML
    from IPython.display import display as DISPLAY
except ImportError:
    pass

from collections import ChainMap
import saspy as sp

if TYPE_CHECKING:
    from saspy.sasresults import SASresults


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
        copy = self.__class__(*self._args, **{k: self.__getattribute__(k) for k in self._kwargs})
        for key, value in kwargs.items():
            copy.__setattr__(key, value)
        return copy

    def __or__(self, other):
        if isinstance(other, TabulationItem):
            return Grouping([self, other])
        if type(other) == Grouping:
            return other.add(self, True)

    def __mul__(self, other):
        if self.child:
            self.child = self.child.__mul__(other)
        else:
            # always clone for composition purposes
            return self.with_(child=other)
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
        if type(other) == Grouping:
            return other.add_all(self.items, True)
        return self.add(other)

    def __mul__(self, other):
        if self.child:
            self.child = self.child.__mul__(other)
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
    if value == False:
        # mainly used for clearing all labels w/ label=False
        kwargs = [{key: ''} for i in range(n)]
    elif value and isinstance(value, str):
        kwargs = [{key: value} for i in range(n)]
    elif value and len(value) == n:
        kwargs = [{key: value[i]} for i in range(n)]
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
        self.logger.debug("Initialization of SAS Macro: " + self.sas.saslog())

    @staticmethod
    def as_class(*args, **kwargs):
        return Class(*args, **kwargs)

    @staticmethod
    def classes(*args, labels: list = []):
        label_kwargs = build_kwargs('label', labels, len(args))
        return [Class(args[i], **label_kwargs[i]) for i in range(len(args))]

    @staticmethod
    def as_var(*args, **kwargs):
        return Var(*args, **kwargs)

    @staticmethod
    def vars(*args, labels: list = []):
        label_kwargs = build_kwargs('label', labels, len(args))
        return [Var(args[i], **label_kwargs[i]) for i in range(len(args))]

    @staticmethod
    def stat(*args, **kwargs):
        return Statistic(*args, **kwargs)

    @staticmethod
    def stats(*args, labels: list = [], formats: list = []):
        label_kwargs = build_kwargs('label', labels, len(args))
        format_kwargs = build_kwargs('format', formats, len(args))
        return [
            Statistic(args[i], **dict(ChainMap(label_kwargs[i], format_kwargs[i])))
            for i in range(len(args))
        ]

    def table(self, **kwargs: dict) -> 'SASresults':
        """
        Executes a PROC TABULATE statement and displays results in HTML

        :param left: the query for the left side of the table
        :param top: the query for the top of the table
        :return:
        """
        return self.execute_table('HTML', **kwargs)

    def text_table(self, **kwargs: dict) -> 'SASresults':
        """
        Executes a PROC TABULATE statement and displays results as plain text

        :param left: the query for the left side of the table
        :param top: the query for the top of the table
        :return:
        """
        return self.execute_table('text', **kwargs)

    def to_dataframe(self, **kwargs: dict) -> 'SASresults':
        """
        Executes a PROC TABULATE statement and converts results to a MultiIndex DataFrame

        :param left: the query for the left side of the table
        :param top: the query for the top of the table
        :return:
        """
        return self.execute_table('Pandas', **kwargs)

    def execute_table(self, _output_type, **kwargs: dict) -> 'SASresults':
        """
        executes a PROC TABULATE statement 

        You must specify an output type to use this method, of 'HTML', 'text', or 'Pandas'.
        There are three convenience functions for generating specific output; see:
            .text_table()
            .table()
            .to_dataframe()

        :param _output_type: style of output to use
        :param left: the query for the left side of the table
        :param top: the query for the top of the table
        :return:
        """

        left = kwargs.pop('left', None)
        top = kwargs.pop('top', None)
        sets = dict(classes=set(), vars=set())
        left._gather(sets)
        if top: top._gather(sets)

        table = top \
                and '%s, %s' % (str(left), str(top)) \
                or str(left)

        proc_kwargs = dict(
            cls=' '.join(sets['classes']),
            var=' '.join(sets['vars']),
            table=table
        )

        # permit additional valid options if passed; for now, just 'where'
        proc_kwargs.update(kwargs)

        # we can't easily use the SASProcCommons approach for submiting, 
        # since this is merely an output / display proc for us;
        # but we can at least use it to check valid options in the canonical saspy way
        required_options = {'cls', 'var', 'table'}
        allowed_options = {'cls', 'var', 'table', 'where'}
        verifiedKwargs = sp.sasproccommons.SASProcCommons._stmt_check(self, required_options, allowed_options,
                                                                      proc_kwargs)

        if (_output_type == 'Pandas'):
            # for pandas, use the out= directive
            code = "proc tabulate data=%s.%s %s out=temptab;\n" % (
            self.data.libref, self.data.table, self.data._dsopts())
        else:
            code = "proc tabulate data=%s.%s %s;\n" % (self.data.libref, self.data.table, self.data._dsopts())

        # build the code
        for arg, value in verifiedKwargs.items():
            code += "  %s %s;\n" % (arg == 'cls' and 'class' or arg, value)
        code += "run;"

        # teach_me_SAS
        if self.sas.nosub:
            print(code)
            return

        # submit the code
        ll = self.data._is_valid()

        if _output_type == 'HTML':
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

        elif _output_type == 'text':
            if not ll:
                html = self.data.HTML
                self.data.HTML = 1
                ll = self.sas._io.submit(code, 'text')
                self.data.HTML = html
            print(ll['LST'])
            return

        elif _output_type == 'Pandas':
            return self.to_nested_dataframe(code)

    def to_nested_dataframe(self, code):
        result = self.sas.submit(code)
        outdata = self.sas.sd2df('temptab')

        # slice groupings (classes) and stats from results table
        classes = outdata.columns[:outdata.columns.tolist().index('_TYPE_')].tolist()
        stats = outdata.columns[outdata.columns.tolist().index('_TABLE_') + 1:].tolist()

        # build frame with nested indices
        frame = pd.DataFrame.from_dict({
            tuple([row['_TYPE_'][i] == '1' and row[c] or '_ALL_' for i, c in enumerate(classes)]): dict(
                (stat, row[stat]) for stat in stats)
            for row in outdata.to_dict(orient='records')
        }, orient='index')
        frame.index = frame.index.set_names(classes)

        return frame
