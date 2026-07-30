#!/usr/bin/env python
# @Author: Arian Mollik Wasi
# @Date: 2024-08-20
# @Description: Improved Shell lexer for Pygments with better fastero command highlighting
"""Pygments Shell Lexer shell_lexer/shell.py

    * http://pygments.org/docs/lexerdevelopment/
    * Enhanced shell lexer specifically for fastero documentation
"""
from __future__ import print_function

from pygments.lexer import RegexLexer, bygroups, words, include
from pygments.token import (
    Keyword, Literal, Name, Operator, Punctuation, Generic, Text, 
    Comment, String, Number, Error
)

class ImprovedShellLexer(RegexLexer):
    """Improved Shell lexer for Pygments with enhanced fastero command support.
        
    Extends:
        pygments.lexer.RegexLexer
        
    Features:
        - Dimmed options (--option, -o)
        - Colored command names (first word)  
        - Colored strings
        - Special handling for fastero commands
    """
    
    name = 'ImprovedShell'
    aliases = ['improved-shell', 'ishell', 'bash-enhanced']
    filenames = ['*.sh', '*.bash']
    mimetypes = ['application/x-sh', 'text/x-shellscript']
    
    tokens = {
        'root': [
            # Comments
            (r'#.*$', Comment.Single),
            
            # Shebang
            (r'^#!.*$', Comment.Preproc),
            
            # Command at start of line (first word)
            (r'^(\s*)([a-zA-Z_][a-zA-Z0-9_.-]*)', bygroups(Text, Name.Builtin)),
            
            # Python module calls (python -m fastero)
            (r'(\bpython\b)(\s+)(-m)(\s+)(\bfastero\b)', 
             bygroups(Name.Builtin, Text, Generic.Strong, Text, Name.Builtin.Pseudo)),
            
            # Long options (dimmed)
            (r'(--[a-zA-Z-]+)', Generic.Weak),
            
            # Short options (dimmed)  
            (r'(-[a-zA-Z])', Generic.Weak),
            
            # Strings with single quotes
            (r"'([^'\\]|\\.)*'", String.Single),
            
            # Strings with double quotes
            (r'"([^"\\]|\\.)*"', String.Double),
            
            # Backslash continuation
            (r'\\\s*\n', Text),
            
            # File paths
            (r'[./~][^\s]*', String.Other),
            
            # Numbers
            (r'\b\d+\b', Number.Integer),
            
            # Environment variables
            (r'\$[a-zA-Z_][a-zA-Z0-9_]*', Name.Variable),
            (r'\$\{[^}]+\}', Name.Variable),
            
            # Common shell operators
            (r'[|&;<>(){}]', Punctuation),
            
            # Pipes and redirects
            (r'[|&>]+', Operator),
            
            # Whitespace
            (r'\s+', Text),
            
            # Everything else
            (r'.', Text),
        ]
    }


# Sample shell script for testing
sample_shell = """#!/bin/bash
# This is a sample shell script for testing the lexer

python -m fastero \\
    --from-json python_http_library_benchmark_input.json \\
    --runs 25 \\
    --export-json export/python_http_library_benchmark.json \\
    --export-csv export/python_http_library_benchmark.csv \\
    --export-yaml export/python_http_library_benchmark.yaml \\
    --export-markdown export/python_http_library_benchmark.md \\
    --export-svg export/python_http_library_benchmark.svg \\
    --export-asciidoc export/python_http_library_benchmark.adoc \\
    --export-image export/python_http_library_benchmark.png \\
    --export-plot export/python_http_library_benchmark_plot.png \\
    --label-format "{snippet_name}"

echo "Benchmark complete!"

# Another example
fastero "print('hello')" "print('world')" -n "greeting1" -n "greeting2" --runs 100
"""

if __name__ == '__main__':
    # Test the lexer
    from pygments import highlight
    from pygments.formatters import TerminalFormatter
    
    lexer = ImprovedShellLexer()
    formatter = TerminalFormatter()
    result = highlight(sample_shell, lexer, formatter)
    print(result)