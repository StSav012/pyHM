from ctypes import c_int32

from . import c_uint_, dll

__all__ = [
    "get_cycles",
    "get_section_count",
    "get_section_length",
    "set_cycles",
    "set_section_count",
    "set_section_length",
]


def get_section_length(obj: int) -> int:
    dll.TRecord_getSectionLength.restype = c_int32
    dll.TRecord_getSectionLength.argtypes = [c_uint_]
    return dll.TRecord_getSectionLength(obj)


def set_section_length(obj: int, value: int) -> int:
    dll.TRecord_setSectionLength.argtypes = [c_uint_, c_int32]
    return dll.TRecord_setSectionLength(obj, value)


def get_section_count(obj: int) -> int:
    dll.TRecord_getSectionCount.argtypes = [c_uint_]
    return dll.TRecord_getSectionCount(obj)


def set_section_count(obj: int, value: int) -> int:
    dll.TRecord_setSectionCount.argtypes = [c_uint_, c_int32]
    return dll.TRecord_setSectionCount(obj, value)


def get_cycles(obj: int) -> int:
    dll.TRecord_getCycles.restype = c_int32
    dll.TRecord_getCycles.argtypes = [c_uint_]
    return dll.TRecord_getCycles(obj)


def set_cycles(obj: int, value: int) -> int:
    dll.TRecord_setCycles.argtypes = [c_uint_, c_int32]
    return dll.TRecord_setCycles(obj, value)
