# coding=utf-8

import os
import logging
from glob import glob
from shutil import move
from os import mkdir, makedirs
from typing import List, Sequence
from os.path import exists, join, dirname, basename, isfile, isabs, abspath, isdir

from .extime import timestamp


class DirectoryExistsError(FileExistsError):
    pass


class PathNotFoundError(FileNotFoundError):
    pass


def create_dir(*path_parts: str, is_file=False, report_exist_error=False, copy_if_exists=False):
    """
    拼接路径并创建相关的目录，返回拼接的路径。

    Args:
        is_file (bool, optional): 如果路径是一个目录，创建目录；如果路径是一个文件，创建文件所在的父目录. Defaults to False.
        exist_error (bool, optional): 如果拼接的目录路径或者文件所在的父目录存在则抛出异常. Defaults to False.
        copy_if_exists (bool, optional): 如果拼接的目录路径或者文件所在的父目录存在则备份它. Defaults to False.

    Returns:
        str: 拼接的目录或者文件路径
    """
    path = join(*path_parts)
    target = dirname(path) if is_file else path

    if not exists(target):
        makedirs(target)
    elif report_exist_error:
        raise DirectoryExistsError(target)
    elif copy_if_exists:
        new_target = join(dirname(target), f"{basename(target)}_{timestamp()}")
        logging.debug(f"mv {target} to {new_target}")
        move(target, new_target)
        makedirs(new_target)

    return path


create_dir_if_not_exists = create_dir


def must_exist(*path_parts: str):
    "拼接路径，并保证路径一定存在"
    path = join(*path_parts)
    if not exists(path):
        raise PathNotFoundError(path)
    return path


def split_basename(filepath: str):
    "从文件路径的 basename 中拆分出 (filename, extname)"
    _base = basename(filepath)
    if "." not in filepath:
        return (_base, None)
    else:
        arr = _base[::-1].split(".", 1)
        return (arr[1][::-1], arr[0][::-1])


def filename(fp: str):
    """文件名：从文件 basename 中移除了文件扩展名"""
    return split_basename(fp)[0]


def extname(fp: str):
    "文件扩展名：最后一个句号后面的内容；没有句号时返回 None"
    return split_basename(fp)[1]


def glob_list(patterns: Sequence[str]):
    "取出指定路径模式列表包含的所有路径"
    results = []
    for pattern in patterns:
        for r in glob(pattern):
            results.append(r)
    return results


def list_files(dp: str, extensions=None):
    files = []
    if extensions is None:
        extensions = []
    exts = [f".{i.strip('.')}" for i in extensions]
    if len(exts) == 0:
        exts = [""]
    for ext in exts:
        for x in glob(f"{dp}/*{ext}"):
            files.append(x)
        for x in glob(f"{dp}/**/*{ext}"):
            files.append(x)
    return files


def get_path_by_filename(name: str, dirs: List[str], exts=None, report_dup_error=False):
    "通过 filename 查找指定目录列表下是否存在对应文件"
    if exts is None:
        exts = ["json", "toml", "yaml"]
    for dir in dirs:
        r = glob_list([f"{dir}/{name}.*", f"{dir}/**/{name}.*"])
        if len(r) == 1:
            return r[0]
        elif len(r) > 1:
            if report_dup_error:
                raise Exception(f"more than one file found for {name}")
            else:
                target = r[0]
                Q = {x.split(".")[-1]: i for i, x in enumerate(r)}
                for k in exts:
                    if Q.get(k) is not None:
                        target = r[Q[k]]
                        break
                logging.warning(f"more than one file found for {name}")
                return target

    raise FileNotFoundError(f"no related file for {name}")
