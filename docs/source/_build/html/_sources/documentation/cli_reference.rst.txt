#############
CLI Reference
#############

.. meta::
   :description: Python timeit CLI for the 21st century.
   :author: Arian Mollik Wasi
   :copyright: Arian Mollik Wasi
   :keywords: Python, Timeit, Fastero, Wasi Master, Arian Mollik Wasi
   :language: English
   :og:title: Fastero Documentation - CLI Reference
   :og:site_name: Fastero
   :og:type: website
   :og:url: https://fastero.readthedocs.io
   :og:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :og:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
   :twitter:card: summary_large_image
   :twitter:title: Fastero Documentation - CLI Reference
   :twitter:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
   :twitter:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out

This is a hand-written version of the CLI Reference.
It may be outdated, if it is please kindly remind me
to update it in a github issue or open a pull request.
In the case of it being out of date (not having some option or argument),
You may want to check out the :doc:`Automated CLI Reference <./cli_reference_automated>`.

This does not cover exporting, those are covered in their own page :ref:`Exporting Reference <exporting-reference>` and
the parameters are covered in :ref:`CLI Reference (Automated) <cli-reference-automated>`


Also, this version is very long and filled with examples. :)


*******
fastero
*******

.. code-block:: shell

   fastero [CODE_SNIPPETS...] [OPTIONS]

Arguments
^^^^^^^^^

These are the positional arguments, opposed to options, these don't
require any prefix and are directly passed

.. option:: CODE_SNIPPETS

   The snippets to benchmark. There may be multiple

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero "str(1)" "f'{1}'"

      .. details:: Output

         If the image below looks blurry then click it to open it in fullscreen

         .. image:: ../_static/images/str_vs_fstring.png
            :width: 1161
            :alt: Output image

   Any of these can be ``-``, to get the input later. Useful for multi-line inputs

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero - -

      .. details:: Output

         If the image below looks blurry then click it to open it in fullscreen

         .. image:: ../_static/images/code_input_with_prompt.gif
            :width: 1233
            :alt: Output image

   You can also use ``file:`` to read output from a file. If your code starts with ``file:``,
   you can escape this behavior by adding 2 spaces after the ``:``, e.g. ``file:  foo``

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero "file: foo.py" "file: bar.py"

      .. details:: Output

         If the image below looks blurry then click it to open it in fullscreen

         .. image:: ../_static/images/code_input_with_file.png
            :width: 1233
            :alt: Output image

   The filename for ``file:`` can also be ``stdin`` to accept output piped from another program

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         echo "str(1)" | fastero "file: stdin"

   All of these can also be used together.

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero "str(1)" "file: bar.py" -

      This would mean the first argument is ``str(1)``,
      the second argument is the contents of bar.py,
      the third argument is the one given later

      .. TODO: Add Output (Preferably a GIF)
      .. .. details:: Output

      ..    If the image below looks blurry then click it to open it in fullscreen

      ..    .. image:: ../_static/images/code_input_with_file.png
      ..       :width: 1233
      ..       :alt: Output image


Options
^^^^^^^

.. option:: -v, --version

   Output the version of fastero that is currently being used

.. option:: -h, --help

   Show the help message

.. option:: -n, --snippet-name <NAME>

   Assign a name to a snippet.

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero "f'{1}'" -n "f-string"

      .. details:: Output

         If the image below looks blurry then click it to open it in fullscreen

         .. image:: ../_static/images/assigning_a_name_to_a_snippet.png
            :width: 1233
            :alt: Output image

   This argument can be used multiple times

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero "f'{1}'" "'{}'.format(1)" -n "f-string" -n "str.format()"

      .. details:: Output

         If the image below looks blurry then click it to open it in fullscreen

         .. image:: ../_static/images/assigning_names_to_multiple_snippets.png
            :width: 1233
            :alt: Output image

