from typing import Mapping, TypeVar
from typing import List, Generator, Callable, Mapping, Generic, Dict, Sequence, Union, Tuple
from typing_extensions import Self

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

Record = Mapping[K, V]
SRecord = Mapping[str, V]
SSRecord = Mapping[str, str]
SNRecord = Mapping[str, int]
SBRecord = Mapping[str, bool]
Array = List
RecordList = Array[SSRecord]

__all__ = [
    Record,
    SRecord,
    SSRecord,
    SNRecord,
    SBRecord,
    List,
    Array,
    RecordList,
    Generator,
    Self,
    Callable,
    Mapping,
    TypeVar,
    Generic,
    Dict,
    Sequence,
]
