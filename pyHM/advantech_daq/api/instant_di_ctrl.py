from _ctypes import Array
from ctypes import POINTER, c_double, c_int32, c_uint8

from . import c_uint_, dll

__all__ = [
    "get_di_cosint_ports",
    "get_di_pmint_ports",
    "get_diint_channels",
    "get_noise_filter",
    "get_noise_filter_block_time",
    "read_any",
    "read_bit",
    "set_noise_filter_block_time",
    "snap_start",
    "snap_stop",
]


def read_any(
    obj: int, portStart: int, portCount: int, dataArray: Array[c_uint8]
) -> int:
    dll.TInstantDiCtrl_ReadAny.argtypes = [
        c_uint_,
        c_int32,
        c_int32,
        POINTER(c_uint8),
    ]
    return dll.TInstantDiCtrl_ReadAny(obj, portStart, portCount, dataArray)


def read_bit(obj: int, port: int, bit: int, data: Array[c_uint8]) -> int:
    dll.TInstantDiCtrl_ReadBit.argtypes = [
        c_uint_,
        c_int32,
        c_int32,
        POINTER(c_uint8),
    ]
    return dll.TInstantDiCtrl_ReadBit(obj, port, bit, data)


def snap_start(obj: int) -> int:
    dll.TInstantDiCtrl_SnapStart.argtypes = [c_uint_]
    return dll.TInstantDiCtrl_SnapStart(obj)


def snap_stop(obj: int) -> int:
    dll.TInstantDiCtrl_SnapStop.argtypes = [c_uint_]
    return dll.TInstantDiCtrl_SnapStop(obj)


def get_noise_filter_block_time(obj: int) -> float:
    dll.TInstantDiCtrl_getNoiseFilterBlockTime.restype = c_double
    dll.TInstantDiCtrl_getNoiseFilterBlockTime.argtypes = [c_uint_]
    return dll.TInstantDiCtrl_getNoiseFilterBlockTime(obj)


def set_noise_filter_block_time(obj: int, value: float) -> int:
    dll.TInstantDiCtrl_setNoiseFilterBlockTime.argtypes = [c_uint_, c_double]
    return dll.TInstantDiCtrl_setNoiseFilterBlockTime(obj, c_double(value))


def get_noise_filter(obj: int) -> int:
    dll.TInstantDiCtrl_getNoiseFilter.argtypes = [c_uint_]
    dll.TInstantDiCtrl_getNoiseFilter.restype = c_uint_
    return dll.TInstantDiCtrl_getNoiseFilter(obj)


def get_diint_channels(obj: int) -> int:
    dll.TInstantDiCtrl_getDiintChannels.argtypes = [c_uint_]
    dll.TInstantDiCtrl_getDiintChannels.restype = c_uint_
    return dll.TInstantDiCtrl_getDiintChannels(obj)


def get_di_cosint_ports(obj: int) -> int:
    dll.TInstantDiCtrl_getDiCosintPorts.argtypes = [c_uint_]
    dll.TInstantDiCtrl_getDiCosintPorts.restype = c_uint_
    return dll.TInstantDiCtrl_getDiCosintPorts(obj)


def get_di_pmint_ports(obj: int) -> int:
    dll.TInstantDiCtrl_getDiPmintPorts.argtypes = [c_uint_]
    dll.TInstantDiCtrl_getDiPmintPorts.restype = c_uint_
    return dll.TInstantDiCtrl_getDiPmintPorts(obj)
