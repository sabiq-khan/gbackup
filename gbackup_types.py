from typing import Dict, Optional, Union
from dataclasses import dataclass


@dataclass
class GBackupArgs():
    """
    Arguments:

    src_dir - The directory being backed up

    ignore_file - File listing files/dirs to exclude, in tar exclude syntax

    dest_dir - The directory that the backup will be written to

    key_file - File containing GPG key used to encrypt backup
    """
    src_dir: str
    ignore_file: str
    dest_dir: str
    key_file: Optional[str]

    def __contains__(self, property: str) -> bool:
        """Checks if dataclass instance contains property"""
        return property in self.__dict__
    
    def to_dict(self) -> Dict[str, Union[str, Optional[str]]]:
        """Returns inner Dict of properties"""
        return self.__dict__

