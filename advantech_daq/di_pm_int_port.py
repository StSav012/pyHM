# -*- coding:utf-8 -*-

from advantech_daq import ErrorCode
from advantech_daq.api import di_pmint_port, is_error_code

__all__ = ["DIPmIntPort"]


class DIPmIntPort:
    def __init__(self, native_di_pm_port_obj: int) -> None:
        self._obj: int = native_di_pm_port_obj

    @property
    def port(self) -> int:
        return di_pmint_port.get_port(self._obj)

    @property
    def mask(self) -> int:
        return di_pmint_port.get_mask(self._obj)

    @mask.setter
    def mask(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(
            di_pmint_port.set_mask(self._obj, value & 0xFF)
        )
        if is_error_code(ret):
            raise ValueError(f"set mask is failed, the error code is 0x{ret.value:X}")

    @property
    def pattern(self) -> int:
        return di_pmint_port.get_pattern(self._obj)

    @pattern.setter
    def pattern(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(
            di_pmint_port.set_pattern(self._obj, value & 0xFF)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set pattern is failed, the error code is 0x{ret.value:X}"
            )
