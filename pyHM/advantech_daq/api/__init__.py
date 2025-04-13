import os
import platform

# noinspection PyProtectedMember
from _ctypes import Array, _Pointer
from ctypes import (
    POINTER,
    c_int32,
    c_uint32,
    c_uint64,
    c_ulong,
    c_wchar,
    c_wchar_p,
    CDLL,
    create_unicode_buffer,
)

from .. import ErrorCode, MathInterval, ValueUnit

c_uint_: type
if platform.architecture()[0] == "32bit":
    c_uint_ = c_uint32
else:
    c_uint_ = c_uint64

dll: CDLL
if os.name == "nt":
    from ctypes import windll

    dll = windll.LoadLibrary("biodaq")
else:
    from ctypes import cdll

    dll = cdll.LoadLibrary("libbiodaq.so")

__all__ = [
    "adx_enum_to_string",
    "adx_get_value_range_information",
    "is_error_code",
    "dll",
    "c_uint_",
]


def adx_enum_to_string(enumName: str, enumValue: int, enumStrLen: int) -> str:
    p_str: Array[c_wchar] = create_unicode_buffer("\0", enumStrLen)
    dll.AdxEnumToString.argtypes = [c_wchar_p, c_uint32, c_uint32, c_wchar_p]
    dll.AdxEnumToString.restype = c_int32
    dll.AdxEnumToString(enumName, enumValue, enumStrLen, p_str)
    return p_str.value


def adx_get_value_range_information(
    valueRangeArg: int,
    sizeofDesc: int,
    pDescription: "_Pointer[c_wchar]",
    pMathIntervalRange: "_Pointer[MathInterval]",
    pValueUnit: "_Pointer[c_int32]",
) -> int:
    dll.AdxGetValueRangeInformation.argtypes = [
        c_uint32,
        c_uint32,
        c_wchar_p,
        POINTER(MathInterval),
        POINTER(ValueUnit),
    ]
    dll.AdxGetValueRangeInformation.restype = c_uint32

    return dll.AdxGetValueRangeInformation(
        valueRangeArg, sizeofDesc, pDescription, pMathIntervalRange, pValueUnit
    )


def is_error_code(ret: ErrorCode | int) -> bool:
    if not isinstance(ret, (ErrorCode, int)):
        raise TypeError("an int or an ErrorCode is required")
    if isinstance(ret, ErrorCode):
        ret = ret.value
    if c_ulong(ret).value >= c_ulong(0xC0000000).value:
        return True
    return False