.. option:: -s, --setup <STMT>

   Provide some code to use as the initial setup for the benchmark snippets.
   This can be used to initialize classes, set variables, import libraries etc.

   .. admonition:: **Default**
      :class: default

      The default value for setup is ``pass``. This is done to be consistent with
      `timeit <https://docs.python.org/3/library/timeit.html#timeit.timeit>`_

   The format is the exact same as the ``CODE_SNIPPETS`` argument. Meaning it
   supports the ``file:`` directive to get from an file or stdin and the ``"-"``
   parameter to enter multiline input in a prompt

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero --setup "l = [0]" "a, = l" "a = l[0]"

      .. details:: Output

         If the image below looks blurry then click it to open it in fullscreen

         .. image:: ../_static/images/setup.png
            :width: 1233
            :alt: Output image

.. option:: -f, --from-json <FILE>

   Get input from a json file.

   .. admonition:: Format
      :class: info

      If you only want to get parameters, the format should be this:

      .. code-block:: json

         {
            "setup": "l = [0]",
            "results": [
               {
                  "snippet_name": "unpacking",
                  "snippet_code": "a, = l"
               },
               {
                  "snippet_name": "indexing",
                  "snippet_code": "a = l[0]"
               }
            ]
         }

      The keys ``snippet_name`` and ``setup`` are optional!

      If you however, want to get other information like the :term:`mean` and :term:`standard deviation`,
      you have to use a json file specifically generated by fastero, or one that uses the same format as fastero,

      .. seealso::

         ``--export-json``, `\--json <#cmdoption-j>`_

   .. admonition:: Example
      :class: hint

      Assuming the contents of foo.json are as above:

      .. code-block:: shell

         fastero --from-json foo.json

      Then the output will be the one showed at the end of the ``--setup`` section

   You can do a whole bunch of stuff by using this flag. For example if you want to
   re-preview the results from a json file, you can run

   .. code-block:: shell

      fastero --from-json foo.json --only-export

   Yes I know, this option name is bit unintuitive, since this doesn't have any export parameters,
   but when I named this option, I thought about what if people want to only export the data
   from the json file, I am open to renaming suggestions though

   If you want to export the results in one of the export formats, then you can add those export options
   alongside the ``--from-json`` and ``--only-export``, e.g.

   .. code-block:: shell

      fastero --from-json foo.json --only-export --export-image

   So now, it will get the run results from the ``foo.json`` file and then export a png file with those results

.. option:: -j, --json

   Only print json results. This is simillar to the ``--export-json`` option but instead of exporting to a file,
   this outputs the json results to standard output. This is given only for scripting purposes. A better reasoning
   is given in `Command Line Interface Guidelines`_

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero "f'{1}'" "'{}'.format(1)" -n "f-string" -n "str.format()" --json

      .. details:: Output

         .. code-block:: json

            {
               "setup": "pass",
               "results": [
                  {
                        "snippet_code": "f'{1}'",
                        "snippet_name": "f-string",
                        "runs": 55000000,
                        "mean": 5.442414363636363e-08,
                        "median": 5.392934e-08,
                        "min": 5.3144839999999946e-08,
                        "max": 6.013294000000001e-08,
                        "stddev": 1.926783849689808e-09
                  },
                  {
                        "snippet_code": "'{}'.format(1)",
                        "snippet_name": "str.format()",
                        "runs": 18000000,
                        "mean": 1.652621666666668e-07,
                        "median": 1.649461000000003e-07,
                        "min": 1.6389370000000002e-07,
                        "max": 1.6862390000000005e-07,
                        "stddev": 1.424589255715445e-09
                  }
               ]
            }

.. option:: -q, --quiet

   If used, there will be no output printed.

   This is useful if you are running it from a script and don't want the output polluting your terminal

   .. TODO: Add an example

.. option:: -e, --only-export

   If used alongside --from-json, skips the benchmarking part and just exports the data.
   The json file needs to to contain the exported data or else this won't work.

