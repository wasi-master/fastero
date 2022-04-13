"""Utilities to be used for fastero."""
import sys
import re
import time
from enum import Enum
import timeit
from typing import List, Union

import click
from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.formatted_text import HTML
from rich import box
from rich.console import Console, Group
from rich.progress import ProgressColumn
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax

time_regex = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)((?:ms|s|m|h|d)?)")
time_dict = {"ns": 1e-09, "us": 1e-06, "ms": 0.001, "s": 1, "m": 60, "h": 3600, "d": 86400}
TIME_FORMAT_UNITS = ["ns", "us", "ms", "s", "dynamic"]


def convert_time(argument, param):
    """Convert a time argument to a string representing seconds."""

    if isinstance(argument, (float, int)):
        return argument

    matches = time_regex.findall(argument.lower())
    if not matches:
        raise click.BadParameter(
            f'Converting to time failed for parameter <{param.name}>: '
            "The time is empty or invalid"
        )
    time = 0.0
    for value, key in matches:
        try:
            time += time_dict[key] * float(value)
        except KeyError:
            raise click.BadParameter(
                f'Converting to time failed for parameter <{param.name}>: {key} is an invalid time-type! '
                f"{argument}ns/{argument}us/{argument}ms/{argument}s/{argument}m/{argument}h/{argument}d "
                "etc. are valid!"
            )
        except ValueError:
            raise click.BadParameter(
                f'Converting to time failed for parameter <{param.name}>:'
                f"{value} is not a number!"
            )
    return time


def prompt_continuation(width, line_number, wrap_count):
    """Display line numbers and '->' before soft wraps."""
    if wrap_count > 0:
        text = " " * (width - 3) + "➜"
    else:
        text = f"{line_number + 1}"
    return HTML(f'<style fg="#aaaaaa">{text} </style>')


def get_code_input(_prompt="Enter code ", theme="dracula"):
    """
    Ask the use to enter some code as input.

    Parameters
    ----------
    _prompt : str, optional
        What text to show the user to ask for code, by default "Enter code "
    theme : str, optional
        What theme to use for the code syntax highlighting, by default "dracula"

    Returns
    -------
    str
        The code that was gotten
    """
    code_style = style_from_pygments_cls(get_style_by_name(theme))
    style = merge_styles(
        [
            code_style,
            Style.from_dict(
                {
                    "text": "white",
                    "hint": "ansibrightblack",
                    "bracket": "#7c7c7c",
                    "key": "#aaaaaa bg:#222222",
                    "line_num": "#aaaaaa",
                }
            ),
        ]
    )

    message = [
        ("class:text", _prompt),
        ("class:bracket", "["),
        ("class:key", "Alt+Enter"),
        ("class:hint", " or "),
        ("class:key", "Esc+Enter"),
        ("class:hint", " to submit"),
        ("class:bracket", "]"),
        ("class:text", ":"),
        ("class:text", "\n"),
        ("class:line_num", "1 "),
    ]

    try:
        text = prompt(
            message,
            multiline=True,
            style=style,
            lexer=PygmentsLexer(PythonLexer),
            validator=PythonCodeValidator(),
            validate_while_typing=False,
            prompt_continuation=prompt_continuation,
            include_default_pygments_style=False,
        )
    except KeyboardInterrupt:
        return None
    return text


class PythonCodeValidator(Validator):
    """Validator for Python code."""

    def validate(self, document):
        """
        Validate python code.

        Tries to compile the code using the compile() function and
        if it fails then raises a ValidationError
        """
        text = document.text

        try:
            compile(text, "<code>", "exec")
        except Exception as e:
            raise ValidationError(message=str(e), cursor_position=getattr(e, "offset", 0))


class Time(click.ParamType):
    """Time parameter."""

    def convert(self, value, param, ctx):
        """Convert value to time in seconds."""
        return convert_time(value, param)


