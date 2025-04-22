from typing import Final

DEFAULT_MOTOR_STEP_ANGLE: Final[float] = 0.8
DEFAULT_DELAY_BETWEEN_CYCLES: Final[float] = 10
# Толщина атмосферы по кислороду(м)
ATMOSPHERE_THICKNESS_O2: Final[float] = 5300

RECEIVER_MARK_TYPE = str

# Высота калибровочных измерений над уровнем моря(м), город Долгопрудный
ELEVATION_CAL: Final[float] = 180
# Калибровочное поглощение O₂
TAU_O2_CAL: Final[dict[RECEIVER_MARK_TYPE, float]] = {
    "0": 0.04549523810,  # 3мм, город Долгопрудный
    "1": 0.02406190476,  # 2мм, город Долгопрудный
}
# Калибровочный множитель H₂O
PHI_H2O_CAL: Final[dict[RECEIVER_MARK_TYPE, float]] = {
    "0": 0.1076285714,  # 3мм, город Долгопрудный
    "1": 0.2458285714,  # 2мм, город Долгопрудный
}

DEVICE_DESCRIPTION: Final[str] = "USB-4716,BID#0"

RECEIVERS: Final[tuple[RECEIVER_MARK_TYPE, ...]] = ("0", "1")
WAVELENGTHS: Final[tuple[float, ...]] = (3, 2)

DI_MOTOR_ZERO: Final[int] = 0
DO_DIRECTION: Final[int] = 7
DO_MOTOR_STEP_PULSE: Final[int] = 6
