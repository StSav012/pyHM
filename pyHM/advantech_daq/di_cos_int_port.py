from . import ErrorCode
from .api import di_cosint_port, is_error_code

__all__ = ["DICosIntPort"]


class DICosIntPort:
    def __init__(self, native_di_cos_int_port_obj: int) -> None:
        self._obj: int = native_di_cos_int_port_obj

    @property
    def port(self) -> int:
        return di_cosint_port.get_port(self._obj)

    # The channels in the port that enabled change of state interrupt
    @property
    def mask(self) -> int:
        return di_cosint_port.get_mask(self._obj)

    @mask.setter
    def mask(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(
            di_cosint_port.set_mask(self._obj, value & 0xFF)
        )
        if is_error_code(ret):
            raise ValueError(f"set mask is failed, the error code is 0x{ret.value:X}")
