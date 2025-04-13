from . import Scenario
from .api import array, dio_ctrl_base
from .daq_ctrl_base import DAQCtrlBase
from .dio_features import DIOFeatures
from .dio_port import DIOPort

__all__ = ["DIOCtrlBase"]


class DIOCtrlBase(DAQCtrlBase):
    def __init__(
        self,
        scenario: Scenario,
        dev_info: str,
        profile_path: str = "",
    ) -> None:
        self._dio_features: DIOFeatures | None = None
        self._dio_ports: list[DIOPort] = []
        # self._dio_ports.append(DIOPort(None))
        # self._dio_ports = []
        super().__init__(scenario, dev_info, profile_path)

    @property
    def features(self) -> DIOFeatures:
        if self._dio_features is None:
            self._dio_features = DIOFeatures(dio_ctrl_base.get_features(self._obj))
        return self._dio_features

    @property
    def portCount(self) -> int:
        return self.features.portCount

    @property
    def ports(self) -> list[DIOPort]:
        if not self._dio_ports:
            native_array: int = dio_ctrl_base.get_ports(self._obj)
            count: int = self.portCount
            for i in range(count):
                self._dio_ports.append(DIOPort(array.get_item(native_array, i)))

        return self._dio_ports
