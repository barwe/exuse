import os
import toml
import logging
from os import path
from typing import List, Mapping

def _extract_unique_keys(rawdata: Mapping):
    '''遍历嵌套字典所有深度上的键，提取出键名唯一的键值对，即排除出现两次及以上键名的键值对'''
    qd = {}
    dup_keys = []

    def iterate(k, v):
        if isinstance(v, dict):
            for x, y in v.items():
                iterate(x, y)
        else:
            if qd.get(k) is not None:
                dup_keys.append(k)
            qd[k] = v

    for k, v in rawdata.items():
        iterate(k, v)

    for k in dup_keys:
        qd.pop(k)

    return qd


def get_nested_key(obj: dict, nested_key: str, nest_delimiter='.', handle_key_error=None):
    """从嵌套字典中按照嵌套键取出对应的值

    Args:
        obj (dict): 一个字典
        nested_key (str): 嵌套的键
        nest_delimiter (str, optional): 键嵌套的分隔符. Defaults to '.'.
        handle_key_error (str, optional): 怎么处理异常. Defaults to None. `RAISE_ERROR`表示抛出异常，否则返回值

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """

    keys = nested_key.split(nest_delimiter)
    tmp = obj
    for key in keys:
        try:
            tmp = tmp[key]
        except KeyError as e:
            if handle_key_error == 'RAISE_ERROR':
                raise e
            else:
                return handle_key_error

    return tmp


class EnvLoader:
    '''
    Memebers:
    - `rootdir`: project root dir
    - `env_file`: path of env.toml
    - `raw`: json object loaded from `env_file`
    '''

    def __init__(self, env_file: str = None, strict=False, checking_path=False):
        """
        Args:
            env_file (str, optional): 环境配置文件. 默认为项目根目录下的 env.toml 文件.
            strict (bool, optional): 是否启用严格验证. Defaults to False.
            启用严格验证时，如果查询的键在文件中未定义，抛出异常；否则返回键本身.
        """
        self.rootdir = os.environ['ENV_LOADER_ROOT']

        if env_file is None: env_file = path.join(self.rootdir, 'env.toml')
        assert path.isfile(env_file) and env_file.endswith('.toml')
        self.env_file = env_file

        logging.debug(f'load environments from {env_file}')
        self.raw = toml.load(self.env_file)
        self._uniq_kvs = _extract_unique_keys(self.raw)

        self.use_strict = strict
        if strict:
            logging.info('enable STRICT mode when checking ENV keys, this may cause KeyError')

        self.checking_path = checking_path

        self.tempdir = path.join(self.rootdir, 'temp')

    def __str__(self):
        return f'EnvLoader<file="{self.env_file}">'

    def get_raw(self, dotted_key: str):
        """从环境字典中取出原始值

        Args:
            dotted_key (str): 嵌套的键，或者单键

        Returns:
            str: 禁用严格模式的情景下，键存在时返回其值，不存在时返回键本身
        """
        # 直接通过单键取出值，自动进行深层遍历
        if '.' not in dotted_key:
            try:
                return self._uniq_kvs[dotted_key]
            except KeyError as e:
                if self.use_strict:
                    logging.error(f'未定义或者重复定义的键：{dotted_key}')
                    raise e
                else:
                    return dotted_key
        # 嵌套的键
        else:
            try:
                get_nested_key(self.raw, dotted_key, handle_key_error='RAISE_ERROR')
            except KeyError as e:
                if self.use_strict:
                    logging.error(f'未定义的键：{dotted_key}')
                    raise e
                else:
                    return dotted_key

    def fix_path(self, _path: str) -> str:
        """
        从环境文件中取出的路径如果是相对路径，则需要修复为相对于项目根目录的绝对路径

        Args:
            _path (str): 相对路径或者绝对路径，绝对路径不进行修复

        Returns:
            str: 绝对路径
        """
        if path.isabs(_path):
            return _path
        else:
            return path.abspath(path.join(self.rootdir, _path))

    def get_path(self, dotted_key: str) -> str:
        v = self.get_raw(dotted_key)
        v = self.fix_path(v)
        if self.checking_path and not path.exists(v):
            logging.error(f'路径不存在：{v}')
            raise Exception(v)
        return v

    def get_path_list(self, dotted_key: str) -> List[str]:
        arr = self.get_raw(dotted_key)
        _paths = []
        for _path in arr:
            v = self.fix_path(_path)
            if self.checking_path and not path.exists(v):
                logging.error(f'路径不存在：{v}')
                raise Exception(v)
            _paths.append(v)
        return _paths
