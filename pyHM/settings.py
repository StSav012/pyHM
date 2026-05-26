import codecs
import re
from collections.abc import Collection, Hashable, Iterable, Iterator, Sequence
from contextlib import contextmanager, suppress
from math import nan
from pathlib import Path
from typing import Any, NamedTuple, overload

from qtpy.QtCore import (
    QByteArray,
    QCoreApplication,
    QDataStream,
    QDate,
    QDateTime,
    QDir,
    QFileDevice,
    QFileInfo,
    QIODevice,
    QObject,
    QTime,
    QTimeZone,
    QTimer,
)
from qtpy.QtWidgets import QWidget

from .constants import (
    DEFAULT_DELAY_BETWEEN_CYCLES,
    DEFAULT_MOTOR_STEP_ANGLE,
    RECEIVERS,
    RECEIVER_MARK_TYPE,
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


try:
    from qtpy.QtCore import QVariant

    def serialize_qobject(dt: object) -> bytes | bytearray | memoryview:
        ba = QByteArray()
        QVariant(dt).save(QDataStream(ba, QIODevice.OpenModeFlag.ReadWrite))
        return ba.data()

    def deserialize_qobject(type_name: str, data: str) -> object:
        if type_name == "ByteArray":
            return escaped_bytes_to_q_byte_array(data)
        v: QVariant = QVariant()
        v.load(QDataStream(escaped_bytes_to_q_byte_array(data)))
        return v.value()
except ImportError:
    from qtpy.QtCore import Qt

    def str_to_sized(string: str | QByteArray, encoding: str = "utf-16be") -> bytes:
        if isinstance(string, QByteArray):
            string = string.data().decode("ascii")
        sb: bytes = string.encode(encoding)
        return len(sb).to_bytes(4) + sb

    def bytes_to_qdate(data: bytes) -> QDate:
        assert len(data) == 8
        return QDate(-4714, 11, 24).addDays(int.from_bytes(data, byteorder="big"))

    def bytes_to_qtime(data: bytes) -> QTime:
        assert len(data) == 4
        return QTime.fromMSecsSinceStartOfDay(int.from_bytes(data, byteorder="big"))

    def qdate_to_bytes(d: QDate) -> bytes:
        return d.daysTo(QDate(-4714, 11, 24)).to_bytes(8)

    def qtime_to_bytes(t: QTime) -> bytes:
        return t.msecsSinceStartOfDay().to_bytes(4)

    def serialize_qobject(dt: QDate | QDateTime | QTime) -> bytes:
        data: bytes
        match dt:
            case QDate():
                dt: QDate
                data = (0x0E).to_bytes(4)
                data += b"\0"  # always?
                data += qdate_to_bytes(dt)
                return data
            case QTime():
                dt: QTime
                data = (0x0F).to_bytes(4)
                data += b"\0"  # always?
                data += qtime_to_bytes(dt)
                return data
            case QDateTime():
                dt: QDateTime
                data = (0x10).to_bytes(4)
                data += b"\0"  # always?
                data += dt.date().daysTo(QDate(-4713, 1, 1).addDays(-38)).to_bytes(8)
                data += dt.time().msecsSinceStartOfDay().to_bytes(4)
                data += int(dt.timeSpec()).to_bytes(1)
                if dt.timeSpec() == Qt.TimeSpec.OffsetFromUTC:
                    data += dt.offsetFromUtc().to_bytes(4)
                elif dt.timeSpec() == Qt.TimeSpec.TimeZone:
                    tz = dt.timeZone()
                    if not tz.isValid():
                        data += str_to_sized("-No Time Zone Specified!")
                    elif not tz.displayName(dt).startswith("UTC"):
                        data += str_to_sized(tz.id())
                    else:
                        data += str_to_sized("OffsetFromUtc")
                        data += str_to_sized(tz.displayName(dt))
                        data += tz.offsetFromUtc(dt).to_bytes(4)
                        data += str_to_sized(tz.displayName(dt))
                        data += str_to_sized(tz.displayName(dt))
                        data += tz.daylightTimeOffset(dt).to_bytes(4)
                        data += str_to_sized(tz.displayName(dt))
                return data
            case _:
                raise TypeError("Unsupported type", type(dt))

    def deserialize_qobject(
        type_name: str, data: str
    ) -> QByteArray | QDate | QDateTime | QTime:
        if type_name == "ByteArray":
            return escaped_bytes_to_q_byte_array(data)
        b_data: bytes = escaped_bytes_to_q_bytes(data)
        match type_name:
            case "Date":
                assert int.from_bytes(b_data[:4], byteorder="big") == 0x0E
                return bytes_to_qdate(b_data[5:13])
            case "Time":
                assert int.from_bytes(b_data[:4], byteorder="big") == 0x0F
                return bytes_to_qtime(b_data[5:9])
            case "DateTime":
                assert int.from_bytes(b_data[:4], byteorder="big") == 0x10
                spec: Qt.TimeSpec = Qt.TimeSpec(b_data[17])
                if spec == Qt.TimeSpec.OffsetFromUTC:
                    return QDateTime(
                        bytes_to_qdate(b_data[5:13]),
                        bytes_to_qtime(b_data[13:17]),
                        spec,
                        int.from_bytes(b_data[18:22], byteorder="big"),
                    )
                if spec == Qt.TimeSpec.TimeZone:
                    return QDateTime(
                        bytes_to_qdate(b_data[5:13]),
                        bytes_to_qtime(b_data[13:17]),
                        QTimeZone(b_data[18:]),
                    )
                return QDateTime(
                    bytes_to_qdate(b_data[5:13]),
                    bytes_to_qtime(b_data[13:17]),
                    spec,
                )
            case _:
                raise ValueError("Unsupported type name", type_name)


def bytes_to_variant(b: bytes | bytearray | memoryview) -> str:
    _s = ""
    for _b in b:
        if _b == 0:
            _s += r"\0"
        elif _b == 0x07:
            _s += r"\a"
        elif _b == 0x08:
            _s += r"\b"
        elif _b in b"ABCDEFabcdef":
            _s += rf"\x{_b:x}"
        elif 0x40 <= _b < 0x80 or _b in b"/+-!: ":
            _s += chr(_b)
        else:
            _s += rf"\x{_b:x}"
    return _s


U32_PATTERN: re.Pattern[str] = re.compile(
    r"%(U[\dABCDEFabcdef]{4}|[\dABCDEFabcdef]{2})"
)
NUMBER_PATTERN: re.Pattern[str] = re.compile(
    r"[+-]?[\d_]*(?:\.[\d_]*)?(?:[eE][+-]?[\d_]*)?"
)
SERIALIZED_QT_VALUE_PATTERN: re.Pattern[str] = re.compile(r"@(\w+)\((.+)\)")
SHORT_HEX_CHAR_PATTERN: re.Pattern[str] = re.compile(r"\\x(.)(?![\dABCDEFabcdef])")


def u32_to_char(m: re.Match[str]) -> str:
    if (g := m.group(1)).startswith("U"):
        return chr(int(g[1:], 16))
    return chr(int(g, 16))


def decode_u32(s: str) -> str:
    return U32_PATTERN.sub(u32_to_char, s)


def silent_time_from_iso(s: str) -> QDateTime | None:
    with suppress(Exception):
        return QDateTime.fromString(s, Qt.DateFormat.ISODateWithMs)
    return None


def escaped_bytes_to_q_bytes(data: str) -> bytes:
    return codecs.escape_decode(
        SHORT_HEX_CHAR_PATTERN.sub(r"\x0{0[1]}".format, data),
    )[0]


def escaped_bytes_to_q_byte_array(data: str) -> QByteArray:
    return QByteArray(escaped_bytes_to_q_bytes(data))


# noinspection PyPep8Naming
class QSettings(QObject):
    def __init__(self, filename: str, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._filename: str = filename
        self._data: dict[str, Any] = {}

        self._group_stack: list[str] = []

        self._pending_changes: bool = False
        self._last_update_time: QDateTime = QDateTime.currentDateTime()

        self._read_file()

        if QCoreApplication.instance():
            self._sync_timer: QTimer = QTimer(self)
            self._sync_timer.timeout.connect(self.sync)
            self._sync_timer.start(4096)

        self.destroyed.connect(self.sync)

    def __del__(self) -> None:
        self.sync()

    def fileName(self) -> str:
        return self._filename

    def group(self) -> str | None:
        if not self._group_stack:
            return None
        return self._group_stack[-1]

    def beginGroup(self, group: str) -> None:
        self._group_stack.append(group)
        data = self._data
        for group in self._group_stack:
            if group not in data:
                data[group] = {}
                self._pending_changes = True
            data = data[group]

    def endGroup(self) -> None:
        self._group_stack.pop(-1)

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

    def childKeys(self) -> list[str]:
        data = self._data
        for group in self._group_stack:
            if not isinstance(data := data.get(group, None), dict):
                return []
        return [key for key in data if not isinstance(data[key], dict)]

    def childGroups(self) -> list[str]:
        data = self._data
        for group in self._group_stack:
            if not isinstance(data := data.get(group, None), dict):
                return []
        return [key for key in data if isinstance(data[key], dict)]

    def contains(self, key: str) -> bool:
        data = self._data
        for group in self._group_stack:
            if not isinstance(data := data.get(group, None), dict):
                return False
        return key in data and not isinstance(data[key], dict)

    @overload
    def value(self, key: str) -> object: ...
    @overload
    def value[T](
        self,
        key: str,
        default_value: T,
        value_type: type[T] | None = None,
        /,
    ) -> T: ...

    def value[T](self, *args) -> object:
        key: str
        default_value: T
        value_type: type[T]
        match args:
            case (key,):
                data = self._data
                for group in self._group_stack:
                    data = data[group]
                return data[key]
            case (key, default_value):
                data = self._data
                for group in self._group_stack:
                    data = data[group]
                return type(default_value)(data.get(key, default_value))
            case (key, default_value, value_type):
                data = self._data
                for group in self._group_stack:
                    data = data[group]
                return value_type(data.get(key, default_value))
            case _:
                raise ValueError

    def setValue(self, key: str, value: object) -> None:
        data = self._data
        for group in self._group_stack:
            if group not in data:
                data[group] = {}
                self._pending_changes = True
            data = data[group]
        if key not in data or data[key] != value:
            data[key] = value
            self._pending_changes = True

    def sync(self) -> None:
        last_mod_time: QDateTime = QFileInfo(self._filename).fileTime(
            QFileDevice.FileTime.FileModificationTime
        )
        if self._pending_changes:
            self._write_file()
            self._last_update_time = QDateTime.currentDateTime()
        elif last_mod_time > self._last_update_time:
            self._read_file()
            self._last_update_time = last_mod_time

    def _read_file(self) -> None:
        if not Path(self.fileName()).exists():
            return
        lines: list[str] = (
            Path(self.fileName()).read_text(encoding="utf-8").splitlines()
        )
        data = self._data
        for line in map(str.strip, lines):
            if not line:
                continue
            if line.casefold() == "[general]":
                data = self._data
            elif line.startswith("[") and line.endswith("]"):
                data = self._data
                groups: list[str] = line[1:-1].split("/")
                for group in map(decode_u32, groups):
                    if group not in data:
                        data[group] = {}
                        self._pending_changes = True
                    if not isinstance(data[group], dict):
                        raise ValueError(f"Name {group} is already in use")
                    data = data[group]
            elif "=" in line:
                key, value = line.split("=", maxsplit=1)
                key = decode_u32(key.strip())
                value = value.strip()
                if NUMBER_PATTERN.fullmatch(value):
                    value = float(value)
                    if value.is_integer():
                        value = int(value)
                elif m := SERIALIZED_QT_VALUE_PATTERN.fullmatch(value):
                    value = deserialize_qobject(m[1], m[2])
                elif (dt := silent_time_from_iso(value)) is not None:
                    value = dt
                else:
                    if value.startswith("@@"):
                        value = value[1:]
                    value = decode_u32(value)
                data[key] = value

    def _write_file(self) -> None:
        lines: list[str] = []
        if self.childKeys():
            lines.append("[General]")
            for key in self.childKeys():
                value = self.value(key)
                if isinstance(value, QByteArray):
                    value = f"@ByteArray({bytes_to_variant(value.data())})"
                elif isinstance(value, QDateTime):
                    value = f"@DateTime({bytes_to_variant(serialize_qobject(value))})"
                elif isinstance(value, QDate):
                    value = f"@Date({bytes_to_variant(serialize_qobject(value))})"
                elif isinstance(value, QTime):
                    value = f"@Time({bytes_to_variant(serialize_qobject(value))})"
                elif isinstance(value, str) and value.startswith("@"):
                    value = "@" + value
                key = key.replace("%", "%25")
                lines.append(f"{key} = {value}")
            lines.append("")

        for group in self.childGroups():
            lines.append(f"[{group}]")
            with self.section(group):
                for key in self.childKeys():
                    value = self.value(key)
                    if isinstance(value, QByteArray):
                        value = f"@ByteArray({bytes_to_variant(value.data())})"
                    elif isinstance(value, QDateTime):
                        value = (
                            f"@DateTime({bytes_to_variant(serialize_qobject(value))})"
                        )
                    elif isinstance(value, QDate):
                        value = f"@Date({bytes_to_variant(serialize_qobject(value))})"
                    elif isinstance(value, QTime):
                        value = f"@Time({bytes_to_variant(serialize_qobject(value))})"
                    elif isinstance(value, str) and value.startswith("@"):
                        value = "@" + value
                    key = key.replace("%", "%25")
                    lines.append(f"{key} = {value}")
            lines.append("")
        Path(self.fileName()).write_text("\n".join(lines), encoding="utf-8")
        return


# noinspection PyPep8Naming
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
            parent,
        )

    def toString(self, exclusions: Collection[str] = ("state", "geometry")) -> str:
        lines = []
        for group in self.childGroups():
            if group in exclusions:
                continue
            lines.append(f"[{group}]")
            with self.section(group):
                for key in self.childKeys():
                    value = self.value(key)
                    if isinstance(value, QDateTime):
                        value = value.toString("dd.MM.yyyy h:mm:ss")
                    lines.append(f"{key} = {value}")
            lines.append("")
        for key in self.childKeys():
            lines.append(f"{key} = {self.value(key)}")
        return "\n".join(lines)

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
