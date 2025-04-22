import logging
import traceback
from contextlib import suppress
from math import cos, exp, isnan, log, nan, radians
from os import getenv, linesep
from typing import ClassVar, Final

from qtpy.QtCore import (
    QDateTime,
    QDir,
    QFile,
    QIODevice,
    QObject,
    QTextStream,
    QThread,
    Qt,
    Signal,
)

from .advantech_daq import AISignalType, ErrorCode, ValueRange
from .advantech_daq.api import adx_enum_to_string, is_error_code
from .advantech_daq.instant_ao_ctrl import InstantAOCtrl
from .advantech_daq.instant_di_ctrl import InstantDICtrl
from .advantech_daq.instant_do_ctrl import InstantDoCtrl
from .advantech_daq.waveform_ai_ctrl import WaveformAICtrl
from .constants import (
    DI_MOTOR_ZERO,
    DO_DIRECTION,
    DO_MOTOR_STEP_PULSE,
    RECEIVERS,
    RECEIVER_MARK_TYPE,
    WAVELENGTHS,
    DEVICE_DESCRIPTION,
    PHI_H2O_CAL,
    ELEVATION_CAL,
    ATMOSPHERE_THICKNESS_O2,
    TAU_O2_CAL,
)
from .numeric import tau_by_min_square_method_kd
from .settings import Settings

__all__ = ["ThreadHM"]

sectionLength = 1024

logger: logging.Logger = logging.getLogger("ThreadHM")
logging.basicConfig(
    level=logging.getLevelNamesMapping().get(
        getenv("LOG_LEVEL", "").upper(), logging.INFO
    )
)


