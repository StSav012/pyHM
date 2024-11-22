# -*- coding:utf-8 -*-
from _ctypes import Array
from ctypes import c_uint8
from typing import Iterable

from advantech_daq import ErrorCode, Scenario
from advantech_daq.api import instant_do_ctrl
from advantech_daq.dio_ctrl_base import DIOCtrlBase


class InstantDoCtrl(DIOCtrlBase):
    def __init__(self, dev_info: str, profile_path: str = "") -> None:
        super().__init__(Scenario.InstantDO, dev_info, profile_path)

    def writeAny(self, start_port: int, data: Iterable[int]) -> ErrorCode:
        """port count == len(data)"""
        data = list(data)
        data_array = (c_uint8 * len(data))(*data)
        ret: int = instant_do_ctrl.write_any(
            self._obj, start_port, len(data), data_array
        )
        return ErrorCode.lookup(ret)

    def writeBit(self, port: int, bit: int, data: bool | int) -> ErrorCode:
        ret: int = instant_do_ctrl.write_bit(self._obj, port, bit, data)
        return ErrorCode.lookup(ret)

    def readAny(self, portStart: int, portCount: int) -> tuple[ErrorCode, list[int]]:
        data_array: Array[c_uint8] = (c_uint8 * portCount)()
        ret: int = instant_do_ctrl.read_any(self._obj, portStart, portCount, data_array)
        return ErrorCode.lookup(ret), [data_array[i] for i in range(portCount)]

    def readBit(self, port: int, bit: int) -> tuple[ErrorCode, int]:
        data_array: Array[c_uint8] = (c_uint8 * 1)()
        ret: int = instant_do_ctrl.read_bit(self._obj, port, bit, data_array)
        return ErrorCode.lookup(ret), data_array[0]
