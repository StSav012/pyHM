# noinspection PyProtectedMember
from _ctypes import Array, _Pointer
from ctypes import (
    POINTER,
    c_byte,
    c_double,
    c_int32,
    c_uint8,
    c_void_p,
    c_wchar,
    c_wchar_p,
)

from . import c_uint_, dll

__all__ = [
    "calculate_absolute_time",
    "get_access_mode",
    "get_base_addresses",
    "get_board_id",
    "get_board_version",
    "get_description",
    "get_device_number",
    "get_dll_version",
    "get_driver_version",
    "get_hot_reset_preventable",
    "get_hw_specific",
    "get_installed_devices",
    "get_interrupts",
    "get_location",
    "get_private_region_length",
    "get_product_id",
    "get_supported_events",
    "get_supported_scenarios",
    "get_supported_terminal_board",
    "get_terminal_board",
    "read_private_region",
    "read_register",
    "refresh",
    "set_board_id",
    "set_description",
    "set_hw_specific",
    "set_locate_enabled",
    "set_terminal_board",
    "synchronize_timebase",
    "write_private_region",
    "write_register",
]


def refresh(dev_obj: int) -> int:
    dll.TDeviceCtrl_Refresh.argtypes = [c_void_p]
    return dll.TDeviceCtrl_Refresh(dev_obj)


def read_register(
    dev_obj: int, space: int, offset: int, length: int, data_arr: Array[c_byte]
) -> int:
    dll.TDeviceCtrl_ReadRegister.argtypes = [
        c_void_p,
        c_int32,
        c_int32,
        c_int32,
        c_void_p,
    ]  # need attention
    return dll.TDeviceCtrl_ReadRegister(dev_obj, space, offset, length, data_arr)


def write_register(
    dev_obj: int, space: int, offset: int, length: int, data_arr: Array[c_byte]
) -> int:
    dll.TDeviceCtrl_WriteRegister.argtypes = [
        c_void_p,
        c_int32,
        c_int32,
        c_int32,
        c_void_p,
    ]  # need attention
    return dll.TDeviceCtrl_WriteRegister(dev_obj, space, offset, length, data_arr)


def read_private_region(
    dev_obj: int, signature: int, length: int, data_arr: Array[c_uint8]
) -> int:
    dll.TDeviceCtrl_ReadPrivateRegion.argtypes = [
        c_void_p,
        c_int32,
        c_int32,
        POINTER(c_uint8),
    ]  # need attention
    return dll.TDeviceCtrl_ReadPrivateRegion(dev_obj, signature, length, data_arr)


def write_private_region(
    dev_obj: int, signature: int, length: int, data_arr: Array[c_uint8]
) -> int:
    dll.TDeviceCtrl_WritePrivateRegion.argtypes = [
        c_void_p,
        c_int32,
        c_int32,
        POINTER(c_uint8),
    ]  # need attention
    return dll.TDeviceCtrl_WritePrivateRegion(dev_obj, signature, length, data_arr)


def synchronize_timebase(dev_obj: int) -> int:
    dll.TDeviceCtrl_SynchronizeTimebase.argtypes = [c_void_p]
    return dll.TDeviceCtrl_SynchronizeTimebase(dev_obj)


def calculate_absolute_time(dev_obj: int, relativeTime: float) -> float:
    dll.TDeviceCtrl_CalculateAbsoluteTime.restype = c_double
    dll.TDeviceCtrl_CalculateAbsoluteTime.argtypes = [c_void_p, c_double]
    return dll.TDeviceCtrl_CalculateAbsoluteTime(dev_obj, c_double(relativeTime))


def get_device_number(dev_obj: int) -> int:
    dll.TDeviceCtrl_getDeviceNumber.restype = c_int32
    dll.TDeviceCtrl_getDeviceNumber.argtypes = [c_void_p]
    return dll.TDeviceCtrl_getDeviceNumber(dev_obj)


def get_description(dev_obj: int, length: int, descr: Array[c_wchar]) -> int:
    dll.TDeviceCtrl_getDescription.argtypes = [
        c_void_p,
        c_int32,
        c_wchar_p,
    ]  # need attention
    return dll.TDeviceCtrl_getDescription(dev_obj, length, descr)


def set_description(dev_obj: int, length: int, descr: Array[c_wchar]) -> int:
    dll.TDeviceCtrl_setDescription.argtypes = [
        c_void_p,
        c_int32,
        c_wchar_p,
    ]  # need attention
    return dll.TDeviceCtrl_setDescription(dev_obj, length, descr)


def get_access_mode(dev_obj: int) -> int:
    dll.TDeviceCtrl_getAccessMode.argtypes = [c_void_p]
    return dll.TDeviceCtrl_getAccessMode(dev_obj)


def get_product_id(dev_obj: int) -> int:
    dll.TDeviceCtrl_getProductId.argtypes = [c_void_p]
    return dll.TDeviceCtrl_getProductId(dev_obj)


def get_board_id(dev_obj: int) -> int:
    dll.TDeviceCtrl_getBoardId.restype = c_int32
    dll.TDeviceCtrl_getBoardId.argtypes = [c_void_p]
    return dll.TDeviceCtrl_getBoardId(dev_obj)


