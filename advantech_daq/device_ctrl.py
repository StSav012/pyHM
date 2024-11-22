# -*- coding:utf-8 -*-
# noinspection PyProtectedMember
from _ctypes import Array, _Pointer
from ctypes import (
    c_byte,
    c_int32,
    c_uint8,
    c_wchar,
    create_unicode_buffer,
    pointer,
)

from advantech_daq import (
    AccessMode,
    DeviceTreeNode,
    ErrorCode,
    EventId,
    ProductId,
    TerminalBoard,
    utils,
)
from advantech_daq.api import array, device_ctrl, is_error_code

__all__ = ["DeviceCtrl"]


class DeviceCtrl:
    def __init__(self, native_dev: int) -> None:
        self._obj: int = native_dev

    # method
    def refresh(self) -> ErrorCode:
        return ErrorCode.lookup(device_ctrl.refresh(self._obj))

    def readRegister(
        self,
        space: int,
        offset: int,
        length: int,
    ) -> tuple[ErrorCode, list[int]]:
        data_array: Array[c_byte] = (c_byte * length)()
        ret: ErrorCode = ErrorCode.lookup(
            device_ctrl.read_register(self._obj, space, offset, length, data_array)
        )
        if is_error_code(ret):
            return ret, []
        return ret, [data_array[i] for i in range(length)]

    def writeRegister(
        self,
        space: int,
        offset: int,
        data: list[int] | bytes | bytearray,
    ) -> ErrorCode:
        if not isinstance(data, (list, bytes, bytearray)):
            raise TypeError("a list is required")
        data_array: Array[c_byte] = (c_byte * len(data))(*data)
        ret: ErrorCode = ErrorCode.lookup(
            device_ctrl.write_register(self._obj, space, offset, len(data), data_array)
        )
        return ret

    def readPrivateRegion(
        self, signature: int, length: int
    ) -> tuple[ErrorCode, list[int]]:
        data_array: Array[c_uint8] = (c_uint8 * length)()

        ret: ErrorCode = ErrorCode.lookup(
            device_ctrl.read_private_region(self._obj, signature, length, data_array)
        )
        if is_error_code(ret):
            return ret, []
        return ret, [data_array[i] for i in range(length)]

    def writePrivateRegion(
        self,
        signature: int,
        data: list[int] | bytes | bytearray,
    ) -> ErrorCode:
        if not isinstance(data, (list, bytes, bytearray)):
            raise TypeError("a list is required")

        data_array: Array[c_uint8] = (c_uint8 * len(data))(*data)

        ret: ErrorCode = ErrorCode.lookup(
            device_ctrl.write_private_region(
                self._obj, signature, len(data), data_array
            )
        )
        return ret

    def synchronizeTimeBase(self) -> ErrorCode:
        return ErrorCode.lookup(device_ctrl.synchronize_timebase(self._obj))

    def calculateAbsoluteTime(self, relativeTime: float) -> float:
        if not isinstance(relativeTime, float):
            raise TypeError("a float is required")
        return device_ctrl.calculate_absolute_time(self._obj, relativeTime)

    # properties
    @property
    def deviceNumber(self) -> int:
        return device_ctrl.get_device_number(self._obj)

    @property
    def description(self) -> bytes:
        descr: Array[c_wchar] = create_unicode_buffer(256)
        device_ctrl.get_description(self._obj, 256, descr)
        return descr.value.encode()

    @description.setter
    def description(self, desc: Array[c_wchar]) -> None:
        ret: ErrorCode = ErrorCode.lookup(
            device_ctrl.set_description(self._obj, len(desc), desc)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set description is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def accessMode(self) -> AccessMode:
        return utils.toAccessMode(device_ctrl.get_access_mode(self._obj))

    @property
    def productId(self) -> ProductId:
        return utils.toProductId(device_ctrl.get_product_id(self._obj))

    @property
    def boardId(self) -> int:
        return device_ctrl.get_board_id(self._obj)

    @boardId.setter
    def boardId(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("an in is required")
        ret: ErrorCode = ErrorCode.lookup(device_ctrl.set_board_id(self._obj, value))
        if is_error_code(ret):
            raise ValueError(
                f"set boardId is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def boardVersion(self) -> bytes:
        version: Array[c_wchar] = create_unicode_buffer(256)
        device_ctrl.get_board_version(self._obj, 256, version)
        return version.value.encode()

    @property
    def driverVersion(self) -> bytes:
        version: Array[c_wchar] = create_unicode_buffer(256)
        device_ctrl.get_driver_version(self._obj, 256, version)
        return version.value.encode()

    @property
    def dllVersion(self) -> bytes:
        version: Array[c_wchar] = create_unicode_buffer(256)
        device_ctrl.get_dll_version(self._obj, 256, version)
        return version.value.encode()

    @property
    def location(self) -> bytes:
        version: Array[c_wchar] = create_unicode_buffer(256)
        device_ctrl.get_location(self._obj, 256, version)
        return version.value.encode()

    @property
    def privateRegionLength(self) -> int:
        return device_ctrl.get_private_region_length(self._obj)

    @property
    def hotResetPreventable(self) -> int:
        return device_ctrl.get_hot_reset_preventable(self._obj)

    @property
    def baseAddresses(self) -> list[int]:
        return array.to_int64(device_ctrl.get_base_addresses(self._obj), True)

    @property
    def interrupts(self) -> list[int]:
        return array.to_int32(device_ctrl.get_interrupts(self._obj), True)

    @property
    def supportedTerminalBoard(self) -> list[TerminalBoard]:
        return array.to_terminal_board(
            device_ctrl.get_supported_terminal_board(self._obj), True
        )

    @property
    def supportedEvents(self) -> list[EventId]:
        return array.to_event_id(device_ctrl.get_supported_events(self._obj), True)

    @property
    def supportedScenarios(self) -> int:
        return device_ctrl.get_supported_scenarios(self._obj)

    @property
    def terminalBoard(self) -> TerminalBoard:
        return utils.toTerminalBoard(device_ctrl.get_terminal_board(self._obj))

    @terminalBoard.setter
    def terminalBoard(self, value: TerminalBoard) -> None:
        if not isinstance(value, TerminalBoard):
            raise TypeError("a TerminalBoard is required")
        ret: ErrorCode = ErrorCode.lookup(
            device_ctrl.set_terminal_board(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set terminalBoard is failed, the error code is 0x{ret.value:X}"
            )

    def setLocateEnabled(self, value: bool) -> ErrorCode:
        if not isinstance(value, bool):
            raise TypeError("a bool is required")
        return ErrorCode.lookup(device_ctrl.set_locate_enabled(self._obj, value))

    @property
    def installedDevices(self) -> list[DeviceTreeNode]:
        return array.to_device_tree_node(device_ctrl.get_installed_devices(), True)

    def getHwSpecific(self, name: Array[c_wchar]) -> tuple[ErrorCode, int | None]:
        data_array: Array[c_int32] = (c_int32 * 1)()
        size: c_int32 = c_int32(4)
        p_size: _Pointer[c_int32] = pointer(size)
        ret: ErrorCode = ErrorCode.lookup(
            device_ctrl.get_hw_specific(self._obj, name, p_size, data_array)
        )
        if ret == ErrorCode.Success:
            data = data_array[0]
        else:
            data = None
        return ret, data

    def setHwSpecific(self, name: Array[c_wchar], data: int) -> ErrorCode:
        data_array: Array[c_int32] = (c_int32 * 1)(data)
        ret: ErrorCode = ErrorCode.lookup(
            device_ctrl.set_hw_specific(self._obj, name, 4, data_array)
        )
        return ret
