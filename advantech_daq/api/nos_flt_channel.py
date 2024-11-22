# -*- coding:utf-8 -*-
from ctypes import c_int8

from advantech_daq.api import c_uint_, dll

__all__ = ["get_channel", "get_enabled", "set_enabled"]


def get_channel(obj: int) -> int:
    dll.TNosFltChannel_getChannel.argtypes = [c_uint_]
    return dll.TNosFltChannel_getChannel(obj)


def get_enabled(obj: int) -> int:
    dll.TNosFltChannel_getEnabled.restype = c_int8
    dll.TNosFltChannel_getEnabled.argtypes = [c_uint_]
    return dll.TNosFltChannel_getEnabled(obj)


def set_enabled(obj: int, value: int) -> int:
    dll.TNosFltChannel_setEnabled.argtypes = [c_uint_, c_int8]
    return dll.TNosFltChannel_setEnabled(obj, value)
