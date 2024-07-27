import getpass
import os
import sys
from logging import Logger, StreamHandler, Formatter, INFO

LOGGER: Logger = Logger("gbackup")
LOGGER.setLevel(INFO)
HANDLER = StreamHandler(sys.stdout)
HANDLER.setLevel(INFO)
FORMATTER = Formatter(
    "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

def get_username() -> str:
    try:
        username: str = os.environ["SUDO_USER"]
    except KeyError:
        try:
            username = os.getlogin()
        except OSError:
            username = getpass.getuser()

    return username
            

USERNAME: str = get_username()
HOME_DIR: str = f"/home/{USERNAME}"
DEFAULT_BACKUP_DIR: str = f"{HOME_DIR}/Documents/Backups"

BACKUP_FILE_EXTENSION: str = "gbackup.tar.gz"
IGNORE_FILE_NAME: str = ".gbackignore"

HELP_MESSAGE: str = \
"""
Usage: ./gbackup.py [--src_dir SOURCE_DIRECTORY] [--ignore_file IGNORE_FILE] [--dest_dir DESTINATION_DIRECTORY] [--key_file GPG_KEY_FILE] [--help/-h]

Creates a backup of a specified directory. 
Certain files can be excluded from the directory by adding a `.gbackignore` file to the directory being backed up. This `.gbackignore` file should list names or wildcard patterns for the files and directories to exclude, following tar's `--exclude-from` syntax.

Options:
	--src_dir       Path to directory being backed up. Default value is current user's home directory.

	--dest_dir      Path to directory where backup will be created. Default value is current user's `Documents/Backups` directory.

    --key_file      Path to file containing GPG key to encrypt backup. No encryption if not provided.

	--help/-h       Prints this help message.

Examples:
    # Backing up home directory
    ./gbackup.py --src_dir $HOME --dest_dir $HOME/Documents/Backup --key_file $HOME/key.gpg

    # In light of defaults, the following also works
    ./gbackup.py --key_file $HOME/key.gpg

    # Backing up a different directory
    ./gbackup.py --src_dir $HOME/Documents
"""
