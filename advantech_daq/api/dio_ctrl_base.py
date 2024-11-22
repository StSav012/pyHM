# -*- coding:utf-8 -*-
from ctypes import c_int32

from advantech_daq.api import c_uint_, dll

__all__ = ["get_features", "get_port_count", "get_ports"]


def get_features(obj: int) -> int:
    dll.TDioCtrlBase_getFeatures.argtypes = [c_uint_]
    dll.TDioCtrlBase_getFeatures.restype = c_uint_
    return dll.TDioCtrlBase_getFeatures(obj)


def get_port_count(obj: int) -> int:
    dll.TDioCtrlBase_getPortCount.restype = c_int32
    dll.TDioCtrlBase_getPortCount.argtypes = [c_uint_]
    return dll.TDioCtrlBase_getPortCount(obj)


def get_ports(obj: int) -> int:
    dll.TDioCtrlBase_getPorts.argtypes = [c_uint_]
    dll.TDioCtrlBase_getPorts.restype = c_uint_
    return dll.TDioCtrlBase_getPorts(obj)
