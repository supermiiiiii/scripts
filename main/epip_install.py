"""
Installs provided python packages if they do not already exist.
"""

import argparse
import os
from shutil import which
from subprocess import Popen
import sys
from typing import NamedTuple, Sequence


Arguments = NamedTuple(
    "Arguments",
    [("python_packages", Sequence[str]), ("python_versions", Sequence[float])],
)


def install_pypacks(pypacks: Sequence[str], pyver: float) -> None:
    python = f"python{pyver}"

    all_pypacks = ["pip"]
    all_pypacks.extend(pypacks)
    for pypack in all_pypacks:
        print(f"----- Upgrading {pypack}...")

        if pypack.startswith("/"):
            os.chdir(pypack)
            os.system("rm -rf *.egg-info")
            pip_args = ["-e", "."]
        else:
            pip_args = [pypack]

        pip_cmd_list = [python, "-m", "pip", "install", "--user", "-U"]
        pip_cmd_list.extend(pip_args)
        ps = Popen(pip_cmd_list)
        ps.communicate()


def python_version_exists(pyver: float) -> bool:
    if which(f"python{pyver}") is None:
        return False
    return True


def parse_cli_args(argv: Sequence[str]) -> Arguments:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-v",
        action="append",
        dest="python_versions",
        metavar="MAJOR.MINOR",
        type=float,
        help=(
            "A valid python version number (e.g. 2.7, 3.6, 3.7, etc....). This"
            " option can be provided more than once."
        ),
    )
    parser.add_argument(
        "python_packages",
        metavar="PYPACK",
        nargs="+",
        type=str,
        help="Python packages to install (if not already installed).",
    )

    args = parser.parse_args(argv[1:])

    if args.python_versions is None:
        parser.error(
            "At least one python version number must be provided (using the -v"
            " option)."
        )

    return Arguments(**dict(args._get_kwargs()))


def main(argv: Sequence[str] = None) -> int:
    if argv is None:
        argv = sys.argv

    args = parse_cli_args(argv)

    is_first_pyver = True
    for pyver in args.python_versions:
        if not python_version_exists(pyver):
            raise SystemExit(f"[ERROR]: python{pyver} is not installed.")

        if is_first_pyver:
            is_first_pyver = False
        else:
            print()

        print(f"===== Python {pyver} =====")
        install_pypacks(args.python_packages, pyver)

    return 0


if __name__ == "__main__":
    sys.exit(main())
