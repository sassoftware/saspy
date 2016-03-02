from pygments import highlight
from pygments.lexer import RegexLexer
from pygments.token import *
from pygments.style import Style

class SASLogStyle(Style):
    default_style = ""
    styles = {
        Comment:                '#0000FF',
        Keyword:                'bold #ff0000',
        Name:                   '#008000',
        String:                 '#111'
    }

class SASLogLexer(RegexLexer):
    __all__ = ['SASLogLexer']
    name = 'Lexer to Color SAS Logs equivilent to DMS'
    tokens = {
        'root': [
            (r'^\d+.*((\n|\t|\n\t)[ ]([^WEN].*)(.*))*', String),
            (r'^NOTE.*((\n|\t|\n\t)[ ]([^WEN].*)(.*))*', Comment.Multiline, 'note'),
            (r'^ERROR.*((\n|\t|\n\t)[ ]([^WEN].*)(.*))*', Keyword.Multiline, 'error'),
            (r'^WARNING.*((\n|\t|\n\t)[ ]([^WEN].*)(.*))*', Name.Multiline, 'warning'),
            (r'\s', Text)
        ],
        'error': [
            (r'^\s+.*$',Keyword.Multiline),
            (r'^\S+.*$',Keyword.Multiline,'#pop')
        ],
        'note': [
            (r'^\s+.[\s\S]*',Comment.Multiline),
            (r'^\S+.[\s\S]*',Comment.Multiline,'#pop')
        ],
        'warning': [
            (r'^\s+.*$',Name.Multiline),
            (r'^\S+.*$',Name.Multiline,'#pop')
        ]
        
    }