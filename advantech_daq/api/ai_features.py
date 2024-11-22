# -*- coding:utf-8 -*-
# noinspection PyProtectedMember
from _ctypes import _Pointer
from ctypes import POINTER, c_double, c_int, c_int32, c_int8

from advantech_daq import MathInterval
from advantech_daq.api import c_uint_, dll

__all__ = [
    "get_bridge_resistances",
    "get_buffered_ai_supported",
    "get_burnout_return_types",
    "get_burst_scan_supported",
    "get_channel_count_base",
    "get_channel_count_max",
    "get_channel_start_base",
    "get_channel_type",
    "get_cjc_channels",
    "get_connection_types",
    "get_convert_clock_range",
    "get_convert_clock_sources",
    "get_coupling_types",
    "get_data_mask",
    "get_data_size",
    "get_exciting_voltage_range",
    "get_filter_cutoff_freq1_range",
    "get_filter_cutoff_freq_range",
    "get_filter_types",
    "get_iepe_types",
    "get_impedance_types",
    "get_measure_types",
    "get_overall_connection",
    "get_overall_value_range",
    "get_resolution",
    "get_retriggerable",
    "get_sampling_method",
    "get_scan_clock_range",
    "get_scan_clock_sources",
    "get_scan_count_max",
    "get_thermo_supported",
    "get_timestamp_resolution",
    "get_trigger_actions",
    "get_trigger_count",
    "get_trigger_delay_range",
    "get_trigger_filter_cutoff_freq_range",
    "get_trigger_filter_types",
    "get_trigger_hysteresis_index_max",
    "get_trigger_hysteresis_index_step",
    "get_trigger_source_vrg",
    "get_trigger_sources",
    "get_value_ranges",
]


