import os
import shutil
import logging
from os import path


class DirExistsError(FileExistsError):
    ...


def create_dir(_path: str, clean_up=True, report_error=False):
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
