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

# Name of file that lists other files to be excluded from backup
IGNORE = ".gbackignore"