class ThreadHM(QThread):
    stateChanged: ClassVar[Signal] = Signal(str, int, int)
    dataObtained: ClassVar[Signal] = Signal(RECEIVER_MARK_TYPE, int, float)
    absorptionCalculated: ClassVar[Signal] = Signal(
        QDateTime, RECEIVER_MARK_TYPE, float, float
    )
    dataFileChanged: ClassVar[Signal] = Signal(str)

    def __init__(self, settings: Settings, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.settings: Settings = settings
        self.motor_position: float = 0.0

        # инициализация устройства "0" для измерения
        self._emit_state(self.tr("Initializing…"), 0, 0)

        channel_count: Final[int] = self.settings.channel_count
        sample_rate: Final[float] = self.settings.sample_rate

        # инициализация АЦП
        self.wf_ai_ctrl: WaveformAICtrl = WaveformAICtrl(DEVICE_DESCRIPTION)
        self.wf_ai_ctrl.conversion.channelStart = 0
        self.wf_ai_ctrl.conversion.channelCount = channel_count
        self.wf_ai_ctrl.conversion.clockRate = sample_rate
        for channel in self.wf_ai_ctrl.channels:
            channel.signalType = AISignalType.Differential

        # инициализация ЦАП
        self.instant_ao: InstantAOCtrl = InstantAOCtrl(DEVICE_DESCRIPTION)
        self._dac: Final[dict[RECEIVER_MARK_TYPE, list[float]]] = self.settings.dac
        for receiver, channel in zip(RECEIVERS, self.instant_ao.channels):
            # find best output range
            min_dac: float = min(self._dac[receiver])
            max_dac: float = max(self._dac[receiver])
            max_abs_dac: float = max(abs(min_dac), abs(max_dac))
            value_range: ValueRange = ValueRange.V_Neg10To10

            for limit, range_key in zip(
                [5.0, 10.0],
                [ValueRange.V_Neg5To5, ValueRange.V_Neg10To10],
                strict=True,
            ):
                if max_abs_dac <= limit:
                    value_range = range_key
                    break

            # noinspection PyPep8Naming
            channel.valueRange = value_range

        self.instant_di_ctrl: InstantDICtrl = InstantDICtrl(DEVICE_DESCRIPTION)
        self.instant_do_ctrl: InstantDoCtrl = InstantDoCtrl(DEVICE_DESCRIPTION)

        self._emit_state(self.tr("Initialized"))

    def _is_error_occurred(self, ret: ErrorCode) -> bool:
        if is_error_code(ret):
            self._emit_state(
                self.tr("Error {}: {}").format(
                    hex(ret.value),
                    adx_enum_to_string("ErrorCode", ret.value, 256),
                ),
            )
            traceback.print_stack()
            return True
        return False

    def _emit_state(self, msg: str, pos: int = 0, max_pos: int = 0) -> None:
        if max_pos <= 0.0:
            logger.info(msg)
        else:
            logger.debug(msg)
        self.stateChanged.emit(msg, pos, max_pos)

    def get_di_bit(self, bit_num: int) -> bool:
        ret: ErrorCode
        data: int
        ret, data = self.instant_di_ctrl.readBit(0, bit_num)
        if self._is_error_occurred(ret):
            return False
        logger.debug(f"Read data {data} from bit #{bit_num}")
        return bool(data)

    def set_do_bit(self, bit_num: int, value: bool) -> None:
        logger.debug(f"Writing data {value} to bit #{bit_num}")
        ret: ErrorCode = self.instant_do_ctrl.writeBit(0, bit_num, value)
        self._is_error_occurred(ret)

    def motor_get_zero(self) -> bool:
        v: bool = self.get_di_bit(DI_MOTOR_ZERO)
        logger.debug(f"At zero? {v}")
        return v

    def motor_step(self, direction: bool) -> None:
        # Направление
        self.set_do_bit(DO_DIRECTION, direction)
        QThread.msleep(1)
        # Шаг
        for on in (True, False):
            self.set_do_bit(DO_MOTOR_STEP_PULSE, on)
            QThread.msleep(10)
        # Положение
        if direction:
            self.motor_position -= self.settings.motor_const
        else:
            self.motor_position += self.settings.motor_const

    def motor_find_zero(self) -> None:
        for i in range(500):
            if self.motor_get_zero():
                self.motor_position = -self.settings.angle_correction
                self.motor_set_angle(0)
            else:
                self.motor_step(True)

    def motor_set_angle(self, angle: float) -> None:
        # разница положения в количестве шагов
        step_count: int = round(
            (angle - self.motor_position) / self.settings.motor_const
        )
        # направление
        if direction := (step_count < 0):
            step_count = -step_count
        # вращение
        for i in range(step_count):
            self.motor_step(direction)

    def run(self) -> None:
        angles: Final[list[float]] = self.settings.angles
        if not angles:
            self._emit_state(self.tr("Error: no angles provided"))
            return
        # date_time_start: Final[QDateTime] = self.settings.date_time_start
        # date_time_stop: Final[QDateTime] = self.settings.date_time_stop
        cycle_count: Final[int] = self.settings.cycle_count
        channel_count: Final[int] = self.settings.channel_count
        sample_count: Final[int] = self.settings.sample_count
        save_adc: Final[bool] = self.settings.save_adc
        result_dir: Final[QDir] = self.settings.result_dir
        altitude: Final[float] = self.settings.elevation
        interval: Final[float] = self.settings.interval

        if not result_dir.exists():
            parents: list[str] = [result_dir.dirName()]
            while result_dir.cdUp() and not result_dir.exists():
                parents.append(result_dir.dirName())
            for parent in reversed(parents):
                result_dir.mkdir(parent)
                result_dir.cd(parent)

        # Создание файла с результатом
        file_data: QFile = QFile(
            result_dir.filePath(
                QDateTime.currentDateTime().toString("yyyy-MM-dd_hh-mm-ss") + ".dat"
            )
        )
        if not file_data.open(
            QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text
        ):
            self._emit_state(
                self.tr("Error {}: {}").format(
                    file_data.error(), file_data.errorString()
                )
            )
            return

        file_data_stream: QTextStream = QTextStream(file_data)
        file_data_stream << self.settings.toString() << linesep
        file_data_stream << "[Данные]" << linesep
        for wavelength in WAVELENGTHS:
            (
                file_data_stream
                << "\t".join(
                    (
                        f"{wavelength}мм_2Угла",
                        f"{wavelength}мм_{len(angles) - 1}Углов",
                        "   +/-   ",
                        f"{wavelength}мм Q г/см2",
                    )
                )
                << "\t"
            )
        file_data_stream << "\t".join(("Дата/Время_наблюдения", "TDateTime")) << "\t"
        for wavelength in WAVELENGTHS:
            (
                file_data_stream
                << "\t".join(
                    f"{wavelength}мм_SD_{index}" for index in range(len(angles))
                )
                << "\t"
            )
        file_data_stream << "Описание" << linesep
        file_data_stream.flush()

        self.dataFileChanged.emit(file_data.fileName())

        # Время начала измерения
        # while (
        #     not self.isInterruptionRequested()
        #     and date_time_start > QDateTime.currentDateTime()
        # ):
        #     self._emit_state(
        #         self.tr("Measurement will start at {}").format(
        #             date_time_start.toString()
        #         )
        #     )
        #     QThread.sleep(1)

        ret: ErrorCode

        # Основной цикл...
        while not self.isInterruptionRequested() and (
            now := QDateTime.currentDateTime()
        ):  # < date_time_stop
            # Мотор -> 0
            self._emit_state(self.tr("Mirror → “0”"))
            self.motor_find_zero()
            QThread.sleep(1)

            data_sd: dict[RECEIVER_MARK_TYPE, list[float]] = {"0": [], "1": []}
            data_mean: dict[RECEIVER_MARK_TYPE, list[float]] = {"0": [], "1": []}
            data_res: dict[RECEIVER_MARK_TYPE, float] = {"0": nan, "1": nan}
            tau0: dict[RECEIVER_MARK_TYPE, float] = {"0": nan, "1": nan}
            d_tau: dict[RECEIVER_MARK_TYPE, float] = {"0": nan, "1": nan}
            lnk_tav_t_rel: dict[RECEIVER_MARK_TYPE, float] = {"0": nan, "1": nan}
            d_lnk_tav_t_rel: dict[RECEIVER_MARK_TYPE, float] = {"0": nan, "1": nan}
            tau_o2: dict[RECEIVER_MARK_TYPE, float] = {"0": nan, "1": nan}
            q_g_per_sm2: dict[RECEIVER_MARK_TYPE, float] = {"0": nan, "1": nan}
            for index, angle in enumerate(angles):
                if self.isInterruptionRequested():
                    break

                # Установка угла наблюдения
                self._emit_state(
                    self.tr("Setting angle #{} = {}°").format(index, round(angle, 3))
                )
                self.motor_set_angle(angle)
                QThread.sleep(2)

                data_adc: dict[int, list[list[float]]] = {}
                # Измерение
                for cycle in range(cycle_count):
                    if self.isInterruptionRequested():
                        break

                    self._emit_state(
                        self.tr("Measuring at angle #{} = {}°…").format(
                            index, round(angle, 3)
                        ),
                        cycle,
                        cycle_count,
                    )
                    # полупериоды
                    for period in (0, 1):
                        logger.debug(f"Period {period}")
                        # установка напряжения ЦАПов
                        ret = self.instant_ao.writeAny(
                            0,
                            None,
                            [self._dac[receiver][period] for receiver in RECEIVERS],
                        )
                        if self._is_error_occurred(ret):
                            return

                        # сбор данных
                        data: list[float] = []
                        data_piece: list[float]
                        while len(data) < channel_count * sample_count:
                            if self.isInterruptionRequested():
                                break
                            ret = self.wf_ai_ctrl.prepare()
                            if self._is_error_occurred(ret):
                                return
                            ret = self.wf_ai_ctrl.start()
                            if self._is_error_occurred(ret):
                                return
                            (
                                ret,
                                data_piece,
                                *_,
                            ) = self.wf_ai_ctrl.getDataF64(
                                channel_count * sample_count - len(data), -1
                            )
                            if self._is_error_occurred(ret):
                                return
                            data.extend(data_piece)
                            logger.debug(
                                f"Got {len(data) / channel_count * sample_count:.2%} of data"
                            )
                        if period not in data_adc:
                            data_adc[period] = []
                        data_adc[period].append(data)
                        ret = self.wf_ai_ctrl.stop()
                        if self._is_error_occurred(ret):
                            return
                # цикл измерения

                if self.isInterruptionRequested():
                    break

                # установка напряжения ЦАПов в “0”
                ret = self.instant_ao.writeAny(
                    0,
                    None,
                    [0 for _receiver in RECEIVERS],
                )
                if self._is_error_occurred(ret):
                    return

                # Расчет результата синхронного детектирования для текущего угла каждого приемника
                for receiver, wavelength in zip(RECEIVERS, WAVELENGTHS, strict=True):
                    self._emit_state(
                        self.tr("Calculating results for {}-mm receiver…").format(
                            wavelength
                        )
                    )

                    mean = [
                        sum(
                            sum(d_cycle[int(receiver) :: channel_count])
                            / (len(d_cycle) // channel_count)
                            for d_cycle in data_adc[period]
                        )
                        / len(data_adc[period])
                        for period in (0, 1)
                    ]

                    data_sd[receiver].append((mean[0] - mean[1]) / 2)
                    data_mean[receiver].append((mean[0] + mean[1]) / 2)

                    self.dataObtained.emit(receiver, index, data_mean[receiver][-1])

                # сохранение служебного файла
                if save_adc:
                    file_adc: QFile = QFile(
                        result_dir.filePath(
                            now.toString("yyyy-MM-dd_hh-mm-ss-zzz") + ".dat"
                        )
                    )
                    if file_adc.open(
                        QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text
                    ):
                        file_adc_stream: QTextStream = QTextStream(file_adc)
                        for cycle in range(cycle_count):
                            self._emit_state(
                                self.tr("Saving debug data…"),
                                cycle,
                                cycle_count,
                            )
                            for period in (0, 1):
                                for sample in range(sample_count):
                                    str_buf: list[str] = [
                                        str(
                                            sample + (period + cycle * 2) * sample_count
                                        )
                                    ]
                                    for channel in range(channel_count):
                                        str_buf.append(
                                            "%e"
                                            % data_adc[period][cycle][
                                                sample * sample_count + channel
                                            ]
                                        )
                                    file_adc_stream << "\t".join(str_buf) << linesep

                        (
                            file_adc_stream
                            << "\t".join(("Receiver", "Angle", "SD", "Mean"))
                            << linesep
                        )

                        for receiver in RECEIVERS:
                            (
                                file_adc_stream
                                << "\t".join(
                                    map(
                                        str,
                                        (
                                            receiver,
                                            index,
                                            data_sd[receiver][index],
                                            data_mean[receiver][index],
                                        ),
                                    )
                                )
                                << linesep
                            )

                        file_adc.close()
                    else:
                        self._emit_state(
                            self.tr("Error {}: {}").format(
                                file_adc.error(), file_adc.errorString()
                            )
                        )
            # углы измерения

            if self.isInterruptionRequested():
                break

            # Расчет поглощения
            self._emit_state(self.tr("Absorption calculation…"))
            description: str = ""

            for receiver, wavelength in zip(RECEIVERS, WAVELENGTHS, strict=True):
                description += "Пр.{}мм:".format(wavelength)

                a: float
                b: float = nan
                c: float = nan
                index = len(angles) - 1
                while index > 0:
                    angle = angles[index]
                    description += "Угол{}:".format(index)
                    # первый косинус
                    a = cos(radians(angle))
                    if a == 0.0:
                        description += "Первый косинус = 0;"
                        index -= 1
                        continue
                    # второй косинус
                    b = cos(radians(angles[0]))
                    if b == 0.0:
                        description += "Второй косинус = 0;"
                        index -= 1
                        break
                    # разность косинусов
                    b = 1 / a - 1 / b
                    if b == 0.0:
                        description += "Разность косинусов = 0;"
                        index -= 1
                        continue
                    # знаменатель в логарифме
                    c = data_sd[receiver][-1] - data_sd[receiver][index]
                    if c == 0.0:
                        description += "Знаменатель в логарифме = 0;"
                        index -= 1
                        continue
                    e = data_sd[receiver][-1] - data_sd[receiver][0]
                    # Знак аргумента логарифма
                    c = e / c
                    if c < 0.0:
                        description += "Знак аргумента логарифма;"
                        index -= 1
                        continue
                    break
                # углы
                # расчет поглощения
                if index < 1:
                    description += "?!; "
                elif isnan(b) or isnan(c) or b == 0.0 or c <= 0.0:
                    description += "bad; "
                else:
                    description += "Ok; "
                    data_res[receiver] = (1 / b) * log(c)
            # Приемники

            for receiver in RECEIVERS:
                # Наименьшие квадраты по 11 углам
                (
                    tau0[receiver],
                    d_tau[receiver],
                    lnk_tav_t_rel[receiver],
                    d_lnk_tav_t_rel[receiver],
                ) = tau_by_min_square_method_kd(
                    angles,
                    data_sd[receiver],
                    data_sd[receiver][-1],
                )
                tau_o2[receiver] = TAU_O2_CAL[receiver] * exp(
                    -(altitude - ELEVATION_CAL) / ATMOSPHERE_THICKNESS_O2
                )
                q_g_per_sm2[receiver] = (tau0[receiver] - tau_o2["1"]) / PHI_H2O_CAL[
                    receiver
                ]

            # Сохранение данных
            self._emit_state(self.tr("Saving data…"))
            for receiver in RECEIVERS:
                (
                    file_data_stream
                    << "\t".join(
                        map(
                            lambda x: "%5.4e" % x,
                            (
                                data_res[receiver],
                                tau0[receiver],
                                d_tau[receiver],
                                q_g_per_sm2[receiver],
                            ),
                        )
                    )
                    << "\t"
                )
            (file_data_stream << now.toString(Qt.DateFormat.ISODate) << "\t")
            # time as number
            (
                file_data_stream
                << QDateTime(1899, 12, 29, 23, 30, 17).msecsTo(now) / 86400e3
                << "\t"
            )
            for receiver in RECEIVERS:
                (
                    file_data_stream
                    << "\t".join(map(lambda x: "%5.4e" % x, data_sd[receiver]))
                    << "\t"
                )
            file_data_stream << description << linesep
            file_data_stream.flush()

            # данные на форму
            for receiver in RECEIVERS:
                self.absorptionCalculated.emit(
                    now,
                    receiver,
                    data_res[receiver],
                    tau0[receiver],
                )

            # Интервал между циклами
            for i in range(int(interval)):
                if self.isInterruptionRequested():
                    break
                self._emit_state(
                    self.tr("Waiting between measurements for {} sec.").format(
                        interval
                    ),
                    i,
                    round(interval),
                )
                QThread.sleep(1)
            if not interval.is_integer() and not self.isInterruptionRequested():
                QThread.usleep(round(1_000_000 * (interval // 1)))

        self._emit_state(self.tr("Measurement is finished"))

    def __del__(self) -> None:
        # `RuntimeError`: wrapped C/C++ object of type ThreadHM has been deleted
        #  appears when deleting the instance, using PyQt5/6
        with suppress(RuntimeError):
            # `AttributeError` appears when crashed in `__init__`
            with suppress(AttributeError):
                self.instant_di_ctrl.dispose()
            with suppress(AttributeError):
                self.instant_do_ctrl.dispose()
            with suppress(AttributeError):
                self.instant_ao.dispose()
            with suppress(AttributeError):
                self.wf_ai_ctrl.dispose()
            self._emit_state(self.tr("Disposed of the DAQ objects"))
