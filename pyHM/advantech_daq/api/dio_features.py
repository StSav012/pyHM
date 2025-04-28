# noinspection PyProtectedMember
from _ctypes import _Pointer
from ctypes import POINTER, c_int8, c_int32

from .. import MathInterval
from . import c_uint_, dll

__all__ = [
    "get_channel_count_max",
    "get_di_data_mask",
    "get_di_noise_filter_block_time_range",
    "get_di_noise_filter_of_channels",
    "get_di_noise_filter_supported",
    "get_di_supported",
    "get_do_circuit_selectable_types",
    "get_do_data_mask",
    "get_do_freeze_signal_sources",
    "get_do_preset_value_depository",
    "get_do_reflect_wdt_feed_interval_range",
    "get_do_supported",
    "get_port_count",
    "get_port_programmable",
    "get_ports_type",
]


def get_port_programmable(obj: int) -> int:
    dll.TDioFeatures_getPortProgrammable.restype = c_int8
    dll.TDioFeatures_getPortProgrammable.argtypes = [c_uint_]
    return dll.TDioFeatures_getPortProgrammable(obj)


def get_channel_count_max(obj: int) -> int:
    dll.TDioFeatures_getChannelCountMax.restype = c_int32
    dll.TDioFeatures_getChannelCountMax.argtypes = [c_uint_]
    return dll.TDioFeatures_getChannelCountMax(obj)


def get_port_count(obj: int) -> int:
    dll.TDioFeatures_getPortCount.restype = c_int32
    dll.TDioFeatures_getPortCount.argtypes = [c_uint_]
    return dll.TDioFeatures_getPortCount(obj)


def get_ports_type(obj: int) -> int:
    dll.TDioFeatures_getPortsType.argtypes = [c_uint_]
    dll.TDioFeatures_getPortsType.restype = c_uint_
    return dll.TDioFeatures_getPortsType(obj)


def get_di_supported(obj: int) -> int:
    dll.TDioFeatures_getDiSupported.restype = c_int8
    dll.TDioFeatures_getDiSupported.argtypes = [c_uint_]
    return dll.TDioFeatures_getDiSupported(obj)


def get_do_supported(obj: int) -> int:
    dll.TDioFeatures_getDoSupported.restype = c_int8
    dll.TDioFeatures_getDoSupported.argtypes = [c_uint_]
    return dll.TDioFeatures_getDoSupported(obj)


def get_di_data_mask(obj: int) -> int:
    dll.TDioFeatures_getDiDataMask.argtypes = [c_uint_]
    dll.TDioFeatures_getDiDataMask.restype = c_uint_
    return dll.TDioFeatures_getDiDataMask(obj)


def get_di_noise_filter_supported(obj: int) -> int:
    dll.TDioFeatures_getDiNoiseFilterSupported.restype = c_int8
    dll.TDioFeatures_getDiNoiseFilterSupported.argtypes = [c_uint_]
    return dll.TDioFeatures_getDiNoiseFilterSupported(obj)


def get_di_noise_filter_of_channels(obj: int) -> int:
    dll.TDioFeatures_getDiNoiseFilterOfChannels.argtypes = [c_uint_]
    dll.TDioFeatures_getDiNoiseFilterOfChannels.restype = c_uint_
    return dll.TDioFeatures_getDiNoiseFilterOfChannels(obj)


def get_di_noise_filter_block_time_range(
    obj: int,
    mathIntervalValue: "_Pointer[MathInterval]",
) -> int:
    dll.TDioFeatures_getDiNoiseFilterBlockTimeRange.argtypes = [
        c_uint_,
        POINTER(MathInterval),
    ]
    return dll.TDioFeatures_getDiNoiseFilterBlockTimeRange(obj, mathIntervalValue)


def get_do_data_mask(obj: int) -> int:
    dll.TDioFeatures_getDoDataMask.argtypes = [c_uint_]
    return dll.TDioFeatures_getDoDataMask(obj)


def get_do_freeze_signal_sources(obj: int) -> int:
    dll.TDioFeatures_getDoFreezeSignalSources.argtypes = [c_uint_]
    return dll.TDioFeatures_getDoFreezeSignalSources(obj)


def get_do_reflect_wdt_feed_interval_range(
    obj: int,
    mathInterValValue: "_Pointer[MathInterval]",
) -> int:
    dll.TDioFeatures_getDoReflectWdtFeedIntervalRange.argtypes = [
        c_uint_,
        POINTER(MathInterval),
    ]
    return dll.TDioFeatures_getDoReflectWdtFeedIntervalRange(obj, mathInterValValue)


def get_do_preset_value_depository(obj: int) -> int:
    dll.TDioFeatures_getDoPresetValueDepository.argtypes = [c_uint_]
    return dll.TDioFeatures_getDoPresetValueDepository(obj)


def get_do_circuit_selectable_types(obj: int) -> int:
    dll.TDioFeatures_getDoCircuitSelectableTypes.argtypes = [c_uint_]
    return dll.TDioFeatures_getDoCircuitSelectableTypes(obj)
