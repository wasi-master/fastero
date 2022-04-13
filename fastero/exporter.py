"""Module for exporting data."""

import click

from .utils import choose_unit, format_snippet
from rich.console import Console
from rich.terminal_theme import TerminalTheme


class Exporter:
    """Class for managing and exporting data."""

    def __init__(self, console: Console = None, alt_console: Console = None, setup: str = None):
        """
        Initialize the exporter.

        Parameters
        ----------
        console : Console, optional
            The console object to print data, by default None
        alt_console : Console, optional
            The console object to print data to only be shown in runtime, by default None
        setup : str, optional
            The code used for the setup
        """
        self.snippets = []
        self.console = console
        self.alt_console = alt_console
        self.setup = setup
        self._export_needed = False

    def add_result(
        self,
        snippet_code: str,
        snippet_name: str,
        runs: int,
        mean: int,
        median: int,
        stddev: int,
        min: int,
        max: int
    ):
        """
        Add a result to the exporter's list of results.

        Parameters
        ----------
        snippet_code : str
            The code for the snippet
        snippet_name : str
            The name for the snippet
        runs : int
            The amount of times the snippet ran
        mean : int
            The mean from all runs of the snippet
        median : int
            The median from all runs of the snippet
        stddev : int
            The standard deviation from all runs of the snippet
        min : int
            The fastest run from all runs of the snippet
        max : int
            The slowest run from all runs of the snippet
        """
        self.snippets.append(
            {
                "snippet_code": snippet_code,
                "snippet_name": snippet_name,
                "runs": runs,
                "mean": mean,
                "median": median,
                "min": min,
                "max": max,
                "stddev": stddev,
            }
        )

    def export_json(self, filename, stdout=False):
        """
        Export results to a JSON file.

        Parameters
        ----------
        filename : Union[str, Path]
            The path of the file to where the results will be exported
        stdout : bool
            If used, print the results to stdout and return
        """
        import json
        if stdout:
            return print(
                json.dumps(
                    {
                        "setup": self.setup,
                        "results": self.snippets,
                    },
                    indent=4,
                )
            )
        with self.alt_console.status("Exporting JSON"):
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "$schema": "https://api.jsonbin.io/b/625164e2d8a4cc06909e3be7/5",
                        "setup": self.setup,
                        "results": self.snippets,
                    },
                    f,
                    indent=4,
                )

            self.alt_console.print("[green] Success:[/] exported as JSON")

    def export_csv(self, filename):
        """
        Export results to a CSV file.

        Parameters
        ----------
        filename : Union[str, Path]
            The path of the file to where the results will be exported
        """
        with self.alt_console.status("Exporting CSV"):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(
                    ",".join(
                        i.replace("_", " ").title().replace("Stddev", "Standard Deviation")
                        for i in self.snippets[0].keys()
                    )
                    + "\n"
                )
                for snippet in self.snippets:
                    f.write(",".join(map(str, snippet.values())) + "\n")
            self.alt_console.print("[green] Success:[/] exported as CSV")

    def export_yaml(self, filename):
        """
        Export results to a YAML file.

        Parameters
        ----------
        filename : Union[str, Path]
            The path of the file to where the results will be exported
        """
        with self.alt_console.status("Exporting YAML"):
            try:
                from yaml import dump
            except ImportError:
                self.alt_console.print(
                    "[red b]Error:[/] The package [#bbbbbb on #222222]PyYAML[/] is not installed. "
                    "Please install it in order to export yaml."
                )
                raise click.exceptions.Exit()
            try:
                from yaml import CDumper as Dumper
            except ImportError:
                from yaml import Dumper

            with open(filename, "w", encoding="utf-8") as f:
                f.write(dump({"results": self.snippets}))
            self.alt_console.print("[green] Success:[/] exported as YAML")

    def export_markdown(self, filename, unit: str = None):
        """
        Export results to a Markdown file as a table.

        Parameters
        ----------
        filename : Union[str, Path]
            The path of the file to where the results will be exported
        unit : str, optional
            The unit to be used, use None for dynamic units. by default None
        """
        with self.alt_console.status("Exporting Markdown"):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(
                    "|"
                    + "|".join(
                        i.replace("_", " ")
                        .replace("|", "\\|")
                        .title()
                        .replace("Stddev", "Standard Deviation")
                        for i in self.snippets[0].keys()
                    )
                    + "|\n"
                )
                f.write("|" + "|".join(["---"] * len(self.snippets[0].keys())) + "|\n")
                for snippet in self.snippets:
                    f.write(
                        "|"
                        + "|".join(
                            [
                                choose_unit(x, unit=unit, asciimode=False) if isinstance(x, float) else str(x)
                                for x in
                                snippet.values()
                            ]
                        )
                        + "|\n"
                    )
            self.alt_console.print("[green] Success:[/] exported as Markdown")

    def export_asciidoc(self, filename, unit: str = None):
        """
        Export results to a AsciiDoc file as a table.

        Parameters
        ----------
        filename : Union[str, Path]
            The path of the file to where the results will be exported
        unit : str, optional
            The unit to be used, use None for dynamic units. by default None
        """
        with self.alt_console.status("Exporting AsciiDoc"):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(
                    '[cols="'
                    + "".join([","] * (len(self.snippets[0].keys()) - 1))
                    + '" options="header"]\n'
                )
                f.write("|===\n")
                f.write(
                    "|"
                    + "|".join(
                        i.replace("_", " ")
                        .replace("|", "\\|")
                        .title()
                        .replace("Stddev", "Standard Deviation")
                        for i in self.snippets[0].keys()
                    )
                    + "\n"
                )
                for snippet in self.snippets:
                    f.write(
                        "|"
                        + "|".join(
                            [
                                choose_unit(x, unit=unit, asciimode=False) if isinstance(x, float) else str(x)
                                for x in
                                snippet.values()
                            ]
                        )
                        + "\n"
                    )
                f.write("|===\n")
            self.alt_console.print("[green] Success:[/] exported as AsciiDoc")

    def export_html(self, filename, unit: str):
        """
        Export results to a HTML file as a table.

        Parameters
        ----------
        filename : Union[str, Path]
            The path of the file to where the results will be exported
        unit : str, optional
            The unit to be used, use None for dynamic units. by default None
        """
        from html import escape

        with self.alt_console.status("Exporting HTML"):
            with open(filename, "w", encoding="utf-8") as f:
                f.write("<table><thead><tr>\n")
                for header_item in self.snippets[0].keys():
                    formatted = escape(header_item.replace('_', ' ').title().replace('Stddev', 'Standard Deviation'))
                    f.write(
                        f"<th>{formatted}</th>\n"
                    )
                f.write("</tr></thead>\n<tbody>")
                for snippet in self.snippets:
                    f.write("<tr>\n")
                    f.write(f"<td>{snippet['snippet_code']}</td>\n<td>{snippet['snippet_name']}</td>\n")
                    f.write(
                        "\n  ".join(
                            f"<td>{escape(choose_unit(snippet['mean'], unit=unit, asciimode=False))}</td>\n"
                            for value in snippet.values()[2:]
                        )
                    )
                    f.write("</tr>\n")
                f.write("</table>")
            self.alt_console.print("[green] Success:[/] exported as HTML")

    def export_svg(self, filename):
        """
        Export results (console output) to a SVG file.

        Parameters
        ----------
        filename : Union[str, Path]
            The path of the file to where the results will be exported
        """
        with self.alt_console.status("Exporting SVG"):
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.console.export_svg(title="Python Benchmark Output", clear=False))
            self.alt_console.print("[green] Success:[/] exported as SVG")

    def export_image(self, filename, browser="chrome", add_watermark=True, background="random"):
        """
        Export results (console output) to a CSV file.

        Parameters
        ----------
        filename : Union[str, Path]
            The path of the file to where the results will be exported
        browser : str
            The name of the browser to use for the screenshot.
            Any of chrome, firefox, edge, opera, safari
        """
        import platform
        import os.path
        import tempfile
        import random
        from pathlib import Path

        # For previews in my IDE and on the GitHub website (using extensions)
        rgb = lambda r, g, b: (r, g, b)

        ORIGINAL_TERMINAL_THEME = TerminalTheme(
            rgb(12, 12, 12),
            rgb(242, 242, 242),
            [
                rgb(12, 12, 12),
                rgb(205, 49, 49),
                rgb(13, 188, 121),
                rgb(229, 229, 16),
                rgb(36, 114, 200),
                rgb(138, 115, 255),
                rgb(17, 168, 205),
                rgb(229, 229, 229),
            ],
            [
                rgb(82, 82, 82),
                rgb(241, 76, 76),
                rgb(35, 209, 139),
                rgb(245, 245, 67),
                rgb(59, 142, 234),
                rgb(214, 112, 214),
                rgb(41, 184, 219),
                rgb(229, 229, 229),
            ],
        )
        DRACULA_TERMINAL_THEME = TerminalTheme(
            rgb(40, 42, 54),
            rgb(248, 248, 242),
            [
                rgb(40, 42, 54),
                rgb(255, 85, 85),
                rgb(80, 250, 123),
                rgb(241, 250, 140),
                rgb(189, 147, 249),
                rgb(255, 121, 198),
                rgb(139, 233, 253),
                rgb(248, 248, 242),
            ],
            [
                rgb(100, 113, 162),
                rgb(251, 109, 113),
                rgb(113, 255, 151),
                rgb(254, 255, 169),
                rgb(214, 171, 253),
                rgb(253, 144, 222),
                rgb(169, 255, 254),
                rgb(255, 255, 255),
            ],
        )
        CUSTOM_TERMINAL_THEME = TerminalTheme(
            rgb(34, 33, 44),
            rgb(248, 248, 242),
            [
                rgb(34, 33, 44),
                rgb(251, 149, 132),
                rgb(138, 255, 128),
                rgb(255, 255, 128),
                rgb(48, 184, 243),
                rgb(149, 128, 255),  # magenta/purple
                # rgb(255, 121, 198),  # pink
                rgb(128, 255, 234),
                rgb(248, 248, 242),
            ],
            [
                rgb(121, 112, 169),
                rgb(253, 202, 194),
                rgb(167, 237, 209),
                rgb(254, 255, 219),
                rgb(211, 231, 245),
                rgb(221, 208, 243),
                rgb(219, 255, 249),
                rgb(255, 255, 255),
            ],
        )
        gradients = [
        """\
        body {{
            background: linear-gradient(to right, #91EAE4, #86A8E7, #7F7FD5);
        }}""",
        """\
        body {{
            background: linear-gradient(to right, #240b36, #c31432);
        }}""",
        """\
        body {{
            background: linear-gradient(to right, #f5af19, #f12711);
        }}""",
        """\
        body {{
            background: linear-gradient(to right, #2ebf91, #8360c3);
        }}""",
        """\
        body {{
            background: linear-gradient(to right, #ec2F4B, #009FFF);
        }}""",
        """\
        body {{
            background-image: linear-gradient( 109.6deg,  rgba(61,245,167,1) 11.2%, rgba(9,111,224,1) 91.1% );
        }}""",
        """\
        body {{
            background-image: linear-gradient( 117deg,  rgba(123,216,96,1) 39.2%, rgba(255,255,255,1) 126.2% );
        }}""",
        """\
        body {{
            background-image: linear-gradient( 132.6deg,  rgba(71,139,214,1) 23.3%, rgba(37,216,211,1) 84.7% );
        }}""",
        """\
        body {{
            background-image: radial-gradient( circle farthest-corner at 10% 20%,  rgba(37,145,251,0.98) 0.1%, rgba(0,7,128,1) 99.8% );
        }}""",
        """\
        body {{
            background-image: radial-gradient( circle farthest-corner at 10% 20%,  rgba(171,102,255,1) 0%, rgba(116,182,247,1) 90% );
        }}""",
        """\
        body {{
            background-image: linear-gradient( 134.6deg,  rgba(201,37,107,1) 15.4%, rgba(116,16,124,1) 74.7% );
        }}""",
        """\
        body {{
            background-image: radial-gradient( circle farthest-corner at 14.2% 24%,  rgba(239,61,78,1) 0%, rgba(239,61,78,0.81) 51.8%, rgba(239,61,78,0.53) 84.6% );
        }}""",
        """\
        body {{
            background-image: radial-gradient( circle farthest-corner at 10% 20%,  rgba(14,174,87,1) 0%, rgba(12,116,117,1) 90% );
        }}""",
        """\
        body {{
            background-image: linear-gradient( 109.6deg,  rgba(61,245,167,1) 11.2%, rgba(9,111,224,1) 91.1% );
        }}""",
        """\
        body {{
            background-image: radial-gradient( circle farthest-corner at 32.7% 82.7%,  rgba(173,0,171,1) 8.3%, rgba(15,51,92,1) 79.4% );
        }}""",
        """\
        body {{
            background-image: linear-gradient( 109.6deg,  rgba(24,138,141,1) 11.2%, rgba(96,221,142,1) 91.1% );
        }}""",
        ]
        SVGLIB_SVG_FORMAT = """\
<svg width="100%" height="{total_height}" viewBox="0 0 {total_width} {total_height}"
     xmlns="http://www.w3.org/2000/svg">
    <style>
""" + (random.choice(gradients) if background == 'random' else ("body{{background: " + background + ";background-size: cover;}}")) + """
        span {{
            display: inline-block;
            white-space: pre;
            vertical-align: top;
            font-size: {font_size}px;
            font-family:'Fira Code','Cascadia Code',Monaco,Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace;
        }}
        a {{
            text-decoration: none;
            color: inherit;
        }}
        #wrapper {{
            padding: 130px;
            padding-top: 100px;
        }}
        #terminal {{
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: {theme_background_color};
            border-radius: 14px;
            box-shadow: rgb(10 10 10 / 50%) 0px 8px 24px;
        }}
        #terminal-header {{
            position: relative;
            width: 100%;
            background-color: #38374a;
            margin-bottom: 12px;
            font-weight: bold;
            border-radius: 14px 14px 0 0;
            color: {theme_foreground_color};
            font-size: 18px;
        }}
        #terminal-title-tab {{
            display: inline-block;
            margin-top: 14px;
            margin-left: 124px;
            font-family: sans-serif;
            padding: 14px 28px;
            border-radius: 8px 8px 0 0;
            background-color: {theme_background_color};
        }}
        #terminal-traffic-lights {{
            position: absolute;
            top: 24px;
            left: 20px;
        }}
        #terminal-body {{
            line-height: {line_height}px;
            padding: 14px;
        }}
        #watermark {{
            position: absolute;
            bottom: 5px;
            right: 5px;
            text-align: right;
            color: white;
            opacity: 0.8;
            margin-right: 2em;
            font-size: 1.25em;
            font-family: Comfortaa,Montserrat,Futura,Poppins,Josefin Sans,Raleway,Quicksand,Caviar Dreams,League Spartan,Sofia Pro,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Helvetica Neue,Arial,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;
            text-shadow: 5px 5px 10px rgba(12, 12, 12, 0.4);
        }}
        {stylesheet}
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
                        <div id="terminal-title-tab">{title}</div>
                    </div>
                    <div id='terminal-body'>
                        {code}
                    </div>
                </div>
            </div>"""+("""\
        <p id="watermark">Fastero</p>
""" if add_watermark else "") + """\
        </body>
    </foreignObject>
</svg>
"""

        with self.alt_console.status("Exporting initial SVG…"):

            svg_data = self.console.export_svg(title="Python Benchmark Output", clear=False, theme=CUSTOM_TERMINAL_THEME, code_format=SVGLIB_SVG_FORMAT)
            tempdir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())
            svg_file_location = os.path.join(tempdir, "fastero.svg")
            with open(svg_file_location, "w", encoding="utf-8") as svg_file:
                svg_file.write(svg_data)
        with self.alt_console.status("Opening headless browser window…"):
            try:
                import selenium
                from selenium import webdriver
            except ImportError:
                self.alt_console.print(
                    "[red b]Error:[/] The package [#bbbbbb on #222222]selenium[/] is not installed. Please install it in order to export images. It is required to convert svg to png"
                )
                raise click.exceptions.Exit()

            if browser =="chrome":
                from selenium.webdriver.chrome.options import Options
                options = Options()
                options.headless = True
                options.add_argument("--force-device-scale-factor=1")
                options.add_argument("--window-size=1920x2560")
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                driver = webdriver.Chrome(options=options)
            elif browser == "firefox":
                from selenium.webdriver.firefox.options import Options
                options = Options()
                options.headless = True
                options.add_argument("--force-device-scale-factor=1")
                options.add_argument("--window-size=1920x2560")
                driver = webdriver.Firefox(options=options, service_log_path=os.devnull)
            elif browser == "edge":
                from selenium.webdriver.edge.options import Options
                options = Options()
                options.headless = True
                options.add_argument("--force-device-scale-factor=1")
                options.add_argument("--window-size=1920x2560")
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                driver = webdriver.Edge(options=options)
            elif browser == "opera":
                from selenium.webdriver.opera.options import Options
                options = Options()
                options.headless = True
                options.add_argument("--force-device-scale-factor=1")
                options.add_argument("--window-size=1920x2560")
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                driver = webdriver.Opera(options=options)
            elif browser == "safari":
                from selenium.webdriver.safari.options import Options
                options = Options()
                options.headless = True
                options.add_argument("--force-device-scale-factor=1")
                options.add_argument("--window-size=1920x2560")
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                driver = webdriver.Safari(options=options)
        with self.alt_console.status("Loading SVG in headless browser"):
            driver.get(f'file://{svg_file_location}')
            png_file_location = os.path.join(tempdir, "fastero.png")
            driver.maximize_window()
            # driver.execute_script("$('#wrapper').css('zoom', 5);")
            # driver.execute_script("document.body.style.zoom='80%'")
        with self.alt_console.status("Capturing screenshot of SVG…"):
            # body = driver.find_element_by_tag_name('body')
            # body.screenshot(png_file_location)
            driver.save_screenshot(png_file_location)
        with self.alt_console.status("Closing headless browser window…"):
            driver.quit()
        with self.alt_console.status("Cropping screenshot…"):
            try:
                from PIL import Image, ImageChops
            except ImportError:
                self.alt_console.print(
                    "[red b]Error:[/] The package [#bbbbbb on #222222]Pillow[/] is not installed. Please install it in order to export images."
                )
                raise click.exceptions.Exit()

            def trim(im):
                bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
                diff = ImageChops.difference(im, bg)
                diff = ImageChops.add(diff, diff, 2.0, -100)
                bbox = diff.getbbox()
                if bbox:
                    return im.crop(bbox)
                return im

            im = Image.open(png_file_location)
            im = im.convert('RGB')
            im = trim(im)
            im.save(filename)

            for temp_file in (svg_file_location, png_file_location):
                os.remove(temp_file)

            self.alt_console.print("[green] Success:[/] exported as Image")

    def export_plot(self, filename, unit=None, label_format="{snippet_code}", dark_background=False, bar_color="#99bc5a"):
        """
        Export results to a PNG file as a Bar plot.

        Parameters
        ----------
        filename : Union[str, Path]
            The path of the file to where the results will be exported
        """
        def add_value_labels(ax, spacing=5):
            """Add labels to the end of each bar in a bar chart.

            Arguments:
                ax (matplotlib.axes.Axes): The matplotlib object containing the axes
                    of the plot to annotate.
                spacing (int): The distance between the labels and the bars.
            """

            # For each bar: Place a label
            for rect in ax.patches:
                # Get X and Y placement of label from rect.
                y_value = rect.get_height()
                x_value = rect.get_x() + rect.get_width() / 2

                # Number of points between bar and label. Change to your liking.
                space = spacing
                # Vertical alignment for positive values
                va = "bottom"

                # If value of bar is negative: Place label below bar
                if y_value < 0:
                    # Invert space to place label below
                    space *= -1
                    # Vertically align label at top
                    va = "top"

                # Use Y value as label and format number with one decimal place
                label = choose_unit(y_value, unit=unit, asciimode=False)

                # Create annotation
                ax.annotate(
                    label,  # Use `label` as label
                    (x_value, y_value),  # Place label at end of the bar
                    xytext=(0, space),  # Vertically shift label by `space`
                    textcoords="offset points",  # Interpret `xytext` as offset in points
                    ha="center",  # Horizontally center label
                    va=va,
                )  # Vertically align label differently for
                # positive and negative values.

        with self.alt_console.status("Exporting Bar Plot"):
            try:
                import matplotlib.pyplot as plt
            except ImportError:
                self.alt_console.print(
                    "[red b]Error:[/] The package [#bbbbbb on #222222]matplotlib[/] is not installed. Please install it in order to export plots."
                )
                raise click.exceptions.Exit()
            try:
                import numpy as np
            except ImportError:
                self.alt_console.print(
                    "[red b]Error:[/] The package [#bbbbbb on #222222]numpy[/] is not installed. Please install it in order to export plots."
                )
                raise click.exceptions.Exit()

            if dark_background:
                plt.style.use('dark_background')

            # set width of bar
            barWidth = 0.20

            labels = list(
                label_format.format(
                    snippet_name=i["snippet_name"], snippet_code=i["snippet_code"], runs=i["runs"]
                )
                for i in self.snippets
            )
            means = list(i["mean"] for i in self.snippets)
            # medians = list(i["median"] for i in self.snippets)
            # mins = list(i["min"] for i in self.snippets)
            # maxes = list(i["max"] for i in self.snippets)

            # Set position of bar on X axis
            br1 = np.arange(len(labels))
            # br2 = [x + barWidth for x in br1]
            # br3 = [x + barWidth for x in br2]
            # br4 = [x + barWidth for x in br3]

            # Make the plot
            ax = plt.axes()
            plt.bar(br1, means, color=bar_color, width=barWidth, edgecolor="grey", label="Mean")
            # plt.bar(
            #     br2,
            #     medians,
            #     color ='g',
            #     width = barWidth,
            #     edgecolor ='grey',
            #     label ='Median'
            # )
            # plt.bar(
            #     br3,
            #     mins,
            #     color ='b',
            #     width = barWidth,
            #     edgecolor ='grey',
            #     label ='Min'
            # )
            # plt.bar(
            #     br4,
            #     maxes,
            #     color ='yellow',
            #     width = barWidth,
            #     edgecolor ='grey',
            #     label ='Max'
            # )

            plt.xlabel("Snippet", fontweight="bold", fontsize=11)
            plt.ylabel("Mean Time", fontweight="bold", fontsize=11)

            add_value_labels(ax)
            # plt.xticks(
            #     [r + barWidth for r in range(len(means))],
            #     labels
            # )
            plt.xticks([r for r in range(len(means))], labels)
            try:
                ax.yaxis.set_ticks(ax.get_yticks().tolist())
            except AttributeError:
                # Maybe it's alreay an list
                ax.yaxis.set_ticks(ax.get_yticks())
            ax.set_yticklabels([choose_unit(x, unit=unit, asciimode=False) for x in ax.get_yticks().tolist()])
            plt.tight_layout()
            # plt.legend()
            # plt.show()
            plt.savefig(filename, bbox_inches="tight")
            self.alt_console.print("[green] Success:[/] exported plot as PNG")
