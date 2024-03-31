#!/usr/bin/env python3
import os
import re
import tarfile
from constants import LOGGER, IGNORE

# Reads ignore file and creates regexes to exclude files
def parse_ignore():
    try:
        if os.path.getsize(IGNORE) == 0:
            LOGGER.info(f"{IGNORE} is empty. No files to exclude.")
            return None, None

        dir_regex = ""
        file_regex = ""

        LOGGER.info(f"Parsing {IGNORE}...")
        with open(IGNORE, "r") as file:
            for line in file:
                line = line.strip("\n")
                LOGGER.info(f"Read line: {line}")
                capture_group = f"({line})|"
                LOGGER.info(f"Created capturing group: {capture_group}")
                if line.endswith("/"):
                    dir_regex += capture_group
                    LOGGER.info(f"Capturing group added to directory regex.")
                else:
                    file_regex += capture_group
                    LOGGER.info("Capturing group added to file regex.")

        dir_regex, file_regex = dir_regex.rstrip("|"), file_regex.rstrip("|")

        LOGGER.info(f"Directory regex: {dir_regex}")
        LOGGER.info(f"File regex: {file_regex}")

        return dir_regex, file_regex
    except (
        FileNotFoundError,
        OSError,
        ValueError,
        TypeError,
        Exception
    ) as e:
        LOGGER.error(e)
        raise e


# Scoped globally since parameters can't be passed to exclude()
DIR_REGEX, FILE_REGEX = parse_ignore()


# Filter function for tar.add()
def exclude(tarinfo):
    filename = tarinfo.name

    if DIR_REGEX is not None:
        dir_match = re.match(DIR_REGEX, filename)

    if FILE_REGEX is not None:
        file_match = re.match(FILE_REGEX, filename)

    if (dir_match is None) and (file_match is None):
        return tarinfo

    return None


def main():
    with tarfile.open(name="backup.tar.gz", mode="w:gz") as tar:
        # TODO: Debug this tar.add() call
        tar.add("~", filter=exclude)


if __name__ == "__main__":
    main()
