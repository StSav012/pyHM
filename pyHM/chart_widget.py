from collections import deque
from math import ceil, floor
from typing import Collection, cast

from qtpy.QtCharts import QChart, QChartView, QDateTimeAxis, QLineSeries, QValueAxis
from qtpy.QtCore import QDateTime, QPointF, Qt, Slot
from qtpy.QtWidgets import QWidget

__all__ = ["ChartWidget"]


class ChartWidget(QChartView):
    def __init__(self, parent: QWidget | None = None) -> None:
        chart: QChart = QChart()
        super().__init__(chart, parent)

        self.time_axis: QDateTimeAxis = QDateTimeAxis()
        self.time_axis.setFormat(self.tr("hh:mm:ss"))
        self.time_axis.setTitleText(self.tr("Time"))

        self.value_axis: QValueAxis = QValueAxis()
        self.value_axis.setTickCount(6)
        self.value_axis.setTitleText(self.tr("τ (Nep)"))

        chart.addAxis(self.time_axis, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(self.value_axis, Qt.AlignmentFlag.AlignLeading)

        self._series: dict[int, QLineSeries] = {}

        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

    def series(self, index: int) -> QLineSeries:
        if index not in self._series:
            series = self._series[index] = QLineSeries()
            self.chart().addSeries(series)
            series.setPointsVisible(True)
            series.attachAxis(self.time_axis)
            series.attachAxis(self.value_axis)
            series.pointAdded.connect(self._on_point_added)
            series.pointRemoved.connect(self._on_point_removed)
            series.pointsRemoved.connect(self._on_points_removed)
            series.visibleChanged.connect(self._on_visibility_changed)
        return self._series[index]

    @Slot(int)
    def _on_point_added(self, index: int) -> None:
        this_series: QLineSeries = cast(QLineSeries, self.sender())
        all_points: deque[QPointF] = deque()
        for series in self._series.values():
            if not series.isVisible():
                continue
            all_points.extend(series.points())
            if series is this_series:
                all_points.append(series.points()[index])
        self._scale_to_data(all_points)

    @Slot(int)
    def _on_point_removed(self, index: int) -> None:
        this_series: QLineSeries = cast(QLineSeries, self.sender())
        all_points: deque[QPointF] = deque()
        for series in self._series.values():
            if not series.isVisible():
                continue
            points: list[QPointF] = series.points()
            if series is this_series:
                points.pop(index)
            all_points.extend(points)
        self._scale_to_data(all_points)

    @Slot(int, int)
    def _on_points_removed(self, index: int, count: int) -> None:
        this_series: QLineSeries = cast(QLineSeries, self.sender())
        all_points: deque[QPointF] = deque()
        for series in self._series.values():
            if not series.isVisible():
                continue
            points: list[QPointF] = series.points()
            if series is this_series:
                for _ in range(count):
                    points.pop(index)
            all_points.extend(points)
        self._scale_to_data(all_points)

    @Slot()
    def _on_visibility_changed(self) -> None:
        all_points: deque[QPointF] = deque()
        for series in self._series.values():
            if not series.isVisible():
                continue
            all_points.extend(series.points())
        self._scale_to_data(all_points)

    def _scale_to_data(self, points: Collection[QPointF]) -> None:
        if not points:
            return
        self.time_axis.setRange(
            QDateTime.fromMSecsSinceEpoch(floor(min([point.x() for point in points]))),
            QDateTime.fromMSecsSinceEpoch(ceil(max([point.x() for point in points]))),
        )
        self.value_axis.setRange(
            min([point.y() for point in points]),
            max([point.y() for point in points]),
        )
