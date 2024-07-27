#!/usr/bin/env python3
from dataclasses import dataclass
import os
import sys
import time
import subprocess
from subprocess import CompletedProcess
from typing import Dict, List, Optional, Union
from constants import BACKUP_FILE_EXTENSION, DEFAULT_BACKUP_DIR, HOME_DIR, HELP_MESSAGE, IGNORE_FILE_NAME, USERNAME
from logging import Logger


@dataclass
class GBackupArgs():
    """
    Arguments:
    src_dir - Absolute path to the directory being backed up
    dest_dir - Absolute path to the directory that the backup will be written to
    key_file - Absolute path to the file containing GPG key used to encrypt backup
    """
    src_dir: str = HOME_DIR
    dest_dir: str = DEFAULT_BACKUP_DIR
    key_file: Optional[str] = None

    def __contains__(self, property: str) -> bool:
        """Checks if dataclass instance contains property"""
        return property in self.__dict__
    
    def to_dict(self) -> Dict[str, Union[str, Optional[str]]]:
        """Returns inner Dict of properties"""
        return self.__dict__


class GBackup:
    def __init__(self, logger: Logger):
        self.logger: Logger = logger

    @classmethod
    def read_args(cls, args: List[str]) -> GBackupArgs:
        validated_args: GBackupArgs = GBackupArgs()

        # Validating number of arguments
        if len(args) == 0:
            return validated_args
        elif (len(args) == 1) and ((args[0] == "--help") or (args[0] == "-h")):
            print(HELP_MESSAGE)
            sys.exit(0)
        elif (len(args) % 2 == 1) or (len(args) > 4):
            if ("--help" in args) or ("-h" in args):
                print(HELP_MESSAGE)
                sys.exit(0)
            err_msg: str = f"Invalid number of arguments: Recieved {len(args)}."
            raise ValueError(f"{err_msg}\n{help()}")

        # Validating argument names and values
        while len(args) > 0:
            option: str = args.pop(0).lstrip("--")
            if (option == "--help") or (option == "-h"):
                print(HELP_MESSAGE)
                sys.exit(0)
            elif option in validated_args:
                arg: str = args.pop(0)
                setattr(validated_args, option, arg)
            else:
                err_msg = f"Invalid option: '{option}' is not a valid option."
                raise ValueError(f"{err_msg}\n{help()}")

        return validated_args

    def _create_backup(self, args: GBackupArgs) -> str:
        self.logger.info(f"Starting backup of {args.src_dir}...")
        self.logger.info(f"Current user: {USERNAME}")
        self.logger.info(f"Current working directory: {os.getcwd()}")

        curr_time: str = time.strftime("%Y-%m-%d-%H%M", time.gmtime())
        self.logger.info(f"Current time: {curr_time}")
        backup_name: str = f"{curr_time}-{BACKUP_FILE_EXTENSION}"
        backup_path: str = f"{args.dest_dir}/{backup_name}"

        self.logger.info(f"Creating compressed archive '{backup_path}'...")
        tar_args: List[str] = [
            "tar",
            "-czf",
            backup_path,
            f"--exclude={os.path.relpath(args.dest_dir, args.src_dir)}",
            args.src_dir
        ]
        ignorefile_path: str = f"{args.src_dir}/{IGNORE_FILE_NAME}"
        if os.path.exists(ignorefile_path):
            tar_args.insert(-1, f"--exclude-from={ignorefile_path}")
            self.logger.info(f"Found .gbackignore at '{ignorefile_path}'.")

        self.logger.info(f"Running tar with the following options: {' '.join(tar_args)}")
        tar: CompletedProcess = subprocess.run(
            tar_args,
            shell=False,
            capture_output=True
        )

        self.logger.info(tar.stdout)
        if (tar.returncode != 0):
            raise ChildProcessError(tar.stderr)
        self.logger.info(f"Tar complete!")
        self.logger.info(f"Compressed archive created at '{backup_path}'!")

        return backup_path

    def _encrypt_backup(self, backup_path: str, key_file: str) -> str:
        self.logger.info(f"Current working directory: {os.getcwd()}")

        encrypted_backup_path: str = f"{backup_path}.gpg"
        self.logger.info(f"Encrypting compressed archive at '{encrypted_backup_path}'...")

        gpg_args: List[str] = [
            "gpg",
            "--batch",
            "--passphrase-file",
            key_file,
            "-c",
            backup_path
        ]
        self.logger.info(f"Running gpg with the following arguments: {' '.join(gpg_args)}")
        gpg: CompletedProcess = subprocess.run(
            gpg_args,
            shell=False,
            capture_output=True
        )

        self.logger.info(gpg.stdout)
        if (gpg.returncode != 0):
            raise ChildProcessError(gpg.stderr)
        
        self.logger.info("GPG complete!")
        self.logger.info(f"Encrypted archive created at '{encrypted_backup_path}'!")

        encrypted_backup_path: str = f"{backup_path}.gpg"
        return encrypted_backup_path

    def __call__(self, args: GBackupArgs = GBackupArgs()):
        self.logger.info(f"Received the following arguments: {args.to_dict()}")
        backup_path: str = self._create_backup(args)
        encrypted_backup_path: Optional[str] = None
        if args.key_file is not None:
            key_file: str = args.key_file
            encrypted_backup_path = self._encrypt_backup(backup_path, key_file)
        
        self.logger.info(f"Backup created at '{encrypted_backup_path or backup_path}'.")
