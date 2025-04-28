from _ctypes import Array
from ctypes import POINTER, c_double, c_int16, c_int32, c_void_p

from .. import DataMark
from . import c_uint_, dll

__all__ = [
    "get_data",
    "prepare",
    "start",
    "stop",
    "get_conversion",
    "get_record",
    "get_trigger",
]


def prepare(obj: int) -> int:
    dll.TWaveformAiCtrl_Prepare.argtypes = [c_uint_]
    return dll.TWaveformAiCtrl_Prepare(obj)


def start(obj: int) -> int:
    dll.TWaveformAiCtrl_Start.argtypes = [c_uint_]
    return dll.TWaveformAiCtrl_Start(obj)


def stop(obj: int) -> int:
    dll.TWaveformAiCtrl_Stop.argtypes = [c_uint_]
    return dll.TWaveformAiCtrl_Stop(obj)


def get_data(
    obj: int,
    dt: int,
    count: int,
    buffer: Array[c_int16] | Array[c_int32] | Array[c_double],
    timeout: int,
    returned: Array[c_int32],
    startTime: Array[c_double] | None,
    markCount: Array[c_int32] | None,
    markBuf: Array[DataMark] | None,
) -> int:
    dll.TWaveformAiCtrl_GetData.argtypes = [
        c_uint_,
        c_int32,
        c_int32,
        c_void_p,
        c_int32,
        POINTER(c_int32),
        POINTER(c_double),
        POINTER(c_int32),
        POINTER(DataMark),
    ]
    return dll.TWaveformAiCtrl_GetData(
        obj, dt, count, buffer, timeout, returned, startTime, markCount, markBuf
    )


def get_conversion(obj: int) -> int:
    dll.TWaveformAiCtrl_getConversion.argtypes = [c_uint_]
    dll.TWaveformAiCtrl_getConversion.restype = c_uint_
    return dll.TWaveformAiCtrl_getConversion(obj)


def get_record(obj: int) -> int:
    dll.TWaveformAiCtrl_getRecord.argtypes = [c_uint_]
    dll.TWaveformAiCtrl_getRecord.restype = c_uint_
    return dll.TWaveformAiCtrl_getRecord(obj)


def get_trigger(obj: int, trigIdx: int) -> int:
    dll.TWaveformAiCtrl_getTrigger.argtypes = [c_uint_, c_int32]
    dll.TWaveformAiCtrl_getTrigger.restype = c_uint_
    return dll.TWaveformAiCtrl_getTrigger(obj, trigIdx)
