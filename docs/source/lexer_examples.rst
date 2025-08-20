##################
Lexer Examples
##################

.. meta::
   :description: Examples showing the enhanced syntax highlighting for shell and AsciiDoc content
   :author: Arian Mollik Wasi
   :copyright: Arian Mollik Wasi

This page demonstrates the enhanced syntax highlighting provided by the custom lexers for shell commands and AsciiDoc content in fastero documentation.

Enhanced Shell Highlighting
---------------------------

The improved shell lexer provides better syntax highlighting for fastero commands:

.. code-block:: shell

    # Install fastero with dependencies
    pip install "fastero[export]"
    
    # Run a simple benchmark
    fastero "sum([1,2,3])" "sum((1,2,3))" --runs 10 --export-json results.json
    
    # Use python module syntax
    python -m fastero "len('hello')" --plain --warmup 5

.. code-block:: bash

    # More complex example with multiple options
    fastero \
        "list(range(100))" \
        "tuple(range(100))" \
        --runs 25 \
        --export-plot chart.png \
        --chart-title "List vs Tuple Performance" \
        --export-csv results.csv \
        --export-asciidoc results.adoc

AsciiDoc Syntax Highlighting
----------------------------

The AsciiDoc lexer provides proper highlighting for AsciiDoc content:

.. code-block:: asciidoc

    = Fastero Benchmark Results
    :author: Benchmark Runner
    :email: runner@example.com
    
    == Performance Comparison
    
    This document contains *performance* results from _fastero_ benchmarks.
    
    === Results Table
    
    [cols=",,,,,,," options="header"]
    |===
    |Snippet Code|Snippet Name|Runs|Mean|Median|Min|Max|Standard Deviation
    |str(1)|Benchmark 1|20000000|136.5 ns|134.7 ns|134.1 ns|147.7 ns|4.2 ns
    |f'{1}'|Benchmark 2|55000000|54.9 ns|55.1 ns|53.4 ns|56.3 ns|1.0 ns
    |===
    
    === Key Findings
    
    * `f-strings` are significantly faster than `str()` conversion
    * The performance difference is ~2.5x in this test
    * Both approaches have very low standard deviation
    
    === Links and References
    
    See the https://fastero.readthedocs.io[fastero documentation] for more details.
    
    image:chart.png[Performance Chart]

Features Demonstrated
---------------------

**Shell Lexer Features:**

* **Command highlighting**: Commands like `fastero`, `python`, `pip` are highlighted
* **Dimmed options**: CLI flags like `--runs`, `--export-json`, `-m` are dimmed for better visual hierarchy
* **String highlighting**: Quoted arguments are properly colored
* **File path recognition**: File extensions and paths are highlighted
* **Line continuation**: Backslash continuations are handled correctly

**AsciiDoc Lexer Features:**

* **Document structure**: Headers with `=` are properly highlighted
* **Attributes**: Document attributes like `:author:` are highlighted
* **Inline formatting**: *bold*, _italic_, and `monospace` text
* **Tables**: Table syntax including headers and separators
* **Lists**: Both bullet and numbered lists
* **Links**: URL and cross-reference linking
* **Images**: Image inclusion syntax
* **Code blocks**: Inline code with backticks

Both lexers integrate seamlessly with Sphinx's documentation generation system and provide enhanced readability for fastero's documentation.