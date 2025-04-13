from _ctypes import Array
from ctypes import POINTER, c_double, c_int, c_int32, c_wchar, c_wchar_p

from . import c_uint_, dll
from .. import MapFuncPiece

__all__ = [
    "get_burn_short_ret_value",
    "get_burnout_ret_type",
    "get_burnout_ret_value",
    "get_channel",
    "get_coupling_type",
    "get_filter_cutoff_freq",
    "get_filter_cutoff_freq1",
    "get_filter_type",
    "get_iepe_type",
    "get_impedance_type",
    "get_logical_number",
    "get_scale_table",
    "get_sensor_description",
    "get_signal_type",
    "get_value_range",
    "set_burn_short_ret_value",
    "set_burnout_ret_type",
    "set_burnout_ret_value",
    "set_coupling_type",
    "set_filter_cutoff_freq",
    "set_filter_cutoff_freq1",
    "set_filter_type",
    "set_iepe_type",
    "set_impedance_type",
    "set_scale_table",
    "set_sensor_description",
    "set_signal_type",
    "set_value_range",
]


def get_channel(obj: int) -> int:
    dll.TAiChannel_getChannel.restype = c_int32
    dll.TAiChannel_getChannel.argtypes = [c_uint_]
    return dll.TAiChannel_getChannel(obj)


def get_logical_number(obj: int) -> int:
    dll.TAiChannel_getLogicalNumber.restype = c_int32
    dll.TAiChannel_getLogicalNumber.argtypes = [c_uint_]
    return dll.TAiChannel_getLogicalNumber(obj)


def get_value_range(obj: int) -> int:
    dll.TAiChannel_getValueRange.restype = c_int
    dll.TAiChannel_getValueRange.argtypes = [c_uint_]
    return dll.TAiChannel_getValueRange(obj)


def set_value_range(obj: int, valueRangeValue: int) -> int:
    dll.TAiChannel_setValueRange.argtypes = [c_uint_, c_int32]
    return dll.TAiChannel_setValueRange(obj, valueRangeValue)


def get_signal_type(obj: int) -> int:
    dll.TAiChannel_getSignalType.restype = c_int
    dll.TAiChannel_getSignalType.argtypes = [c_uint_]
    return dll.TAiChannel_getSignalType(obj)


def set_signal_type(obj: int, aiSignalTypeValue: int) -> int:
    dll.TAiChannel_setSignalType.argtypes = [c_uint_, c_int32]
    return dll.TAiChannel_setSignalType(obj, aiSignalTypeValue)


def get_burnout_ret_type(obj: int) -> int:
    dll.TAiChannel_getBurnoutRetType.restype = c_int
    dll.TAiChannel_getBurnoutRetType.argtypes = [c_uint_]
    return dll.TAiChannel_getBurnoutRetType(obj)


def set_burnout_ret_type(obj: int, burnoutRetTypeValue: int) -> int:
    dll.TAiChannel_setBurnoutRetType.argtypes = [c_uint_, c_int32]
    return dll.TAiChannel_setBurnoutRetType(obj, burnoutRetTypeValue)


def get_burnout_ret_value(obj: int) -> int:
    dll.TAiChannel_getBurnoutRetValue.restype = c_double
    dll.TAiChannel_getBurnoutRetValue.argtypes = [c_uint_]
    return dll.TAiChannel_getBurnoutRetValue(obj)


def set_burnout_ret_value(obj: int, value: float) -> int:
    dll.TAiChannel_setBurnoutRetValue.argtypes = [c_uint_, c_double]
    return dll.TAiChannel_setBurnoutRetValue(obj, c_double(value))


def get_burn_short_ret_value(obj: int) -> float:
    dll.TAiChannel_getBurnShortRetValue.restype = c_double
    dll.TAiChannel_getBurnShortRetValue.argtypes = [c_uint_]
    return dll.TAiChannel_getBurnShortRetValue(obj)


def set_burn_short_ret_value(obj: int, value: float) -> int:
    dll.TAiChannel_setBurnShortRetValue.argtypes = [c_uint_, c_double]
    return dll.TAiChannel_setBurnShortRetValue(obj, c_double(value))


def get_filter_type(obj: int) -> int:
    dll.TAiChannel_getFilterType.restype = c_int
    dll.TAiChannel_getFilterType.argtypes = [c_uint_]
    return dll.TAiChannel_getFilterType(obj)


