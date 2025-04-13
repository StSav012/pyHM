from _ctypes import Array
from ctypes import POINTER, c_byte, c_double, c_int32

from . import c_uint_, dll

__all__ = [
    "get_channel_count",
    "get_channel_map",
    "get_channel_start",
    "get_clock_rate",
    "get_clock_source",
    "set_channel_count",
    "set_channel_map",
    "set_channel_start",
    "set_clock_rate",
    "set_clock_source",
]


def get_clock_source(obj: int) -> int:
    dll.TConversion_getClockSource.argtypes = [c_uint_]
    return dll.TConversion_getClockSource(obj)


def set_clock_source(obj: int, value: int) -> int:
    dll.TConversion_setClockSource.argtypes = [c_uint_, c_int32]
    return dll.TConversion_setClockSource(obj, value)


def get_clock_rate(obj: int) -> float:
    dll.TConversion_getClockRate.restype = c_double
    dll.TConversion_getClockRate.argtypes = [c_uint_]
    return dll.TConversion_getClockRate(obj)


def set_clock_rate(obj: int, value: float) -> int:
    dll.TConversion_setClockRate.argtypes = [c_uint_, c_double]
    return dll.TConversion_setClockRate(obj, c_double(value))


def get_channel_start(obj: int) -> int:
    dll.TConversion_getChannelStart.restype = c_int32
    dll.TConversion_getChannelStart.argtypes = [c_uint_]
    return dll.TConversion_getChannelStart(obj)


def set_channel_start(obj: int, value: int) -> int:
    dll.TConversion_setChannelStart.argtypes = [c_uint_, c_int32]
    return dll.TConversion_setChannelStart(obj, value)


def get_channel_count(obj: int) -> int:
    dll.TConversion_getChannelCount.restype = c_int32
    dll.TConversion_getChannelCount.argtypes = [c_uint_]
    return dll.TConversion_getChannelCount(obj)


def set_channel_count(obj: int, value: int) -> int:
    dll.TConversion_setChannelCount.argtypes = [c_uint_, c_int32]
    return dll.TConversion_setChannelCount(obj, value)


def get_channel_map(obj: int, count: int, chMap: Array[c_byte]) -> int:
    dll.TConversion_getChannelMap.argtypes = [
        c_uint_,
        c_int32,
        POINTER(c_byte),
    ]  # need attention
    return dll.TConversion_getChannelMap(obj, count, chMap)


def set_channel_map(obj: int, count: int, chMap: Array[c_byte]) -> int:
    dll.TConversion_setChannelMap.argtypes = [
        c_uint_,
        c_int32,
        POINTER(c_byte),
    ]  # need attention
    return dll.TConversion_setChannelMap(obj, count, chMap)
