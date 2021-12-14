import typing

from rich import print

from . import _base


class Fold(typing.NamedTuple):
    axis: str
    at: int


class Dot(typing.NamedTuple):
    x: int
    y: int


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'folds.txt'

    def __init__(self) -> None:
        super().__init__()

        inp = list(self._input)
        self.folds = [fold for fold in inp if isinstance(fold, Fold)]
        self.dots = {dot for dot in inp if isinstance(dot, Dot)}

        self.x = max(self.dots, key=lambda d: d.x).x + 1
        self.y = max(self.dots, key=lambda d: d.y).y + 1

    @property
    def dots_number(self) -> int:
        return len(self.dots)

    @property
    def rich(self) -> str:
        paper = [["." for _ in range(self.x)] for _ in range(self.y)]
        for dot in self.dots:
            paper[dot.y][dot.x] = "[bold][blue]#[/blue][/bold]"
        return "\n".join(("".join(line) for line in paper))

    @staticmethod
    def _preprocess_line(line: str) -> Dot | Fold | None:
        if not line:
            return None

        if line.startswith('fold along'):
            fold = line.split()[-1]
            axis, _, at = fold.partition('=')
            return Fold(axis=axis, at=int(at))

        x, _, y = line.partition(',')
        return Dot(x=int(x), y=int(y))

    def solve1(self) -> int:
        self.fold_once(fold=self.folds[0])
        return self.dots_number

    def solve2(self) -> int:
        for fold in self.folds:
            self.fold_once(fold=fold)
        print(self.rich)
        return self.dots_number

    def fold_once(self, fold: Fold) -> None:
        match fold.axis:
            case 'x':
                self.dots = self.fold_x(dots=self.dots, at=fold.at)
                self.x = fold.at
            case 'y':
                self.dots = self.fold_y(dots=self.dots, at=fold.at)
                self.y = fold.at
            case other:
                raise ValueError(f"Unknown direction {other}")

    @staticmethod
    def fold_y(dots: set[Dot], at: int) -> set[Dot]:
        new_dots = set()

        for dot in dots:
            if dot.y < at:
                new_dots.add(dot)
            if dot.y > at:
                new_dots.add(Dot(x=dot.x, y=2 * at - dot.y))

        return new_dots

    @staticmethod
    def fold_x(dots: set[Dot], at: int) -> set[Dot]:
        new_dots = set()

        for dot in dots:
            if dot.x < at:
                new_dots.add(dot)
            if dot.x > at:
                new_dots.add(Dot(x=2 * at - dot.x, y=dot.y))

        return new_dots
