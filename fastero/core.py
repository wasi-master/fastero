"""Core file for fastero."""
import os
import statistics

from pathlib import Path
from math import floor, ceil
from typing import List, Optional, Union

import rich
import rich_click as click
from rich.console import Console, ConsoleOptions
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax

from .__init__ import __version__ as VERSION
from .utils import (MofNCompleteColumn, StatefulColumn, Time, TIME_FORMAT_UNITS,
                    get_code_input, choose_unit, format_snippet, make_bar_plot,
                    _Timer as Timer
                    )
from .exporter import Exporter


# Help command formatting configuration
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.ERRORS_EPILOGUE = "For issues, visit https://github.com/wasi-master/fastero"
click.rich_click.STYLE_HELPTEXT = "none"
click.rich_click.OPTION_GROUPS = dict.fromkeys(
    ("python -m fastero", "fastero", "pipx run fastero"),
    [
        {
            "name": "Arguments",
            "options": ['CODE_SNIPPETS']
        },
        {
            "name": "General",
            "options": ["--warmup", "--time-unit", "--snippet-name", "--code-theme", "--from-json",
                        "--quiet", "--json", "--version", "--help"],
        },
        {
            "name": "Runs",
            "options": ["--runs", "--min-runs", "--max-runs"],
        },
        {
            "name": "Execution",
            "options": ["--setup", "--total-time", "--time-per-batch"],
        },
        {
            "name": "Exporting",
            "options": ["--export-json", "--export-csv", "--export-yaml", "--export-markdown", "--export-svg",
                        "--export-asciidoc", "--export-plot", "--label-format", "--dark-background", "--bar-color",
                        "--export-html", "--export-image", "--background", "--selenium-browser", "--watermark",
                        "--only-export"]
        }
    ]
)


def autorange_callback(n, t):
    """Show the number currently being tried by autorange in the autorange progress bar."""
    console.stateful_data[0] = f"(trying [magenta]{n}[/])"


def set_prompt_toolkit_color():
    """Rich has excellent color system detection, use that for prompt_tooklit too."""
    color_system = console.color_system
    if color_system == "standard":
        os.environ["PROMPT_TOOLKIT_COLOR_DEPTH"] = "DEPTH_1_BIT"
    elif color_system == "windows":
        os.environ["PROMPT_TOOLKIT_COLOR_DEPTH"] = "DEPTH_4_BIT"
    elif color_system == "256":
        os.environ["PROMPT_TOOLKIT_COLOR_DEPTH"] = "DEPTH_8_BIT"
    elif color_system == "truecolor":
        os.environ["PROMPT_TOOLKIT_COLOR_DEPTH"] = "DEPTH_24_BIT"


# An console for things that need to be exported, and
# an alternative console for things that
# only need to be shown to the user at runtime but not exported.
console = Console(highlight=False, record=True)
alt_console = Console(highlight=False, record=False, stderr=True)
# Stateful data is used in the progress bar to display data.
# This is set as an attribute of console to avoid using global variables.
console.stateful_data = {}
# An exporter instance is set as a attribute of console to avoid using global variables.
# HACK: This can probably be removed and it should still work.
console.exporter = Exporter(console=console, alt_console=alt_console)
# Setting the color profile to the one from rich. To be consistent.
set_prompt_toolkit_color()


