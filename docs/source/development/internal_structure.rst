#################
Internal Stucture
#################

.. meta::
   :description: Python timeit CLI for the 21st century.
   :author: Arian Mollik Wasi
   :copyright: Arian Mollik Wasi
   :keywords: Python, Timeit, Fastero, Wasi Master, Arian Mollik Wasi
   :language: English
   :og:title: Fastero Documentation - Internal Structure
   :og:site_name: Fastero
   :og:type: website
   :og:url: https://fastero.readthedocs.io
   :og:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :og:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :twitter:card: summary_large_image
   :twitter:title: Fastero Documentation - Internal Structure
   :twitter:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :twitter:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :google-site-verification: upUCfyFeU0JcauOrq_fs4NssKvSo3FzLEnJBTWDBiHY

Fastero's internal structure isn't really the best.
It's arguably even worse than my other projects.
Most of this project was planned and built as fast
as possible without much thought being given to the
design and readability of the code.

Repository Layout
-----------------

* ``.vscode/``
   * ``settings.json`` - Visual Studio Code project specific settings
* ``docs/`` - Documentation for the project
   * ``source/`` - Source code for the documentation
      * ``_static/`` - Static files for the website
      * ``*.rst`` - RST files. These are used for the actual content of the documentation
* ``examples/`` - Examples on how to use fastero
   *  ``export/`` - Examples on how the exported data looks
   * ``*.ps1`` - Powershell script files. These can be ran on Windows
   * ``*.sh`` - Shell script files. These can be ran on Linux and MacOS
* ``fastero/`` - Source code for fastero
    * ``__init__.py`` - The ``__init__.py`` files are required to make Python
      treat directories containing the file as packages.
    * ``__main__.py`` - The ``__main__.py`` is used for python programs that
      need to be ran from the command line. For example, ``python -m fastero``
    * ``core.py`` - Contains the core code from fastero
    * ``exporter.py`` - Contains code used for all kinds of different output formats
    * ``utils.py`` - Short and simple utility functions and classes used by fastero

* ``.gitattributes`` - File used to tell git to perform `LF Normalization`_
* ``.gitignore`` - File used to tell git what files to not include in the repository
* ``LICENSE`` - License information for the source code
* ``logo.png`` and ``logo.jpg`` - The logo of fastero
* ``README.md`` - A guide that gives users a detailed description of the project.
* ``schema.json`` - The schema used for the JSON export.
* ``setup.cfg`` - The configuration file for setuptools
* ``setup.py`` - The python file for setuptools
* ``TODO.md`` - List of things yet to do

.. _LF Normalization: https://www.aleksandrhovhannisyan.com/blog/crlf-vs-lf-normalizing-line-endings-in-git/#crlf-vs-lf-what-are-line-endings-anyway