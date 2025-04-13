from _ctypes import Array
from ctypes import c_int32, c_wchar, create_unicode_buffer
from typing import Iterable

from . import (
    AISignalType,
    BurnoutRetType,
    CouplingType,
    ErrorCode,
    FilterType,
    IEPEType,
    ImpedanceType,
    MapFuncPiece,
    ValueRange,
    utils,
)
from .api import ai_channel, is_error_code

__all__ = ["AIChannel"]


class AIChannel:
    def __init__(self, ai_channel_obj: int) -> None:
        self._obj: int = ai_channel_obj

    @property
    def channel(self) -> int:
        return ai_channel.get_channel(self._obj)

    @property
    def logicalNumber(self) -> int:
        return ai_channel.get_logical_number(self._obj)

    @property
    def valueRange(self) -> ValueRange:
        return utils.toValueRange(ai_channel.get_value_range(self._obj))

    @valueRange.setter
    def valueRange(self, value: ValueRange) -> None:
        if not isinstance(value, ValueRange):
            raise TypeError("a ValueRange is required")
        ret: ErrorCode = ErrorCode.lookup(ai_channel.set_value_range(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set valueRange is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def signalType(self) -> AISignalType:
        return utils.toAISignalType(ai_channel.get_signal_type(self._obj))

    @signalType.setter
    def signalType(self, value: AISignalType) -> None:
        if not isinstance(value, AISignalType):
            raise TypeError("an AISignalType is required")
        ret: ErrorCode = ErrorCode.lookup(ai_channel.set_signal_type(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set signalType is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def burnoutRetType(self) -> BurnoutRetType:
        return utils.toBurnoutRetType(ai_channel.get_burnout_ret_type(self._obj))

    @burnoutRetType.setter
    def burnoutRetType(self, value: BurnoutRetType) -> None:
        if not isinstance(value, BurnoutRetType):
            raise TypeError("a BurnoutRetType is required")
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.set_burnout_ret_type(self._obj, int(value))
        )
        if is_error_code(ret):
            raise ValueError(
                f"set burnoutRetType is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def burnoutRetValue(self) -> int:
        return ai_channel.get_burnout_ret_value(self._obj)

    @burnoutRetValue.setter
    def burnoutRetValue(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.set_burnout_ret_value(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set burnoutRetValue is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def burnShortRetValue(self) -> float:
        return ai_channel.get_burn_short_ret_value(self._obj)

    @burnShortRetValue.setter
    def burnShortRetValue(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.set_burn_short_ret_value(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set burnShortRetValue is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def filterType(self) -> FilterType:
        return utils.toFilterType(ai_channel.get_filter_type(self._obj))

    @filterType.setter
    def filterType(self, value: FilterType) -> None:
        if not isinstance(value, FilterType):
            raise TypeError("a FilterType is required")
        ret: ErrorCode = ErrorCode.lookup(ai_channel.set_filter_type(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set filterType is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def filterCutoffFreq(self) -> float:
        return ai_channel.get_filter_cutoff_freq(self._obj)

    @filterCutoffFreq.setter
    def filterCutoffFreq(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.set_filter_cutoff_freq(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set filterCutoffFreq is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def filterCutoffFreq1(self) -> float:
        return ai_channel.get_filter_cutoff_freq1(self._obj)

    @filterCutoffFreq1.setter
    def filterCutoffFreq1(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.set_filter_cutoff_freq1(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set filterCutoffFreq1 is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def couplingType(self) -> CouplingType:
        return utils.toCouplingType(ai_channel.get_coupling_type(self._obj))

    @couplingType.setter
    def couplingType(self, value: CouplingType) -> None:
        if not isinstance(value, CouplingType):
            raise TypeError("a CouplingType is required")
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.set_coupling_type(self._obj, int(value))
        )
        if is_error_code(ret):
            raise ValueError(
                f"set couplingType is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def iepeType(self) -> IEPEType:
        return utils.toIEPEType(ai_channel.get_iepe_type(self._obj))

    @iepeType.setter
    def iepeType(self, value: IEPEType) -> None:
        if not isinstance(value, IEPEType):
            raise TypeError("an IEPEType is required")
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.set_iepe_type(self._obj, int(value))
        )
        if is_error_code(ret):
            raise ValueError(
                f"set iepeType is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def impedanceType(self) -> ImpedanceType:
        return utils.toImpedanceType(ai_channel.get_impedance_type(self._obj))

    @impedanceType.setter
    def impedanceType(self, value: ImpedanceType) -> None:
        if not isinstance(value, ImpedanceType):
            raise TypeError("an ImpedanceType is required")
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.set_impedance_type(self._obj, int(value))
        )
        if is_error_code(ret):
            raise ValueError(
                f"set impedanceType is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def sensorDescription(self) -> tuple[ErrorCode, bytes]:
        desc: Array[c_wchar] = create_unicode_buffer(1024)
        p_size: Array[c_int32] = (c_int32 * 1)(1024)
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.get_sensor_description(self._obj, p_size, desc)
        )
        if ret == ErrorCode.ErrorBufferTooSmall:
            desc = create_unicode_buffer(p_size[0])
            ret = ErrorCode.lookup(
                ai_channel.get_sensor_description(self._obj, p_size, desc)
            )

        return ret, desc.value.encode()

    @sensorDescription.setter
    def sensorDescription(self, value: Array[c_wchar]) -> None:
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.set_sensor_description(self._obj, len(value), value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set sensorDescription is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def scaleTable(self) -> list[MapFuncPiece]:
        p_size: Array[c_int32] = (c_int32 * 1)(32)
        buffer: Array[MapFuncPiece] = (MapFuncPiece * 32)()
        ret: ErrorCode = ErrorCode.lookup(
            ai_channel.get_scale_table(self._obj, p_size, buffer)
        )
        if ret == ErrorCode.ErrorBufferTooSmall:
            buffer = (MapFuncPiece * p_size[0])()
            ret = ErrorCode.lookup(
                ai_channel.get_scale_table(self._obj, p_size, buffer)
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
            ai_channel.set_scale_table(self._obj, len(table), data_array)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set scaleTable is failed, the error code is 0x{ret.value:X}"
            )
