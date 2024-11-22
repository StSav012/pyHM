# -*- coding:utf-8 -*-
from ctypes import byref, pointer

from advantech_daq import (
    MathInterval,
    SamplingMethod,
    SignalDrop,
    TriggerAction,
    ValueRange,
    utils,
)
from advantech_daq.api import ao_features, array

__all__ = ["AOFeatures"]


class AOFeatures:
    def __init__(self, native_feature: int) -> None:
        self._obj: int = native_feature

    # DAC features
    @property
    def resolution(self) -> int:
        return ao_features.get_resolution(self._obj)

    @property
    def dataSize(self) -> int:
        return ao_features.get_data_size(self._obj)

    @property
    def dataMask(self) -> int:
        return ao_features.get_data_mask(self._obj)

    # channel features
    @property
    def channelCountMax(self) -> int:
        return ao_features.get_channel_count_max(self._obj)

    @property
    def valueRanges(self) -> list[ValueRange]:
        return array.to_value_range(ao_features.get_value_ranges(self._obj), True)

    @property
    def externalRefAntiPolar(self) -> bool:
        return True if ao_features.get_external_ref_anti_polar(self._obj) else False

    @property
    def externalRefRange(self) -> MathInterval:
        x: MathInterval = MathInterval()
        ao_features.get_external_ref_range(self._obj, pointer(x))
        return x

    # buffered ao->basic features
    @property
    def bufferedAoSupported(self) -> bool:
        return True if ao_features.get_buffered_ao_supported(self._obj) else False

    @property
    def samplingMethod(self) -> SamplingMethod:
        return utils.toSamplingMethod(ao_features.get_sampling_method(self._obj))

    @property
    def channelStartBase(self) -> int:
        return ao_features.get_channel_start_base(self._obj)

    @property
    def channelCountBase(self) -> int:
        return ao_features.get_channel_count_base(self._obj)

    # buffered ao->conversion clock features
    @property
    def convertClockSources(self) -> list[SignalDrop]:
        return array.to_signal_drop(
            ao_features.get_convert_clock_sources(self._obj), True
        )

    @property
    def convertClockRange(self) -> MathInterval:
        x: MathInterval = MathInterval()
        ao_features.get_convert_clock_range(self._obj, pointer(x))
        return x

    # buffered ao->trigger features
    @property
    def triggerCount(self) -> int:
        return ao_features.get_trigger_count(self._obj)

    @property
    def retriggerable(self) -> bool:
        return True if ao_features.get_retriggerable(self._obj) else False

    # trigger 0
    @property
    def triggerSupported(self) -> bool:
        return self.triggerCount != 0

    # trigger 1
    @property
    def trigger1Supported(self) -> bool:
        return self.triggerCount > 1

    def getTriggerActions(self, trigger: int = 0) -> list[TriggerAction]:
        return array.to_trigger_action(
            ao_features.get_trigger_actions(self._obj, trigger), True
        )

    def getTriggerDelayRange(self, trigger: int = 0) -> MathInterval:
        x: MathInterval = MathInterval()
        ao_features.get_trigger_delay_range(self._obj, trigger, byref(x))
        return x

    def getTriggerSources(self, trigger: int = 0) -> list[SignalDrop]:
        return array.to_signal_drop(
            ao_features.get_trigger_sources(self._obj, trigger), True
        )
