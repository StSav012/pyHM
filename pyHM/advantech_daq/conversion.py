from _ctypes import Array
from ctypes import c_byte

from . import ErrorCode, SignalDrop, utils
from .api import conversion, is_error_code

__all__ = ["Conversion"]


class Conversion:
    def __init__(self, native_conv_obj: int, channel_count: int) -> None:
        self._obj: int = native_conv_obj
        self._channel_count: int = channel_count

    @property
    def clockSource(self) -> SignalDrop:
        return utils.toSignalDrop(conversion.get_clock_source(self._obj))

    @clockSource.setter
    def clockSource(self, value: SignalDrop) -> None:
        if not isinstance(value, SignalDrop):
            raise TypeError("a SignalDrop is required")
        ret: ErrorCode = ErrorCode.lookup(conversion.set_clock_source(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set clockSource is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def clockRate(self) -> float:
        return conversion.get_clock_rate(self._obj)

    @clockRate.setter
    def clockRate(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret = ErrorCode.lookup(conversion.set_clock_rate(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set clockRate is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def channelStart(self) -> int:
        return conversion.get_channel_start(self._obj)

    @channelStart.setter
    def channelStart(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(
            conversion.set_channel_start(self._obj, int(value))
        )
        if is_error_code(ret):
            raise ValueError(
                f"set channelStart is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def channelCount(self) -> int:
        return conversion.get_channel_count(self._obj)

    @channelCount.setter
    def channelCount(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(
            conversion.set_channel_count(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set channelCount is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def channelMap(self) -> list[int]:
        data_array: Array[c_byte] = (c_byte * self._channel_count)()
        conversion.get_channel_map(self._obj, self._channel_count, data_array)
        return [data_array[i] for i in range(self._channel_count)]

    @channelMap.setter
    def channelMap(self, value: list[int] | bytes | bytearray) -> None:
        if not isinstance(value, (list, bytes, bytearray)):
            raise TypeError("a list is required")
        data_array: Array[c_byte] = (c_byte * len(value))(*value)
        ret: ErrorCode = ErrorCode.lookup(
            conversion.set_channel_map(self._obj, len(value), data_array)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set channelMap is failed, the error code is 0x{ret.value:X}"
            )