def get_resolution(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getResolution.restype = c_int32
    dll.TAiFeatures_getResolution.argtypes = [c_uint_]
    return dll.TAiFeatures_getResolution(aiFeatureObj)


def get_data_size(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getDataSize.restype = c_int32
    dll.TAiFeatures_getDataSize.argtypes = [c_uint_]
    return dll.TAiFeatures_getDataSize(aiFeatureObj)


def get_data_mask(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getDataMask.restype = c_int32
    dll.TAiFeatures_getDataMask.argtypes = [c_uint_]
    return dll.TAiFeatures_getDataMask(aiFeatureObj)


# new: timestamp resolution


def get_timestamp_resolution(aiFeatureObj: int) -> float:
    dll.TAiFeatures_getTimestampResolution.restype = c_double
    dll.TAiFeatures_getTimestampResolution.argtypes = [c_uint_]
    return dll.TAiFeatures_getTimestampResolution(aiFeatureObj)


#  channel features


def get_channel_count_max(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getChannelCountMax.restype = c_int32
    dll.TAiFeatures_getChannelCountMax.argtypes = [c_uint_]
    return dll.TAiFeatures_getChannelCountMax(aiFeatureObj)


def get_channel_type(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getChannelType.restype = c_int
    dll.TAiFeatures_getChannelType.argtypes = [c_uint_]
    return dll.TAiFeatures_getChannelType(aiFeatureObj)


def get_overall_value_range(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getOverallValueRange.restype = c_int8
    dll.TAiFeatures_getOverallValueRange.argtypes = [c_uint_]
    return dll.TAiFeatures_getOverallValueRange(aiFeatureObj)


def get_value_ranges(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getValueRanges.argtypes = [c_uint_]
    dll.TAiFeatures_getValueRanges.restype = c_uint_
    return dll.TAiFeatures_getValueRanges(aiFeatureObj)


def get_burnout_return_types(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getBurnoutReturnTypes.argtypes = [c_uint_]
    dll.TAiFeatures_getBurnoutReturnTypes.restype = c_uint_
    return dll.TAiFeatures_getBurnoutReturnTypes(aiFeatureObj)


def get_connection_types(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getConnectionTypes.argtypes = [c_uint_]
    dll.TAiFeatures_getConnectionTypes.restype = c_uint_
    return dll.TAiFeatures_getConnectionTypes(aiFeatureObj)


def get_overall_connection(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getOverallConnection.restype = c_int8
    dll.TAiFeatures_getOverallConnection.argtypes = [c_uint_]
    return dll.TAiFeatures_getOverallConnection(aiFeatureObj)


# filter


def get_filter_types(aiFeatureObj: int) -> int:
    dll.TAiFeatures_getFilterTypes.argtypes = [c_uint_]
    dll.TAiFeatures_getFilterTypes.restype = c_uint_
    return dll.TAiFeatures_getFilterTypes(aiFeatureObj)


def get_filter_cutoff_freq_range(
    aiFeaturesObj: int,
    mathIntervalVal: "_Pointer[MathInterval]",
) -> int:
    dll.TAiFeatures_getFilterCutoffFreqRange.argtypes = [
        c_uint_,
        POINTER(MathInterval),
    ]
    return dll.TAiFeatures_getFilterCutoffFreqRange(aiFeaturesObj, mathIntervalVal)


def get_filter_cutoff_freq1_range(
    aiFeaturesObj: int,
    mathIntervalVal: "_Pointer[MathInterval]",
) -> int:
    dll.TAiFeatures_getFilterCutoffFreq1Range.argtypes = [
        c_uint_,
        POINTER(MathInterval),
    ]
    return dll.TAiFeatures_getFilterCutoffFreq1Range(aiFeaturesObj, mathIntervalVal)


# CJC features


def get_thermo_supported(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getThermoSupported.restype = c_int8
    dll.TAiFeatures_getThermoSupported.argtypes = [c_uint_]
    return dll.TAiFeatures_getThermoSupported(aiFeaturesObj)


def get_cjc_channels(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getCjcChannels.argtypes = [c_uint_]
    dll.TAiFeatures_getCjcChannels.restype = c_uint_
    return dll.TAiFeatures_getCjcChannels(aiFeaturesObj)


# buffered ai -> basic features


def get_buffered_ai_supported(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getBufferedAiSupported.restype = c_int8
    dll.TAiFeatures_getBufferedAiSupported.argtypes = [c_uint_]
    return dll.TAiFeatures_getBufferedAiSupported(aiFeaturesObj)


def get_sampling_method(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getSamplingMethod.restype = c_int
    dll.TAiFeatures_getSamplingMethod.argtypes = [c_uint_]
    return dll.TAiFeatures_getSamplingMethod(aiFeaturesObj)


def get_channel_start_base(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getChannelStartBase.restype = c_int32
    dll.TAiFeatures_getChannelStartBase.argtypes = [c_uint_]
    return dll.TAiFeatures_getChannelStartBase(aiFeaturesObj)


def get_channel_count_base(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getChannelCountBase.restype = c_int32
    dll.TAiFeatures_getChannelCountBase.argtypes = [c_uint_]
    return dll.TAiFeatures_getChannelCountBase(aiFeaturesObj)


# buffered ai->conversion clock features


def get_convert_clock_sources(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getConvertClockSources.argtypes = [c_uint_]
    dll.TAiFeatures_getConvertClockSources.restype = c_uint_
    return dll.TAiFeatures_getConvertClockSources(aiFeaturesObj)


def get_convert_clock_range(
    aiFeaturesObj: int,
    mathIntervalValue: "_Pointer[MathInterval]",
) -> int:
    dll.TAiFeatures_getConvertClockRange.argtypes = [
        c_uint_,
        POINTER(MathInterval),
    ]
    return dll.TAiFeatures_getConvertClockRange(aiFeaturesObj, mathIntervalValue)


# buffered ai->burst scan


def get_burst_scan_supported(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getBurstScanSupported.restype = c_int8
    dll.TAiFeatures_getBurstScanSupported.argtypes = [c_uint_]
    return dll.TAiFeatures_getBurstScanSupported(aiFeaturesObj)


def get_scan_clock_sources(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getScanClockSources.argtypes = [c_uint_]
    dll.TAiFeatures_getScanClockSources.restype = c_uint_
    return dll.TAiFeatures_getScanClockSources(aiFeaturesObj)


def get_scan_clock_range(
    aiFeaturesObj: int,
    mathIntervalValue: "_Pointer[MathInterval]",
) -> int:
    dll.TAiFeatures_getScanClockRange.argtypes = [c_uint_, POINTER(MathInterval)]
    return dll.TAiFeatures_getScanClockRange(aiFeaturesObj, mathIntervalValue)


def get_scan_count_max(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getScanCountMax.restype = c_int32
    dll.TAiFeatures_getScanCountMax.argtypes = [c_uint_]
    return dll.TAiFeatures_getScanCountMax(aiFeaturesObj)


# buffered ai->trigger features


def get_retriggerable(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getRetriggerable.restype = c_int8
    dll.TAiFeatures_getRetriggerable.argtypes = [c_uint_]
    return dll.TAiFeatures_getRetriggerable(aiFeaturesObj)


def get_trigger_count(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getTriggerCount.restype = c_int32
    dll.TAiFeatures_getTriggerCount.argtypes = [c_uint_]
    return dll.TAiFeatures_getTriggerCount(aiFeaturesObj)


def get_trigger_filter_types(aiFeaturesObj: int, reserved: int) -> int:
    dll.TAiFeatures_getTriggerFilterTypes.argtypes = [c_uint_, c_int32]
    dll.TAiFeatures_getTriggerFilterTypes.restype = c_uint_
    return dll.TAiFeatures_getTriggerFilterTypes(aiFeaturesObj, reserved)


def get_trigger_filter_cutoff_freq_range(
    aiFeaturesObj: int,
    reserved: int,
    mathIntervalValue: "_Pointer[MathInterval]",
) -> int:
    dll.TAiFeatures_getTriggerFilterCutoffFreqRange.argtypes = [
        c_uint_,
        c_int32,
        POINTER(MathInterval),
    ]
    return dll.TAiFeatures_getTriggerFilterCutoffFreqRange(
        aiFeaturesObj, reserved, mathIntervalValue
    )


# buffered ai->trigger0/1/.../x features


def get_trigger_actions(aiFeaturesObj: int, trigger: int) -> int:
    dll.TAiFeatures_getTriggerActions.argtypes = [c_uint_, c_int32]
    dll.TAiFeatures_getTriggerActions.restype = c_uint_
    return dll.TAiFeatures_getTriggerActions(aiFeaturesObj, trigger)


def get_trigger_delay_range(
    aiFeaturesObj: int,
    trigger: int,
    mathIntervalX: "_Pointer[MathInterval]",
) -> int:
    dll.TAiFeatures_getTriggerDelayRange.argtypes = [
        c_uint_,
        c_int32,
        POINTER(MathInterval),
    ]
    return dll.TAiFeatures_getTriggerDelayRange(aiFeaturesObj, trigger, mathIntervalX)


def get_trigger_sources(aiFeaturesObj: int, trigger: int) -> int:
    dll.TAiFeatures_getTriggerSources.argtypes = [c_uint_, c_int32]
    dll.TAiFeatures_getTriggerSources.restype = c_uint_
    return dll.TAiFeatures_getTriggerSources(aiFeaturesObj, trigger)


def get_trigger_source_vrg(aiFeaturesObj: int, trigger: int) -> int:
    dll.TAiFeatures_getTriggerSourceVrg.argtypes = [c_uint_, c_int32]
    return dll.TAiFeatures_getTriggerSourceVrg(aiFeaturesObj, trigger)


def get_trigger_hysteresis_index_max(aiFeaturesObj: int, trigger: int) -> float:
    dll.TAiFeatures_getTriggerHysteresisIndexMax.argtypes = [c_uint_, c_int32]
    dll.TAiFeatures_getTriggerHysteresisIndexMax.restype = c_double
    return dll.TAiFeatures_getTriggerHysteresisIndexMax(aiFeaturesObj, trigger)


def get_trigger_hysteresis_index_step(aiFeaturesObj: int, trigger: int) -> int:
    dll.TAiFeatures_getTriggerHysteresisIndexStep.argtypes = [c_uint_, c_int32]
    return dll.TAiFeatures_getTriggerHysteresisIndexStep(aiFeaturesObj, trigger)


# new coupling & IEPE & Impedance


def get_coupling_types(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getCouplingTypes.argtypes = [c_uint_]
    dll.TAiFeatures_getCouplingTypes.restype = c_uint_
    return dll.TAiFeatures_getCouplingTypes(aiFeaturesObj)


def get_iepe_types(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getIepeTypes.argtypes = [c_uint_]
    dll.TAiFeatures_getIepeTypes.restype = c_uint_
    return dll.TAiFeatures_getIepeTypes(aiFeaturesObj)


def get_impedance_types(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getImpedanceTypes.argtypes = [c_uint_]
    dll.TAiFeatures_getImpedanceTypes.restype = c_uint_
    return dll.TAiFeatures_getImpedanceTypes(aiFeaturesObj)


# new: sensor features


def get_measure_types(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getMeasureTypes.argtypes = [c_uint_]
    dll.TAiFeatures_getMeasureTypes.restype = c_uint_
    return dll.TAiFeatures_getMeasureTypes(aiFeaturesObj)


def get_bridge_resistances(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getBridgeResistances.argtypes = [c_uint_]
    dll.TAiFeatures_getBridgeResistances.restype = c_uint_
    return dll.TAiFeatures_getBridgeResistances(aiFeaturesObj)


def get_exciting_voltage_range(aiFeaturesObj: int) -> int:
    dll.TAiFeatures_getExcitingVoltageRange.argtypes = [c_uint_]
    return dll.TAiFeatures_getExcitingVoltageRange(aiFeaturesObj)