def format_snippet(snippet, code_theme="dracula", replace_newlines : bool = False) -> Text:
    """
    Format the snippet to be displayed.

    Tries to use name if given, otherwise uses the code as fallback
    """
    code = snippet['snippet_code'].strip().replace("\n", ";") if replace_newlines else snippet['snippet_code']
    if snippet['snippet_name'].startswith("Benchmark"):
        result = Syntax('', 'python', theme=code_theme).highlight(code)
        result.rstrip()
    else:
        result = Text(snippet['snippet_name'], style="cyan")
    return result



def choose_unit(value: int, unit: str = None, asciimode: bool = False):
    """
    Choose the unit used for the value.

    Parameters
    ----------
    value : int
        time taken in nanoseconds
    unit : str, optional
        The unit to be used, use None for dynamic units. by default None
    asciimode : bool, optional
        Whether to use ascii character instead of unicode, by default False.

    Returns
    -------
    str
        The value formatted according to the unit
    """
    if unit == "dynamic":
        unit = None
    micro = trychar("µs", "us", asciimode)
    units = {
        "s": ("s", 1.0, 3),
        "ms": ("ms", 0.001, 2),
        "us": (micro, 1e-06, 2),
        "ns": ("ns", 1e-09, 1),
    }
    if unit is None:
        for suffix, magnitude, precision in units.values():
            if value > magnitude:
                break
    else:
        suffix, magnitude, precision = units[unit]
    return f"{round(value/magnitude, precision)} {suffix}"


def trychar(char: str, fallback: str, asciimode: bool = False):
    """
    Try to use char and if not supported by the console, use fallback.

    Parameters
    ----------
    char : str
        The character to try to use
    fallback : str
        The character to use if char isn't available
    asciimode : bool, optional
        Whether to use ascii character instead of unicode, by default False.

    Returns
    -------
    str
        The character that is available between char and fallback
    """
    if asciimode is True:
        # If ascii mode is requested then simply return the fallback
        return fallback
    if asciimode is False:
        # If non-ascii mode is requested then simply return the input char
        return char
    if hasattr(sys.stdout, "encoding") and sys.stdout.encoding:
        try:
            char.encode(sys.stdout.encoding)
        except Exception:
            pass
        else:
            return char
    return fallback


class StatefulColumn(ProgressColumn):
    """Column for showing data that has state."""

    def __init__(self, console):
        """
        Initialize the stateful column.

        Parameters
        ----------
        console : rich.console.Console
            The console to get stateful data from
        """
        self.console = console
        super().__init__()

    def render(self, task):
        """Render the column data."""
        return self.console.stateful_data.get(task.id, "")


class MofNCompleteColumn(ProgressColumn):
    """Column for showing done tasks and total tasks."""

    def render(self, task):
        """Render the column data."""
        return f"[red]{task.completed:,}/{task.total:,}[/]"


def make_bar_plot(labels: List[Text], amounts: List[int], ascii_only: bool = False) -> Panel:
    """
    Generate a bar plot to display in the terminal.

    Parameters
    ----------
    labels : List[Text]
        The labels
    amounts : List[int]
        The amounts
    ascii_only : bool
        Whether to only use ascii characters, by default False
    """
    COLORS = [
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white"
    ]
    char = "▆" if not ascii_only else "*"
    largest_amount = max(amounts)

    table = Table(
        "Name", "Time Taken", "Bar",
        show_header=False,
        show_edge=False,
        box=box.SIMPLE_HEAD,
        padding=(0, 0)
    )
    for i, (label, amount) in enumerate(zip(labels, amounts)):
        amount_formatted = choose_unit(amount)
        label.style = "default on default"
        label.rstrip()
        table.add_row(
            label,
            Text(f"[{str(amount_formatted)}]:", style='cyan on default'),
            Text(char * round((amount / largest_amount) * 50), style=COLORS[i % 7])
        )
    return Panel(table, title="Bar Chart", subtitle="(lower is better)", expand=False, box=box.HEAVY, border_style="dim")

class _Timer(timeit.Timer):
    def __init__(self, *args, **kwargs):
        self.stmt = kwargs.get('stmt')
        super().__init__(*args, **kwargs)