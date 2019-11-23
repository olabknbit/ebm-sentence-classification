from os import listdir
from os.path import isfile, isdir, join

from typing import List


def save_data_with_dir_creation(directory: str, filename: str, lines: List[str]) -> None:
    import os

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            print("Creation of directory %s failed" % directory)
        else:
            print("Successfully created directory %s " % directory)

    # save data to files
    with open(directory + filename, 'w') as f:
        f.writelines(lines)


def get_all_dirnames(directory: str) -> List[str]:
    onlydirs = [d for d in listdir(directory) if isdir(join(directory, d))]
    return onlydirs


def get_all_dirpaths(directory: str) -> List[str]:
    onlydirs = [join(directory, d) for d in get_all_dirnames(directory)]
    return onlydirs


def get_all_filenames(directory: str) -> List[str]:
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    return onlyfiles


def get_all_filepaths(directory: str) -> List[str]:
    onlyfiles = [join(directory, f) for f in get_all_filenames(directory)]
    return onlyfiles


def get_all_filepaths_rec(directory: str) -> List[str]:
    paths = get_all_filepaths(directory)
    for dir_path in get_all_dirpaths(directory):
        paths = paths + get_all_filepaths_rec(dir_path)
    return paths
