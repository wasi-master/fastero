"""Utilities to be used for fastero."""
import sys
import re
import timeit

import click
from rich import box
from rich.progress import ProgressColumn
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax

time_regex = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)((?:ns|us|ms|s|m|h|d)?)")
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

    from prompt_toolkit.formatted_text import HTML

    if wrap_count > 0:
        text = " " * (width - 3) + "➜"
    else:
        text = f"{line_number + 1}"
    return HTML(f'<style fg="#aaaaaa">{text} </style>')


def get_python_completer():
    from prompt_toolkit.formatted_text import HTML

    try:
        import ptpython
    except ImportError:
        import keyword, builtins, types
        from prompt_toolkit.completion import WordCompleter
        def find_description(item):
            if keyword.iskeyword(item):
                return HTML("<ansimagenta>keyword</ansimagenta>")
            elif item.endswith("Error"):
                return HTML("<ansired>exception</ansired>")
            elif item.endswith("Warning"):
                return HTML("<ansiyellow>warning</ansiyellow>")
            item = eval(item)
            if isinstance(item, types.BuiltinFunctionType):
                return HTML("<ansigreen>built-in function</ansigreen>")
            return HTML(f"<ansicyan>{type(item).__name__}</ansicyan>")

        keywords_and_builtins = list(set(keyword.kwlist + dir(builtins)))
        return WordCompleter(
            keywords_and_builtins,
            meta_dict={i: find_description(i) for i in keywords_and_builtins}
        )
    else:
        from ptpython.completer import PythonCompleter

        return PythonCompleter(lambda: {}, lambda: {}, lambda: False)



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

    from pygments.lexers.python import PythonLexer
    from pygments.styles import get_style_by_name
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.shortcuts import prompt
    from prompt_toolkit.styles import Style, merge_styles
    from prompt_toolkit.styles.pygments import style_from_pygments_cls
    from prompt_toolkit.lexers import PygmentsLexer
    from prompt_toolkit.validation import Validator, ValidationError
    from prompt_toolkit.formatted_text import HTML

    try:
        from ptpython.validator import PythonValidator
    except ImportError:
        class PythonValidator(Validator):
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

    completer = get_python_completer()

    def bottom_toolbar():
        return HTML(f'Autocomplete: <b><style bg="ansired">{completer.__class__.__name__}</style></b>!')

    try:
        text = prompt(
            message,
            multiline=True,
            style=style,
            lexer=PygmentsLexer(PythonLexer),
            completer=completer,
            bottom_toolbar=bottom_toolbar,
            validator=PythonValidator(),
            validate_while_typing=False,
            prompt_continuation=prompt_continuation,
            include_default_pygments_style=False,
        )
    except KeyboardInterrupt:
        return None
    return text

