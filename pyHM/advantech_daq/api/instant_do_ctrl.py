from _ctypes import Array
from ctypes import POINTER, byref, c_int32, c_uint8

from . import c_uint_, dll

__all__ = ["read_any", "read_bit", "write_any", "write_bit"]


def write_any(
    obj: int,
    startPort: int,
    portCount: int,
    dataArray: Array[c_uint8],
) -> int:
    dll.TInstantDoCtrl_WriteAny.argtypes = [
        c_uint_,
        c_int32,
        c_int32,
        POINTER(c_uint8),
    ]
    return dll.TInstantDoCtrl_WriteAny(obj, startPort, portCount, dataArray)


def read_any(
    obj: int, startPort: int, portCount: int, dataArray: Array[c_uint8]
) -> int:
    dll.TInstantDoCtrl_ReadAny.argtypes = [
        c_uint_,
        c_int32,
        c_int32,
        POINTER(c_uint8),
    ]
    return dll.TInstantDoCtrl_ReadAny(obj, startPort, portCount, dataArray)


def write_bit(obj: int, port: int, bit: int, data: int | bool) -> int:
    dll.TInstantDoCtrl_WriteBit.argtypes = [c_uint_, c_int32, c_int32, c_uint8]
    return dll.TInstantDoCtrl_WriteBit(obj, port, bit, data)


def read_bit(obj: int, port: int, bit: int, data: Array[c_uint8]) -> int:
    dll.TInstantDoCtrl_ReadBit.argtypes = [
        c_uint_,
        c_int32,
        c_int32,
        POINTER(c_uint8),
    ]
    return dll.TInstantDoCtrl_ReadBit(obj, port, bit, byref(data))
