from IPython.core.display import HTML
from pygments import highlight
from pygments.lexer import RegexLexer
from pygments.formatters import HtmlFormatter
from pygments.token import *
from pygments.style import Style

class SASLogStyle(Style):
    default_style = ""
    styles = {
        Comment:                '#0000FF',
        Keyword:                'bold #ff0000',
        Name:                   '#008000',
        String:                 'bg:#eee #111',
        Text:                   'bg:#eee #111'
    }

class SASLogLexer(RegexLexer):
    __all__ = ['SASLogLexer']
    name = 'Lexer to Color SAS Logs equivilent to DMS'

    tokens = {
        'root': [
            (r'\d+.*$', String),
            (r'^NOTE.*$', Comment),
            (r'^ERROR.*$', Keyword),
            (r'^WARNING.*$', Name)
        ]
    }


