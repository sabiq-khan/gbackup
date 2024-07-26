import os
from typing import Dict, Optional, Union
from dataclasses import dataclass

from constants import DEFAULT_BACKUP_DIR, HOME_DIR


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

