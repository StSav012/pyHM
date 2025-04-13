from . import Scenario
from .ai_features import AIFeatures
from .ai_channel import AIChannel
from .api import ai_ctrl_base, array
from .daq_ctrl_base import DAQCtrlBase

__all__ = ["AICtrlBase"]


class AICtrlBase(DAQCtrlBase):
    def __init__(
        self,
        scenario: Scenario,
        dev_info: str,
        profile_path: str = "",
    ) -> None:
        self._ai_features: AIFeatures | None = None
        self._ai_channels: list[AIChannel] = []
        # self._ai_channels.append(AIChannel(None))
        # self._ai_channels = []
        super().__init__(scenario, dev_info, profile_path)

    @property
    def features(self) -> AIFeatures:
        if self._ai_features is None:
            self._ai_features = AIFeatures(ai_ctrl_base.get_features(self._obj))
        return self._ai_features

    @property
    def channels(self) -> list[AIChannel]:
        if not self._ai_channels:
            count: int = self.features.channelCountMax
            native_array: int = ai_ctrl_base.get_channels(self._obj)
            for i in range(count):
                self._ai_channels.append(AIChannel(array.get_item(native_array, i)))
        return self._ai_channels

    @property
    def channelCount(self) -> int:
        return ai_ctrl_base.get_channel_count(self._obj)
