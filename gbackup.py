#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from typing import List
from constants import LOGGER, HELP_MESSAGE, DEFAULT_ARGS
from gbackup_types import GBackupArgs


def help():
    return HELP_MESSAGE


def read_args(args: List[str]) -> GBackupArgs:
    validated_args: GBackupArgs = DEFAULT_ARGS

    # Checks that correct number of arguments were passed
    if len(args) == 0:
        return validated_args
    elif (len(args) == 1) and ((args[0] == "--help") or (args[0] == "-h")):
        print(help())
        sys.exit(0)
    elif (len(args) % 2 == 1) or (len(args) > 4):
        if ("--help" in args) or ("-h" in args):
            print(help())
            sys.exit(0)
        err_msg: str = f"Invalid number of arguments: Recieved {len(args)}."
        raise ValueError(f"{err_msg}\n{help()}")

    # Checks that correct values were passed for arguments
    while len(args) > 0:
        option: str = args.pop(0).lstrip("--")
        if option in validated_args.keys():
            arg: str = args.pop(0)
            validated_args[option] = arg
        elif (option == "--help") or (option == "-h"):
            print(help())
            sys.exit(0)
        else:
            err_msg = f"Invalid option: '{option}' is not a valid option."
            raise ValueError(f"{err_msg}\n{help()}")

    return validated_args


def create_backup(args: GBackupArgs) -> str:
    LOGGER.info(f"Starting backup of {args['src']}...")

    LOGGER.info(f"Navigating to {args['src']}...")
    os.chdir(os.path.dirname(args["src"]))

    curr_time: str = time.strftime("%Y-%m-%d-%H%M", time.gmtime())
    LOGGER.info(f"Current time: {curr_time}")

    backup_name: str = f"{curr_time}-backup.tar.gz"
    backup_path: str = f"{args['dest']}/{backup_name}"
    LOGGER.info(f"Creating compressed archive '{backup_path}'...")
    # TODO: Find out why `--exclude-from` not working
    tar = subprocess.run(
        [
            "tar",
            "-czvf",
            backup_path,
            f"--exclude-from={args['ignore']}",
            "."
        ],
        shell=False,
        capture_output=True
    )

    LOGGER.info(tar.stdout)
    if (tar.returncode != 0):
        raise ChildProcessError(tar.stderr)

    return backup_path


def main():
    try:
        args: GBackupArgs = read_args(sys.argv[1:])
        backup_path: str = create_backup(args)
    except Exception as e:
        LOGGER.error(e)
        raise e


if __name__ == "__main__":
    main()
