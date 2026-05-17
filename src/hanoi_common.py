from __future__ import annotations

from dataclasses import dataclass, field


TOWER_NAMES = ("Source", "Helper", "Target")


@dataclass
class HanoiStep:
    mode: str
    move_number: int
    total_moves: int
    towers: list[list[int]]
    phase: str
    headline: str
    detail: str
    from_tower: int | None = None
    to_tower: int | None = None
    subproblem: str = ""
    path: tuple[str, ...] = field(default_factory=tuple)
    loop_rule: str = ""


def build_towers(disks: int) -> list[list[int]]:
    return [list(range(disks, 0, -1)), [], []]


def copy_towers(towers: list[list[int]]) -> list[list[int]]:
    return [tower[:] for tower in towers]


def optimal_move_count(disks: int) -> int:
    return 2**disks - 1


def tower_name(index: int) -> str:
    return TOWER_NAMES[index]


def disk_count_text(disks: int) -> str:
    return f"{disks} disk" if disks == 1 else f"{disks} disks"


def describe_recursive_subproblem(
    disks: int, source: int, target: int, helper: int
) -> str:
    return (
        f"Move {disk_count_text(disks)} from {tower_name(source)} "
        f"to {tower_name(target)} using {tower_name(helper)}."
    )
