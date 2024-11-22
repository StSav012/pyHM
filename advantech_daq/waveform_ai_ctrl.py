# -*- coding:utf-8 -*-
from _ctypes import Array, sizeof
from ctypes import c_double, c_int, c_int16, c_int32

from advantech_daq import DataMark, ErrorCode, Scenario
from advantech_daq.ai_ctrl_base import AICtrlBase
from advantech_daq.api import waveform_ai_ctrl
from advantech_daq.conversion import Conversion
from advantech_daq.record import Record
from advantech_daq.trigger import Trigger

__all__ = ["WaveformAICtrl"]


class WaveformAICtrl(AICtrlBase):
    def __init__(self, dev_info: str, profile_path: str = ""):
        self._conversion: Conversion | None = None
        self._record: Record | None = None
        self._triggers: list[Trigger] = []
        # self._triggers.append(Trigger(None))
        # self._triggers = []
        super().__init__(Scenario.WaveformAI, dev_info, profile_path)

    @property
    def conversion(self) -> Conversion:
        if self._conversion is None:
            self._conversion = Conversion(
                waveform_ai_ctrl.get_conversion(self._obj),
                self.features.channelCountMax,
            )
        return self._conversion

    @property
    def record(self) -> Record:
        if self._record is None:
            self._record = Record(waveform_ai_ctrl.get_record(self._obj))
        return self._record

    @property
    def trigger(self) -> list[Trigger]:
        if not self._triggers:
            for i in range(self.features.triggerCount):
                self._triggers.append(
                    Trigger(waveform_ai_ctrl.get_trigger(self._obj, i))
                )
        return self._triggers

    def prepare(self) -> ErrorCode:
        return ErrorCode.lookup(waveform_ai_ctrl.prepare(self._obj))

    def start(self) -> ErrorCode:
        return ErrorCode.lookup(waveform_ai_ctrl.start(self._obj))

    def stop(self) -> ErrorCode:
        return ErrorCode.lookup(waveform_ai_ctrl.stop(self._obj))

    def getDataI16(
        self,
        count: int,
        timeout: int = 0,
        startTime: float | None = None,
        markCount: int | None = None,
    ) -> tuple[
        ErrorCode,
        list[int] | list[float],
        None | float,
        None | list[DataMark],
    ]:
        return self.__getData(c_int16, count, timeout, startTime, markCount)

    def getDataI32(
        self,
        count: int,
        timeout: int = 0,
        startTime: float | None = None,
        markCount: int | None = None,
    ) -> tuple[
        ErrorCode,
        list[int] | list[float],
        None | float,
        None | list[DataMark],
    ]:
        return self.__getData(c_int32, count, timeout, startTime, markCount)

    def getDataF64(
        self,
        count: int,
        timeout: int = 0,
        startTime: float | None = None,
        markCount: int | None = None,
    ) -> tuple[
        ErrorCode,
        list[int] | list[float],
        None | float,
        None | list[DataMark],
    ]:
        return self.__getData(c_double, count, timeout, startTime, markCount)

    def __getData(
        self,
        dtype: type[c_int16] | type[c_int32] | type[c_double],
        count: int,
        timeout: int,
        startTime: float | None,
        markCount: int | None,
    ) -> tuple[
        ErrorCode,
        list[int] | list[float],
        None | float,
        None | list[DataMark],
    ]:
        data_arr: Array[c_int16] | Array[c_int32] | Array[c_double] = (dtype * count)()

        returned: Array[c_int] = (c_int * 1)()
        start_time_clock: Array[c_double] | None
        if startTime is not None:
            start_time_clock = (c_double * 1)(startTime)
        else:
            start_time_clock = None

        mark_buf_tmp: Array[DataMark] | None
        mark_count_tmp: Array[c_int32] | None
        if markCount is not None and isinstance(markCount, int):
            mark_buf_tmp = (DataMark * markCount)()
            mark_count_tmp = (c_int32 * 1)(markCount)
        else:
            mark_buf_tmp = None
            mark_count_tmp = None

        ret: ErrorCode = ErrorCode.lookup(
            waveform_ai_ctrl.get_data(
                self._obj,
                sizeof(dtype),
                count,
                data_arr,
                timeout,
                returned,
                start_time_clock,
                mark_count_tmp,
                mark_buf_tmp,
            )
        )

        return (
            ret,
            [data_arr[i] for i in range(returned[0])],
            None if start_time_clock is None else start_time_clock[0],
            (
                None
                if mark_count_tmp is None or mark_buf_tmp is None
                else [mark_buf_tmp[i] for i in range(mark_count_tmp[0])]
            ),
        )
