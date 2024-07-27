#!/usr/bin/env python3
import sys
from gbackup import GBackup, GBackupArgs
from constants import LOGGER

def main():
    try:
        gbackup: GBackup = GBackup(logger=LOGGER)
        args: GBackupArgs = GBackup.read_args(sys.argv[1:])
        gbackup(args)
    except Exception as e:
        LOGGER.error(e)
        raise e

if __name__ == "__main__":
    main()
