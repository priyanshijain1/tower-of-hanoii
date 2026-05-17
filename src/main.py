import argparse

from .cli_display import play_demo
from .iterative_hanoi import generate_iterative_steps
from .recursive_hanoi import generate_recursive_steps


def parse_args():
    parser = argparse.ArgumentParser(
        description="Visual Tower of Hanoi demo with recursive and iterative modes."
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["recursive", "iterative"],
        default="recursive",
        help="which solving style to animate (default: recursive)",
    )
    parser.add_argument(
        "disks",
        nargs="?",
        type=int,
        default=4,
        help="number of disks to animate (default: 4)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2,
        help="seconds to pause between frames (default: 2)",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="show a short explanation after the animation",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.disks < 1 or args.disks > 8:
        raise SystemExit("Please choose a disk count between 1 and 8.")

    if args.mode == "recursive":
        steps = generate_recursive_steps(args.disks)
    else:
        steps = generate_iterative_steps(args.disks)

    play_demo(steps, delay=args.delay, explain=args.explain)


if __name__ == "__main__":
    main()
