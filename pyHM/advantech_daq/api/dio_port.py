from ctypes import c_int32, c_uint8

from . import c_uint_, dll

__all__ = [
    "get_di_inverse_port",
    "get_di_open_state",
    "get_direction",
    "get_do_circuit_type",
    "get_do_preset_value",
    "get_port",
    "set_di_inverse_port",
    "set_di_open_state",
    "set_direction",
    "set_do_circuit_type",
    "set_do_preset_value",
]


def get_port(obj: int) -> int:
    dll.TDioPort_getPort.restype = c_int32
    dll.TDioPort_getPort.argtypes = [c_uint_]
    return dll.TDioPort_getPort(obj)


def get_direction(obj: int) -> int:
    dll.TDioPort_getDirection.argtypes = [c_uint_]
    return dll.TDioPort_getDirection(obj)


def set_direction(obj: int, value: int) -> int:
    dll.TDioPort_setDirection.argtypes = [c_uint_, c_int32]
    return dll.TDioPort_setDirection(obj, value)


def get_di_inverse_port(obj: int) -> int:
    dll.TDioPort_getDiInversePort.restype = c_uint8
    dll.TDioPort_getDiInversePort.argtypes = [c_uint_]
    return dll.TDioPort_getDiInversePort(obj)


def set_di_inverse_port(obj: int, value: int) -> int:
    dll.TDioPort_setDiInversePort.argtypes = [c_uint_, c_uint8]
    return dll.TDioPort_setDiInversePort(obj, value)


def get_di_open_state(obj: int) -> int:
    dll.TDioPort_getDiOpenState.restype = c_uint8
    dll.TDioPort_getDiOpenState.argtypes = [c_uint_]
    return dll.TDioPort_getDiOpenState(obj)


def set_di_open_state(obj: int, value: int) -> int:
    dll.TDioPort_setDiOpenState.argtypes = [c_uint_, c_uint8]
    return dll.TDioPort_setDiOpenState(obj, value)


def get_do_preset_value(obj: int) -> int:
    dll.TDioPort_getDoPresetValue.restype = c_uint8
    dll.TDioPort_getDoPresetValue.argtypes = [c_uint_]
    return dll.TDioPort_getDoPresetValue(obj)


def set_do_preset_value(obj: int, value: int) -> int:
    dll.TDioPort_setDoPresetValue.argtypes = [c_uint_, c_uint8]
    return dll.TDioPort_setDoPresetValue(obj, value)


def get_do_circuit_type(obj: int) -> int:
    dll.TDioPort_getDoCircuitType.argtypes = [c_uint_]
    return dll.TDioPort_getDoCircuitType(obj)


def set_do_circuit_type(obj: int, value: int) -> int:
    dll.TDioPort_setDoCircuitType.argtypes = [c_uint_, c_int32]
    return dll.TDioPort_setDoCircuitType(obj, value)
