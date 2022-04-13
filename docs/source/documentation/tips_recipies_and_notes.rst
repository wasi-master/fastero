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


