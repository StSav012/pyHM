# -*- coding:utf-8 -*-
from ctypes import c_double, c_int32

from advantech_daq.api import c_uint_, dll

__all__ = [
    "get_action",
    "get_delay_count",
    "get_edge",
    "get_filter_cutoff_freq",
    "get_filter_type",
    "get_hysteresis_index",
    "get_level",
    "get_source",
    "set_action",
    "set_delay_count",
    "set_edge",
    "set_filter_cutoff_freq",
    "set_filter_type",
    "set_hysteresis_index",
    "set_level",
    "set_source",
]


def get_source(obj: int) -> int:
    dll.TTrigger_getSource.argtypes = [c_uint_]
    dll.TTrigger_getSource.restype = c_int32
    return dll.TTrigger_getSource(obj)


def set_source(obj: int, value: int) -> int:
    dll.TTrigger_setSource.argtypes = [c_uint_, c_int32]
    return dll.TTrigger_setSource(obj, value)


def get_edge(obj: int) -> int:
    dll.TTrigger_getEdge.argtypes = [c_uint_]
    dll.TTrigger_getEdge.restype = c_int32
    return dll.TTrigger_getEdge(obj)


def set_edge(obj: int, value: int) -> int:
    dll.TTrigger_setEdge.argtypes = [c_uint_, c_int32]
    return dll.TTrigger_setEdge(obj, value)


def get_level(obj: int) -> float:
    dll.TTrigger_getLevel.argtypes = [c_uint_]
    dll.TTrigger_getLevel.restype = c_double
    return dll.TTrigger_getLevel(obj)


def set_level(obj: int, value: float) -> int:
    dll.TTrigger_setLevel.argtypes = [c_uint_, c_double]
    return dll.TTrigger_setLevel(obj, c_double(value))


def get_action(obj: int) -> int:
    dll.TTrigger_getAction.argtypes = [c_uint_]
    dll.TTrigger_getAction.restype = c_int32
    return dll.TTrigger_getAction(obj)


def set_action(obj: int, value: int) -> int:
    dll.TTrigger_setAction.argtypes = [c_uint_, c_int32]
    return dll.TTrigger_setAction(obj, value)


def get_delay_count(obj: int) -> int:
    dll.TTrigger_getDelayCount.argtypes = [c_uint_]
    dll.TTrigger_getDelayCount.restype = c_int32
    return dll.TTrigger_getDelayCount(obj)


def set_delay_count(obj: int, value: int) -> int:
    dll.TTrigger_setDelayCount.argtypes = [c_uint_, c_int32]
    return dll.TTrigger_setDelayCount(obj, value)


def get_hysteresis_index(obj: int) -> float:
    dll.TTrigger_getHysteresisIndex.argtypes = [c_uint_]
    dll.TTrigger_getHysteresisIndex.restype = c_double
    return dll.TTrigger_getHysteresisIndex(obj)


def set_hysteresis_index(obj: int, value: float) -> int:
    dll.TTrigger_setHysteresisIndex.argtypes = [c_uint_, c_double]
    return dll.TTrigger_setHysteresisIndex(obj, c_double(value))


def get_filter_type(obj: int) -> int:
    dll.TTrigger_getFilterType.argtypes = [c_uint_]
    dll.TTrigger_getFilterType.restype = c_int32
    return dll.TTrigger_getFilterType(obj)


def set_filter_type(obj: int, value: int) -> int:
    dll.TTrigger_setFilterType.argtypes = [c_uint_, c_int32]
    return dll.TTrigger_setFilterType(obj, value)


def get_filter_cutoff_freq(obj: int) -> float:
    dll.TTrigger_getFilterCutoffFreq.argtypes = [c_uint_]
    dll.TTrigger_getFilterCutoffFreq.restype = c_double
    return dll.TTrigger_getFilterCutoffFreq(obj)


def set_filter_cutoff_freq(obj: int, value: float) -> int:
    dll.TTrigger_setFilterCutoffFreq.argtypes = [c_uint_, c_double]
    return dll.TTrigger_setFilterCutoffFreq(obj, c_double(value))
