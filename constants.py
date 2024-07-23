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
    src=HOMEDIR,
    ignore=HOMEDIR_IGNORE,
    dest=BACKUPDIR
)

HELP_MESSAGE: str = \
"""
Usage: ./gbackup.py [--src SOURCE_DIRECTORY] [--ignore IGNORE_FILE] [--dest DESTINATION_DIRECTORY] [--help/-h]

Creates a backup of a specified directory.

Options:
	--src           String representing the path to the directory being backed up.

    --ignore        String representing the name of a file containing file/directory names to exclude from backup.

	--dest          String representing the path of the directory where the backup will be created.

	--help/-h       Prints this help message.

Examples:
    # Backing up home directory
    ./gbackup --src $HOME --ignore $HOME/.gbackignore --dest $HOME/Documents/Backup
"""
