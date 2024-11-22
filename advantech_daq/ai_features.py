# -*- coding:utf-8 -*-
from ctypes import byref, pointer

from advantech_daq import (
    AISignalType,
    AIChannelType,
    BurnoutRetType,
    CouplingType,
    FilterType,
    IEPEType,
    ImpedanceType,
    MathInterval,
    SamplingMethod,
    SignalDrop,
    TriggerAction,
    ValueRange,
    utils,
)
from advantech_daq.api import ai_features, array

__all__ = ["AIFeatures"]


class AIFeatures:
    def __init__(self, native_feature: int) -> None:
        self._obj: int = native_feature

    # ADC features
    @property
    def resolution(self) -> int:
        return ai_features.get_resolution(self._obj)

    @property
    def dataSize(self) -> int:
        return ai_features.get_data_size(self._obj)

    @property
    def dataMask(self) -> int:
        return ai_features.get_data_mask(self._obj)

    @property
    def timestampResolution(self) -> float:
        return ai_features.get_timestamp_resolution(self._obj)

    # channel features
    @property
    def channelCountMax(self) -> int:
        return ai_features.get_channel_count_max(self._obj)

    @property
    def channelType(self) -> AIChannelType:
        return utils.toAiChannelType(ai_features.get_channel_type(self._obj))

    @property
    def overallValueRange(self) -> bool:
        return True if ai_features.get_overall_value_range(self._obj) else False

    @property
    def valueRanges(self) -> list[ValueRange]:
        return array.to_value_range(ai_features.get_value_ranges(self._obj), True)

    @property
    def burnoutReturnTypes(self) -> list[BurnoutRetType]:
        return array.to_burnout_ret_type(
            ai_features.get_burnout_return_types(self._obj), True
        )

    @property
    def connectionTypes(self) -> list[AISignalType]:
        return array.to_ai_signal_type(
            ai_features.get_connection_types(self._obj), True
        )

    @property
    def overallConnection(self) -> bool:
        return True if ai_features.get_overall_connection(self._obj) else False

    @property
    def couplingTypes(self) -> list[CouplingType]:
        return array.to_coupling_type(ai_features.get_coupling_types(self._obj), True)

    @property
    def iepeTypes(self) -> list[IEPEType]:
        return array.to_iepe_type(ai_features.get_iepe_types(self._obj), True)

    @property
    def impedanceTypes(self) -> list[ImpedanceType]:
        return array.to_impedance_type(ai_features.get_impedance_types(self._obj), True)

    @property
    def filterTypes(self) -> list[FilterType]:
        return array.to_filter_type(ai_features.get_filter_types(self._obj), True)

    @property
    def filterCutoffFreqRange(self) -> MathInterval:
        x: MathInterval = MathInterval()
        ai_features.get_filter_cutoff_freq_range(self._obj, pointer(x))
        return x

    @property
    def filterCutoffFreq1Range(self) -> MathInterval:
        x: MathInterval = MathInterval()
        ai_features.get_filter_cutoff_freq1_range(self._obj, pointer(x))
        return x

    # cjc features
    @property
    def thermoSupported(self) -> bool:
        return True if ai_features.get_thermo_supported(self._obj) else False

    @property
    def cjcChannels(self) -> list[int]:
        return array.to_int32(ai_features.get_cjc_channels(self._obj), True)

    # buffered ai -> basic features
    @property
    def bufferedAiSupported(self) -> bool:
        return True if ai_features.get_buffered_ai_supported(self._obj) else False

    @property
    def samplingMethod(self) -> SamplingMethod:
        return utils.toSamplingMethod(ai_features.get_sampling_method(self._obj))

    @property
    def channelStartBase(self) -> int:
        return ai_features.get_channel_start_base(self._obj)

    @property
    def channelCountBase(self) -> int:
        return ai_features.get_channel_count_base(self._obj)

    # buffered ai -> conversion clock features
    @property
    def convertClockSources(self) -> list[SignalDrop]:
        return array.to_signal_drop(
            ai_features.get_convert_clock_sources(self._obj), True
        )

    @property
    def convertClockRange(self) -> MathInterval:
        x: MathInterval = MathInterval()
        ai_features.get_convert_clock_range(self._obj, pointer(x))
        return x

    # buffered ai -> burst scan
    @property
    def burstScanSupported(self) -> bool:
        return True if ai_features.get_burst_scan_supported(self._obj) else False

    @property
    def scanClockSources(self) -> list[SignalDrop]:
        return array.to_signal_drop(ai_features.get_scan_clock_sources(self._obj), True)

    @property
    def scanClockRange(self) -> MathInterval:
        x: MathInterval = MathInterval()
        ai_features.get_scan_clock_range(self._obj, pointer(x))
        return x

    @property
    def scanCountMax(self) -> int:
        return ai_features.get_scan_count_max(self._obj)

    # buffered ai->trigger features
    @property
    def triggerCount(self) -> int:
        return ai_features.get_trigger_count(self._obj)

    @property
    def retriggerable(self) -> bool:
        return True if ai_features.get_retriggerable(self._obj) else False

    @property
    def triggerFilterTypes(self) -> list[FilterType]:
        return array.to_filter_type(
            ai_features.get_trigger_filter_types(self._obj, 0), True
        )

    @property
    def triggerFilterCutoffFreq(self) -> MathInterval:
        x: MathInterval = MathInterval()
        ai_features.get_trigger_filter_cutoff_freq_range(self._obj, 0, byref(x))
        return x

    # trigger 0
    @property
    def triggerSupported(self) -> bool:
        return self.triggerCount != 0

    # trigger 1
    @property
    def trigger1Supported(self) -> bool:
        return self.triggerCount > 1

    # buffered ai->trigger0/1/../x features
    def getTriggerActions(self, trigger: int = 0) -> list[TriggerAction]:
        return array.to_trigger_action(
            ai_features.get_trigger_actions(self._obj, trigger), True
        )

    def getTriggerDelayRange(self, trigger: int = 0) -> MathInterval:
        x: MathInterval = MathInterval()
        ai_features.get_trigger_delay_range(self._obj, trigger, byref(x))
        return x

    def getTriggerSources(self, trigger: int = 0) -> list[SignalDrop]:
        return array.to_signal_drop(
            ai_features.get_trigger_sources(self._obj, trigger), True
        )

    def getTriggerSourceVrg(self, trigger: int = 0) -> ValueRange:
        return utils.toValueRange(
            ai_features.get_trigger_source_vrg(self._obj, trigger)
        )

    def getTriggerHysteresisIndexMax(self, trigger: int = 0) -> float:
        return ai_features.get_trigger_hysteresis_index_max(self._obj, trigger)

    def getTriggerHysteresisIndexStep(self, trigger: int = 0) -> int:
        return ai_features.get_trigger_hysteresis_index_step(self._obj, trigger)