def factors(n):
    return sorted(
        set(
            factor for i in range(1, int(n**0.5) + 1) if n % i == 0
            for factor in (i, n//i)
        )
    )


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


def make_bar_plot(labels, amounts, ascii_only = False) -> Panel:
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
        # Store setup for our custom handling
        self.setup_code = kwargs.get('setup', 'pass')
        super().__init__(*args, **kwargs)
        
    def _extract_globals_and_assignments(self, code):
        """Extract global declarations and top-level assignments that might conflict."""
        import ast
        
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return set(), {}
            
        globals_vars = set()
        assignments = {}
        
        # Look at all nodes, including nested ones for global declarations
        for node in ast.walk(tree):
            if isinstance(node, ast.Global):
                globals_vars.update(node.names)
        
        # Only look at top-level assignments
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        # Try to get the value if it's a simple constant
                        if isinstance(node.value, (ast.Constant, ast.Num, ast.Str)):
                            try:
                                if hasattr(node.value, 'value'):  # ast.Constant
                                    assignments[var_name] = node.value.value
                                elif hasattr(node.value, 'n'):  # ast.Num (older Python)
                                    assignments[var_name] = node.value.n
                                elif hasattr(node.value, 's'):  # ast.Str (older Python)
                                    assignments[var_name] = node.value.s
                            except:
                                pass
                                
        return globals_vars, assignments
    
    def timeit(self, number=timeit.default_number):
        """Enhanced timeit that handles global variables properly."""
        # Check if we have a global/assignment conflict
        if self.stmt:
            globals_vars, assignments = self._extract_globals_and_assignments(self.stmt)
            conflicting_vars = globals_vars & assignments.keys()
            
            if conflicting_vars:
                # We have a conflict - need to modify execution
                return self._timeit_with_globals(number, conflicting_vars, assignments)
        
        # No conflict, use standard timeit
        return super().timeit(number)
        
    def _timeit_with_globals(self, number, conflicting_vars, assignments):
        """Execute timing with proper global variable handling."""
        import ast
        import types
        
        # Create a modified version of the statement
        # Remove top-level assignments for conflicting variables
        tree = ast.parse(self.stmt)
        
        # Filter out conflicting assignments from the statement
        new_body = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                # Check if this assigns to any conflicting variable
                assigns_conflicting = False
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in conflicting_vars:
                        assigns_conflicting = True
                        break
                if not assigns_conflicting:
                    new_body.append(node)
            else:
                new_body.append(node)
        
        tree.body = new_body
        modified_stmt = ast.unparse(tree) if new_body else "pass"
        
        # Create a global namespace with the conflicting variables
        execution_globals = {}
        execution_globals.update(self.inner.__globals__)
        
        # Add the conflicting variables to globals
        for var in conflicting_vars:
            if var in assignments:
                execution_globals[var] = assignments[var]
        
        # Create a new timer with modified statement and proper globals
        # Need to properly indent the modified statement for the loop
        modified_stmt_lines = modified_stmt.split('\n')
        indented_stmt = '\n        '.join(modified_stmt_lines)
        
        timer_code = f"""
def inner(_it, _timer):
    {self.setup_code}
    _t0 = _timer()
    for _i in _it:
        {indented_stmt}
    _t1 = _timer()
    return _t1 - _t0
"""
        
        # Execute the timer code in our custom globals
        local_vars = {}
        exec(timer_code, execution_globals, local_vars)
        inner_func = local_vars['inner']
        
        # Time the execution
        it = iter(range(number))
        timing = inner_func(it, self.timer)
        return timing
    
    def warmup(self, number=10):
        """
        Perform proper warmup runs to prepare the execution environment.
        
        This method executes the statement multiple times in the same
        environment that will be used for the actual benchmark, helping
        to warm up JIT compilation, caches, and other optimizations.
        
        Parameters
        ----------
        number : int, optional
            Number of warmup iterations, by default 10
        """
        # Execute the setup once
        if self.setup_code and self.setup_code != 'pass':
            namespace = {}
            namespace.update(self.inner.__globals__)
            exec(self.setup_code, namespace)
        
        # Check if we have global/assignment conflicts like in timeit
        if self.stmt:
            globals_vars, assignments = self._extract_globals_and_assignments(self.stmt)
            conflicting_vars = globals_vars & assignments.keys()
            
            if conflicting_vars:
                # Use the same conflict resolution as in timeit
                return self._warmup_with_globals(number, conflicting_vars, assignments)
        
        # Standard warmup - just execute the statement multiple times
        namespace = {}
        namespace.update(self.inner.__globals__)
        
        # Execute setup once in the namespace
        if self.setup_code and self.setup_code != 'pass':
            exec(self.setup_code, namespace)
            
        # Execute the statement multiple times for warmup
        for _ in range(number):
            try:
                exec(self.stmt, namespace)
            except Exception:
                # If execution fails, we'll let the main benchmark handle the error
                break
    
    def _warmup_with_globals(self, number, conflicting_vars, assignments):
        """Warmup with proper global variable handling."""
        # Same logic as _timeit_with_globals but for warmup
        modified_stmt = self.stmt
        
        # Remove global declarations from the statement for execution
        for var in conflicting_vars:
            modified_stmt = modified_stmt.replace(f'global {var}', f'# global {var}')
        
        # Create a global namespace with the conflicting variables
        execution_globals = {}
        execution_globals.update(self.inner.__globals__)
        
        # Add the conflicting variables to globals
        for var in conflicting_vars:
            if var in assignments:
                execution_globals[var] = assignments[var]
        
        # Execute setup once
        if self.setup_code and self.setup_code != 'pass':
            exec(self.setup_code, execution_globals)
            
        # Execute the modified statement multiple times for warmup
        for _ in range(number):
            try:
                exec(modified_stmt, execution_globals)
            except Exception:
                # If execution fails, we'll let the main benchmark handle the error
                break