from __future__ import annotations

from collections.abc import Iterator

from hanoi_common import (
    HanoiStep,
    copy_towers,
    build_towers,
    describe_recursive_subproblem,
    disk_count_text,
    optimal_move_count,
    tower_name,
)


def describe_path_step(disks: int, source: int, target: int) -> str:
    return f"solve {disk_count_text(disks)}: {tower_name(source)} -> {tower_name(target)}"


def generate_recursive_steps(disks: int) -> Iterator[HanoiStep]:
    towers = build_towers(disks)
    total_moves = optimal_move_count(disks)
    move_number = 0

    yield HanoiStep(
        mode="recursive",
        move_number=0,
        total_moves=total_moves,
        towers=copy_towers(towers),
        phase="Start",
        headline="Start with the full tower.",
        detail="Recursion keeps shrinking the problem until only one disk is left.",
        subproblem=describe_recursive_subproblem(disks, 0, 2, 1),
        path=(describe_path_step(disks, 0, 2),),
    )

    def solve(
        n: int,
        source: int,
        target: int,
        helper: int,
        path: tuple[str, ...],
    ) -> Iterator[HanoiStep]:
        nonlocal move_number

        current_path = path + (describe_path_step(n, source, target),)
        subproblem = describe_recursive_subproblem(n, source, target, helper)

        if n > 1:
            yield HanoiStep(
                mode="recursive",
                move_number=move_number,
                total_moves=total_moves,
                towers=copy_towers(towers),
                phase="Break down",
                headline=f"First move the smaller stack of {disk_count_text(n - 1)}.",
                detail=(
                    f"To move {disk_count_text(n)}, we first move the top "
                    f"{disk_count_text(n - 1)} to {tower_name(helper)}."
                ),
                subproblem=subproblem,
                path=current_path,
            )

        if n == 1:
            disk = towers[source].pop()
            towers[target].append(disk)
            move_number += 1

            yield HanoiStep(
                mode="recursive",
                move_number=move_number,
                total_moves=total_moves,
                towers=copy_towers(towers),
                phase="Base case",
                headline=f"Move disk {disk} directly.",
                detail="Only one disk is left, so no smaller subproblem is needed.",
                from_tower=source,
                to_tower=target,
                subproblem=subproblem,
                path=current_path,
            )
            return

        yield from solve(n - 1, source, helper, target, current_path)

        yield HanoiStep(
            mode="recursive",
            move_number=move_number,
            total_moves=total_moves,
            towers=copy_towers(towers),
            phase="Return",
            headline=f"Come back to the {disk_count_text(n)} problem.",
            detail=f"The smaller stack is out of the way, so disk {n} can move now.",
            subproblem=subproblem,
            path=current_path,
        )

        disk = towers[source].pop()
        towers[target].append(disk)
        move_number += 1

        yield HanoiStep(
            mode="recursive",
            move_number=move_number,
            total_moves=total_moves,
            towers=copy_towers(towers),
            phase="Move largest",
            headline=f"Move disk {disk}.",
            detail="This is the largest disk in the current subproblem.",
            from_tower=source,
            to_tower=target,
            subproblem=subproblem,
            path=current_path,
        )

        yield HanoiStep(
            mode="recursive",
            move_number=move_number,
            total_moves=total_moves,
            towers=copy_towers(towers),
            phase="Rebuild",
            headline=f"Place the smaller {disk_count_text(n - 1)} back on top.",
            detail=(
                f"Now solve the {disk_count_text(n - 1)} problem again to rebuild the tower."
            ),
            subproblem=subproblem,
            path=current_path,
        )

        yield from solve(n - 1, helper, target, source, current_path)

    yield from solve(disks, 0, 2, 1, ())
