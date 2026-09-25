import dataclasses
import functools
import inspect
from collections.abc import Callable
from time import monotonic_ns


def timethis(name_or_function: str | Callable | None = None, log_callback: Callable = print):
    def _get_name(obj):
        if inspect.ismethod(obj):
            return f"{obj.__class__.__name__}::{obj.__name__}"
        return obj.__name__

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            callsite = get_callsite()
            start = monotonic_ns()
            results = func(*args, **kwargs)
            delta = Timedelta(monotonic_ns(), start)
            name = name_or_function
            log_callback(f"{_get_name(func) if name is None else name} @ {callsite} took {delta}.")
            return results 
        return wrapper

    if callable(name_or_function):
        decorated = name_or_function
        name_or_function = None
        return decorator(decorated)
    
    return decorator


class Timedelta:
    MICROSECONDS_DIV = 1_000
    MILLISECONDS_DIV = 1_000_000
    SECONDS_DIV = 1_000_000_000

    def __init__(self, end_ns: int, start_ns: int):
        self.end = end_ns
        self.start = start_ns
        assert end_ns >= start_ns, (end_ns, start_ns)
        self.delta = end_ns - start_ns

    def __repr__(self):
        formatted = None
        if self.delta > self.SECONDS_DIV:
            formatted = f"{self.delta / self.SECONDS_DIV} s"
        elif self.delta > self.MILLISECONDS_DIV:
            formatted = f"{self.delta / self.MILLISECONDS_DIV} ms"
        elif self.delta > self.MICROSECONDS_DIV:
            formatted = f"{self.delta / self.MICROSECONDS_DIV} us"
        else:
            formatted = f"{self.delta}"
        
        assert formatted is not None

        return formatted


@dataclasses.dataclass(repr=False)
class Location:
    filename: str
    line: int

    def __repr__(self) -> str:
        return f"{self.filename}:{self.line}"


def get_callsite() -> Location:
    callstack = inspect.stack()
    line_number = callstack[2].lineno
    filename = callstack[2].filename
    return Location(filename, line_number)