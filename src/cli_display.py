from __future__ import annotations

import os
import sys
import time

from .hanoi_common import HanoiStep, TOWER_NAMES


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def type_line(text: str, char_delay: float = 0.018, pause_after: float = 0.28):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(char_delay)
    sys.stdout.write("\n")
    sys.stdout.flush()
    time.sleep(pause_after)


def pause(delay: float, minimum: float = 0.2):
    time.sleep(max(delay, minimum))


def format_disk(size: int, max_disk: int) -> str:
    slot_width = max(13, max_disk * 2 + 5)

    if size == 0:
        return "|".center(slot_width)

    fill = "=" * (size * 2 - 1)
    middle = len(fill) // 2
    fill = fill[:middle] + str(size) + fill[middle + 1 :]
    return f"[{fill}]".center(slot_width)


def format_marker(index: int, from_tower: int | None, to_tower: int | None, width: int) -> str:
    if index == from_tower:
        return "from".center(width)
    if index == to_tower:
        return "to".center(width)
    return " ".center(width)


def format_label(index: int, from_tower: int | None, to_tower: int | None, width: int) -> str:
    name = TOWER_NAMES[index]
    if index == from_tower or index == to_tower:
        return f"< {name} >".center(width)
    return name.center(width)


def render_board(step: HanoiStep):
    max_disk = max(
        sum((tower for tower in step.towers), []),
        default=0,
    )
    slot_width = max(13, max_disk * 2 + 5)
    gap = "   "

    for row_index in range(max_disk - 1, -1, -1):
        row = []
        for tower in step.towers:
            size = tower[row_index] if row_index < len(tower) else 0
            row.append(format_disk(size, max_disk))
        print(gap.join(row))

    print(gap.join(format_marker(i, step.from_tower, step.to_tower, slot_width) for i in range(3)))
    print(gap.join(("_" * slot_width) for _ in range(3)))
    print(gap.join(format_label(i, step.from_tower, step.to_tower, slot_width) for i in range(3)))


def render_recursive_context(step: HanoiStep):
    print(f"Subproblem: {step.subproblem}")
    print("Recursive call stack:")
    last_index = len(step.path) - 1

    for depth, item in enumerate(step.path):
        indent = "  " * depth
        branch = "-> "
        marker = "   [current]" if depth == last_index else ""
        print(f"{indent}{branch}{item}{marker}")

    if len(step.path) > 1:
        print(f"Parent frame : {step.path[-2]}")
    print(f"Current frame: {step.path[-1]}")


def render_iterative_context(step: HanoiStep):
    print(f"Loop rule: {step.loop_rule}")


def render_step(step: HanoiStep):
    clear_screen()
    print("=" * 72)
    print(f"Tower of Hanoi | {step.mode.title()} | Move {step.move_number}/{step.total_moves}")
    print(f"Phase : {step.phase}")
    print(f"Focus : {step.headline}")
    print(f"Why   : {step.detail}")

    if step.mode == "recursive":
        render_recursive_context(step)
    else:
        render_iterative_context(step)

    print("-" * 72)
    render_board(step)


def explain_recursive():
    print()
    type_line("What you just saw:")
    type_line("The problem kept turning into a smaller copy of itself.")
    type_line("The stack was moved aside, one bigger disk moved, and the stack was rebuilt.")
    print()
    type_line("That is recursion.")
    type_line("The same idea solves the full tower and every smaller tower inside it.")


def explain_iterative():
    print()
    type_line("What you just saw:")
    type_line("The solver did not call itself.")
    type_line("It kept repeating a fixed loop of legal moves.")
    print()
    type_line("That is iteration.")
    type_line("The tower is solved by following a steady rule step by step.")


def play_demo(steps, delay: float, explain: bool):
    last_step = None

    for step in steps:
        render_step(step)
        pause(delay)
        last_step = step

    if last_step is None:
        return

    print()
    print(f"Completed in {last_step.move_number} moves.")
    print(f"Minimum possible moves: {last_step.total_moves}")

    if explain:
        if last_step.mode == "recursive":
            explain_recursive()
        else:
            explain_iterative()
