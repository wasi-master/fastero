.. _exporting-reference:
###################
Exporting Reference
###################

.. meta::
    :description: Python timeit CLI for the 21st century.
    :author: Arian Mollik Wasi
    :copyright: Arian Mollik Wasi
    :keywords: Python, Timeit, Fastero, Wasi Master, Arian Mollik Wasi
    :language: English
    :og:title: Fastero Documentation - Exporting Reference
    :og:site_name: Fastero
    :og:type: website
    :og:url: https://fastero.readthedocs.io
    :og:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
    :og:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
    :twitter:card: summary_large_image
    :twitter:title: Fastero Documentation - Exporting Reference
    :twitter:image: https://i.ibb.co/ysbFf3b/python-http-library-benchmark.png
    :twitter:description: Python timeit CLI for the 21st century. Fastero is a beautiful and flexible timeit (cli) alternative that you have to check out
    :google-site-verification: upUCfyFeU0JcauOrq_fs4NssKvSo3FzLEnJBTWDBiHY

.. role:: raw-html(raw)
   :format: html

Exporting JSON
--------------

To export :term:`JSON` to a file you would use
the ``--export-json`` flag

.. admonition:: Example
    :class: hint

    .. code-block:: shell

        fastero "str(1)" "f'{1}'" --export-json foo.json

    This will save a ``foo.json`` file with the following contents:

    .. code-block:: json
        :caption: foo.json

        {
            "$schema": "https://raw.githubusercontent.com/wasi-master/fastero/main/schema.json",
            "setup": "pass",
            "results": [
                {
                    "snippet_code": "str(1)",
                    "snippet_name": "Benchmark 1",
                    "runs": 20000000,
                    "mean": 1.3559740499999998e-07,
                    "median": 1.3493814999999998e-07,
                    "min": 1.3349034999999999e-07,
                    "max": 1.400591e-07,
                    "stddev": 2.0184569021422298e-09
                },
                {
                    "snippet_code": "f'{1}'",
                    "snippet_name": "Benchmark 2",
                    "runs": 55000000,
                    "mean": 5.494544181818183e-08,
                    "median": 5.508430000000004e-08,
                    "min": 5.336672e-08,
                    "max": 5.630708000000002e-08,
                    "stddev": 1.0314662950365168e-09
                }
            ]
        }

This JSON output can then be used to re-run the results using the following command:

.. code-block:: shell

    fastero --from-json foo.json

If you wish to not re-run the results but just get the output that was shown previously, run the following command:

.. code-block:: shell

    fastero --from-json foo.json --only-export

You can also use other arguments with this!

Exporting CSV
-------------

To export a :term:`CSV` file, use the following command:

.. admonition:: Example
    :class: hint

    .. code-block:: shell

        fastero "str(1)" "f'{1}'" --export-csv foo.csv

    This will save a ``foo.csv`` file with the following contents:

    .. code-block:: csv
        :caption: foo.csv

        Snippet Code,Snippet Name,Runs,Mean,Median,Min,Max,Standard Deviation
        str(1),Benchmark 1,22000000,1.3751392272727268e-07,1.370651999999999e-07,1.3411479999999997e-07,1.464300999999999e-07,3.5374505786910588e-09
        f'{1}',Benchmark 2,55000000,5.954033636363639e-08,5.472532000000001e-08,5.307487999999996e-08,8.249068000000008e-08,1.1289950152743191e-08

    .. csv-table:: CSV Preview
        :header: Snippet Code,Snippet Name,Runs,Mean,Median,Min,Max,Standard Deviation

        str(1),Benchmark 1,22000000,1.3751392272727268e-07,1.370651999999999e-07,1.3411479999999997e-07,1.464300999999999e-07,3.5374505786910588e-09
        f'{1}',Benchmark 2,55000000,5.954033636363639e-08,5.472532000000001e-08,5.307487999999996e-08,8.249068000000008e-08,1.1289950152743191e-08



Exporting YAML
--------------

To export :term:`YAML` to a file you would use
the ``--export-yaml`` flag