.. option:: -w, --warmup <NUM>

   Perform NUM warmup runs before the actual benchmark. Perform this only for presistent improvements.
   Otherwise all performance gains are lost on each batch

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero "f'{1}'" "'{}'.format(1)" -n "f-string" -n "str.format()" --warmup 100_000

         Tip: The _ is used in replacement of a comma, you can omit it.

   This is due to how fastero benchmarking works. It relies on timeit and timeit doesn't have a warmup
   parameter, so I'm thinking about subclassing :py:class:`timeit.Timer` and implementing a warmup parameter myself.

.. option:: -c, --code-theme <THEME_NAME>

   Theme for code input and output, also applicable if “-” is used for any of the parameters,

   .. admonition:: **Default**
      :class: default

      The default theme is **one-dark**

   For a list of the themes see https://pygments.org/styles

   .. tip::

      .. details:: Best Themes

         These are the best themes: (in my opinion of course)

         .. raw:: html

            <div>
               <h4 id="one-dark">one-dark</h4>
               <div class="highlight" style="background: #282C34"><pre style="line-height: 125%;"><span></span><span style="color: #C678DD">from</span> <span style="color: #E06C75">typing</span> <span style="color: #C678DD">import</span> <span style="color: #E06C75">Iterator</span>

            <span style="color: #7F848E"># This is an example</span>
            <span style="color: #C678DD">class</span> <span style="color: #E5C07B">Math</span><span style="color: #ABB2BF">:</span>
               <span style="color: #61AFEF">@staticmethod</span>
               <span style="color: #C678DD">def</span> <span style="color: #61AFEF; font-weight: bold">fib</span><span style="color: #ABB2BF">(</span><span style="color: #E06C75">n</span><span style="color: #ABB2BF">:</span> <span style="color: #E5C07B">int</span><span style="color: #ABB2BF">)</span> <span style="color: #56B6C2">-&gt;</span> <span style="color: #E06C75">Iterator</span><span style="color: #ABB2BF">[</span><span style="color: #E5C07B">int</span><span style="color: #ABB2BF">]:</span>
                  <span style="color: #98C379">""" Fibonacci series up to n """</span>
                  <span style="color: #E06C75">a</span><span style="color: #ABB2BF">,</span> <span style="color: #E06C75">b</span> <span style="color: #56B6C2">=</span> <span style="color: #D19A66">0</span><span style="color: #ABB2BF">,</span> <span style="color: #D19A66">1</span>
                  <span style="color: #C678DD">while</span> <span style="color: #E06C75">a</span> <span style="color: #56B6C2">&lt;</span> <span style="color: #E06C75">n</span><span style="color: #ABB2BF">:</span>
                        <span style="color: #C678DD">yield</span> <span style="color: #E06C75">a</span>
                        <span style="color: #E06C75">a</span><span style="color: #ABB2BF">,</span> <span style="color: #E06C75">b</span> <span style="color: #56B6C2">=</span> <span style="color: #E06C75">b</span><span style="color: #ABB2BF">,</span> <span style="color: #E06C75">a</span> <span style="color: #56B6C2">+</span> <span style="color: #E06C75">b</span>

            <span style="color: #E06C75">result</span> <span style="color: #56B6C2">=</span> <span style="color: #E5C07B">sum</span><span style="color: #ABB2BF">(</span><span style="color: #E06C75">Math</span><span style="color: #56B6C2">.</span><span style="color: #E06C75">fib</span><span style="color: #ABB2BF">(</span><span style="color: #D19A66">42</span><span style="color: #ABB2BF">))</span>
            <span style="color: #E5C07B">print</span><span style="color: #ABB2BF">(</span><span style="color: #98C379">"The answer is {}"</span><span style="color: #56B6C2">.</span><span style="color: #E06C75">format</span><span style="color: #ABB2BF">(</span><span style="color: #E06C75">result</span><span style="color: #ABB2BF">))</span>
            </pre></div>

               </div>

         .. raw:: html

            <div>
               <h4 id="material">material</h4>
               <div class="highlight" style="background: #263238"><pre style="line-height: 125%;"><span></span><span style="color: #89DDFF; font-style: italic">from</span> <span style="color: #FFCB6B">typing</span> <span style="color: #89DDFF; font-style: italic">import</span> <span style="color: #EEFFFF">Iterator</span>

            <span style="color: #546E7A; font-style: italic"># This is an example</span>
            <span style="color: #BB80B3">class</span> <span style="color: #FFCB6B">Math</span><span style="color: #89DDFF">:</span>
               <span style="color: #82AAFF">@staticmethod</span>
               <span style="color: #BB80B3">def</span> <span style="color: #82AAFF">fib</span><span style="color: #89DDFF">(</span><span style="color: #EEFFFF">n</span><span style="color: #89DDFF">:</span> <span style="color: #82AAFF">int</span><span style="color: #89DDFF">)</span> <span style="color: #89DDFF">-&gt;</span> <span style="color: #EEFFFF">Iterator</span><span style="color: #89DDFF">[</span><span style="color: #82AAFF">int</span><span style="color: #89DDFF">]:</span>
                  <span style="color: #546E7A; font-style: italic">""" Fibonacci series up to n """</span>
                  <span style="color: #EEFFFF">a</span><span style="color: #89DDFF">,</span> <span style="color: #EEFFFF">b</span> <span style="color: #89DDFF">=</span> <span style="color: #F78C6C">0</span><span style="color: #89DDFF">,</span> <span style="color: #F78C6C">1</span>
                  <span style="color: #BB80B3">while</span> <span style="color: #EEFFFF">a</span> <span style="color: #89DDFF">&lt;</span> <span style="color: #EEFFFF">n</span><span style="color: #89DDFF">:</span>
                        <span style="color: #BB80B3">yield</span> <span style="color: #EEFFFF">a</span>
                        <span style="color: #EEFFFF">a</span><span style="color: #89DDFF">,</span> <span style="color: #EEFFFF">b</span> <span style="color: #89DDFF">=</span> <span style="color: #EEFFFF">b</span><span style="color: #89DDFF">,</span> <span style="color: #EEFFFF">a</span> <span style="color: #89DDFF">+</span> <span style="color: #EEFFFF">b</span>

            <span style="color: #EEFFFF">result</span> <span style="color: #89DDFF">=</span> <span style="color: #82AAFF">sum</span><span style="color: #89DDFF">(</span><span style="color: #EEFFFF">Math</span><span style="color: #89DDFF">.</span><span style="color: #EEFFFF">fib</span><span style="color: #89DDFF">(</span><span style="color: #F78C6C">42</span><span style="color: #89DDFF">))</span>
            <span style="color: #82AAFF">print</span><span style="color: #89DDFF">(</span><span style="color: #C3E88D">"The answer is </span><span style="color: #89DDFF">{}</span><span style="color: #C3E88D">"</span><span style="color: #89DDFF">.</span><span style="color: #EEFFFF">format</span><span style="color: #89DDFF">(</span><span style="color: #EEFFFF">result</span><span style="color: #89DDFF">))</span>
            </pre></div>

               </div>

         .. raw:: html

            <div>
               <h4 id="dracula">dracula</h4>
               <div class="highlight" style="background: #282a36"><pre style="line-height: 125%;"><span></span><span style="color: #ff79c6">from</span> <span style="color: #f8f8f2">typing</span> <span style="color: #ff79c6">import</span> <span style="color: #f8f8f2">Iterator</span>

            <span style="color: #6272a4"># This is an example</span>
            <span style="color: #ff79c6">class</span> <span style="color: #50fa7b">Math</span><span style="color: #f8f8f2">:</span>
               <span style="color: #f8f8f2">@staticmethod</span>
               <span style="color: #ff79c6">def</span> <span style="color: #50fa7b">fib</span><span style="color: #f8f8f2">(n:</span> <span style="color: #8be9fd; font-style: italic">int</span><span style="color: #f8f8f2">)</span> <span style="color: #ff79c6">-&gt;</span> <span style="color: #f8f8f2">Iterator[</span><span style="color: #8be9fd; font-style: italic">int</span><span style="color: #f8f8f2">]:</span>
                  <span style="color: #bd93f9">""" Fibonacci series up to n """</span>
                  <span style="color: #f8f8f2">a,</span> <span style="color: #f8f8f2">b</span> <span style="color: #ff79c6">=</span> <span style="color: #ffb86c">0</span><span style="color: #f8f8f2">,</span> <span style="color: #ffb86c">1</span>
                  <span style="color: #ff79c6">while</span> <span style="color: #f8f8f2">a</span> <span style="color: #ff79c6">&lt;</span> <span style="color: #f8f8f2">n:</span>
                        <span style="color: #ff79c6">yield</span> <span style="color: #f8f8f2">a</span>
                        <span style="color: #f8f8f2">a,</span> <span style="color: #f8f8f2">b</span> <span style="color: #ff79c6">=</span> <span style="color: #f8f8f2">b,</span> <span style="color: #f8f8f2">a</span> <span style="color: #ff79c6">+</span> <span style="color: #f8f8f2">b</span>

            <span style="color: #f8f8f2">result</span> <span style="color: #ff79c6">=</span> <span style="color: #8be9fd; font-style: italic">sum</span><span style="color: #f8f8f2">(Math</span><span style="color: #ff79c6">.</span><span style="color: #f8f8f2">fib(</span><span style="color: #ffb86c">42</span><span style="color: #f8f8f2">))</span>
            <span style="color: #8be9fd; font-style: italic">print</span><span style="color: #f8f8f2">(</span><span style="color: #bd93f9">"The answer is {}"</span><span style="color: #ff79c6">.</span><span style="color: #f8f8f2">format(result))</span>
            </pre></div>

               </div>

         .. raw::html

            <div>
               <h4 id="monokai">monokai</h4>
               <div class="highlight" style="background: #272822"><pre style="line-height: 125%;"><span></span><span style="color: #f92672">from</span> <span style="color: #f8f8f2">typing</span> <span style="color: #f92672">import</span> <span style="color: #f8f8f2">Iterator</span>

            <span style="color: #75715e"># This is an example</span>
            <span style="color: #66d9ef">class</span> <span style="color: #a6e22e">Math</span><span style="color: #f8f8f2">:</span>
               <span style="color: #a6e22e">@staticmethod</span>
               <span style="color: #66d9ef">def</span> <span style="color: #a6e22e">fib</span><span style="color: #f8f8f2">(n:</span> <span style="color: #f8f8f2">int)</span> <span style="color: #f92672">-&gt;</span> <span style="color: #f8f8f2">Iterator[int]:</span>
                  <span style="color: #e6db74">""" Fibonacci series up to n """</span>
                  <span style="color: #f8f8f2">a,</span> <span style="color: #f8f8f2">b</span> <span style="color: #f92672">=</span> <span style="color: #ae81ff">0</span><span style="color: #f8f8f2">,</span> <span style="color: #ae81ff">1</span>
                  <span style="color: #66d9ef">while</span> <span style="color: #f8f8f2">a</span> <span style="color: #f92672">&lt;</span> <span style="color: #f8f8f2">n:</span>
                        <span style="color: #66d9ef">yield</span> <span style="color: #f8f8f2">a</span>
                        <span style="color: #f8f8f2">a,</span> <span style="color: #f8f8f2">b</span> <span style="color: #f92672">=</span> <span style="color: #f8f8f2">b,</span> <span style="color: #f8f8f2">a</span> <span style="color: #f92672">+</span> <span style="color: #f8f8f2">b</span>

            <span style="color: #f8f8f2">result</span> <span style="color: #f92672">=</span> <span style="color: #f8f8f2">sum(Math</span><span style="color: #f92672">.</span><span style="color: #f8f8f2">fib(</span><span style="color: #ae81ff">42</span><span style="color: #f8f8f2">))</span>
            <span style="color: #f8f8f2">print(</span><span style="color: #e6db74">"The answer is {}"</span><span style="color: #f92672">.</span><span style="color: #f8f8f2">format(result))</span>
            </pre></div>

               </div>

         .. raw:: html

            <div>
               <h3 id="monokai">monokai</h3>
               <div class="highlight" style="background: #272822"><pre style="line-height: 125%;"><span></span><span style="color: #f92672">from</span> <span style="color: #f8f8f2">typing</span> <span style="color: #f92672">import</span> <span style="color: #f8f8f2">Iterator</span>

            <span style="color: #75715e"># This is an example</span>
            <span style="color: #66d9ef">class</span> <span style="color: #a6e22e">Math</span><span style="color: #f8f8f2">:</span>
               <span style="color: #a6e22e">@staticmethod</span>
               <span style="color: #66d9ef">def</span> <span style="color: #a6e22e">fib</span><span style="color: #f8f8f2">(n:</span> <span style="color: #f8f8f2">int)</span> <span style="color: #f92672">-&gt;</span> <span style="color: #f8f8f2">Iterator[int]:</span>
                  <span style="color: #e6db74">""" Fibonacci series up to n """</span>
                  <span style="color: #f8f8f2">a,</span> <span style="color: #f8f8f2">b</span> <span style="color: #f92672">=</span> <span style="color: #ae81ff">0</span><span style="color: #f8f8f2">,</span> <span style="color: #ae81ff">1</span>
                  <span style="color: #66d9ef">while</span> <span style="color: #f8f8f2">a</span> <span style="color: #f92672">&lt;</span> <span style="color: #f8f8f2">n:</span>
                        <span style="color: #66d9ef">yield</span> <span style="color: #f8f8f2">a</span>
                        <span style="color: #f8f8f2">a,</span> <span style="color: #f8f8f2">b</span> <span style="color: #f92672">=</span> <span style="color: #f8f8f2">b,</span> <span style="color: #f8f8f2">a</span> <span style="color: #f92672">+</span> <span style="color: #f8f8f2">b</span>

            <span style="color: #f8f8f2">result</span> <span style="color: #f92672">=</span> <span style="color: #f8f8f2">sum(Math</span><span style="color: #f92672">.</span><span style="color: #f8f8f2">fib(</span><span style="color: #ae81ff">42</span><span style="color: #f8f8f2">))</span>
            <span style="color: #f8f8f2">print(</span><span style="color: #e6db74">"The answer is {}"</span><span style="color: #f92672">.</span><span style="color: #f8f8f2">format(result))</span>
            </pre></div>

               </div>

         .. raw:: html

            <div>
               <h4 id="native">native</h4>
               <div class="highlight" style="background: #202020"><pre style="line-height: 125%;"><span></span><span style="color: #6ebf26; font-weight: bold">from</span> <span style="color: #71adff; text-decoration: underline">typing</span> <span style="color: #6ebf26; font-weight: bold">import</span> <span style="color: #d0d0d0">Iterator</span>

            <span style="color: #ababab; font-style: italic"># This is an example</span>
            <span style="color: #6ebf26; font-weight: bold">class</span> <span style="color: #71adff; text-decoration: underline">Math</span><span style="color: #d0d0d0">:</span>
               <span style="color: #ffa500">@staticmethod</span>
               <span style="color: #6ebf26; font-weight: bold">def</span> <span style="color: #71adff">fib</span><span style="color: #d0d0d0">(n:</span> <span style="color: #2fbccd">int</span><span style="color: #d0d0d0">)</span> <span style="color: #d0d0d0">-&gt;</span> <span style="color: #d0d0d0">Iterator[</span><span style="color: #2fbccd">int</span><span style="color: #d0d0d0">]:</span>
                  <span style="color: #ed9d13">""" Fibonacci series up to n """</span>
                  <span style="color: #d0d0d0">a,</span> <span style="color: #d0d0d0">b</span> <span style="color: #d0d0d0">=</span> <span style="color: #51b2fd">0</span><span style="color: #d0d0d0">,</span> <span style="color: #51b2fd">1</span>
                  <span style="color: #6ebf26; font-weight: bold">while</span> <span style="color: #d0d0d0">a</span> <span style="color: #d0d0d0">&lt;</span> <span style="color: #d0d0d0">n:</span>
                        <span style="color: #6ebf26; font-weight: bold">yield</span> <span style="color: #d0d0d0">a</span>
                        <span style="color: #d0d0d0">a,</span> <span style="color: #d0d0d0">b</span> <span style="color: #d0d0d0">=</span> <span style="color: #d0d0d0">b,</span> <span style="color: #d0d0d0">a</span> <span style="color: #d0d0d0">+</span> <span style="color: #d0d0d0">b</span>

            <span style="color: #d0d0d0">result</span> <span style="color: #d0d0d0">=</span> <span style="color: #2fbccd">sum</span><span style="color: #d0d0d0">(Math.fib(</span><span style="color: #51b2fd">42</span><span style="color: #d0d0d0">))</span>
            <span style="color: #2fbccd">print</span><span style="color: #d0d0d0">(</span><span style="color: #ed9d13">"The answer is {}"</span><span style="color: #d0d0d0">.format(result))</span>
            </pre></div>

               </div>

         .. raw:: html

            <div>
               <h4 id="fruity">fruity</h4>
               <div class="highlight" style="background: #111111"><pre style="line-height: 125%;"><span></span><span style="color: #fb660a; font-weight: bold">from</span> <span style="color: #ffffff">typing</span> <span style="color: #fb660a; font-weight: bold">import</span> <span style="color: #ffffff">Iterator</span>

            <span style="color: #008800; font-style: italic; background-color: #0f140f"># This is an example</span>
            <span style="color: #fb660a; font-weight: bold">class</span> <span style="color: #ffffff">Math:</span>
               <span style="color: #ffffff">@staticmethod</span>
               <span style="color: #fb660a; font-weight: bold">def</span> <span style="color: #ff0086; font-weight: bold">fib</span><span style="color: #ffffff">(n:</span> <span style="color: #ffffff">int)</span> <span style="color: #ffffff">-&gt;</span> <span style="color: #ffffff">Iterator[int]:</span>
                  <span style="color: #0086d2">""" Fibonacci series up to n """</span>
                  <span style="color: #ffffff">a,</span> <span style="color: #ffffff">b</span> <span style="color: #ffffff">=</span> <span style="color: #0086f7; font-weight: bold">0</span><span style="color: #ffffff">,</span> <span style="color: #0086f7; font-weight: bold">1</span>
                  <span style="color: #fb660a; font-weight: bold">while</span> <span style="color: #ffffff">a</span> <span style="color: #ffffff">&lt;</span> <span style="color: #ffffff">n:</span>
                        <span style="color: #fb660a; font-weight: bold">yield</span> <span style="color: #ffffff">a</span>
                        <span style="color: #ffffff">a,</span> <span style="color: #ffffff">b</span> <span style="color: #ffffff">=</span> <span style="color: #ffffff">b,</span> <span style="color: #ffffff">a</span> <span style="color: #ffffff">+</span> <span style="color: #ffffff">b</span>

            <span style="color: #ffffff">result</span> <span style="color: #ffffff">=</span> <span style="color: #ffffff">sum(Math.fib(</span><span style="color: #0086f7; font-weight: bold">42</span><span style="color: #ffffff">))</span>
            <span style="color: #ffffff">print(</span><span style="color: #0086d2">"The answer is {}"</span><span style="color: #ffffff">.format(result))</span>
            </pre></div>

               </div>

         There are others such as ``solarized-dark``, ``gruvbox-dark`` and many more!

   .. admonition:: Demonstation
      :class: important

      .. tab:: One Dark

         This image is basically the console output with this theme, generated by fastero itself

         .. image:: ../_static/images/one_dark_theme_demo.png

      .. tab:: Material

         This image is basically the console output with this theme, generated by fastero itself

         .. image:: ../_static/images/material_theme_demo.png

      .. tab:: Dracula

         This image is basically the console output with this theme, generated by fastero itself

         .. image:: ../_static/images/dracula_theme_demo.png

      .. tab:: Monokai

         This image is basically the console output with this theme, generated by fastero itself

         .. image:: ../_static/images/monokai_theme_demo.png

      .. tab:: Native

         This image is basically the console output with this theme, generated by fastero itself

         .. image:: ../_static/images/native_theme_demo.png

      .. tab:: Fruity

         This image is basically the console output with this theme, generated by fastero itself

         .. image:: ../_static/images/fruity_theme_demo.png

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero "f'{1}'" "'{}'.format(1)" -n "f-string" -n "str.format()" --code-theme monokai

.. option:: -t, --total-time <TIME>

   How long to test each snippet for. Format: 500ms, 10s, 1m5s, 1.5m, 1h40m15s, etc.

   .. admonition:: **Default**
      :class: default

      The default duration for benchmarking each code snippet is **3 seconds**

   The algorithm is simple, it gets the ``--time-per-batch`` parameter (by default 200ms), figures out how
   many runs will be done within that time. Then calculates how many batches will be possible within this ``<TIME>``,
   and that's your run count, manually specifying \--runs overrides this. To control the maximum and minimum you can use
   `\--max-runs <#cmdoption-M>`_ and `\--min-runs <#cmdoption-m>`_ respectively.

   .. seealso::

      `\--time-per-batch <#cmdoption-b>`_

.. option:: -b, --time-per-batch <TIME>

   How long each test batch will last for, increase this to make the tests more accurate at the cost of
   making progress bar less smooth.

   .. admonition:: **Default**
      :class: default

      The default duration for each batch is **200 milliseconds**

   Also change ``--total-time`` accordingly or else statistics won’t work when it can only do a single batch,
   therefore it can't determine the mean, median, standard deviation etc.

   .. seealso::

      `\--total-time <#cmdoption-t>`_

.. option:: -u, --time-unit <UNIT>

   Set the time unit to be used. Possible values: ns, us, ms, s, dynamic

   .. admonition:: **Default**
      :class: default

      The default the time unit is **dynamic** meaning it depends on the time itself,
      it is generally the best possible unit for the time.

   .. admonition:: Applications
      :class: caution

      This applies to the the console output and the
      ``asciidoc``, ``markdown``, ``html``, ``svg``, ``png``, and ``plot`` export options

   .. admonition:: Example
      :class: hint

      .. code-block:: shell

         fastero "f'{1}'" "'{}'.format(1)" -n "f-string" -n "str.format()" --time-unit ms

      .. details:: Output

         If the image below looks blurry then click it to open it in fullscreen

         .. image:: ../_static/images/time_unit_demo.png
            :width: 1292
            :alt: Output image

   .. admonition:: Available Values

      * **ns** (nanoseconds)
      * **us** (microseconds)
      * **ms** (milliseconds)
      * **s** (seconds)
      * **dynamic** (dynamic value)

.. option:: -r, --runs <NUM>

   Perform exactly NUM runs for each snippet. By default, the number of runs is automatically determined

   This is not guaranteed and there may be a maximum of 2 more runs if NUM isn't divisible by 3

.. option:: -m, --min-runs <NUM>

   Perform at least NUM runs for each snippet

   This exists to aid in controlling the algorithm mentioned in `\--total-time <#cmdoption-t>`_

.. option:: -m, --min-runs <NUM>

   Perform at most NUM runs for each snippet

   This exists to aid in controlling the algorithm mentioned in `\--total-time <#cmdoption-t>`_

For information about the exporting options, see :ref:`Exporting <exporting-reference>` or
if you only want to see the parameters see :ref:`CLI Reference (Automated) <cli-reference-automated>`

.. _Command Line Interface Guidelines: https://clig.dev/#:~:text=Display%20output%20as%20formatted%20JSON%20if%20%2D%2Djson%20is%20passed.