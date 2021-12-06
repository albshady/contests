import dataclasses

from rich import print

from . import _base


BOARD_SIZE = 5


@dataclasses.dataclass
class Cell:
    value: int
    marked: bool = False

    @property
    def rich(self) -> str:
        color = 'green' if self.marked else 'red'
        return f'[{color}]{self.value}[/{color}]'


@dataclasses.dataclass
class Board:
    field: list[list[Cell]]
    solved: bool = False

    @property
    def score(self) -> int:
        score = 0
        for row in self.field:
            for cell in row:
                if not cell.marked:
                    score += cell.value
        return score

    def mark(self, /, number: int) -> None:
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                if cell.value != number:
                    continue

                cell.marked = True
                if any((self._is_row_solved(y=y), self._is_column_solved(x=x))):
                    self.solved = True

    def _is_row_solved(self, /, y: int) -> bool:
        return all(cell.marked for cell in self.field[y])

    def _is_column_solved(self, /, x: int) -> bool:
        return all(row[x].marked for row in self.field)

    @property
    def rich(self) -> str:
        rows = []
        for row in self.field:
            rows.append('\t'.join(cell.rich for cell in row))
        return '\n'.join(rows)


class Solver(_base.BaseSolver):
    _INPUT_FILENAME = 'bingo.txt'
    _numbers: list[int]

    def __init__(self) -> None:
        super().__init__()
        self._boards: list[Board] = []
        self._solved_boards_count: int = 0

    def _setup_boards(self) -> None:
        field = []

        for i, line in enumerate(self._input):
            if i == 0:
                self._numbers = [int(n) for n in line.strip().split(',')]
                continue

            if not line:
                continue

            field.append([Cell(value=int(n)) for n in line.strip().split()])

            if len(field) == BOARD_SIZE:
                self._boards.append(Board(field=field))
                field = []

    def solve1(self) -> int:
        self._setup_boards()

        for incoming_number in self._numbers:
            for board in self._boards:
                board.mark(number=incoming_number)
                if board.solved:
                    print(board.rich)
                    return board.score * incoming_number

        raise ValueError("No board is solved!")

    def solve2(self) -> int:
        self._setup_boards()
        print("total boards:", len(self._boards))

        for incoming_number in self._numbers:
            for board in self._boards:
                if board.solved:
                    continue

                board.mark(number=incoming_number)
                if board.solved:
                    print(f"Board is solved by {incoming_number}")
                    print(board.rich)
                    self._solved_boards_count += 1

                if self._all_boards_solved:
                    print(f"Last board is solved by {incoming_number}")
                    print(board.rich)
                    return board.score * incoming_number

        raise ValueError("Last board is still unsolved!")

    @property
    def _all_boards_solved(self) -> bool:
        return len(self._boards) == self._solved_boards_count
