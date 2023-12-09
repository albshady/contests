import functools
import pathlib
import time
import typing

import iters


PS = typing.ParamSpec('PS')
T = typing.TypeVar('T')


@iters.wrap_iter
def read_lines(filepath: pathlib.Path) -> typing.Iterable[str]:
    with open(filepath) as file:
        for line in file:
            yield line


def time_it(func: typing.Callable[PS, T]) -> typing.Callable[PS, T]:
    @functools.wraps(func)
    def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> T:
        start = time.time()
        result = func(*args, **kwargs)
        total = time.time() - start
        print(f"{func.__name__} took {total:.2f} seconds")
        return result

    return wrapper


def print_decorator(func: typing.Callable[PS, T]) -> typing.Callable[PS, T]:
    @functools.wraps(func)
    def wrapper(*args: PS.args, **kwargs: PS.kwargs) -> T:
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args}, {kwargs}) -> {result}")
        return result

    return wrapper


def print_with_context(context):
    return functools.partial(print_identity, context=context)


def print_identity(x, context=None):
    if context is None:
        print(x)
    else:
        print(context, x)
    return x
