from . import ErrorCode, Scenario
from .ao_channel import AOChannel
from .ao_features import AOFeatures
from .api import ao_ctrl_base, array, is_error_code
from .daq_ctrl_base import DAQCtrlBase

__all__ = ["AOCtrlBase"]


class AOCtrlBase(DAQCtrlBase):
    def __init__(
        self,
        scenario: Scenario,
        dev_info: str,
        profile_path: str = "",
    ) -> None:
        self._ao_features: AOFeatures | None = None
        self._ao_channels: list[AOChannel] = []
        # TODO: WTF??
        # self._ao_channels.append(AOChannel(None))
        # self._ao_channels.clear()
        super().__init__(scenario, dev_info, profile_path)

    @property
    def features(self) -> AOFeatures:
        if self._ao_features is None:
            self._ao_features = AOFeatures(ao_ctrl_base.get_features(self._obj))
        return self._ao_features

    @property
    def channels(self) -> list[AOChannel]:
        if not self._ao_channels:
            count = self.features.channelCountMax
            native_channel_arr = ao_ctrl_base.get_channels(self._obj)
            for i in range(count):
                self._ao_channels.append(
                    AOChannel(array.get_item(native_channel_arr, i))
                )
        return self._ao_channels

    @property
    def channelCount(self) -> int:
        return self.features.channelCountMax

    @property
    def extRefValueForUnipolar(self) -> float:
        return ao_ctrl_base.get_ext_ref_value_for_unipolar(self._obj)

    @extRefValueForUnipolar.setter
    def extRefValueForUnipolar(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret = ErrorCode.lookup(
            ao_ctrl_base.set_ext_ref_value_for_unipolar(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set extRefValueForUnipolar is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def extRefValueForBipolar(self) -> float:
        return ao_ctrl_base.get_ext_ref_value_for_bipolar(self._obj)

    @extRefValueForBipolar.setter
    def extRefValueForBipolar(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret = ErrorCode.lookup(
            ao_ctrl_base.set_ext_ref_value_for_bipolar(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set extRefValueForBipolar is failed, the error code is 0x{ret.value:X}"
            )
