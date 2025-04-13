from ctypes import Array, c_int
from typing import Iterable

from . import ErrorCode, MapFuncPiece, ValueRange, utils
from .api import ao_channel, is_error_code

__all__ = ["AOChannel"]


class AOChannel:
    def __init__(self, ao_channel_obj: int) -> None:
        self._obj: int = ao_channel_obj

    @property
    def channel(self) -> int:
        return ao_channel.get_channel(self._obj)

    @property
    def valueRange(self) -> ValueRange:
        return utils.toValueRange(ao_channel.get_value_range(self._obj))

    @valueRange.setter
    def valueRange(self, value: ValueRange) -> None:
        if not isinstance(value, ValueRange):
            raise TypeError("a ValueRange is required")
        ret = ErrorCode.lookup(ao_channel.set_value_range(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set valueRange is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def extRefBipolar(self) -> float:
        return ao_channel.get_ext_ref_bipolar(self._obj)

    @extRefBipolar.setter
    def extRefBipolar(self, value: int | float) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret = ErrorCode.lookup(ao_channel.set_ext_ref_bipolar(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set extRefBipolar is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def extRefUnipolar(self) -> float:
        return ao_channel.get_ext_ref_unipolar(self._obj)

    @extRefUnipolar.setter
    def extRefUnipolar(self, value: int | float) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret = ErrorCode.lookup(ao_channel.set_ext_ref_unipolar(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set extRefUnipolar is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def scaleTable(self) -> list[MapFuncPiece]:
        p_size: Array[c_int] = (c_int * 1)(32)
        buffer: Array[MapFuncPiece] = (MapFuncPiece * 32)()
        ret: ErrorCode = ErrorCode.lookup(
            ao_channel.get_scale_table(self._obj, p_size, buffer)
        )
        if ret == ErrorCode.ErrorBufferTooSmall:
            buffer = (MapFuncPiece * p_size[0])()
            ret = ErrorCode.lookup(
                ao_channel.get_scale_table(self._obj, p_size, buffer)
            )

        if is_error_code(ret):
            raise ValueError(
                f"get scaleTable is failed, the error code is 0x{ret.value:X}"
            )
        else:
            return [buffer[i] for i in range(p_size[0])]

    @scaleTable.setter
    def scaleTable(self, table: Iterable[MapFuncPiece]) -> None:
        table = list(table)
        data_array: Array[MapFuncPiece] = (MapFuncPiece * len(table))(*table)
        ret: ErrorCode = ErrorCode.lookup(
            ao_channel.set_scale_table(self._obj, len(table), data_array)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set scaleTable is failed, the error code is 0x{ret.value:X}"
            )
