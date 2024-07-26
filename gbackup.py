#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from subprocess import CompletedProcess
from typing import List
from constants import LOGGER, HELP_MESSAGE, DEFAULT_ARGS
from gbackup_types import GBackupArgs


def help() -> str:
    return HELP_MESSAGE


def read_args(args: List[str]) -> GBackupArgs:
    validated_args: GBackupArgs = DEFAULT_ARGS

    LOGGER.info("Validating number of arguments...")
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
    LOGGER.info("Number of arguments valid!")

    LOGGER.info("Validating arguments...")
    while len(args) > 0:
        option: str = args.pop(0).lstrip("--")
        if (option == "--help") or (option == "-h"):
            print(help())
            sys.exit(0)
        elif option in validated_args:
            arg: str = args.pop(0)
            setattr(validated_args, option, arg)
        else:
            err_msg = f"Invalid option: '{option}' is not a valid option."
            raise ValueError(f"{err_msg}\n{help()}")
    LOGGER.info(f"Arguments valid! Found the following arguments: {validated_args.to_dict()}")

    return validated_args


def create_backup(args: GBackupArgs) -> str:
    LOGGER.info(f"Starting backup of {args.src_dir}...")

    LOGGER.info(f"Navigating to {args.src_dir}...")
    os.chdir(os.path.dirname(args.src_dir))

    curr_time: str = time.strftime("%Y-%m-%d-%H%M", time.gmtime())
    LOGGER.info(f"Current time: {curr_time}")

    backup_name: str = f"{curr_time}-backup.tar.gz"
    backup_path: str = f"{args.dest_dir}/{backup_name}"
    LOGGER.info(f"Creating compressed archive '{backup_path}'...")
    tar: CompletedProcess = subprocess.run(
        [
            "tar",
            "-czf",
            backup_path,
            f"--exclude-from={args.ignore_file}",
            "."
        ],
        shell=False,
        capture_output=True
    )

    LOGGER.info(tar.stdout)
    if (tar.returncode != 0):
        raise ChildProcessError(tar.stderr)
    
    LOGGER.info(f"Compressed archive created at '{backup_path}'!")

    return backup_path


def encrypt_backup(backup_path: str, key_file: str) -> str:
    encrypted_backup_path: str = f"{backup_path}.gpg"
    LOGGER.info(f"Encrypting compressed archive at '{encrypted_backup_path}'...")
    gpg: CompletedProcess = subprocess.run(
        [
            "gpg",
            "--batch",
            "--passphrase-file",
            key_file,
            "-c",
            backup_path
        ],
        shell=False,
        capture_output=True
    )

    LOGGER.info(gpg.stdout)
    if (gpg.returncode != 0):
        raise ChildProcessError(gpg.stderr)
    
    LOGGER.info(f"Encrypted archive created at '{encrypted_backup_path}'!")

    encrypted_backup_path: str = f"{backup_path}.gpg"
    return encrypted_backup_path


def main():
    try:
        args: GBackupArgs = read_args(sys.argv[1:])
        backup_path: str = create_backup(args)
        if args.key_file is not None:
            # TODO: Troubleshoot key file argument
            key_file: str = args.key_file
            encrypted_backup_path: str = encrypt_backup(backup_path, key_file)
        
        LOGGER.info(f"Backup created at '{backup_path or encrypted_backup_path}'.")

    except Exception as e:
        LOGGER.error(e)
        raise e


if __name__ == "__main__":
    main()