def set_filter_type(obj: int, filterTypeValue: int) -> int:
    dll.TAiChannel_setFilterType.argtypes = [c_uint_, c_int32]
    return dll.TAiChannel_setFilterType(obj, filterTypeValue)


def get_filter_cutoff_freq(obj: int) -> float:
    dll.TAiChannel_getFilterCutoffFreq.restype = c_double
    dll.TAiChannel_getFilterCutoffFreq.argtypes = [c_uint_]
    return dll.TAiChannel_getFilterCutoffFreq(obj)


def set_filter_cutoff_freq(obj: int, value: float) -> int:
    dll.TAiChannel_setFilterCutoffFreq.argtypes = [c_uint_, c_double]
    return dll.TAiChannel_setFilterCutoffFreq(obj, c_double(value))


def get_filter_cutoff_freq1(obj: int) -> float:
    dll.TAiChannel_getFilterCutoffFreq1.restype = c_double
    dll.TAiChannel_getFilterCutoffFreq1.argtypes = [c_uint_]
    return dll.TAiChannel_getFilterCutoffFreq1(obj)


def set_filter_cutoff_freq1(obj: int, value: float) -> int:
    dll.TAiChannel_setFilterCutoffFreq1.argtypes = [c_uint_, c_double]
    return dll.TAiChannel_setFilterCutoffFreq1(obj, c_double(value))


def get_coupling_type(obj: int) -> int:
    dll.TAiChannel_getCouplingType.restype = c_int
    dll.TAiChannel_getCouplingType.argtypes = [c_uint_]
    return dll.TAiChannel_getCouplingType(obj)


def set_coupling_type(obj: int, couplingTypeValue: int) -> int:
    dll.TAiChannel_setCouplingType.argtypes = [c_uint_, c_int32]
    return dll.TAiChannel_setCouplingType(obj, couplingTypeValue)


def get_iepe_type(obj: int) -> int:
    dll.TAiChannel_getIepeType.restype = c_int
    dll.TAiChannel_getIepeType.argtypes = [c_uint_]
    return dll.TAiChannel_getIepeType(obj)


def set_iepe_type(obj: int, iepeTypeValue: int) -> int:
    dll.TAiChannel_setIepeType.argtypes = [c_uint_, c_int32]
    return dll.TAiChannel_setIepeType(obj, iepeTypeValue)


def get_impedance_type(obj: int) -> int:
    dll.TAiChannel_getImpedanceType.restype = c_int
    dll.TAiChannel_getImpedanceType.argtypes = [c_uint_]
    return dll.TAiChannel_getImpedanceType(obj)


def set_impedance_type(obj: int, impedanceTypeValue: int) -> int:
    dll.TAiChannel_setImpedanceType.argtypes = [c_uint_, c_int32]
    return dll.TAiChannel_setImpedanceType(obj, impedanceTypeValue)


def get_sensor_description(
    obj: int,
    pSize: Array[c_int32],
    wDescArr: Array[c_wchar],
) -> int:
    dll.TAiChannel_getSensorDescription.argtypes = [
        c_uint_,
        POINTER(c_int32),
        c_wchar_p,
    ]
    return dll.TAiChannel_getSensorDescription(obj, pSize, wDescArr)


def set_sensor_description(obj: int, size: int, wDescArr: Array[c_wchar]) -> int:
    dll.TAiChannel_setSensorDescription.argtypes = [
        c_uint_,
        c_int32,
        c_wchar_p,
    ]
    return dll.TAiChannel_setSensorDescription(obj, size, wDescArr)


def get_scale_table(
    obj: int,
    pSize: Array[c_int32],
    mapFuncPieceTable: Array[MapFuncPiece],
) -> int:
    dll.TAiChannel_getScaleTable.argtypes = [
        c_uint_,
        POINTER(c_int32),
        POINTER(MapFuncPiece),
    ]
    return dll.TAiChannel_getScaleTable(obj, pSize, mapFuncPieceTable)


def set_scale_table(obj: int, size: int, mapFuncPieceTable: Array[MapFuncPiece]) -> int:
    dll.TAiChannel_setScaleTable.argtypes = [
        c_uint_,
        c_int32,
        POINTER(MapFuncPiece),
    ]
    return dll.TAiChannel_setScaleTable(obj, size, mapFuncPieceTable)
