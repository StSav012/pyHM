# -*- coding:utf-8 -*-
from _ctypes import Array
from ctypes import c_uint8

from advantech_daq import ErrorCode, Scenario
from advantech_daq.api import array, instant_di_ctrl, is_error_code
from advantech_daq.di_cos_int_port import DICosIntPort
from advantech_daq.di_int_channel import DIIntChannel
from advantech_daq.di_pm_int_port import DIPmIntPort
from advantech_daq.dio_ctrl_base import DIOCtrlBase
from advantech_daq.noise_filter_channel import NoiseFilterChannel

__all__ = ["InstantDICtrl"]


class InstantDICtrl(DIOCtrlBase):
    def __init__(self, dev_info: str, profile_path: str = "") -> None:
        self._nosFltChans: list[NoiseFilterChannel] = []
        # self._nosFltChans.append(NosFltChannel(None))
        # self._nosFltChans = []
        self._intChans: list[DIIntChannel] = []
        # self._intChans.append(DIIntChannel(None))
        # self._intChans = []
        self._cosPorts: list[DICosIntPort] = []
        # self._cosPorts.append(DICosIntPort(None))
        # self._cosPorts = []
        self._pmPorts: list[DIPmIntPort] = []
        # self._pmPorts.append(DIPmIntPort(None))
        # self._pmPorts = []
        super().__init__(
            Scenario.InstantDI,
            dev_info,
            profile_path,
        )

    @property
    def noiseFilterBlockTime(self) -> float:
        return instant_di_ctrl.get_noise_filter_block_time(self._obj)

    @noiseFilterBlockTime.setter
    def noiseFilterBlockTime(self, value: int | float) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError("a float is required")
        ret: ErrorCode = ErrorCode.lookup(
            instant_di_ctrl.set_noise_filter_block_time(self._obj, value)
        )
        if is_error_code(ret):
            raise ValueError(
                f"set noiseFilterBlockTime is failed, the error code is 0x{ret.value:X}"
            )

    @property
    def noiseFilter(self) -> list[NoiseFilterChannel]:
        if not self._nosFltChans:
            native_arr = instant_di_ctrl.get_noise_filter(self._obj)
            count: int = array.get_length(native_arr)
            for i in range(count):
                self._nosFltChans.append(
                    NoiseFilterChannel(array.get_item(native_arr, i))
                )
        return self._nosFltChans

    @property
    def diIntChannels(self) -> list[DIIntChannel]:
        if not self._intChans:
            native_array = instant_di_ctrl.get_diint_channels(self._obj)
            count: int = array.get_length(native_array)
            for i in range(count):
                self._intChans.append(DIIntChannel(array.get_item(native_array, i)))
        return self._intChans

    @property
    def diCosIntPorts(self) -> list[DICosIntPort]:
        if not self._cosPorts:
            native_array = instant_di_ctrl.get_di_cosint_ports(self._obj)
            count: int = array.get_length(native_array)
            for i in range(count):
                self._cosPorts.append(DICosIntPort(array.get_item(native_array, i)))
        return self._cosPorts

    @property
    def diPmIntPorts(self) -> list[DIPmIntPort]:
        if not self._pmPorts:
            native_array = instant_di_ctrl.get_di_pmint_ports(self._obj)
            count: int = array.get_length(native_array)
            for i in range(count):
                self._pmPorts.append(DIPmIntPort(array.get_item(native_array, i)))
        return self._pmPorts

    def readAny(self, portStart: int, portCount: int) -> tuple[ErrorCode, list[int]]:
        data_array: Array[c_uint8] = (c_uint8 * portCount)()
        ret: int = instant_di_ctrl.read_any(self._obj, portStart, portCount, data_array)
        return ErrorCode.lookup(ret), [data_array[i] for i in range(portCount)]

    def readBit(self, port: int, bit: int) -> tuple[ErrorCode, int]:
        data_array: Array[c_uint8] = (c_uint8 * 1)()
        ret: int = instant_di_ctrl.read_bit(self._obj, port, bit, data_array)
        return ErrorCode.lookup(ret), data_array[0]
