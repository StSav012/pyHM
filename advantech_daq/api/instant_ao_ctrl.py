# -*- coding:utf-8 -*-
from _ctypes import Array
from ctypes import POINTER, c_double, c_int32, c_void_p

from advantech_daq.api import c_uint_, dll

__all__ = ["write_any"]


def write_any(
    obj: int,
    chStart: int,
    chCount: int,
    dataRaw: Array[c_uint_] | None,
    dataScaled: Array[c_double],
) -> int:
    dll.TInstantAoCtrl_WriteAny.argtypes = [
        c_uint_,
        c_int32,
        c_int32,
        c_void_p,
        POINTER(c_double),
    ]
    return dll.TInstantAoCtrl_WriteAny(obj, chStart, chCount, dataRaw, dataScaled)
