import argparse
import importlib


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'day', help='Day number', choices=[str(d) for d in range(1, 26)]
    )
    parser.add_argument('task', help='Task number', choices=('1', '2'))
    args = parser.parse_args()

    day = int(args.day)
    task = int(args.task)

    Solver = importlib.import_module(f'aoc.days.day{day}').Solver
    solver = Solver()
    solution = solver.solve(task=task)

    print(f"{solution=} | {day=} | {task=}")
