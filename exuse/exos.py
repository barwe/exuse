import os
import shutil
import logging
from os import path


class DirExistsError(FileExistsError):
    ...


class PathNotExistsError(Exception):
    ...


def create_dir(*args, clean_up=True, report_error=False):
    _path = path.join(*args)

    if path.isdir(_path):
        if report_error:
            raise DirExistsError(_path)
        if clean_up:
            logging.debug(f'remove and remake {_path}')
            shutil.rmtree(_path)
            os.mkdir(_path)
    else:
        logging.debug(f'make {_path}')
        os.mkdir(_path)

    return _path


def path_should_exist(_path: str):
    if not path.exists(_path):
        raise PathNotExistsError(_path)
    return _path


# 从文件名中拆分出 key 和 extension 两部分
def extname(p: str):
    arr = os.path.basename(p)[::-1].split('.', 1)
    if len(arr) == 1:
        return None
    else:
        return arr[0][::-1]

def filename(p: str):
    arr = os.path.basename(p)[::-1].split('.', 1)
    if len(arr) == 1:
        return os.path.basename(p)
    else:
        return arr[1][::-1]
