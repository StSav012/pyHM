from ctypes import c_int32, c_int8

from . import c_uint_, dll

__all__ = [
    "get_channel",
    "get_enabled",
    "get_gated",
    "get_trig_edge",
    "set_enabled",
    "set_gated",
    "set_trig_edge",
]


def get_channel(diIntChanObj: int) -> int:
    dll.TDiintChannel_getChannel.restype = c_int32
    dll.TDiintChannel_getChannel.argtypes = [c_uint_]
    return dll.TDiintChannel_getChannel(diIntChanObj)


def get_enabled(diIntChanObj: int) -> int:
    dll.TDiintChannel_getEnabled.restype = c_int8
    dll.TDiintChannel_getEnabled.argtypes = [c_uint_]
    return dll.TDiintChannel_getEnabled(diIntChanObj)


def set_enabled(diIntChanObj: int, value: int) -> int:
    dll.TDiintChannel_setEnabled.argtypes = [c_uint_, c_int8]
    return dll.TDiintChannel_setEnabled(diIntChanObj, value)


def get_gated(diIntChanObj: int) -> int:
    dll.TDiintChannel_getGated.restype = c_int8
    dll.TDiintChannel_getGated.argtypes = [c_uint_]
    return dll.TDiintChannel_getGated(diIntChanObj)


def set_gated(diIntChanObj: int, value: int) -> int:
    dll.TDiintChannel_setGated.argtypes = [c_uint_, c_int8]
    return dll.TDiintChannel_setGated(diIntChanObj, value)


def get_trig_edge(diIntChanObj: int) -> int:
    dll.TDiintChannel_getTrigEdge.argtypes = [c_uint_]
    return dll.TDiintChannel_getTrigEdge(diIntChanObj)


def set_trig_edge(diIntChanObj: int, value: int) -> int:
    dll.TDiintChannel_setTrigEdge.argtypes = [c_uint_, c_int32]
    return dll.TDiintChannel_setTrigEdge(diIntChanObj, value)
