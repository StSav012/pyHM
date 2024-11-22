# -*- coding:utf-8 -*-
from advantech_daq import ErrorCode
from advantech_daq.api import is_error_code, nos_flt_channel

__all__ = ["NoiseFilterChannel"]


class NoiseFilterChannel:
    def __init__(self, native_nos_flt_channel_obj: int) -> None:
        self._obj: int = native_nos_flt_channel_obj

    @property
    def channel(self) -> int:
        return nos_flt_channel.get_channel(self._obj)

    @property
    def enabled(self) -> bool:
        return True if nos_flt_channel.get_enabled(self._obj) else False

    @enabled.setter
    def enabled(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("a bool is required")
        ret: ErrorCode = ErrorCode.lookup(nos_flt_channel.set_enabled(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set enabled is failed, the error code is 0x{ret.value:X}"
            )
