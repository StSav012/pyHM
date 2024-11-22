# -*- coding:utf-8 -*-
from ctypes import c_int32

from advantech_daq.api import c_uint_, dll

__all__ = ["get_channel_count", "get_channels", "get_features"]


def get_features(obj: int) -> int:
    dll.TAiCtrlBase_getFeatures.argtypes = [c_uint_]
    dll.TAiCtrlBase_getFeatures.restype = c_uint_
    return dll.TAiCtrlBase_getFeatures(obj)


def get_channels(obj: int) -> int:
    dll.TAiCtrlBase_getChannels.restype = c_uint_
    dll.TAiCtrlBase_getChannels.argtypes = [c_uint_]
    return dll.TAiCtrlBase_getChannels(obj)


def get_channel_count(obj: int) -> int:
    dll.TAiCtrlBase_getChannelCount.restype = c_int32
    dll.TAiCtrlBase_getChannelCount.argtypes = [c_uint_]
    return dll.TAiCtrlBase_getChannelCount(obj)
