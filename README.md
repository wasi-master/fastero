<div align="center">

<img src="https://github.com/wasi-master/fastero/raw/main/logo.png" width=200>

# fastero
 Python timeit CLI for the 21st century

[**Read the Documentation**](https://fastero.readthedocs.io)

</div>

## Installation

Install either with pipx or pip. Both work, use what you want. Or optionally you can install from github using `pip install git+https://github.com/wasi-master/fastero`

## Features

For more info on all of these features, please the [documentation]((https://fastero.readthedocs.io))

- 🌟 *Beautiful* formatted, and colored output. Output is reminiscent of [hyperfine](https://github.com/sharkdp/hyperfine)
- 🤯 *Amazing* exporting options
  - 📊 Export as a bar plot with matplotlib
  - 🌃 Export as a *beautiful* image with the console output
  - ℹ️ Export as Markdown, HTML, CSV, AsciiDoc tables
  - 💾 Export as JSON and YAML data to use them elsewhere
    - 🔁 You can also import the JSON data later within
      fastero to re-run the benchmark with the same parameters
      or to export the data again with different parameters.
- 🚀 Extremely intuitive and easy to use.
- 🔢 Benchmark multiple snippets
  - 🔤 Assign a name to each snippet to make it easier to distinguish
  - 📈 Get nice statistics about the each of the snippet and
    a summary on how fast each of them are compared to each other
- ↩ Enter multiline code in an input with syntax highlighting
- ⏰ Excellent time parsing. Inputs like `500ms`, `10s`, `1m5s`, `1.5m`, `1h30m15s`, etc. work flawlessly
- 🔥 Run a few times without timing with the warmup parameter to fill
  caches and things like that.
- 👨 Customize it to your liking.
  - 🔣 Custom time formats e.g. nanoseconds, microseconds, milliseconds, seconds etc.
  - 🎨 Custom theme for code input and/or output.
- 🎛️ Control how long each snippet is benchmarked for
  - 🔢 Specify a minimum and a maximum amount of runs to calculate
    the number of runs automatically based on run duration
  - 🔟 Or specify a definite number of runs for manual override
- 💻 Cross-platform.
- 🤯 Open source.
- 📚 Extensive documentation.

### Acknowledgements

- [hyperfine](https://github.com/sharkdp/hyperfine) - Inspiration for creating this library and the UI.
- [snappify.io](https://snappify.io) - Inspiration for the Image export.
- [rich](https://github.com/Textualize/rich) - Used for *beautiful* output