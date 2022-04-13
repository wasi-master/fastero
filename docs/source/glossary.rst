########
Glossary
########

.. meta::
   :description: Python timeit CLI for the 21st century.
   :author: Arian Mollik Wasi
   :copyright: Arian Mollik Wasi
   :keywords: Python, Timeit, Fastero, Wasi Master, Arian Mollik Wasi
   :language: English
   :og:title: Fastero Documentation - Glossary
   :og:site_name: Fastero
   :og:type: website
   :og:url: https://fastero.readthedocs.io
   :og:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :og:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :twitter:card: summary_large_image
   :twitter:title: Fastero Documentation - Glossary
   :twitter:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :twitter:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :google-site-verification: upUCfyFeU0JcauOrq_fs4NssKvSo3FzLEnJBTWDBiHY

.. glossary::

    Fastero
        Fastero is the name of the library.
        This name was picked after thinking about a lot of things.
        Namely how `easy it is to type`_, `how much finger travel
        is required`_, trying to `not name it after timeit`_, `keeping
        it short`_, `typing it with one hand`_

    CLI
        A command-line interface (CLI) is a text-based user interface (UI)
        used to run programs, manage computer files and interact with the computer.

    Argument

        Command line arguments are nothing but simply parameters that are specified
        after the name of the program in the system's command line

        .. admonition:: Example
            :class: hint

            .. code-block:: bash

                ls /home/wasi/code

            Here ``ls`` is the name of the program and ``/home/wasi/code`` is the argument

        Some programs may accept multiple arguments.

    Option

        A command-line option or simply option (also known as a flag or switch) modifies the operation of a command

        .. admonition:: Example
            :class: hint

            .. code-block:: bash

                ls --color auto
                ls --color=auto

            In both cases ``ls`` is the name of the program and ``--color`` is the option, with the value ``auto``

    Flag

        A command-line flag (sometimes also called a flag). Is basically a option without a value. This also
        modifies the operation of a command

        .. admonition:: Example
            :class: hint

            .. code-block:: bash

                ls -a
                ls --all

            In both cases ``ls`` is the name of the program and ``-a`` and ``--all`` are the flags.
            Note that ``-a`` is short for ``--all``

    Run
        A single execution of the code snippet. This is simillar to a "loop" in IPython's ``%timeit``

    Batch
        If you're coming from IPython, A batch is like a "run" in IPython's ``%timeit`` magic
        function. The way fastero basically works is that it runs :py:meth:`timeit.Timer.timeit` multiple
        times which in turn, runs the code ``X`` number of times, and fastero gets the average from the numbers
        timeit returns. A batch is basically some ``X`` amount of :term:`runs <run>` of :py:meth:`timeit.Timer.timeit`
        with ``X`` being a number automatically calculated from the `--time-per-batch`_

    Garbage Collection

        The process of freeing memory when it is not used anymore. Python performs garbage
        collection via reference counting and a cyclic garbage collector that is able to
        detect and break reference cycles. The garbage collector can be controlled using
        the gc module.

    Mean
        For a data set, the arithmetic mean, also known as arithmetic average,
        is a central value of a finite set of numbers: specifically, the sum of
        the values divided by the number of values. [#]_

    Standard deviation
        In statistics, the standard deviation is a measure of the amount of variation
        or dispersion of a set of values. A low standard deviation indicates that
        the values tend to be close to the mean (also called the expected value) of
        the set, while a high standard deviation indicates that the values are spread
        out over a wider range. [#]_

    σ
        Standard deviation may be abbreviated SD, and is most commonly represented in
        mathematical texts and equations by the lower case Greek letter sigma σ [#]_

    JSON

        JSON stands for JavaScript Object Notation. It is a lightweight data-interchange
        format. It is easy to parse and generate.

    CSV

        A CSV (comma-separated values) file is a text file that has a specific format which
        allows data to be saved in a table structured format.

    YAML

        YAML stands for "yet another markup language" or "YAML ain't markup language" (a recursive acronym).
        is a human-friendly, cross language, Unicode based data serialization language designed around
        the common native data structures of agile programming languages.

    Markdown

        Markdown is a lightweight markup language that you can use to add
        formatting elements to plaintext text documents.

    AsciiDoc

        AsciiDoc is a text document format for writing notes, documentation,
        articles, books, ebooks, slideshows, web pages, man pages and blogs.

    SVG

        SVG stands for Scalable Vector Graphics. They are scalable without losing
        any quality as opposed to raster graphics.

    Bar Chart

        A bar chart or bar graph is a chart or graph that presents categorical data
        with rectangular bars with heights or lengths proportional to the values that
        they represent.

.. _easy it is to type: https://clig.dev/#:~:text=Make%20it%20easy%20to%20type.%20Some%20words%20flow%20across%20the%20QWERTY%20keyboard%20much%20more%20easily%20than%20others%2C%20and%20it%E2%80%99s%20not%20just%20about%20brevity.%20plum%20may%20be%20short%20but%20it%E2%80%99s%20an%20awkward%2C%20angular%20dance.%20apple%20trips%20you%20up%20with%20the%20double%20letter.%20orange%20is%20longer%20than%20both%2C%20but%20flows%20much%20better.
.. _how much finger travel is required: https://smallstep.com/blog/the-poetics-of-cli-command-names/#:~:text=How%20does%20it%20feel%20to%20type%20the%20command%3F%20Is%20it%20awkward%20or%20satisfying%3F%20How%20much%20finger%20travel%20is%20required%3F%20For%20example%2C%20sha256sum%20feels%20like%20gargling%20sand%2C%20but%20Wireshark%E2%80%99s%20capinfos%20command%20is%20a%20soft%20breeze%20across%20the%20keys.
.. _not name it after timeit: https://smallstep.com/blog/the-poetics-of-cli-command-names/#:~:text=Don%E2%80%99t%20name%20your%20command%20after%20the,Imagine%20if%20Slack%20called%20itself%20webirc.
.. _keeping it short: https://smallstep.com/blog/the-poetics-of-cli-command-names/#:~:text=Not%20all%20of%20the%20best%202%2D5%20letter%20words%20have%20been%20used%20up.%20Please%20don%E2%80%99t%20make%20me%20tab%20complete%20the%20name%20of%20your%20command.
.. _typing it with one hand: https://smallstep.com/blog/the-poetics-of-cli-command-names/#:~:text=Can%20you%20type%20your%20command%20with%20one%20hand%E2%80%94like%20cat%E2%80%94while%20your%20other%20hand%20is%20on%20the%20mouse%3F
.. _--time-per-batch: ./documentation/cli_reference_automated.html#cmdoption-fastero-b
.. [#] From https://en.wikipedia.com/wiki/Mean
.. [#] From `https://en.wikipedia.com/wiki/Standard_deviation <https://en.wikipedia.com/wiki/Standard_deviation#:~:text=In%20statistics%2C%20the,a%20wider%20range.>`_
.. [#] From `https://en.wikipedia.com/wiki/Standard_deviation <https://en.wikipedia.com/wiki/Standard_deviation#:~:text=Standard%20deviation%20may%20be%20abbreviated%20SD%2C%20and%20is%20most%20commonly%20represented%20in%20mathematical%20texts%20and%20equations%20by%20the%20lower%20case%20Greek%20letter%20sigma%20%CF%83%2C>`_
