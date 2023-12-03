import pathlib
import typing

import iter_model


@iter_model.sync_iter
def read_lines(filepath: pathlib.Path) -> typing.Iterable[str]:
    with open(filepath) as file:
        for line in file:
            yield line
