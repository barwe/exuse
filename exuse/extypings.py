from typing import Mapping, TypeVar
from typing import List

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

Record = Mapping[K, V]
SRecord = Mapping[str, V]
SSRecord = Mapping[str, str]
SNRecord = Mapping[str, int]
SBRecord = Mapping[str, bool]
Array = List

__all__ = [
    Record,
    SRecord,
    SSRecord,
    SNRecord,
    SBRecord,
    Array
]
