#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
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
