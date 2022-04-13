##########
Quickstart
##########

.. meta::
   :description: Python timeit CLI for the 21st century.
   :author: Arian Mollik Wasi
   :copyright: Arian Mollik Wasi
   :keywords: Python, Timeit, Fastero, Wasi Master, Arian Mollik Wasi
   :language: English
   :og:title: Fastero Documentation - Quickstart
   :og:site_name: Fastero
   :og:type: website
   :og:url: https://fastero.readthedocs.io
   :og:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :og:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :twitter:card: summary_large_image
   :twitter:title: Fastero Documentation - Quickstart
   :twitter:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :twitter:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :google-site-verification: upUCfyFeU0JcauOrq_fs4NssKvSo3FzLEnJBTWDBiHY

Fastero is available on `PyPI <https://pypi.org/project/fastero/>`_. To install it to your system:

1. Install with pip

   .. tab:: Normal

      .. code-block:: bash

         pip install "fastero"

      This will just install fastero and it's required Dependencies.
      If you want to export plots, images, or yaml then you need the
      extra exporting dependencies

   .. tab:: With Exporting Dependencies

      .. code-block:: bash

         pip install "fastero[export]"

      This will install matplotlib, pyyaml, selenium, and Pillow alongside fastero.
      These libraries are required for exporting specific files

2. Install with pipx

   .. tab:: Normal

      .. code-block:: bash

         pipx install "fastero"

      This will just install fastero and it's required Dependencies.
      If you want to export plots, images, or yaml then you need the
      extra exporting dependencies

   .. tab:: With Exporting Dependencies

      .. code-block:: bash

         pipx install "fastero[export]"

      This will install matplotlib, pyyaml, selenium, and Pillow alongside fastero.
      These libraries are required for exporting specific files

3. Install with pip from github

   .. tab:: Normal

      .. code-block:: bash

         pip install "git+https://github.com/wasi-master/fastero"

      This will just install fastero and it's required Dependencies.
      If you want to export plots, images, or yaml then you need the
      extra exporting dependencies

   .. tab:: With Exporting Dependencies

      .. code-block:: bash

         pip install "fastero[export] @ git+https://github.com/wasi-master/fastero"

      This will install matplotlib, pyyaml, selenium, and Pillow alongside fastero.
      These libraries are required for exporting specific files

.. important::
   Fastero requires python 3.7 and higher

To check if it is installed correctly you can run the following command:

.. code-block:: bash

   fastero --help

If that doesn't work, try:

.. code-block:: bash

   python -m fastero --help

You may need to replace ``python`` with your installation specific python command.
If that still doesn't work, make sure you have python 3.7+ installed and added to path
