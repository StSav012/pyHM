from _ctypes import Array
from ctypes import c_double
from typing import Iterable

from . import ErrorCode, Scenario
from .ao_ctrl_base import AOCtrlBase
from .api import c_uint_, instant_ao_ctrl

__all__ = ["InstantAOCtrl"]


class InstantAOCtrl(AOCtrlBase):
    def __init__(self, dev_info: str, profile_path: str = "") -> None:
        super().__init__(Scenario.InstantAO, dev_info, profile_path)

    def writeAny(
        self,
        start_channel: int,
        raw_data: Iterable[int] | None,
        data_scaled: Iterable[float],
    ) -> ErrorCode:
        data_scaled = list(data_scaled)
        double_array: Array[c_double] = (c_double * len(data_scaled))(*data_scaled)
        int_array: Array[c_uint_] | None
        if raw_data is not None:
            raw_data = list(raw_data)
            int_array = (c_uint_ * len(raw_data))(*raw_data)
        else:
            int_array = None

        return ErrorCode.lookup(
            instant_ao_ctrl.write_any(
                self._obj,
                start_channel,
                len(double_array),
                int_array,
                double_array,
            )
        )