@click.command()
@click.argument("CODE_SNIPPETS", nargs=-1)
@click.option("--snippet-name", "-n", metavar="NAME", multiple=True, help="Give a meaningful name to a snippet. This can be specified multiple times if several snippets are benchmarked.") # noqa
@click.option("--setup", "-s", metavar="STMT", default="pass", show_default=True, help="Code to be executed once in each batch .\nExecution time of this setup code is *not* timed") # noqa
@click.option("--from-json", "-f", metavar="FILE", type=click.Path(dir_okay=False, resolve_path=True, readable=True, writable=False), default=None, help="If used, get all the parameters from FILE. The file needs to be a json file with a schema simillar to exported json files") # noqa
@click.option("--json", "-j", "to_json", is_flag=True, default=False, show_default=False, help="If used, output results in a json format to stdout.") # noqa
@click.option("--quiet", "-q", is_flag=True, default=False, show_default=False, help="If used, there will be no output printed.") # noqa
@click.option("--only-export", "-e", metavar="FILE", is_flag=True, default=None, show_default=True, help="If used alongside ``--from-json``, skips the benchmarking part and just exports the data.") # noqa
@click.option("--warmup", "-w", metavar="NUM", type=click.IntRange(min=1), help="Perform NUM warmup runs before the actual benchmark. Perform this only for presistent improvements. Otherwise all performance gains are lost on each batch") # noqa
@click.option( "--code-theme", "-c", default="one-dark", show_default=True, metavar="THEME_NAME", help="Theme for code input and output, also applicable if \"-\" is used for any of the parameters, For a list see https://pygments.org/styles") # noqa
@click.option("--total-time", "-t", metavar="TIME", default="3s", show_default=True, type=Time(), help="How long to test each snippet for, specifying ``--runs`` overrides this. Format: 500ms, 10s, 1m5s, 1.5m, 1h30m15s, etc.") # noqa
@click.option("--time-per-batch", "-b", metavar="TIME", default="200ms", show_default=True, type=Time(), help="How long each test batch will last for, increase this to make the tests more accurate at the cost of making progress bar less smooth. Also change ``--total-time`` accordingly or else statistics won't work") # noqa
@click.option("--time-unit", "-u", metavar="UNIT", default="dynamic", show_default=True, type=click.Choice(TIME_FORMAT_UNITS, case_sensitive=False), help="Set the time unit to be used. Possible values: ns, us, ms, s, dynamic") # noqa
@click.option("--runs", "-r", metavar="NUM", type=click.IntRange(min=1), help="Perform exactly NUM runs for each snippet. By default, the number of runs is automatically determined") # noqa
@click.option("--min-runs", "-m", metavar="NUM", default=2, show_default=True, type=click.IntRange(min=1), help="Perform at least NUM runs for each snippet") # noqa
@click.option("--max-runs", "-M", metavar="NUM", type=click.IntRange(min=1), help="Perform at least NUM runs for each snippet, by default unlimited.") # noqa
@click.option("--export-json", metavar="FILE", type=click.Path(dir_okay=False, resolve_path=True, readable=False, writable=True), help="Export the timing summary statistics as JSON to the given FILE") # noqa
@click.option("--export-csv", metavar="FILE", type=click.Path(dir_okay=False, resolve_path=True, readable=False, writable=True), help="Export the timing summary statistics as CSV  to the given FILE.") # noqa
@click.option("--export-yaml", metavar="FILE", type=click.Path(dir_okay=False, resolve_path=True, readable=False, writable=True), help="Export the timing summary statistics as YAML to the given FILE.") # noqa
@click.option("--export-markdown", metavar="FILE", type=click.Path(dir_okay=False, resolve_path=True, readable=False, writable=True), help="Export the timing summary statistics as a Markdown table to the given FILE.") # noqa
@click.option("--export-svg", metavar="FILE", type=click.Path(dir_okay=False, resolve_path=True, readable=False, writable=True), help="Export the console output as a svg image to the given FILE") # noqa
@click.option("--export-image", metavar="FILE", type=click.Path(dir_okay=False, resolve_path=True, readable=False, writable=True), help="Export the console output as an image to the given FILE. Exports to svg then uses a headless browser to screenshot that svg output.") # noqa
@click.option("--background", metavar="CSS_COLOR", default='random', show_default=True, help="Specify a custom background for the generated image. This supports anything the CSS background property supports including images, gradients etc. For more info see https://www.w3schools.com/cssref/css3_pr_background.asp") # noqa
@click.option("--selenium-browser", metavar="BROWSER", default="chrome", show_default=True, type=click.Choice(['chrome','edge','firefox', 'opera', 'safari'], case_sensitive=False), help="The browser to use for exporting the image") # noqa
@click.option("--watermark/--no-watermark", default=True, show_default=True, help="Whether to add a watermark to the bottom right corner of the generated image. A watermark helps spread the word") # noqa
@click.option("--export-asciidoc", metavar="FILE", type=click.Path(dir_okay=False, resolve_path=True, readable=False, writable=True), help="Export the timing summary statistics as an AsciiDoc table to the given FILE.") # noqa
@click.option("--export-plot", metavar="FILE", type=click.Path(dir_okay=False, resolve_path=True, readable=False, writable=True), help="Export the timing summary statistics as a image of a bar plot to the given FILE") # noqa
@click.option("--label-format", metavar="FORMAT", default="{snippet_name}\n{snippet_code}", show_default="{snippet_name}\\\\n{snippet_code}", help="Format string for the bar plot, only applicable if the ``--export-plot`` option is specified.") # noqa
@click.option("--dark-background", is_flag=True, default=False, show_default=True, help="If used, the plot background will be in dark mode instead of light") # noqa
@click.option("--bar-color", metavar="MATPLOTLIB_COLOR", default="#99bc5a", show_default=True, help="A color to use for the bars in the bar plot. Must be in matplotlib supported format, For more info see https://matplotlib.org/stable/tutorials/colors/colors.html") # noqa
@click.option("--export-html", metavar="FILE", type=click.Path(dir_okay=False, resolve_path=True, readable=False, writable=True), help="Export the timing summary statistics as html web page to the given FILE") # noqa
@click.version_option(VERSION, '--version', '-v', package_name="fastero", prog_name="fastero") # noqa
@click.help_option('-h', '--help')
def app(
    code_snippets    : List[str],
    snippet_name     : List[str],
    setup            : str,
    from_json        : Path,
    to_json          : bool,
    quiet            : bool,
    only_export      : bool,
    warmup           : int,
    code_theme       : str,
    total_time       : str,
    time_per_batch   : int,
    time_unit        : str,
    runs             : int,
    min_runs         : int,
    max_runs         : int,
    export_json      : Path,
    export_csv       : Path,
    export_yaml      : Path,
    export_markdown  : Path,
    export_svg       : Path,
    export_image     : Path,
    background : str,
    selenium_browser : str,
    watermark        : bool,
    export_asciidoc  : Path,
    export_plot      : Path,
    dark_background  : bool,
    bar_color        : str,
    label_format     : str,
    export_html      : Path
):
    """
    Benchmark each snippet in **CODE_SNIPPETS**.

    Detailed documentation available at https://fastero.readthedocs.io
    """

    # Suppress all output if the user we only wants json
    if quiet or to_json:
        console.file = open(os.devnull, 'a', encoding="utf-8")
        alt_console.file = open(os.devnull, 'a', encoding="utf-8")

        # Emulate a dumb terminal that doesn't know how to show progress bars
        os.environ["TERM"] = "DUMB"

    if from_json and only_export:
        import json

        with open(from_json, 'r') as f:
            data = json.load(f)
            console.exporter.setup = data['setup']
            if data['setup'] and data['setup'] != 'pass':
                console.print(
                    Panel(
                        Syntax(
                            data['setup'], 'python',
                            theme=code_theme,
                            code_width=65,
                            indent_guides=True,
                            line_numbers=True,
                            word_wrap=True
                        ),
                        title="Setup code",
                        border_style='dim',
                        expand=False,
                    )
                )
            for result in data['results']:
                console.exporter.add_result(**result)

                total_runs = int(result['runs'])

                # Format all the statistics (add units such as ns, ms, s)
                formatted_mean = choose_unit(result['mean'], unit=time_unit)
                formatted_stddev = choose_unit(result['stddev'], unit=time_unit)
                formatted_min = choose_unit(result['min'], unit=time_unit)
                formatted_max = choose_unit(result['max'], unit=time_unit)

                # Figure out which statistic takes the highest width
                # This is going to be used for padding
                highest_width = max(len(i) for i in (formatted_mean, formatted_stddev, formatted_min, formatted_max))

                # Print the snippet name and code with syntax highlighting
                console.print(
                    f"[b]{result['snippet_name']}[/]:",
                    Syntax('', 'python', theme=code_theme).highlight(result['snippet_code']),
                    sep=" ",
                    end=""
                )

                console.print(
                    f"  Time  ([green b]mean[/] ± [green]σ[/]):       "
                    f"[green b]{formatted_mean.rjust(highest_width)}[/] ± [green]{formatted_stddev.rjust(highest_width)}[/]"
                )
                console.print(
                    f"  Range ([cyan b]min[/]  … [magenta]max[/]):     "
                    f"[cyan b]{formatted_min.rjust(highest_width)}[/] … [magenta]{formatted_max.rjust(highest_width)}[/]" +
                    f"    " + f"[bright_black]\[runs: {total_runs:,}][/]"
                )
            # Generate a bar plot of all the snippets
            if len(data['results']) > 1:
                plot = make_bar_plot(
                    labels=[format_snippet(i, code_theme=code_theme, replace_newlines=True) for i in data['results']],
                    amounts=[i["min"] for i in data['results']],
                    ascii_only=console.options.ascii_only
                )
                # Simulate a console with 500 width, used to get max bar chart size
                # This is needed because the text is truncated in less wide consoles
                # And measuring the size with the current console [options] will
                # Get the size after truncating the text, I don't want that
                opts = console.options.copy()
                opts.size = (500, 500)
                opts.min_width, opts.max_width = (0, 500)
                # Get the size needed to print the plot
                plot_size = console.measure(plot, options=opts)
                # Print the plot if there it sufficient space
                if console.width > plot_size.minimum:
                    console.print(plot)
                else:
                    alt_console.print("[u yellow]Warning:[/] Bar Chart not printed due to insufficient console width")

                if len(data['results']) > 1:
                    console.print("\n[b]Summary[/]:")
                fastest_snippet = min(data['results'], key=lambda x: x["mean"])
                console.print(" ", format_snippet(fastest_snippet, code_theme=code_theme, replace_newlines=True), "is the fastest.")
                for code_snippet in data['results']:
                    if code_snippet == fastest_snippet:
                        continue
                    console.print(
                        f"    [b green]{round(code_snippet['mean']/fastest_snippet['mean'],2 )}[/] "
                        f"([cyan]{round(code_snippet['min']/fastest_snippet['min'],2 )}[/] …"
                        f" [magenta]{round(code_snippet['max']/fastest_snippet['max'],2 )}[/])"
                        " times faster than",
                        format_snippet(code_snippet, code_theme=code_theme)
                    )

        if to_json:
            console.exporter.export_json("", stdout=True)

        if export_image:
            console.exporter.export_image(export_image, browser=selenium_browser, add_watermark=watermark, background=background)
        if export_svg:
            console.exporter.export_svg(export_svg)
        if export_json:
            console.exporter.export_json(export_json)
        if export_csv:
            console.exporter.export_csv(export_csv)
        if export_markdown:
            console.exporter.export_markdown(export_markdown, unit=time_unit)
        if export_asciidoc:
            console.exporter.export_asciidoc(export_asciidoc, unit=time_unit)
        if export_html:
            console.exporter.export_html(export_html, unit=time_unit)
        if export_yaml:
            console.exporter.export_yaml(export_yaml)
        if export_plot:
            console.exporter.export_plot(
                export_plot, unit=time_unit, label_format=label_format,
                dark_background=dark_background, bar_color=bar_color
            )

        raise click.exceptions.Exit()
    elif from_json:
        import json

        with open(from_json, 'r') as f:
            data = json.load(f)
            setup = data['setup']
            code_snippets = (i['snippet_code'] for i in data['results'])
            snippet_name = (i.get('snippet_name') for i in data['results'])

    # Convert from tuple to list to make mutable
    # This is needed to get the snippets that are set to "-"
    code = list(code_snippets)
    statement_name = list(snippet_name)

    # If there are parameters, Print a rule to separate them from the results
    if any(i == '-' for i in [setup, *code]):
        alt_console.print(Rule("Parameters"))

    # First get the input for setup and then get the other code
    _setup_is_gotten_later = False
    if setup == '-':
        gotten_code = get_code_input(f"Enter code for --setup ")
        if gotten_code is None:
            setup = "pass"
        else:
            setup = gotten_code
            _setup_is_gotten_later = True
    elif setup.startswith("file:"):
        import re

        setup_regex_match = re.match(r"file: ?((?:[\w,\s-]+\.?\w*)+)", setup)
        setup_file = setup_regex_match.group(1)
        if setup_file == "stdin":
            import sys

            setup = sys.stdin.read()
        else:
            path = click.Path(
                exists=True, file_okay=True, dir_okay=False, writable=False,
                readable=True, resolve_path=True, allow_dash=True
            ).convert(setup_file, None, None)
            with open(path, "rt", encoding="utf-8") as f:
                setup = f.read()

    console.exporter.setup = setup

    if setup and setup != "pass" and not _setup_is_gotten_later:
        console.print(
            Panel(
                Syntax(
                    setup, 'python',
                    theme=code_theme,
                    code_width=65,
                    indent_guides=True,
                    line_numbers=True,
                    word_wrap=True
                ),
                title="Setup code",
                border_style='dim',
                expand=False,
            )
        )
    elif setup and setup != "pass" and _setup_is_gotten_later and any((export_svg, export_image)):
        alt_console.print("[cyan]Info:[/] Printing setup to make sure it is shown in the exported output")
        console.print(
            Panel(
                Syntax(
                    setup, 'python',
                    theme=code_theme,
                    code_width=65,
                    indent_guides=True,
                    line_numbers=True,
                    word_wrap=True
                ),
                title="Setup code",
                border_style='dim',
                expand=False,
            )
        )

    # Loop through each snippet and if it has a name provided with the
    # --snippet-name option then use that name, otherwise set the name to "Benchmark {index}".
    for index, code_snippet in enumerate(code):
        try:
            name = statement_name[index]
        except IndexError:
            name = f"Benchmark {index+1}"
            statement_name.insert(index, name)
        # If the snippet isn't provided when using the command. Get it now.
        if code_snippet == "-":
            gotten_code = get_code_input(f"Enter code for {name} ", theme=code_theme)
            if gotten_code is None:
                raise click.Abort()
            # Insert it in place of the "-"
            code[index] = gotten_code
        elif code_snippet.startswith("file:"):
            import re

            code_snippet_regex_match = re.match(r"file: ?((?:[\w,\s-]+\.?\w*)+)", code_snippet)
            code_snippet_file = code_snippet_regex_match.group(1)
            if code_snippet_file == "stdin":
                import sys

                setup = sys.stdin.read()
            else:
                path = click.Path(
                    exists=True, file_okay=True, dir_okay=False, writable=False,
                    readable=True, resolve_path=True, allow_dash=True
                ).convert(code_snippet_file, None, None)
                with open(path, "rt", encoding="utf-8") as f:
                    code[index] = f.read()

    # Print it to the alt console so it doesn't appear in exported Image files
    alt_console.print(Rule("Benchmark started…"))

    if any(
        (export_json, export_csv, export_yaml, export_markdown,
         export_svg, export_image, export_asciidoc, export_plot, export_html)
    ):
        console.exporter._export_needed = True

    _autorange_cache = {}
    for code_snippet, statement_name in zip(code, statement_name):
        timer = Timer(stmt=code_snippet, setup=setup)

        # Print the snippet name and code with syntax highlighting
        console.print(
            f"[b]{statement_name}[/]:",
            Syntax('', 'python', theme=code_theme).highlight(code_snippet),
            sep=" ",
            end=""
        )

        with Progress(
            TextColumn(''),  # Indentation
            SpinnerColumn(),  # Spinner
            TextColumn("[progress.description]{task.description}"),  # Task Description
            StatefulColumn(console),  # Stateful data
            BarColumn(),  # Progress Bar
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),  # Task Percentage
            MofNCompleteColumn(),  # "Done/Total"
            TextColumn("[cyan]ETA[/]"),  # ETA Text
            TimeRemainingColumn(),  # ETA Value
            transient=True,  # Remove it after it's finished
        ) as progress:
            if warmup:
                warmup_task = progress.add_task("Warmup runs…", total=warmup)
                for i in range(warmup):
                    timer.timeit(number=1)
                    progress.update(warmup_task, advance=1)
                progress.remove_task(warmup_task)
            initial_task = progress.add_task("Calculating amount of runs…", total=1, start=False)

            def _autorange(timer: Timer, callback=None):
                # This is a custom timeit.autorange implementation for lower time_taken.
                # This is done to make the progress bar more smoother.
                # This does have one drawback where it makes it slower if there is a long setup

                # Try to get from cache
                if timer.stmt in _autorange_cache:
                    return _autorange_cache[timer.stmt]

                i = 1
                while True:
                    for j in 1, 2, 5, 8:
                        number = i * j
                        time_taken = timer.timeit(number)
                        if callback:
                            callback(number, time_taken)
                        if time_taken >= time_per_batch:
                            _autorange_cache[timer.stmt] = (number, time_taken)
                            return (number, time_taken)
                    i *= 10

            # determine number so that 0.1 <= total time < 2.0
            try:
                num_in_one_batch, time_taken = _autorange(timer, autorange_callback)
            except Exception:
                timer.print_exc()
                raise click.exceptions.Exit()
            progress.remove_task(initial_task)

            # Logic for calculating number of total runs
            if not runs:
                num_of_batches = int(total_time / time_taken)
                total_runs_based_on_time = num_of_batches * num_in_one_batch
                if (total_runs_based_on_time) < min_runs:
                    num_of_batches = min_runs // num_in_one_batch
                if max_runs and (total_runs_based_on_time) > max_runs:
                    num_of_batches = max_runs // num_in_one_batch
            else:
                if runs > num_in_one_batch:
                    num_of_batches = runs // num_in_one_batch
                else:
                    # Do it in three batches to get better statistics
                    num_of_batches = 3
                    num_in_one_batch = ceil(runs / 3)
            total_runs = num_of_batches * num_in_one_batch

            # Start the actual benchmarking process
            progress_task = progress.add_task("Current run:", total=total_runs)
            raw_timings = []
            for _ in range(num_of_batches):
                timed = timer.timeit(num_in_one_batch)
                raw_timings.append(timed)
                console.stateful_data[1] = \
                    f"[green]{choose_unit(raw_timings[-1] / num_in_one_batch, unit=time_unit).rjust(10)}[/]"
                progress.update(progress_task, advance=num_in_one_batch)
            timings = [time_taken_for_entire_batch / num_in_one_batch for time_taken_for_entire_batch in raw_timings]

        # Calculate mean, median, standard_deviation, min, max
        mean = statistics.mean(timings)
        median = statistics.median(timings)
        _min = min(timings)
        _max = max(timings)
        try:
            standard_deviation = statistics.stdev(timings)
        except statistics.StatisticsError:
            standard_deviation = -1

        # Add the statistics to a exporter class to keep track of them
        console.exporter.add_result(
            code_snippet, statement_name, total_runs,
            mean, median, standard_deviation, _min, _max
        )

        # Format all the statistics (add units such as ns, ms, s)
        formatted_mean = choose_unit(mean, unit=time_unit)
        formatted_stddev = choose_unit(standard_deviation, unit=time_unit)
        formatted_min = choose_unit(_min, unit=time_unit)
        formatted_max = choose_unit(_max, unit=time_unit)

        # Figure out which statistic takes the highest width
        # This is going to be used for padding
        highest_width = max(len(i) for i in (formatted_mean, formatted_stddev, formatted_min, formatted_max))


        console.print(
            f"  Time  ([green b]mean[/] ± [green]σ[/]):       "
            f"[green b]{formatted_mean.rjust(highest_width)}[/] ± [green]{formatted_stddev.rjust(highest_width)}[/]"
        )
        console.print(
            f"  Range ([cyan b]min[/]  … [magenta]max[/]):     "
            f"[cyan b]{formatted_min.rjust(highest_width)}[/] … [magenta]{formatted_max.rjust(highest_width)}[/]" +
            f"    " + f"[bright_black]\[runs: {total_runs:,}][/]"
        )

    # If there are multiple code snippets, print a summary
    if len(code) > 1:
        console.print("\n[b]Summary[/]:")
        all_snippets = console.exporter.snippets
        # Generate a bar plot of all the snippets
        plot = make_bar_plot(
            labels=[format_snippet(i, code_theme=code_theme, replace_newlines=True) for i in all_snippets],
            amounts=[i["min"] for i in all_snippets],
            ascii_only=console.options.ascii_only
        )
        # Simulate a console with 500 width, used to get max bar chart size
        # This is needed because the text is truncated in less wide consoles
        # And measuring the size with the current console [options] will
        # Get the size after truncating the text, I don't want that
        opts = console.options.copy()
        opts.size = (500, 500)
        opts.min_width, opts.max_width = (0, 500)
        # Get the size needed to print the plot
        plot_size = console.measure(plot, options=opts)
        # Print the plot if there it sufficient space
        if console.width > plot_size.minimum:
            console.print(plot)
        else:
            alt_console.print("[u yellow]Warning:[/] Bar Chart not printed due to insufficient console width")

        fastest_snippet = min(all_snippets, key=lambda x: x["mean"])
        console.print(" ", format_snippet(fastest_snippet, code_theme=code_theme, replace_newlines=True), "is the fastest.")
        for code_snippet in all_snippets:
            if code_snippet == fastest_snippet:
                continue
            console.print(
                f"    [b green]{round(code_snippet['mean']/fastest_snippet['mean'],2 )}[/] "
                f"([cyan]{round(code_snippet['min']/fastest_snippet['min'],2 )}[/] …"
                f" [magenta]{round(code_snippet['max']/fastest_snippet['max'],2 )}[/])"
                " times faster than",
                format_snippet(code_snippet, code_theme=code_theme)
            )

    # Only print benchmark finished if there are some exports, otherwise
    # Don't need separation since the shell prompt should be enough
    if console.exporter._export_needed:
        alt_console.print(Rule("Benchmark finished…"))

    if to_json:
        console.exporter.export_json("", stdout=True)

    # Export the results, in order of most error prone to least
    if export_svg:
        console.exporter.export_svg(export_svg)
    if export_json:
        console.exporter.export_json(export_json)
    if export_csv:
        console.exporter.export_csv(export_csv)
    if export_markdown:
        console.exporter.export_markdown(export_markdown, unit=time_unit)
    if export_asciidoc:
        console.exporter.export_asciidoc(export_asciidoc, unit=time_unit)
    if export_html:
        console.exporter.export_html(export_html, unit=time_unit)
    if export_yaml:
        console.exporter.export_yaml(export_yaml)
    if export_image:
        console.exporter.export_image(export_image, browser=selenium_browser, add_watermark=watermark, background=background)
    if export_plot:
        console.exporter.export_plot(
            export_plot, unit=time_unit, label_format=label_format,
            dark_background=dark_background, bar_color=bar_color
        )
