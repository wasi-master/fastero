<div align="center">

<img src="https://github.com/wasi-master/fastero/raw/main/logo.png" width=200>

# fastero
 Python timeit CLI for the 21st century

[**Read the Documentation**](https://fastero.readthedocs.io)

</div>

## Installation & Usage

Install either with pipx or pip. Both work, use what you want. Or optionally you can install from github using `pip install git+https://github.com/wasi-master/fastero`

For usage please check out [the documentation](https://fastero.readthedocs.io)

## Features

For more info on all of these features, please the [documentation]((https://fastero.readthedocs.io))

- đ *Beautiful* formatted, and colored output. Output is reminiscent of [hyperfine](https://github.com/sharkdp/hyperfine)
- đ¤¯ *Amazing* exporting options
  - đ Export as a bar plot with matplotlib
  - đ Export as a *beautiful* image with the console output
  - âšī¸ Export as Markdown, HTML, CSV, AsciiDoc tables
  - đž Export as JSON and YAML data to use them elsewhere
    - đ You can also import the JSON data later within
      fastero to re-run the benchmark with the same parameters
      or to export the data again with different parameters.
- đ Extremely intuitive and easy to use.
- đĸ Benchmark multiple snippets
  - đ¤ Assign a name to each snippet to make it easier to distinguish
  - đ Get nice statistics about the each of the snippet and
    a summary on how fast each of them are compared to each other
- âŠ Enter *multiline* code in an input with **syntax highlighting** and ***amazing* autocomplete**
- â° Excellent time parsing. Inputs like `500ms`, `10s`, `1m5s`, `1.5m`, `1h30m15s`, etc. work flawlessly
- đĨ Run a few times without timing with the warmup parameter to fill
  caches and things like that.
- đ¨ Customize it to your liking.
  - đŖ Custom time formats e.g. nanoseconds, microseconds, milliseconds, seconds etc.
  - đ¨ Custom theme for code input and/or output.
- đī¸ Control how long each snippet is benchmarked for
  - đĸ Specify a minimum and a maximum amount of runs to calculate
    the number of runs automatically based on run duration
  - đ Or specify a definite number of runs for manual override
- đģ Cross-platform.
- đ¤¯ Open source.
- đ Extensive documentation.

### Acknowledgements

- [hyperfine](https://github.com/sharkdp/hyperfine) - Inspiration for creating this library and the UI.
- [snappify.io](https://snappify.io) - Inspiration for the Image export.
- [rich](https://github.com/Textualize/rich) - Used for *beautiful* output