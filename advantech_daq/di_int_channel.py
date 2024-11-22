# -*- coding:utf-8 -*-
from advantech_daq import ActiveSignal, ErrorCode, utils
from advantech_daq.api import di_int_channel, is_error_code

__all__ = ["DIIntChannel"]


class DIIntChannel:
    def __init__(self, di_int_chan: int) -> None:
        self._obj: int = di_int_chan

    @property
    def channel(self) -> int:
        return di_int_channel.get_channel(self._obj)

    @property
    def enabled(self) -> bool:
        return True if di_int_channel.get_enabled(self._obj) else False

    @enabled.setter
    def enabled(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("a bool is required")
        ret: ErrorCode = ErrorCode.lookup(di_int_channel.set_enabled(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set enabled is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def gated(self) -> bool:
        return True if di_int_channel.get_gated(self._obj) else False

    @gated.setter
    def gated(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("a bool is required")
        ret: ErrorCode = ErrorCode.lookup(di_int_channel.set_gated(self._obj, value))
        if is_error_code(ret):
            raise ValueError(f"set gated is failed, the error code is 0x{ret.value:X}")

    @property
    def trigEdge(self) -> ActiveSignal:
        return utils.toActiveSignal(di_int_channel.get_trig_edge(self._obj))

    @trigEdge.setter
    def trigEdge(self, value: bool) -> None:
        if not isinstance(value, ActiveSignal):
            raise TypeError("an ActiveSignal is required")
        ret: ErrorCode = ErrorCode.lookup(
            di_int_channel.set_trig_edge(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set trigEdge is failed, the error code is 0x{ret.value:X}"
            )
