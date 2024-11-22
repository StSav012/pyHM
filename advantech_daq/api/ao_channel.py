# -*- coding:utf-8 -*-
from _ctypes import Array
from ctypes import POINTER, c_double, c_int32

from advantech_daq import MapFuncPiece
from advantech_daq.api import c_uint_, dll

__all__ = [
    "get_channel",
    "get_ext_ref_bipolar",
    "get_ext_ref_unipolar",
    "get_scale_table",
    "get_value_range",
    "set_ext_ref_bipolar",
    "set_ext_ref_unipolar",
    "set_scale_table",
    "set_value_range",
]


def get_channel(aoChannelObj: int) -> int:
    dll.TAoChannel_getChannel.restype = c_int32
    dll.TAoChannel_getChannel.argtypes = [c_uint_]
    return dll.TAoChannel_getChannel(aoChannelObj)


def get_value_range(aoChannelObj: int) -> int:
    dll.TAoChannel_getValueRange.argtypes = [c_uint_]
    return dll.TAoChannel_getValueRange(aoChannelObj)


def set_value_range(aoChannelObj: int, valueRange: int) -> int:
    dll.TAoChannel_setValueRange.argtypes = [c_uint_, c_int32]
    return dll.TAoChannel_setValueRange(aoChannelObj, valueRange)


def get_ext_ref_bipolar(aoChannelObj: int) -> float:
    dll.TAoChannel_getExtRefBipolar.restype = c_double
    dll.TAoChannel_getExtRefBipolar.argtypes = [c_uint_]
    return dll.TAoChannel_getExtRefBipolar(aoChannelObj)


def set_ext_ref_bipolar(aoChannelObj: int, value: float) -> int:
    dll.TAoChannel_setExtRefBipolar.argtypes = [c_uint_, c_double]
    return dll.TAoChannel_setExtRefBipolar(aoChannelObj, c_double(value))


def get_ext_ref_unipolar(aoChannelObj: int) -> float:
    dll.TAoChannel_getExtRefUnipolar.restype = c_double
    dll.TAoChannel_getExtRefUnipolar.argtypes = [c_uint_]
    return dll.TAoChannel_getExtRefUnipolar(aoChannelObj)


def set_ext_ref_unipolar(aoChannelObj: int, value: float) -> int:
    dll.TAoChannel_setExtRefUnipolar.argtypes = [c_uint_, c_double]
    return dll.TAoChannel_setExtRefUnipolar(aoChannelObj, c_double(value))


# new: scale table


def get_scale_table(
    aoChannelObj: int,
    pSize: Array[c_int32],
    mapFuncPieceTable: Array[MapFuncPiece],
) -> int:
    dll.TAoChannel_getScaleTable.argtypes = [
        c_uint_,
        POINTER(c_int32),
        POINTER(MapFuncPiece),
    ]
    return dll.TAoChannel_getScaleTable(aoChannelObj, pSize, mapFuncPieceTable)


def set_scale_table(
    aoChannelObj: int,
    size: int,
    mapFuncPieceTable: Array[MapFuncPiece],
) -> int:
    dll.TAoChannel_setScaleTable.argtypes = [
        c_uint_,
        c_int32,
        POINTER(MapFuncPiece),
    ]
    return dll.TAoChannel_setScaleTable(aoChannelObj, size, mapFuncPieceTable)
