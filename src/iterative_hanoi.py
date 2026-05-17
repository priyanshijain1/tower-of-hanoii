from __future__ import annotations

from collections.abc import Iterator

from .hanoi_common import HanoiStep, build_towers, copy_towers, optimal_move_count, tower_name


def make_legal_move(towers: list[list[int]], left: int, right: int) -> tuple[int, int, int]:
    if not towers[left]:
        disk = towers[right].pop()
        towers[left].append(disk)
        return disk, right, left

    if not towers[right]:
        disk = towers[left].pop()
        towers[right].append(disk)
        return disk, left, right

    if towers[left][-1] < towers[right][-1]:
        disk = towers[left].pop()
        towers[right].append(disk)
        return disk, left, right

    disk = towers[right].pop()
    towers[left].append(disk)
    return disk, right, left


def generate_iterative_steps(disks: int) -> Iterator[HanoiStep]:
    towers = build_towers(disks)
    total_moves = optimal_move_count(disks)

    if disks % 2 == 1:
        pair_order = [(0, 2), (0, 1), (1, 2)]
    else:
        pair_order = [(0, 1), (0, 2), (1, 2)]

    first_left, first_right = pair_order[0]

    yield HanoiStep(
        mode="iterative",
        move_number=0,
        total_moves=total_moves,
        towers=copy_towers(towers),
        phase="Start",
        headline="Start the fixed 3-step loop.",
        detail=(
            "Iteration does not call itself. It repeats a small rule until the tower is solved."
        ),
        loop_rule=(
            f"First compare {tower_name(first_left)} and {tower_name(first_right)}. "
            "Then keep repeating the same 3 pair checks."
        ),
    )

    for move_number in range(1, total_moves + 1):
        left, right = pair_order[(move_number - 1) % 3]
        cycle_slot = ((move_number - 1) % 3) + 1

        disk, from_tower, to_tower = make_legal_move(towers, left, right)

        yield HanoiStep(
            mode="iterative",
            move_number=move_number,
            total_moves=total_moves,
            towers=copy_towers(towers),
            phase="Loop step",
            headline=f"Apply loop rule {cycle_slot} of 3.",
            detail=(
                f"Look at {tower_name(left)} and {tower_name(right)}, "
                "then make the only legal move."
            ),
            from_tower=from_tower,
            to_tower=to_tower,
            loop_rule=(
                f"Cycle {cycle_slot}/3: compare {tower_name(left)} and {tower_name(right)}. "
                f"Disk {disk} is the legal move."
            ),
        )