def set_board_id(dev_obj: int, value: int) -> int:
    dll.TDeviceCtrl_setBoardId.argtypes = [c_void_p, c_int32]
    return dll.TDeviceCtrl_setBoardId(dev_obj, value)


def get_board_version(dev_obj: int, length: int, version: Array[c_wchar]) -> int:
    dll.TDeviceCtrl_getBoardVersion.argtypes = [c_void_p, c_int32, c_wchar_p]
    return dll.TDeviceCtrl_getBoardVersion(dev_obj, length, version)


def get_driver_version(dev_obj: int, length: int, version: Array[c_wchar]) -> int:
    dll.TDeviceCtrl_getDriverVersion.argtypes = [c_void_p, c_int32, c_wchar_p]
    return dll.TDeviceCtrl_getDriverVersion(dev_obj, length, version)


def get_dll_version(dev_obj: int, length: int, version: Array[c_wchar]) -> int:
    dll.TDeviceCtrl_getDllVersion.argtypes = [c_void_p, c_int32, c_wchar_p]
    return dll.TDeviceCtrl_getDllVersion(dev_obj, length, version)


def get_location(dev_obj: int, length: int, location: Array[c_wchar]) -> int:
    dll.TDeviceCtrl_getLocation.argtypes = [c_void_p, c_int32, c_wchar_p]
    return dll.TDeviceCtrl_getLocation(dev_obj, length, location)


def get_private_region_length(dev_obj: int) -> int:
    dll.TDeviceCtrl_getPrivateRegionLength.restype = c_int32
    dll.TDeviceCtrl_getPrivateRegionLength.argtypes = [c_void_p]
    return dll.TDeviceCtrl_getPrivateRegionLength(dev_obj)


def get_hot_reset_preventable(dev_obj: int) -> int:
    dll.TDeviceCtrl_getHotResetPreventable.restype = c_int32
    dll.TDeviceCtrl_getHotResetPreventable.argtypes = [c_void_p]
    return dll.TDeviceCtrl_getHotResetPreventable(dev_obj)


def get_base_addresses(dev_obj: int) -> int:
    dll.TDeviceCtrl_getBaseAddresses.argtypes = [c_void_p]
    dll.TDeviceCtrl_getBaseAddresses.restype = c_uint_
    return dll.TDeviceCtrl_getBaseAddresses(dev_obj)


def get_interrupts(dev_obj: int) -> int:
    dll.TDeviceCtrl_getInterrupts.argtypes = [c_void_p]
    dll.TDeviceCtrl_getInterrupts.restype = c_uint_
    return dll.TDeviceCtrl_getInterrupts(dev_obj)


def get_supported_terminal_board(dev_obj: int) -> int:
    dll.TDeviceCtrl_getSupportedTerminalBoard.argtypes = [c_void_p]
    dll.TDeviceCtrl_getSupportedTerminalBoard.restype = c_uint_
    return dll.TDeviceCtrl_getSupportedTerminalBoard(dev_obj)


def get_supported_events(dev_obj: int) -> int:
    dll.TDeviceCtrl_getSupportedEvents.argtypes = [c_void_p]
    dll.TDeviceCtrl_getSupportedEvents.restype = c_uint_
    return dll.TDeviceCtrl_getSupportedEvents(dev_obj)


def get_supported_scenarios(dev_obj: int) -> int:
    dll.TDeviceCtrl_getSupportedScenarios.restype = c_int32
    dll.TDeviceCtrl_getSupportedScenarios.argtypes = [c_void_p]
    return dll.TDeviceCtrl_getSupportedScenarios(dev_obj)


def get_terminal_board(dev_obj: int) -> int:
    dll.TDeviceCtrl_getTerminalBoard.argtypes = [c_void_p]
    return dll.TDeviceCtrl_getTerminalBoard(dev_obj)


def set_terminal_board(dev_obj: int, value: int) -> int:
    dll.TDeviceCtrl_setTerminalBoard.argtypes = [c_void_p, c_int32]
    return dll.TDeviceCtrl_setTerminalBoard(dev_obj, value)


def set_locate_enabled(dev_obj: int, value: int) -> int:
    dll.TDeviceCtrl_setLocateEnabled.argtypes = [c_void_p, c_int32]
    return dll.TDeviceCtrl_setLocateEnabled(dev_obj, value)


def get_installed_devices() -> int:
    dll.TDeviceCtrl_getInstalledDevices.restype = c_uint_
    return dll.TDeviceCtrl_getInstalledDevices()


def get_hw_specific(
    dev_obj: int,
    name: Array[c_wchar],
    pSize: "_Pointer[c_int32]",
    dataArr: Array[c_int32],
) -> int:
    dll.TDeviceCtrl_getHwSpecific.argtypes = [
        c_void_p,
        c_wchar_p,
        POINTER(c_int32),
        c_void_p,
    ]
    return dll.TDeviceCtrl_getHwSpecific(dev_obj, name, pSize, dataArr)


def set_hw_specific(
    dev_obj: int,
    name: Array[c_wchar],
    size: int,
    dataArr: Array[c_int32],
) -> int:
    dll.TDeviceCtrl_setHwSpecific.argtypes = [
        c_void_p,
        c_wchar_p,
        c_int32,
        c_void_p,
    ]
    return dll.TDeviceCtrl_setHwSpecific(dev_obj, name, size, dataArr)
