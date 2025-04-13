from ctypes import c_byte, c_int32, c_uint8

from . import c_uint_, dll

__all__ = ["get_mask", "get_port", "set_mask"]


def get_port(obj: int) -> int:
    dll.TDiCosintPort_getPort.restype = c_int32
    dll.TDiCosintPort_getPort.argtypes = [c_uint_]
    return dll.TDiCosintPort_getPort(obj)


def get_mask(obj: int) -> int:
    dll.TDiCosintPort_getMask.restype = c_byte
    dll.TDiCosintPort_getMask.argtypes = [c_uint_]
    return dll.TDiCosintPort_getMask(obj)


def set_mask(obj: int, value: int) -> int:
    dll.TDiCosintPort_setMask.argtypes = [c_uint_, c_uint8]
    return dll.TDiCosintPort_setMask(obj, value)
