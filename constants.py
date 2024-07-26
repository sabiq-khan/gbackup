import os
import sys
from logging import Logger, StreamHandler, Formatter, INFO
from typing import Dict
from gbackup_types import GBackupArgs

LOGGER: Logger = Logger("gbackup")
LOGGER.setLevel(INFO)
HANDLER = StreamHandler(sys.stdout)
HANDLER.setLevel(INFO)
FORMATTER = Formatter(
    "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

# Home directory of current user
HOMEDIR: str = f"/home/{os.getlogin()}"
# File listing other files to be excluded from backup
HOMEDIR_IGNORE: str = f"{HOMEDIR}/.gbackignore"
# Directory where backups will be created
BACKUPDIR: str = f"{HOMEDIR}/Documents/Backups"

DEFAULT_ARGS: GBackupArgs = GBackupArgs(
    src_dir=HOMEDIR,
    ignore_file=HOMEDIR_IGNORE,
    dest_dir=BACKUPDIR,
    key_file=None
)

HELP_MESSAGE: str = \
"""
Usage: ./gbackup.py [--src_dir SOURCE_DIRECTORY] [--ignore_file IGNORE_FILE] [--dest_dir DESTINATION_DIRECTORY] [--key_file GPG_KEY_FILE] [--help/-h]

Creates a backup of a specified directory.

Options:
	--src_dir       Path to directory being backed up.

    --ignore_file   Path to file containing file/directory names to exclude from backup.

	--dest_dir      Path to directory where the backup will be created.

    --key_file      Path to file containing GPG key to encrypt backup, no encryption if not provided.

	--help/-h       Prints this help message.

Example:
    # Backing up home directory
    ./gbackup --src_dir $HOME --ignore_file $HOME/.gbackignore --dest_dir $HOME/Documents/Backup
"""
