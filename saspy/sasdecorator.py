import logging

from functools import wraps
from saspy.sasproccommons import SASProcCommons
from pdb import set_trace as bp

class procDecorator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARN)
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
                proc = func.__name__.lower()
                inner.proc_decorator = kwargs
                self.logger.debug("processing proc:{}".format(func.__name__))
                self.logger.debug(req_set)
                self.logger.debug("kwargs type: " + str(type(kwargs)))
                if proc in ['hplogistic', 'hpreg']:
                    kwargs['ODSGraphics'] = kwargs.get('ODSGraphics', False)
                if proc == 'hpcluster':
                    proc = 'hpclus'
                legal_set = set(kwargs.keys())
                self.logger.debug(legal_set)
                return SASProcCommons._run_proc(self, proc, req_set, legal_set, **kwargs)
            return inner
        return decorator

    def doc_convert(ls, proc: str = '') -> dict:
        """
        The `doc_convert` method takes two arguments: a list of the valid statements and the proc name.
        It returns a dictionary with two keys, method_stmt and markup_stmt.
        These outputs can be copied into the appropriate product file.

        :param proc: str
        :return: dict with two keys  method_stmt and markup_stmt
        """

        generic_terms = ['procopts', 'stmtpassthrough']
        assert isinstance(ls, set)
        ls_list = [x.lower() for x in ls]
        doc_list = []
        doc_markup = []
        for i in [j for j in ls_list if j not in generic_terms]:
            if i.lower() == 'class':
                i = 'cls'
            doc_mstr = ''.join([':parm ', i, ': The {} variable can only be a string type.'.format(i)])
            doc_str = ': str = None,'

            if i.lower() in ['target', 'input']:
                doc_mstr = ''.join([':parm ', i,
                                    ': The {} variable can be a string, list or dict type. It refers to the dependent, y, or label variable.'.format(i)])
                doc_str = ': [str, list, dict] = None,'
            if i.lower() == 'score':
                doc_str = ": [str, bool, 'SASdata' ] = True,"
            if i.lower() in ['output','out']:
                doc_str = ": [str, bool, 'SASdata' ] = None,"
                doc_mstr = ''.join([':parm ', i,
                                    ': The {} variable can be a string, boolean or SASdata type. The member name for a boolean is "_output".'.format(i)])
            if i.lower() in ['cls']:
                doc_mstr = ''.join([':parm ', i,
                                    ': The {} variable can be a string or list type. It refers to the categorical, or nominal variables.'.format(i)])
                doc_str = ': [str, list] = None,'
            if i.lower() in ['id', 'by']:
                doc_mstr = ''.join([':parm ', i, ': The {} variable can be a string or list type. '.format(i)])
                doc_str = ': [str, list] = None,'
            if i.lower() in ['level', 'irregular', 'slope', 'estimate' ]:
                doc_str = ": [str, bool] = True,"

            doc_list.append(''.join([i, doc_str, '\n']))
            doc_markup.append(''.join([doc_mstr, '\n']))
        doc_list.sort()
        doc_markup.sort()
        # add procopts and stmtpassthrough last for each proc
        for j in generic_terms:
            doc_list.append(''.join([j, doc_str, '\n']))
            doc_mstr = ''.join([':parm ', j,
                                ': The {} variable is a generic option available for advanced use. It can only be a string type.'.format(j)])
            doc_markup.append(''.join([doc_mstr, '\n']))

        doc_markup.insert(0, ''.join([':param data: SASdata object or string. This parameter is required..', '\n']))
        first_line = ''.join(["data: ['SASdata', str] = None,", '\n'])
        if len(proc):
            first_line = ''.join(["def {}(self, data: ['SASdata', str] = None,".format(proc), '\n'])
            doc_markup.insert(0, ''.join(['Python method to call the {} procedure.\n'.format(proc.upper()),
                                          '\n', 'Documentation link:', '\n\n']))
        doc_list.insert(0, first_line)
        doc_list.append("**kwargs: dict) -> 'SASresults':")

        doc_markup.append(''.join([':return: SAS Result Object', '\n']))

        return {'method_stmt' : ''.join(doc_list), 'markup_stmt' : ''.join(doc_markup)}