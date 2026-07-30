#!/usr/bin/env python
# @Author: Arian Mollik Wasi
# @Date: 2024-08-20
# @Description: AsciiDoc lexer for Pygments
"""Pygments AsciiDoc Lexer asciidoc_lexer/asciidoc.py

    * http://pygments.org/docs/lexerdevelopment/
    * https://asciidoc.org/
"""
from __future__ import print_function

from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import (
    Keyword, Literal, Name, Operator, Punctuation, Generic, Text, 
    Comment, String, Number, Error
)

class AsciiDocLexer(RegexLexer):
    """Simple AsciiDoc lexer for Pygments.
        
    Extends:
        pygments.lexer.RegexLexer
        
    Class Variables:
        name {str} -- name of lexer
        aliases {list} – languages, against whose GFM block names AsciiDocLexer will apply
        filenames {list} – file name patterns, for whose contents AsciiDocLexer will apply
        tokens {dict} – regular expressions internally matching AsciiDoc's components
    """
    
    name = 'AsciiDoc'
    aliases = ['asciidoc', 'adoc']
    filenames = ['*.asciidoc', '*.adoc', '*.asc']
    mimetypes = ['text/asciidoc']
    
    tokens = {
        'root': [
            # Document title (level 0)
            (r'^= .+$', Generic.Heading),
            
            # Section titles (levels 1-5)
            (r'^={2,6} .+$', Generic.Subheading),
            
            # Comments
            (r'^//.*$', Comment.Single),
            
            # Block delimiters
            (r'^-{4,}$', Punctuation),
            (r'^={4,}$', Punctuation),
            (r'^\.{4,}$', Punctuation),
            (r'^\*{4,}$', Punctuation),
            (r'^\+{4,}$', Punctuation),
            (r'^_{4,}$', Punctuation),
            
            # Attributes
            (r'^:([^:]+):\s*(.*)$', bygroups(Name.Attribute, String)),
            
            # Lists
            # Unordered lists
            (r'^\s*(\*+)\s+(.+)$', bygroups(Operator, Text)),
            # Ordered lists  
            (r'^\s*(\.\s*)+(.+)$', bygroups(Operator, Text)),
            # Definition lists
            (r'^(.+)::\s*$', Name.Tag),
            (r'^\s+(.+)$', Text),
            
            # Tables
            (r'^\|={3,}$', Punctuation),
            (r'^\|(.*)$', bygroups(Generic.Strong)),
            
            # Block titles
            (r'^\.[A-Za-z].*$', Name.Decorator),
            
            # Inline formatting
            # Bold
            (r'\*([^*\n]+)\*', Generic.Strong),
            # Italic  
            (r'_([^_\n]+)_', Generic.Emph),
            # Monospace
            (r'`([^`\n]+)`', Literal),
            # Superscript
            (r'\^([^^]+)\^', Generic.Emph),
            # Subscript  
            (r'~([^~]+)~', Generic.Emph),
            
            # Links
            (r'(https?://[^\s\[\]]+)(\[[^\]]*\])?', bygroups(Name.Variable, String)),
            (r'(mailto:[^\s\[\]]+)(\[[^\]]*\])?', bygroups(Name.Variable, String)),
            (r'<<([^,>]+)(,[^>]*)?>>', bygroups(Name.Variable, String)),
            
            # Images
            (r'image:([^\[\s]+)(\[[^\]]*\])', bygroups(Name.Variable, String)),
            
            # Macros
            (r'([a-zA-Z0-9_-]+):([^\[\s]+)(\[[^\]]*\])', bygroups(Keyword, Name.Variable, String)),
            
            # Passthroughs
            (r'\+{3}(.+?)\+{3}', Literal),
            (r'\${2}(.+?)\${2}', Literal),
            
            # Line breaks and spaces
            (r'\s+', Text),
            
            # Everything else
            (r'.', Text),
        ]
    }


# Sample AsciiDoc content for testing
sample_asciidoc = """
= Document Title
:author: John Doe
:email: john.doe@example.com

== Introduction

This is a *bold* text and this is _italic_ text.
You can also use `monospace` text.

=== Code Example

----
def hello_world():
    print("Hello, World!")
----

=== Lists

* First item
* Second item
  ** Sub-item
  ** Another sub-item

. Numbered item
. Another numbered item

Definition Term:: 
    This is the definition of the term.

=== Links and Images

Check out https://asciidoc.org[AsciiDoc] for more information.

image:logo.png[Company Logo]

=== Table

|===
|Name |Age |Location

|John
|30
|New York

|Jane
|25
|London
|===
"""

if __name__ == '__main__':
    # Test the lexer
    from pygments import highlight
    from pygments.formatters import TerminalFormatter
    
    lexer = AsciiDocLexer()
    formatter = TerminalFormatter()
    result = highlight(sample_asciidoc, lexer, formatter)
    print(result)