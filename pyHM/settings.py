from contextlib import contextmanager, suppress
from math import nan
from os import linesep
from typing import Hashable, Iterable, Iterator, NamedTuple, Sequence

from qtpy.QtCore import (
    QByteArray,
    QCoreApplication,
    QDateTime,
    QDir,
    QObject,
    QSettings,
)
from qtpy.QtWidgets import QWidget

from .constants import (
    DEFAULT_DELAY_BETWEEN_CYCLES,
    DEFAULT_MOTOR_STEP_ANGLE,
    RECEIVER_MARK_TYPE,
    RECEIVERS,
    WAVELENGTHS,
)
from .location import (
    CLOUD_COVER,
    ELEVATION,
    LATITUDE,
    LONGITUDE,
    PRECIPITATION,
    WEATHER_CODE,
    WEATHER_CODE_MEANINGS,
)

__all__ = ["Settings"]


class Settings(QSettings):
    class CallbackOnly(NamedTuple):
        callback: str

    class SpinboxAndCallback(NamedTuple):
        range: tuple[float, float] | tuple[float, float, float]
        prefix_and_suffix: tuple[str, str]
        callback: str

    class ComboboxAndCallback(NamedTuple):
        combobox_data: Iterable[str] | dict[Hashable, str]
        callback: str

    class EditableComboboxAndCallback(NamedTuple):
        combobox_items: Sequence[str]
        callback: str

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(
            QCoreApplication.applicationName() + ".ini",
            QSettings.Format.IniFormat,
            parent,
        )

    def toString(self) -> str:
        lines = []
        for group in self.childGroups():
            if group in ("state", "geometry"):
                continue
            lines.append(f"[{group}]")
            self.beginGroup(group)
            for key in self.childKeys():
                value = self.value(key)
                if isinstance(value, QDateTime):
                    value = value.toString("dd.MM.yyyy h:mm:ss")
                lines.append(f"{key} = {value}")
            self.endGroup()
            lines.append("")
        for key in self.childKeys():
            lines.append(f"{key} = {self.value(key)}")
        return linesep.join(lines)

    def dialog(
        self,
    ) -> dict[
        (str | tuple[str, tuple[str, ...]]),
        dict[
            str,
            (
                CallbackOnly
                | SpinboxAndCallback
                | ComboboxAndCallback
                | EditableComboboxAndCallback
            ),
        ],
    ]:
        return {
            (self.tr("Where to save results"), ("mdi6.folder-table-outline",)): {
                self.tr("Directory:"): Settings.CallbackOnly(
                    Settings.result_dir.fset.__name__
                ),
            },
            (self.tr("Time"), ("mdi6.clock-outline",)): {
                # self.tr("Measurement start:"): Settings.CallbackOnly(
                #     Settings.date_time_start.fset.__name__
                # ),
                # self.tr("Measurement end:"): Settings.CallbackOnly(
                #     Settings.date_time_stop.fset.__name__
                # ),
                self.tr("Delay between cycles:"): Settings.SpinboxAndCallback(
                    range=(0.0, 1e14),
                    prefix_and_suffix=("", self.tr(" sec")),
                    callback=Settings.interval.fset.__name__,
                ),
                self.tr("Cycles count per position:"): Settings.SpinboxAndCallback(
                    range=(1, 1_000_000_000),
                    prefix_and_suffix=("", ""),
                    callback=Settings.cycle_count.fset.__name__,
                ),
            },
            (self.tr("Motor"), ("mdi6.cog-outline",)): {
                self.tr("Angles:"): Settings.CallbackOnly(
                    callback=Settings.angles.fset.__name__,
                ),
                self.tr("Step size:"): Settings.SpinboxAndCallback(
                    range=(1e-14, 1e14),
                    prefix_and_suffix=("", "°"),
                    callback=Settings.motor_const.fset.__name__,
                ),
                self.tr("Correction angle:"): Settings.SpinboxAndCallback(
                    range=(-360, 360),
                    prefix_and_suffix=("", self.tr("°")),
                    callback=Settings.angle_correction.fset.__name__,
                ),
                self.tr("Zero angle signal:"): Settings.ComboboxAndCallback(
                    {
                        False: self.tr("LOW"),
                        True: self.tr("HIGH"),
                    },
                    Settings.zero_angle_signal.fset.__name__,
                ),
            },
            (self.tr("ADC"), ("mdi6.gauge",)): {
                self.tr("Samples per half a period:"): Settings.SpinboxAndCallback(
                    range=(1, 1_000_000),
                    prefix_and_suffix=("", ""),
                    callback=Settings.sample_count.fset.__name__,
                ),
                self.tr("Sample rate:"): Settings.SpinboxAndCallback(
                    range=(1, 200_000),
                    prefix_and_suffix=("", self.tr(" S/s")),
                    callback=Settings.sample_rate.fset.__name__,
                ),
                self.tr("Write debug file"): Settings.CallbackOnly(
                    Settings.save_adc.fset.__name__
                ),
            },
            (self.tr("DAC"), ("mdi6.square-wave",)): {
                self.tr("Voltage:"): Settings.CallbackOnly(
                    Settings.dac.fset.__name__,
                ),
            },
            (self.tr("Weather"), ("mdi6.weather-partly-snowy-rainy",)): {
                self.tr("Clouds:"): Settings.CallbackOnly(
                    Settings.clouds.fset.__name__,
                ),
                self.tr("Precipitation:"): Settings.CallbackOnly(
                    Settings.precipitation.fset.__name__,
                ),
            },
            (self.tr("Location"), ("mdi6.map-marker-outline",)): {
                self.tr("Latitude:"): Settings.SpinboxAndCallback(
                    range=(-90.0, 90.0),
                    prefix_and_suffix=("", self.tr("°")),
                    callback=Settings.latitude.fset.__name__,
                ),
                self.tr("Longitude:"): Settings.SpinboxAndCallback(
                    range=(-180.0, 180.0),
                    prefix_and_suffix=("", self.tr("°")),
                    callback=Settings.longitude.fset.__name__,
                ),
                self.tr("Elevation:"): Settings.SpinboxAndCallback(
                    range=(-10000.0, 10000.0),
                    prefix_and_suffix=("", self.tr(" m")),
                    callback=Settings.elevation.fset.__name__,
                ),
            },
        }

    @contextmanager
    def section(self, section: str) -> Iterator[None]:
        groups: list[str] = []
        try:
            while group := self.group():
                groups.append(group)
                self.endGroup()
            self.beginGroup(section)
            yield None
        finally:
            self.endGroup()
            for group in groups[::-1]:
                self.beginGroup(group)

    def save_widget(self, o: QWidget, parent_path: Sequence[str] = ()) -> None:
        name: str = o.objectName()
        if not name:
            raise AttributeError(f"No name given for {o}")
        name = ".".join((*parent_path, name))
        with suppress(AttributeError), self.section("state"):
            if hasattr(o, "saveState"):
                # noinspection PyUnresolvedReferences
                self.setValue(name, o.saveState())
        with suppress(AttributeError), self.section("geometry"):
            self.setValue(name, o.saveGeometry())

    def restore_widget(self, o: QWidget, parent_path: Sequence[str] = ()) -> None:
        name: str = o.objectName()
        if not name:
            raise AttributeError(f"No name given for {o}")
        name = ".".join((*parent_path, name))
        with suppress(AttributeError), self.section("state"):
            if hasattr(o, "restoreState"):
                # noinspection PyUnresolvedReferences
                o.restoreState(self.value(name, QByteArray()))
        with suppress(AttributeError), self.section("geometry"):
            o.restoreGeometry(self.value(name, QByteArray()))

    @property
    def angles(self) -> list[float]:
        angles: list[float] = []
        with self.section("Углы"):
            i: int = 0
            while self.contains("Угол " + str(i)):
                angles.append(self.value("Угол " + str(i), nan, float))
                i += 1
        return angles

    @angles.setter
    def angles(self, angles: Iterable[float]) -> None:
        with self.section("Углы"):
            for i, a in enumerate(angles):
                self.setValue("Угол " + str(i), a)

    @property
    def sample_count(self) -> int:
        with self.section("АЦП"):
            return self.value("Количество выборок на канал за полупериод", 256, int)

    @sample_count.setter
    def sample_count(self, sample_count: int) -> None:
        with self.section("АЦП"):
            self.setValue("Количество выборок на канал за полупериод", sample_count)

    @property
    def sample_rate(self) -> int:
        with self.section("АЦП"):
            return self.value("Частота выборок", 68300, int)

    @sample_rate.setter
    def sample_rate(self, sample_rate: int) -> None:
        with self.section("АЦП"):
            self.setValue("Частота выборок", sample_rate)

    @property
    def channel_count(self) -> int:
        with self.section("АЦП"):
            return self.value("Количество каналов", 3, int)

    @channel_count.setter
    def channel_count(self, channel_count: int) -> None:
        with self.section("АЦП"):
            self.setValue("Количество каналов", channel_count)

    @property
    def save_adc(self) -> bool:
        with self.section("АЦП"):
            return self.value("Служебный файл", False, bool)

    @save_adc.setter
    def save_adc(self, save_adc: bool) -> None:
        with self.section("АЦП"):
            self.setValue("Служебный файл", save_adc)

    # @property
    # def gain_list(self) -> list[float]:
    #     gain_list: list[float] = []
    #     with self.section("АЦП"):
    #         i: int = 0
    #         while self.contains("Угол " + str(i)):
    #             gain_list.append(self.value("Усиление канал " + str(i), nan, float))
    #             i += 1
    #     return gain_list
    #
    # @gain_list.setter
    # def gain_list(self, gain_list: Iterable[float]) -> None:
    #     with self.section("АЦП"):
    #         channel_count: int = 0
    #         for i, a in enumerate(gain_list):
    #             self.setValue("Усиление канал " + str(i), a)
    #             channel_count += 1
    #         self.setValue("Количество каналов", channel_count)

    @property
    def dac(self) -> dict[RECEIVER_MARK_TYPE, list[float]]:
        dac: dict[RECEIVER_MARK_TYPE, list[float]] = {}
        with self.section("ЦАП"):
            for receiver, wavelength in zip(RECEIVERS, WAVELENGTHS, strict=True):
                if receiver not in dac:
                    dac[receiver] = []
                for i in range(3):
                    dac[receiver].append(
                        self.value(str(wavelength) + "мм " + str(i), 0, float)
                    )
        return dac

    @dac.setter
    def dac(self, dac: dict[RECEIVER_MARK_TYPE, list[float]]) -> None:
        with self.section("ЦАП"):
            for receiver, wavelength in zip(RECEIVERS, WAVELENGTHS, strict=True):
                for i, _d in enumerate(dac.get(receiver, ())):
                    self.setValue(str(wavelength) + "мм " + str(i), _d)

    @property
    def motor_const(self) -> float:
        with self.section("Двигатель"):
            return self.value("Константа", DEFAULT_MOTOR_STEP_ANGLE, float)

    @motor_const.setter
    def motor_const(self, motor_const: float) -> None:
        with self.section("Двигатель"):
            self.setValue("Константа", motor_const)

    @property
    def angle_correction(self) -> float:
        with self.section("Двигатель"):
            return self.value("Угол коррекции", 0, float)

    @angle_correction.setter
    def angle_correction(self, angle_correction: float) -> None:
        with self.section("Двигатель"):
            self.setValue("Угол коррекции", angle_correction)

    @property
    def zero_angle_signal(self) -> bool:
        with self.section("Двигатель"):
            return self.value("Сигнал нулевого угла", False, bool)

    @zero_angle_signal.setter
    def zero_angle_signal(self, zero_angle_signal: bool) -> None:
        with self.section("Двигатель"):
            self.setValue("Сигнал нулевого угла", zero_angle_signal)

    @property
    def cycle_count(self) -> int:
        with self.section("Настройки"):
            return self.value("Количество периодов модуляции на 1 угол", 400, int)

    @cycle_count.setter
    def cycle_count(self, cycle_count: float) -> None:
        with self.section("Настройки"):
            self.setValue("Количество периодов модуляции на 1 угол", cycle_count)

    @property
    def interval(self) -> float:
        with self.section("Настройки"):
            return self.value(
                "Интервал между измерениями", DEFAULT_DELAY_BETWEEN_CYCLES, float
            )

    @interval.setter
    def interval(self, interval: float) -> None:
        with self.section("Настройки"):
            self.setValue("Интервал между измерениями", interval)

    @property
    def result_dir(self) -> QDir:
        with self.section("Настройки"):
            return QDir(self.value("Путь сохранения результата", QDir.current()))

    @result_dir.setter
    def result_dir(self, result_dir: QDir) -> None:
        with self.section("Настройки"):
            self.setValue("Путь сохранения результата", result_dir)

    # @property
    # def date_time_start(self) -> QDateTime:
    #     with self.section("Время измерения"):
    #         return self.value("Старт", QDateTime.currentDateTime())
    #
    # @date_time_start.setter
    # def date_time_start(self, date_time_start: QDateTime) -> None:
    #     with self.section("Время измерения"):
    #         self.setValue("Старт", date_time_start)
    #
    # @property
    # def date_time_stop(self) -> QDateTime:
    #     with self.section("Время измерения"):
    #         return self.value("Стоп", QDateTime.currentDateTime().addDays(1))
    #
    # @date_time_stop.setter
    # def date_time_stop(self, date_time_stop: QDateTime) -> None:
    #     with self.section("Время измерения"):
    #         self.setValue("Стоп", date_time_stop)

    @property
    def clouds(self) -> str:
        with self.section("Условия наблюдений"):
            return (
                str(CLOUD_COVER)
                if CLOUD_COVER >= 0
                else self.value("Облачность", self.tr("N/D"))
            )

    @clouds.setter
    def clouds(self, clouds: str) -> None:
        with self.section("Условия наблюдений"):
            self.setValue("Облачность", clouds)

    @property
    def precipitation(self) -> str:
        with self.section("Условия наблюдений"):
            return (
                str(PRECIPITATION)
                if PRECIPITATION >= 0
                else self.value("Осадки", self.tr("N/D"))
            )

    @precipitation.setter
    def precipitation(self, p: str) -> None:
        with self.section("Условия наблюдений"):
            self.setValue("Осадки", p)

    @property
    def description(self) -> str:
        with self.section("Условия наблюдений"):
            return self.tr(WEATHER_CODE_MEANINGS.get(WEATHER_CODE, "")) or self.value(
                "Описание", ""
            )

    @description.setter
    def description(self, description: str) -> None:
        with self.section("Условия наблюдений"):
            self.setValue("Описание", description)

    @property
    def elevation(self) -> float:
        with self.section("Условия наблюдений"):
            return self.value("Высота наблюдений(м)", ELEVATION, float)

    @elevation.setter
    def elevation(self, elevation: float) -> None:
        with self.section("Условия наблюдений"):
            self.setValue("Высота наблюдений(м)", elevation)

    @property
    def latitude(self) -> float:
        with self.section("Условия наблюдений"):
            return self.value("Широта", LATITUDE, float)

    @latitude.setter
    def latitude(self, latitude: float) -> None:
        with self.section("Условия наблюдений"):
            self.setValue("Широта", latitude)

    @property
    def longitude(self) -> float:
        with self.section("Условия наблюдений"):
            return self.value("Долгота", LONGITUDE, float)

    @longitude.setter
    def longitude(self, longitude: float) -> None:
        with self.section("Условия наблюдений"):
            self.setValue("Долгота", longitude)
