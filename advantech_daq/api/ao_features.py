# -*- coding:utf-8 -*-
# noinspection PyProtectedMember
from _ctypes import _Pointer
from ctypes import POINTER, c_int32, c_int8

from advantech_daq import MathInterval
from advantech_daq.api import c_uint_, dll

__all__ = [
    "get_buffered_ao_supported",
    "get_channel_count_base",
    "get_channel_count_max",
    "get_channel_start_base",
    "get_convert_clock_range",
    "get_convert_clock_sources",
    "get_data_mask",
    "get_data_size",
    "get_external_ref_anti_polar",
    "get_external_ref_range",
    "get_resolution",
    "get_retriggerable",
    "get_sampling_method",
    "get_trigger_actions",
    "get_trigger_count",
    "get_trigger_delay_range",
    "get_trigger_sources",
    "get_value_ranges",
]


def get_resolution(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getResolution.restype = c_int32
    dll.TAoFeatures_getResolution.argtypes = [c_uint_]
    return dll.TAoFeatures_getResolution(aoFeatureObj)


def get_data_size(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getDataSize.restype = c_int32
    dll.TAoFeatures_getDataSize.argtypes = [c_uint_]
    return dll.TAoFeatures_getDataSize(aoFeatureObj)


def get_data_mask(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getDataMask.restype = c_int32
    dll.TAoFeatures_getDataMask.argtypes = [c_uint_]
    return dll.TAoFeatures_getDataMask(aoFeatureObj)


# channel features


def get_channel_count_max(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getChannelCountMax.restype = c_int32
    dll.TAoFeatures_getChannelCountMax.argtypes = [c_uint_]
    return dll.TAoFeatures_getChannelCountMax(aoFeatureObj)


def get_value_ranges(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getValueRanges.argtypes = [c_uint_]
    dll.TAoFeatures_getValueRanges.restype = c_uint_
    return dll.TAoFeatures_getValueRanges(aoFeatureObj)


def get_external_ref_anti_polar(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getExternalRefAntiPolar.restype = c_int8
    dll.TAoFeatures_getExternalRefAntiPolar.argtypes = [c_uint_]
    return dll.TAoFeatures_getExternalRefAntiPolar(aoFeatureObj)


def get_external_ref_range(
    aoFeatureObj: int,
    mathIntervalObj: "_Pointer[MathInterval]",
) -> int:
    dll.TAoFeatures_getExternalRefRange.argtypes = [c_uint_, POINTER(MathInterval)]
    return dll.TAoFeatures_getExternalRefRange(aoFeatureObj, mathIntervalObj)


# buffered ao->basic features


def get_buffered_ao_supported(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getBufferedAoSupported.restype = c_int8
    dll.TAoFeatures_getBufferedAoSupported.argtypes = [c_uint_]
    return dll.TAoFeatures_getBufferedAoSupported(aoFeatureObj)


def get_sampling_method(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getSamplingMethod.argtypes = [c_uint_]
    return dll.TAoFeatures_getSamplingMethod(aoFeatureObj)


def get_channel_start_base(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getChannelStartBase.restype = c_int32
    dll.TAoFeatures_getChannelStartBase.argtypes = [c_uint_]
    return dll.TAoFeatures_getChannelStartBase(aoFeatureObj)


def get_channel_count_base(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getChannelCountBase.restype = c_int32
    dll.TAoFeatures_getChannelCountBase.argtypes = [c_uint_]
    return dll.TAoFeatures_getChannelCountBase(aoFeatureObj)


# buffered ao->conversion clock features


def get_convert_clock_sources(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getConvertClockSources.argtypes = [c_uint_]
    dll.TAoFeatures_getConvertClockSources.restype = c_uint_
    return dll.TAoFeatures_getConvertClockSources(aoFeatureObj)


def get_convert_clock_range(
    aoFeatureObj: int,
    mathInterval: "_Pointer[MathInterval]",
) -> int:
    dll.TAoFeatures_getConvertClockRange.argtypes = [
        c_uint_,
        POINTER(MathInterval),
    ]
    return dll.TAoFeatures_getConvertClockRange(aoFeatureObj, mathInterval)


# buffered ao->trigger features


def get_trigger_count(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getTriggerCount.restype = c_int32
    dll.TAoFeatures_getTriggerCount.argtypes = [c_uint_]
    return dll.TAoFeatures_getTriggerCount(aoFeatureObj)


def get_retriggerable(aoFeatureObj: int) -> int:
    dll.TAoFeatures_getRetriggerable.restype = c_int8
    dll.TAoFeatures_getRetriggerable.argtypes = [c_uint_]
    return dll.TAoFeatures_getRetriggerable(aoFeatureObj)


# buffered ao->trigger0/1/.../x features


def get_trigger_sources(aoFeatureObj: int, trigger: int) -> int:
    dll.TAoFeatures_getTriggerSources.argtypes = [c_uint_, c_int32]
    dll.TAoFeatures_getTriggerSources.restype = c_uint_
    return dll.TAoFeatures_getTriggerSources(aoFeatureObj, trigger)


def get_trigger_actions(aoFeatureObj: int, trigger: int) -> int:
    dll.TAoFeatures_getTriggerActions.argtypes = [c_uint_, c_int32]
    dll.TAoFeatures_getTriggerActions.restype = c_uint_
    return dll.TAoFeatures_getTriggerActions(aoFeatureObj, trigger)


def get_trigger_delay_range(
    aoFeatureObj: int,
    trigger: int,
    mathIntervalX: "_Pointer[MathInterval]",
):
    dll.TAoFeatures_getTriggerDelayRange.argtypes = [
        c_uint_,
        c_int32,
        POINTER(MathInterval),
    ]
    return dll.TAoFeatures_getTriggerDelayRange(aoFeatureObj, trigger, mathIntervalX)
