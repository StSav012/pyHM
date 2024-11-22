# -*- coding:utf-8 -*-
from advantech_daq import DIOPortDir, DOCircuitType, ErrorCode, utils
from advantech_daq.api import dio_port, is_error_code

__all__ = ["DIOPort"]


class DIOPort:
    def __init__(self, native_port: int) -> None:
        self._obj: int = native_port

    @property
    def port(self) -> int:
        return dio_port.get_port(self._obj)

    @property
    def direction(self) -> DIOPortDir:
        return utils.toDioPortDir(dio_port.get_direction(self._obj))

    @direction.setter
    def direction(self, value: DIOPortDir) -> None:
        if not isinstance(value, DIOPortDir):
            raise TypeError("a DIOPortDir is required")
        ret: ErrorCode = ErrorCode.lookup(dio_port.set_direction(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set direction is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def diInversePort(self) -> int:
        return dio_port.get_di_inverse_port(self._obj)

    @diInversePort.setter
    def diInversePort(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(
            dio_port.set_di_inverse_port(self._obj, value & 0xFF)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set diInversePort is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def diOpenState(self) -> int:
        return dio_port.get_di_open_state(self._obj)

    @diOpenState.setter
    def diOpenState(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(
            dio_port.set_di_open_state(self._obj, value & 0xFF)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set diOpenState is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def doPresetValue(self) -> int:
        return dio_port.get_do_preset_value(self._obj)

    @doPresetValue.setter
    def doPresetValue(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an int is required")
        ret: ErrorCode = ErrorCode.lookup(
            dio_port.set_do_preset_value(self._obj, value & 0xFF)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set doPresetValue is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def doCircuitType(self) -> DOCircuitType:
        return utils.toDoCircuitType(dio_port.get_do_circuit_type(self._obj))

    @doCircuitType.setter
    def doCircuitType(self, value: int) -> None:
        if not isinstance(value, DOCircuitType):
            raise TypeError("a DOCircuitType is required")
        ret: ErrorCode = ErrorCode.lookup(
            dio_port.set_do_circuit_type(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set doCircuitType is failed, the error code is 0x{ret.value:X}"
            )
