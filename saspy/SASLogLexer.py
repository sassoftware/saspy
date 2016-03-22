from pygments.lexer import RegexLexer
import pygments.token
from pygments.style import Style


class SASLogStyle(Style):
    default_style = ""
    styles = {
        pygments.token.Comment: '#0000FF',
        pygments.token.Keyword: 'bold #ff0000',
        pygments.token.Name: '#008000',
        pygments.token.String: '#111'
    }


class SASLogLexer(RegexLexer):
    __all__ = ['SASLogLexer']
    name = 'Lexer to Color SAS Logs equivilent to DMS'
    tokens = {
        'root': [
            (r'^\d+.*((\n|\t|\n\t)[ ]([^WEN].*)(.*))*', pygments.token.String),
            (r'^NOTE.*((\n|\t|\n\t)[ ]([^WEN].*)(.*))*', pygments.token.Comment.Multiline, 'note'),
            (r'^ERROR.*((\n|\t|\n\t)[ ]([^WEN].*)(.*))*', pygments.token.Keyword.Multiline, 'error'),
            (r'^WARNING.*((\n|\t|\n\t)[ ]([^WEN].*)(.*))*', pygments.token.Name.Multiline, 'warning'),
            (r'\s', pygments.token.Text)
        ],
        'error': [
            (r'^\s+.*$', pygments.token.Keyword.Multiline),
            (r'^\S+.*$', pygments.token.Keyword.Multiline, '#pop')
        ],
        'note': [
            (r'^\s+.*$', pygments.token.Comment.Multiline),
            (r'^\S+.*$', pygments.token.Comment.Multiline, '#pop')
        ],
        'warning': [
            (r'^\s+.*$', pygments.token.Name.Multiline),
            (r'^\S+.*$', pygments.token.Name.Multiline, '#pop')
        ]
        
    }
