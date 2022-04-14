#########################
Tips, Recipies, and Notes
#########################

.. meta::
   :description: Python timeit CLI for the 21st century.
   :author: Arian Mollik Wasi
   :copyright: Arian Mollik Wasi
   :keywords: Python, Timeit, Fastero, Wasi Master, Arian Mollik Wasi
   :language: English
   :og:title: Fastero Documentation - Tips, Recipies, and Notes
   :og:site_name: Fastero
   :og:type: website
   :og:url: https://fastero.readthedocs.io
   :og:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :og:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :twitter:card: summary_large_image
   :twitter:title: Fastero Documentation - Tips, Recipies, and Notes
   :twitter:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :twitter:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :google-site-verification: upUCfyFeU0JcauOrq_fs4NssKvSo3FzLEnJBTWDBiHY


.. role:: python(code)
   :language: python
   :class: highlight

Supressing output from the benchmark
""""""""""""""""""""""""""""""""""""

In your setup, use

.. code-block:: python

   import sys, os
   sys.stdout = sys.stderr = open(os.devnull, 'a', encoding='utf-8')

Or in one line:

.. code-block:: python

   import sys, os; sys.stdout = sys.stderr = open(os.devnull, 'a', encoding='utf-8')

Using stdin as an input
"""""""""""""""""""""""

In fastero, ``"-"`` Is not used for stdin, you should use ``"file: stdin"`` instead

100-400ns overhead
""""""""""""""""""

First I'll show you this example

.. code-block:: pycon

   Python 3.11.0a6 (main, Mar  7 2022, 16:46:19) [MSC v.1929 64 bit (AMD64)] on win32
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import timeit
   >>> timeit.timeit(number=1) * 1_000_000
   0.39999940781854093
   >>> timeit.timeit(number=1_000_000)
   0.010034400002041366

Although both of them are supposed to have the same value (in an ideal situation).
The first one is almost 40 times lower.

This also applies to ``number=2`` but the difference is almost cut in half (20 times slower).

.. code-block:: pycon

   >>> timeit.timeit(number=2) * 1_000_000
   0.39999940781854093
   >>> timeit.timeit(number=2_000_000)
   0.019674099999974715

Due to this reason. Using very low run count will result in a 100-400 nanosecond overhead.
This will not matter most of the time. Because, if you are dealing with code so fast that
this is gonna matter, the run count will probably be very high so it won't matter anymore.
But I would still like to mention it here in case someone's wondering

Programmatic Usage
------------------

Although fastero isn't meant to be used programmatically, you can use it, with the use of
shell commands

.. code-block:: python

   import os
   import json

   data = json.loads(os.popen("fastero \"str(1)\" \"f'{1}'\" --json --quiet").read())
   print(data['results'][0]['min'])  # This will output the minimum time required to run "str(1)"
