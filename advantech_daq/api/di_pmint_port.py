# -*- coding:utf-8 -*-
from ctypes import c_int32, c_uint8

from advantech_daq.api import c_uint_, dll

__all__ = ["get_mask", "get_pattern", "get_port", "set_mask", "set_pattern"]


def get_port(obj: int) -> int:
    dll.TDiPmintPort_getPort.restype = c_int32
    dll.TDiPmintPort_getPort.argtypes = [c_uint_]
    return dll.TDiPmintPort_getPort(obj)


def get_mask(obj: int) -> int:
    dll.TDiPmintPort_getMask.restype = c_uint8
    dll.TDiPmintPort_getMask.argtypes = [c_uint_]
    return dll.TDiPmintPort_getMask(obj)


def set_mask(obj: int, value: int) -> int:
    dll.TDiPmintPort_setMask.argtypes = [c_uint_, c_uint8]
    return dll.TDiPmintPort_setMask(obj, value)


def get_pattern(obj: int) -> int:
    dll.TDiPmintPort_getPattern.restype = c_uint8
    dll.TDiPmintPort_getPattern.argtypes = [c_uint_]
    return dll.TDiPmintPort_getPattern(obj)


def set_pattern(obj: int, value: int) -> int:
    dll.TDiPmintPort_setPattern.argtypes = [c_uint_, c_uint8]
    return dll.TDiPmintPort_setPattern(obj, value)
