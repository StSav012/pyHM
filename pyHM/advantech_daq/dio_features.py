from ctypes import pointer

from . import Depository, DOCircuitType, MathInterval, SignalDrop, utils
from .api import array, dio_features

__all__ = ["DIOFeatures"]


class DIOFeatures:
    def __init__(self, native_features: int) -> None:
        self._obj: int = native_features

    # common
    @property
    def portProgrammable(self) -> bool:
        return True if dio_features.get_port_programmable(self._obj) else False

    @property
    def channelCountMax(self) -> int:
        return dio_features.get_channel_count_max(self._obj)

    @property
    def portCount(self) -> int:
        return dio_features.get_port_count(self._obj)

    @property
    def portsType(self) -> list[int]:
        return array.to_byte(dio_features.get_ports_type(self._obj), auto_free=True)

    @property
    def diSupported(self) -> bool:
        return True if dio_features.get_di_supported(self._obj) else False

    @property
    def doSupported(self) -> bool:
        return True if dio_features.get_do_supported(self._obj) else False

    @property
    def diDataMask(self) -> list[int]:
        return array.to_byte(dio_features.get_di_data_mask(self._obj), True)

    @property
    def diNoiseFilterSupported(self) -> bool:
        return True if dio_features.get_di_noise_filter_supported(self._obj) else False

    @property
    def diNoiseFilterOfChannels(self) -> list[int]:
        return array.to_byte(
            dio_features.get_di_noise_filter_of_channels(self._obj), True
        )

    @property
    def diNoiseFilterBlockTimeRange(self) -> MathInterval:
        x: MathInterval = MathInterval()
        dio_features.get_di_noise_filter_block_time_range(self._obj, pointer(x))
        return x

    @property
    def doDataMask(self) -> list[int]:
        return array.to_byte(dio_features.get_do_data_mask(self._obj), True)

    @property
    def doFreezeSignalSources(self) -> list[SignalDrop]:
        return array.to_signal_drop(
            dio_features.get_do_freeze_signal_sources(self._obj), True
        )

    @property
    def reflectWdtFeedIntervalRange(self) -> MathInterval:
        x: MathInterval = MathInterval()
        dio_features.get_do_reflect_wdt_feed_interval_range(self._obj, pointer(x))
        return x

    @property
    def doPresetValueDepository(self) -> Depository:
        return utils.toDepository(
            dio_features.get_do_preset_value_depository(self._obj)
        )

    @property
    def doCircuitSelectableTypes(self) -> list[DOCircuitType]:
        return array.to_do_circuit_type(
            dio_features.get_do_circuit_selectable_types(self._obj), True
        )
