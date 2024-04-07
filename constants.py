import os
import sys
import logging

LOGGER = logging.getLogger("gbackup.py")
LOGGER.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

# Home directory of current user
HOMEDIR = f"/home/{os.getlogin()}"
# File listing other files to be excluded from backup
IGNORE = f"{HOMEDIR}/.gbackignore"
# Directory where backups will be created
BACKUPDIR = f"{HOMEDIR}/Documents/Backups"