.. admonition:: Example
    :class: hint

    .. code-block:: shell

        fastero "str(1)" "f'{1}'" --export-yaml foo.yaml

    This will save a ``foo.yaml`` file with the following contents:

    .. code-block:: yaml
        :caption: foo.yaml

        results:
        - max: 1.4413549999999997e-07
          mean: 1.4256015499999995e-07
          median: 1.4241862500000002e-07
          min: 1.411376499999999e-07
          runs: 20000000
          snippet_code: str(1)
          snippet_name: Benchmark 1
          stddev: 1.0738769558758217e-09
        - max: 8.052079999999985e-08
          mean: 6.093868545454547e-08
          median: 5.8050159999999985e-08
          min: 5.255628000000012e-08
          runs: 55000000
          snippet_code: f'{1}'
          snippet_name: Benchmark 2
          stddev: 9.646527607752279e-09

Exporting Markdown
------------------

To export your results as a :term:`Markdown` table, use the ``--export-markdown`` option

.. admonition:: Example
    :class: hint

    .. code-block:: shell

        fastero 'str(1)' --export-markdown foo.md

    This will save a ``foo.md`` file with the following contents:

    .. code-block:: markdown
        :caption: foo.md

        |Snippet Code|Snippet Name|Runs|Mean|Median|Min|Max|Standard Deviation|
        |---|---|---|---|---|---|---|---|
        |str(1)|Benchmark 1|22000000|136.8 ns|135.6 ns|133.7 ns|142.1 ns|2.9 ns|

    +---------+--------------+----------+----------+----------+----------+----------+-----------+
    | Snippet | Snippet Name | Runs     | Mean     | Median   | Min      | Max      | Standard  |
    | Code    |              |          |          |          |          |          | Deviation |
    +=========+==============+==========+==========+==========+==========+==========+===========+
    | str(1)  | Benchmark 1  | 22000000 | 136.8 ns | 135.6 ns | 133.7 ns | 142.1 ns | 2.9 ns    |
    |         |              |          |          |          |          |          |           |
    |         |              |          |          |          |          |          |           |
    +---------+--------------+----------+----------+----------+----------+----------+-----------+

Exporting AsciiDoc
------------------

To export your results as a :term:`AsciiDoc` table, use the ``--export-asciidoc`` option

.. admonition:: Example
    :class: hint

    .. code-block:: shell

        fastero "str(1)" --export-asciidoc foo.adoc

    This will save a ``foo.adoc`` file with the following contents:

    .. code-block:: asciidoc
        :caption: foo.adoc

        [cols=",,,,,,," options="header"]
        |===
        |Snippet Code|Snippet Name|Runs|Mean|Median|Min|Max|Standard Deviation
        |str(1)|Benchmark 1|20000000|136.5 ns|134.7 ns|134.1 ns|147.7 ns|4.2 ns
        |===


    +---------+--------------+----------+----------+----------+----------+----------+-----------+
    | Snippet | Snippet Name | Runs     | Mean     | Median   | Min      | Max      | Standard  |
    | Code    |              |          |          |          |          |          | Deviation |
    +=========+==============+==========+==========+==========+==========+==========+===========+
    | str(1)  | Benchmark 1  | 20000000 | 136.5 ns | 134.7 ns | 134.1 ns | 147.7 ns | 4.3 ns    |
    |         |              |          |          |          |          |          |           |
    |         |              |          |          |          |          |          |           |
    +---------+--------------+----------+----------+----------+----------+----------+-----------+


Exporting SVG
-------------

To export your console output as a :term:`SVG` file, use the ``--export-svg`` option

