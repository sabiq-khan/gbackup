#!/usr/bin/env python3
import os
import time
import subprocess
from constants import LOGGER, IGNORE, HOMEDIR, BACKUPDIR


def main():
    try:
        LOGGER.info(f"Starting backup of {HOMEDIR}...")

        LOGGER.info(f"Navigating to {HOMEDIR}...")
        os.chdir(os.path.dirname(HOMEDIR))

        curr_time = time.strftime("%Y-%m-%d-%H%M", time.gmtime())
        LOGGER.info(f"Current time: {curr_time}")

        backup_name = f"{curr_time}-backup.tar.gz"
        LOGGER.info(f"Creating compressed archive '{backup_name}'...")
        # TODO: Find out why `--exclude-from` not working
        tar = subprocess.run(
            [
                "tar",
                "-czvf",
                f"{BACKUPDIR}/{backup_name}",
                f"--exclude-from={IGNORE}",
                "."
            ],
            shell=False,
            capture_output=True
        )

        LOGGER.info(tar.stdout)
        if (tar.returncode != 0):
            raise ChildProcessError(tar.stderr)
    except (
        ChildProcessError,
        OSError,
        TypeError,
        ValueError,
        Exception
    ) as e:
        LOGGER.error(e)
        raise e


if __name__ == "__main__":
    main()
