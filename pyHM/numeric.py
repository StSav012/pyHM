from collections import deque
from math import cos, isnan, log, nan, radians, sqrt
from typing import Sequence


def min_square_method(
    x_and_y: Sequence[tuple[float, float]],
) -> tuple[float, float, float, float]:
    """Определение параметров линейной зависимости методом наименьших квадратов"""

    sx: float = 0.0
    sx2: float = 0.0
    sy: float = 0.0
    sy2: float = 0.0
    sxy: float = 0.0

    for x, y in x_and_y:
        sx += x
        sx2 += x**2
        sy += y
        sy2 += y**2
        sxy += x * y

    n: int = len(x_and_y)

    d: float = n * sx2 - sx**2
    if isnan(d) or d == 0.0:
        return nan, nan, nan, nan

    a: float = (n * sxy - sx * sy) / d
    b: float = (sx2 * sy - sx * sxy) / d

    d0_squared: float = (sy2 - (sy**2 - a**2 * d) / n) / (n - 2) if n > 2 else nan

    da_squared: float = d0_squared * n / d
    da: float = sqrt(da_squared) if da_squared >= 0.0 else nan

    db_squared: float = d0_squared * sx2 / d
    db: float = sqrt(db_squared) if db_squared >= 0.0 else nan

    return a, b, da, db


def tau_by_min_square_method_kd(
    theta: Sequence[float],
    d: Sequence[float],
    d0: float,
) -> tuple[float, float, float, float]:
    """Вычисление поглощения в атмосфере по углам и черному телу вписыванием exp"""
    # out:
    # tau: float
    # d_tau: float
    # s0: float
    # lnk_t_av_t_rel: float
    # d_lnk_t_av_t_rel: float
    x_and_y: deque[tuple[float, float]] = deque()
    for theta_i, d_i in zip(theta, d, strict=True):
        if d0 == d_i:
            break
        x_and_y.append((1.0 / cos(radians(theta_i)), log(abs(d0 - d_i))))

    tau: float
    d_tau: float
    lnk_t_av_t_rel: float
    d_lnk_t_av_t_rel: float
    tau, lnk_t_av_t_rel, d_tau, d_lnk_t_av_t_rel = min_square_method(x_and_y)
    if tau < 0:
        tau = -tau
    else:
        tau, d_tau, lnk_t_av_t_rel, d_lnk_t_av_t_rel = 0.0, 0.0, 0.0, 0.0

    return tau, d_tau, lnk_t_av_t_rel, d_lnk_t_av_t_rel
