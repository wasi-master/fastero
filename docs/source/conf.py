# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('./documentation'))
sys.path.insert(0, os.path.abspath('./development'))


# -- Project information -----------------------------------------------------

project = 'fastero'
copyright = '2022, Arian Mollik Wasi'
author = 'Arian Mollik Wasi'

# The full version, including alpha/beta/rc tags
release = '0.1.0rc1'

# -- Pygments lexer patching -------------------------------------------------

from pygments import token
from sphinx.highlighting import lexers
from csv_lexer import CsvLexer

lexers['csv'] = CsvLexer(startinline=True)

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.intersphinx',

    "sphinx-favicon",
    'sphinx_click',
    'sphinx_inline_tabs',
    'sphinx_copybutton',
    'sphinx_rst_builder',
    'sphinxcontrib.details.directive'
]

favicons = [
    {
        "rel": "icon",
        "static-file": "favicon.ico",  # => use `_static/icon.svg`
        "type": "image/x-icon",
    },
    {
        "rel": "icon",
        "sizes": "16x16",
        "static-file": "avicon-16x16.png",
        "type": "image/png",
    },
    {
        "rel": "icon",
        "sizes": "32x32",
        "static-file": "avicon-32x32.png",
        "type": "image/png",
    },
    {
        "rel": "apple-touch-icon",
        "sizes": "180x180",
        "static-file": "apple-touch-icon.png",
        "type": "image/png",
    },
    {
        "rel": "manifest",
        "static-file": "site.webmanifest",
    },
]

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'
html_logo = "_static/logo.png"
html_css_files = [
    'https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap',
    'custom.css'
]
html_theme_options = {
    "light_css_variables": {
        "font-stack": "Quicksand, Raleway, Montserrat, Futura, Poppins, Josefin Sans, Caviar Dreams, League Spartan, Sofia Pro, Segoe UI, Roboto, Ubuntu, Cantarell, Lato, Noto Sans, Arial, Helvetica sans-serif",
        "font-stack--monospace": "Fira Code, MonoLisa, Source Code Pro, Ubuntu Mono, JetBrains Mono, Hack, Monaco, Menlo, Consolas, Courier, monospace",
        "color-api-name": "#9580ff",
        "color-api-pre-name": "#8975eb"
    },
}

html_title = "Fastero Documentation"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']