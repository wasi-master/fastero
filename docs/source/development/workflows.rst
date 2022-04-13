#########
Workflows
#########

.. meta::
   :description: Python timeit CLI for the 21st century.
   :author: Arian Mollik Wasi
   :copyright: Arian Mollik Wasi
   :keywords: Python, Timeit, Fastero, Wasi Master, Arian Mollik Wasi
   :language: English
   :og:title: Fastero Documentation - Workflows
   :og:site_name: Fastero
   :og:type: website
   :og:url: https://fastero.readthedocs.io
   :og:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :og:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :twitter:card: summary_large_image
   :twitter:title: Fastero Documentation - Workflows
   :twitter:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :twitter:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :google-site-verification: upUCfyFeU0JcauOrq_fs4NssKvSo3FzLEnJBTWDBiHY

Cloning the repository
----------------------

To clone the repository, make sure you have `git <https://git-scm.com>`_
installed and available on your system. To clone, run the following command
in a terminal

.. code-block:: shell

    git clone "https://github.com/wasi-master/fastero"

Running the library locally
---------------------------

After making some changes to the code or looking at the code,
you may want to test out the library locally. To install it
from the source code, assuming you are in the root directory of
the repository, run the following command:

.. code-block:: shell

    pip install .

You may need to change ``pip`` to ``pip3`` if you have both python
2 and python 3 installed on your system.

.. admonition:: Alternative
   :class: important

   Alternatively, you can also use the following command to run the CLI
   without installing the library first, do note that this only works in
   the root directory of the repository, to use globally, you have to
   install it.

   .. code-block:: shell

       python -m fastero --help

   ``--help`` is just a demo, you can run any command

Generating the documentation
----------------------------

To build the documentation, you first need to install the requirements from ``requirements-docs.txt``

.. code-block:: shell

    python -m pip install -r requirements-docs.txt

Then you must change the current working directory to the documentation root directory


.. code-block:: shell

    cd docs

Then run the following command to generate the documentation

.. code-block:: shell

    make html

This will generate the required HTML files in the ``build/html`` directory. Go to that directory and open the ``index.html``
file in an web browser and you should see the documentation



