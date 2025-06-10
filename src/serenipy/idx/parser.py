import os
from typing import List

from .data import IdxInfo
from .serializer import IdxSerializer


def parse_file(idx_folder_path: str) -> List[IdxInfo]:
    idx_files = os.listdir(idx_folder_path)
    idx_info_list = []
    for idx_file in idx_files:

        if "idx" in idx_file:
            idx_file_path = idx_folder_path + os.path.sep + idx_file
            idx_info_list.extend(IdxSerializer.deserialize(idx_file_path))

    return idx_info_list


def write_file(idx_info_list: List[IdxInfo]) -> None:
    pass