.. admonition:: Example
    :class: hint

    .. code-block:: shell

        fastero "str(1)" "f'{1}'" --export-svg foo.svg

    .. details:: This will save a ``foo.svg`` file with the following contents

        .. code-block:: html
            :caption: foo.svg

            <svg width="2050.3999999999996" height="670" viewBox="0 0 2050.3999999999996 670"
                xmlns="http://www.w3.org/2000/svg">
                <style>
                    @font-face {
                        font-family: "Fira Code";
                        src: local("FiraCode-Regular"),
                            url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),
                            url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");
                        font-style: normal;
                        font-weight: 400;
                    }
                    @font-face {
                        font-family: "Fira Code";
                        src: local("FiraCode-Bold"),
                            url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),
                            url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");
                        font-style: bold;
                        font-weight: 700;
                    }
                    span {
                        display: inline-block;
                        white-space: pre;
                        vertical-align: top;
                        font-size: 18px;
                        font-family:'Fira Code','Cascadia Code',Monaco,Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace;
                    }
                    a {
                        text-decoration: none;
                        color: inherit;
                    }
                    .blink {
                    animation: blinker 1s infinite;
                    }
                    @keyframes blinker {
                        from { opacity: 1.0; }
                        50% { opacity: 0.3; }
                        to { opacity: 1.0; }
                    }
                    #wrapper {
                        padding: 140px;
                        padding-top: 100px;
                    }
                    #terminal {
                        position: relative;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        background-color: #0c0c0c;
                        border-radius: 14px;
                        outline: 1px solid #484848;
                    }
                    #terminal:after {
                        position: absolute;
                        width: 100%;
                        height: 100%;
                        content: '';
                        border-radius: 14px;
                        background: rgb(71,77,102);
                        background: linear-gradient(90deg, #804D69 0%, #4E4B89 100%);
                        transform: rotate(-4.5deg);
                        z-index: -1;
                    }
                    #terminal-header {
                        position: relative;
                        width: 100%;
                        background-color: #2e2e2e;
                        margin-bottom: 12px;
                        font-weight: bold;
                        border-radius: 14px 14px 0 0;
                        color: #f2f2f2;
                        font-size: 18px;
                        box-shadow: inset 0px -1px 0px 0px #4e4e4e,
                                    inset 0px -4px 8px 0px #1a1a1a;
                    }
                    #terminal-title-tab {
                        display: inline-block;
                        margin-top: 14px;
                        margin-left: 124px;
                        font-family: sans-serif;
                        padding: 14px 28px;
                        border-radius: 6px 6px 0 0;
                        background-color: #0c0c0c;
                        box-shadow: inset 0px 1px 0px 0px #4e4e4e,
                                    0px -4px 4px 0px #1e1e1e,
                                    inset 1px 0px 0px 0px #4e4e4e,
                                    inset -1px 0px 0px 0px #4e4e4e;
                    }
                    #terminal-traffic-lights {
                        position: absolute;
                        top: 24px;
                        left: 20px;
                    }
                    #terminal-body {
                        line-height: 22px;
                        padding: 14px;
                    }
                    .r1 {color: #f2f2f2; text-decoration-color: #f2f2f2;background-color: #0c0c0c;}
            .r2 {font-weight: bold;color: #f2f2f2; text-decoration-color: #f2f2f2;;background-color: #0c0c0c;}
            .r3 {color: #e5c07b; text-decoration-color: #e5c07b; background-color: #282c34}
            .r4 {color: #abb2bf; text-decoration-color: #abb2bf; background-color: #282c34}
            .r5 {color: #d19a66; text-decoration-color: #d19a66; background-color: #282c34}
            .r6 {color: #0dbc79; text-decoration-color: #0dbc79; font-weight: bold;background-color: #0c0c0c;}
            .r7 {color: #0dbc79; text-decoration-color: #0dbc79;background-color: #0c0c0c;}
            .r8 {color: #11a8cd; text-decoration-color: #11a8cd; font-weight: bold;background-color: #0c0c0c;}
            .r9 {color: #bc3fbc; text-decoration-color: #bc3fbc;background-color: #0c0c0c;}
            .r10 {color: #666666; text-decoration-color: #666666;background-color: #0c0c0c;}
            .r11 {color: #98c379; text-decoration-color: #98c379; background-color: #282c34}
            .r12 {color: #7f7f7f; text-decoration-color: #7f7f7f;color: #f2f2f2; text-decoration-color: #f2f2f2;;background-color: #0c0c0c;}
            .r13 {color: #11a8cd; text-decoration-color: #11a8cd; background-color: #0c0c0c}
            .r14 {color: #cd3131; text-decoration-color: #cd3131;background-color: #0c0c0c;}
            .r15 {color: #11a8cd; text-decoration-color: #11a8cd;background-color: #0c0c0c;}
                </style>
                <foreignObject x="0" y="0" width="100%" height="100%">
                    <body xmlns="http://www.w3.org/1999/xhtml">
                        <div id="wrapper">
                            <div id="terminal">
                                <div id='terminal-header'>
                                    <svg id="terminal-traffic-lights" width="90" height="21" viewBox="0 0 90 21" xmlns="http://www.w3.org/2000/svg">
                                        <circle cx="14" cy="8" r="8" fill="#ff6159"/>
                                        <circle cx="38" cy="8" r="8" fill="#ffbd2e"/>
                                        <circle cx="62" cy="8" r="8" fill="#28c941"/>
                                    </svg>
                                    <div id="terminal-title-tab">Python Benchmark Output</div>
                                </div>
                                <div id='terminal-body'>
                                    <div><span class="r2">Benchmark 1</span><span class="r1">: </span><span class="r3">str</span><span class="r4">(</span><span class="r5">1</span><span class="r4">)</span><span class="r1">                                                                                                                                 </span></div>
            <div><span class="r1">  Time  (</span><span class="r6">mean</span><span class="r1"> ± </span><span class="r7">σ</span><span class="r1">):       </span><span class="r6">138.2 ns</span><span class="r1"> ± </span><span class="r7">  2.2 ns</span><span class="r1">                                                                                                       </span></div>
            <div><span class="r1">  Range (</span><span class="r8">min</span><span class="r1">  … </span><span class="r9">max</span><span class="r1">):     </span><span class="r8">135.6 ns</span><span class="r1"> … </span><span class="r9">141.6 ns</span><span class="r1">    </span><span class="r10">[runs: 20,000,000]</span><span class="r1">                                                                                 </span></div>
            <div><span class="r2">Benchmark 2</span><span class="r1">: </span><span class="r11">f&#x27;{</span><span class="r5">1</span><span class="r11">}&#x27;</span><span class="r1">                                                                                                                                 </span></div>
            <div><span class="r1">  Time  (</span><span class="r6">mean</span><span class="r1"> ± </span><span class="r7">σ</span><span class="r1">):       </span><span class="r6">54.6 ns</span><span class="r1"> ± </span><span class="r7"> 0.8 ns</span><span class="r1">                                                                                                         </span></div>
            <div><span class="r1">  Range (</span><span class="r8">min</span><span class="r1">  … </span><span class="r9">max</span><span class="r1">):     </span><span class="r8">53.9 ns</span><span class="r1"> … </span><span class="r9">55.9 ns</span><span class="r1">    </span><span class="r10">[runs: 50,000,000]</span><span class="r1">                                                                                   </span></div>
            <div><span class="r1"></span><span class="r1">                                                                                                                                                    </span></div>
            <div><span class="r2">Summary</span><span class="r1">:</span><span class="r1">                                                                                                                                            </span></div>
            <div><span class="r12">┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Bar Chart ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓</span><span class="r1">                                                                           </span></div>
            <div><span class="r12">┃</span><span class="r1"> </span><span class="r3">str</span><span class="r4">(</span><span class="r5">1</span><span class="r4">)</span><span class="r1"> </span><span class="r13">[135.6 ns]:</span><span class="r1"> </span><span class="r14">▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆</span><span class="r1"> </span><span class="r12">┃</span><span class="r1">                                                                           </span></div>
            <div><span class="r12">┃</span><span class="r1"> </span><span class="r11">f&#x27;{</span><span class="r5">1</span><span class="r11">}&#x27;</span><span class="r1"> </span><span class="r13">[53.9 ns]: </span><span class="r1"> </span><span class="r7">▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆                              </span><span class="r1"> </span><span class="r12">┃</span><span class="r1">                                                                           </span></div>
            <div><span class="r12">┗━━━━━━━━━━━━━━━━━━━━━━━━━━ (lower is better) ━━━━━━━━━━━━━━━━━━━━━━━━━━┛</span><span class="r1">                                                                           </span></div>
            <div><span class="r1">  </span><span class="r11">f&#x27;{</span><span class="r5">1</span><span class="r11">}&#x27;</span><span class="r1"> is the fastest.</span><span class="r1">                                                                                                                            </span></div>
            <div><span class="r1">    </span><span class="r6">2.53</span><span class="r1"> (</span><span class="r15">2.51</span><span class="r1"> … </span><span class="r9">2.53</span><span class="r1">) times faster than </span><span class="r3">str</span><span class="r4">(</span><span class="r5">1</span><span class="r4">)</span><span class="r1">                                                                                                     </span></div>
            <div><span class="r1"></span><span class="r1">                                                                                                                                                    </span></div>
                                </div>
                            </div>
                        </div>
                    </body>
                </foreignObject>
            </svg>

    SVG File Preview:

    .. image:: ../_static/images/svg_output_demo.svg

Exporting a Bar Chart
---------------------

You can generate a :term:`Bar Chart` using the ``--export-plot`` command

.. admonition:: Example
    :class: hint

    .. code-block:: shell

        fastero "str(1)" "f'{1}'" "'{}'.format(1)" "'%d' % 1" --export-plot foo.png

    This will save a ``foo.png`` file like of the following:

    .. image:: ../_static/images/plot_output_demo.png

You can (and you should!) add names to your snippets for easier understanding

.. admonition:: Example
    :class: hint

    .. code-block:: bash

        fastero "str(1)" "f'{1}'" "'{}'.format(1)" "'%d' % 1" \
            -n "str()" -n "f-string" -n "str.format()" -n "prinf style" \
            --export-plot foo.png

    This will save a ``foo.png`` file like of the following:

    .. image:: ../_static/images/named_plot_output_demo.png

You can also provide a custom label format to use. The default is ``{snippet_name}\n{snippet_code}``

.. admonition:: Example
    :class: hint

    .. code-block:: bash

        fastero "str(1)" "f'{1}'" "'{}'.format(1)" "'%d' % 1" \
            -n "str()" -n "f-string" -n "str.format()" -n "prinf style" \
            --export-plot foo.png --label-format "{snippet_name}"

    This will save a ``foo.png`` file like of the following:

    .. image:: ../_static/images/custom_labeled_named_plot_output_demo.png

You can modify the bar color too!

The default color is :raw-html:`<span style="color: #99bc5a">#99bc5a</span>`

For a list of possible color formats and values see `matplotlib docs - specifying colors`_

.. admonition:: Example
    :class: hint

    .. code-block:: bash

        fastero "str(1)" "f'{1}'" "'{}'.format(1)" "'%d' % 1" \
            -n "str()" -n "f-string" -n "str.format()" -n "prinf style" \
            --export-plot foo.png --label-format "{snippet_name}" \
            --bar-color plum

    This will save a ``foo.png`` file like of the following:

    .. image:: ../_static/images/plot_output_custom_bar_color.png

You can change the background color to black using the ``dark-background`` flag

.. admonition:: Example
    :class: hint

    .. code-block:: bash

        fastero "str(1)" "f'{1}'" "'{}'.format(1)" "'%d' % 1" \
            -n "str()" -n "f-string" -n "str.format()" -n "prinf style" \
            --export-plot foo.png --label-format "{snippet_name}" \
            --dark-background

    This will save a ``foo.png`` file like of the following:

    .. image:: ../_static/images/plot_output_demo_dark_background.png

Exporting an Image
------------------

This is in my opinion, the best exporting method! to export an image you should
use the ``--export-image`` flag.

.. admonition:: Example
    :class: hint

    .. code-block:: bash

        fastero "str(1)" "f'{1}'" "'{}'.format(1)" "'%d' % 1" \
            -n "str()" -n "f-string" -n "str.format()" -n "prinf style" \
            --export-image foo.png

    This will save a ``foo.png`` file like of the following:

    .. image:: ../_static/images/image_exporting_demo.png

    (Open the image in a new tab if it looks blurry)

As you can see there is a watermark for Fastero at the bottom left corner,
this can be disabled by using the ``--no-watermark`` flag.

The way this exporting image works is that it first generates a SVG file
using rich, then it opens the SVG in a browser (headless) and takes a screenshot
of that browser page. Then it uses PIL to crop out extraneous white borders that the
screenshot may have, and then you get the image

.. tip::

    You can resize your terminal window to change the size of the terminal in the image.

You can change which browser it uses using the ``--selenium-browser`` flag.

Since this uses PIL, the output formats can be anything PIL supports. For
a list see `Pillow supported formats`_

You can also specify a custom background using the ``--background`` flag. This

.. admonition:: Example
    :class: hint

    .. code-block:: bash

        fastero "str(1)" "f'{1}'" "'{}'.format(1)" "'%d' % 1" \
            -n "str()" -n "f-string" -n "str.format()" -n "prinf style" \
            --export-image foo.png --background 'url("https://images.unsplash.com/photo-1649771763042-453b69911ea0")'

    This will save a ``foo.png`` file like of the following:

    (Open the image in a new tab if it looks blurry)

    .. image:: ../_static/images/image_exporting_with_custom_background.jpg

    Photo by `Eugene Golovesov <https://unsplash.com/photos/2ftpuCgSZA0>`_ on `Unsplash <https://unsplash.com/>`_


.. _matplotlib docs - specifying colors: https://matplotlib.org/stable/tutorials/colors/colors.html
.. _Pillow supported formats: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#fully-supported-formats