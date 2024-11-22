# -*- coding:utf-8 -*-
from ctypes import c_double, c_int32

from advantech_daq.api import c_uint_, dll

__all__ = [
    "get_channel_count",
    "get_channels",
    "get_ext_ref_value_for_bipolar",
    "get_ext_ref_value_for_unipolar",
    "get_features",
    "set_ext_ref_value_for_bipolar",
    "set_ext_ref_value_for_unipolar",
]


def get_features(obj: int) -> int:
    dll.TAoCtrlBase_getFeatures.argtypes = [c_uint_]
    dll.TAoCtrlBase_getFeatures.restype = c_uint_
    return dll.TAoCtrlBase_getFeatures(obj)


def get_channels(obj: int) -> int:
    dll.TAoCtrlBase_getChannels.argtypes = [c_uint_]
    dll.TAoCtrlBase_getChannels.restype = c_uint_
    return dll.TAoCtrlBase_getChannels(obj)


def get_channel_count(obj: int) -> int:
    dll.TAoCtrlBase_getChannelCount.restype = c_int32
    dll.TAoCtrlBase_getChannelCount.argtypes = [c_uint_]
    return dll.TAoCtrlBase_getChannelCount(obj)


def get_ext_ref_value_for_unipolar(obj: int) -> float:
    dll.TAoCtrlBase_getExtRefValueForUnipolar.restype = c_double
    dll.TAoCtrlBase_getExtRefValueForUnipolar.argtypes = [c_uint_]
    return dll.TAoCtrlBase_getExtRefValueForUnipolar(obj)


def set_ext_ref_value_for_unipolar(obj: int, value: float) -> int:
    dll.TAoCtrlBase_setExtRefValueForUnipolar.argtypes = [c_uint_, c_double]
    return dll.TAoCtrlBase_setExtRefValueForUnipolar(obj, c_double(value))


def get_ext_ref_value_for_bipolar(obj: int) -> float:
    dll.TAoCtrlBase_getExtRefValueForBipolar.restype = c_double
    dll.TAoCtrlBase_getExtRefValueForBipolar.argtypes = [c_uint_]
    return dll.TAoCtrlBase_getExtRefValueForBipolar(obj)


def set_ext_ref_value_for_bipolar(obj: int, value: float) -> int:
    dll.TAoCtrlBase_setExtRefValueForBipolar.argtypes = [c_uint_, c_double]
    return dll.TAoCtrlBase_setExtRefValueForBipolar(obj, c_double(value))
