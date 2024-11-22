# -*- coding:utf-8 -*-
from ctypes import POINTER, byref, c_int32, c_void_p, c_wchar_p

from advantech_daq import DeviceInformation
from advantech_daq.api import c_uint_, dll

__all__ = [
    "create",
    "load_profile",
    "add_event_handler",
    "cleanup",
    "dispose",
    "get_device",
    "get_module",
    "get_selected_device",
    "get_state",
    "get_supported_devices",
    "get_supported_modes",
    "remove_event_handler",
    "set_selected_device",
]


def add_event_handler(obj: int, eventId: int, eventProc: int, userParam: int) -> None:
    dll.TDaqCtrlBase_addEventHandler.argtypes = [c_uint_]
    dll.TDaqCtrlBase_addEventHandler(
        obj, eventId, eventProc, userParam
    )  # after add types


def remove_event_handler(
    obj: int, eventId: int, eventProc: int, userParam: int
) -> None:
    dll.TDaqCtrlBase_removeEventHandler.argtypes = [c_uint_]
    dll.TDaqCtrlBase_removeEventHandler(
        obj, eventId, eventProc, userParam
    )  # after add types


def cleanup(obj: int) -> None:
    dll.TDaqCtrlBase_Cleanup.argtypes = [c_uint_]
    dll.TDaqCtrlBase_Cleanup(obj)


def dispose(obj: int) -> None:
    dll.TDaqCtrlBase_Dispose.argtypes = [c_uint_]
    dll.TDaqCtrlBase_Dispose(obj)


def get_selected_device(obj: int, devInfo: DeviceInformation) -> int:
    dll.TDaqCtrlBase_getSelectedDevice.argtypes = [
        c_uint_,
        POINTER(DeviceInformation),
    ]
    return dll.TDaqCtrlBase_getSelectedDevice(obj, byref(devInfo))


def set_selected_device(obj: int, devInfo: DeviceInformation) -> int:
    dll.TDaqCtrlBase_setSelectedDevice.argtypes = [
        c_uint_,
        POINTER(DeviceInformation),
    ]
    return dll.TDaqCtrlBase_setSelectedDevice(obj, byref(devInfo))


def get_state(obj: int) -> int:
    dll.TDaqCtrlBase_getState.argtypes = [c_uint_]
    return dll.TDaqCtrlBase_getState(obj)


def get_device(obj: int) -> int:
    dll.TDaqCtrlBase_getDevice.argtypes = [c_uint_]
    dll.TDaqCtrlBase_getDevice.restype = c_void_p
    return dll.TDaqCtrlBase_getDevice(obj)


def get_supported_devices(obj: int) -> int:
    dll.TDaqCtrlBase_getSupportedDevices.argtypes = [c_uint_]
    dll.TDaqCtrlBase_getSupportedDevices.restype = c_uint_
    return dll.TDaqCtrlBase_getSupportedDevices(obj)


def get_supported_modes(obj: int) -> int:
    dll.TDaqCtrlBase_getSupportedModes.argtypes = [c_uint_]
    dll.TDaqCtrlBase_getSupportedModes.restype = c_uint_
    return dll.TDaqCtrlBase_getSupportedModes(obj)


def create(scenario: int) -> int:
    dll.TDaqCtrlBase_Create.argtypes = [c_int32]
    dll.TDaqCtrlBase_Create.restype = c_uint_
    return dll.TDaqCtrlBase_Create(scenario)


def get_module(obj: int) -> int:
    dll.TDaqCtrlBase_getModule.argtypes = [c_uint_]
    dll.TDaqCtrlBase_getModule.restype = c_void_p
    return dll.TDaqCtrlBase_getModule(obj)


def load_profile(obj: int, profile: str) -> int:
    dll.TDaqCtrlBase_LoadProfile.argtypes = [c_uint_, c_wchar_p]
    return dll.TDaqCtrlBase_LoadProfile(obj, profile)
