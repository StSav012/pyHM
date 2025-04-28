import sys
from functools import partial
from math import isnan
from typing import Callable, Final, Iterable

from qtpy.QtCore import QDateTime, Qt, QThread, Slot, qVersion
from qtpy.QtGui import QCloseEvent, QKeySequence
from qtpy.QtWidgets import (
    QApplication,
    QCheckBox,
    QDockWidget,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStatusBar,
    QStyle,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .chart_widget import ChartWidget
from .constants import RECEIVER_MARK_TYPE, RECEIVERS, WAVELENGTHS
from .preferences import Preferences
from .settings import Settings
from .thread_hm import ThreadHM

__all__ = ["MainWindow", "run_gui"]

_translate: Callable[[str, str], str] = QApplication.translate
_translate("series name", "{}-Angle Method")

_qt_version_info_: Final[tuple[int | str, ...]] = tuple(
    map(lambda _w: int(_w) if _w.isdecimal() else _w, qVersion().split("."))
)


class TableWidget(QTableWidget):
    def __init__(self, angles: Iterable[float], parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels([self.tr("3-mm"), self.tr("2-mm")])
        angles = list(angles)
        self.setRowCount(len(angles))
        self.setVerticalHeaderLabels(
            [self.locale().toString(angle) + "°" for angle in angles]
        )

        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

        self.setWindowTitle(QApplication.applicationName())

        self.settings: Settings = Settings(self)
        try:
            self.thread_hm: ThreadHM = ThreadHM(self.settings, self)
        except ValueError as ex:
            QMessageBox.critical(self, self.tr("Error"), str(ex))
            QApplication.exit()
            exit()

        if Preferences(self.settings, self).exec() == Preferences.DialogCode.Rejected:
            QApplication.exit()
            exit()

        central_widget: QWidget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout: QVBoxLayout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.charts: dict[RECEIVER_MARK_TYPE, ChartWidget] = {}
        for receiver, wavelength in zip(RECEIVERS, WAVELENGTHS, strict=True):
            chart = self.charts[receiver] = ChartWidget(self)
            layout.addWidget(chart)
            chart.chart().setTitle(
                self.tr("Absorption at {}-mm Wavelength").format(wavelength)
            )

        menu_bar: QMenuBar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        menu_view: QMenu = menu_bar.addMenu(self.tr("&View"))

        visibility_dock: QDockWidget = QDockWidget(self.tr("Lines"), self)
        visibility_dock.setObjectName("LinesDock")
        visibility_widget: QWidget = QWidget(visibility_dock)
        visibility_dock.setWidget(visibility_widget)
        visibility_layout: QVBoxLayout = QVBoxLayout()
        visibility_widget.setLayout(visibility_layout)
        self.series_visible_checks: list[QCheckBox] = []
        for index, name in enumerate(
            [
                self.tr("{}-Angle Method").format(2),
                self.tr("{}-Angle Method").format(len(self.settings.angles) - 1),
            ]
        ):
            series_visible_check: QCheckBox = QCheckBox(name, visibility_widget)
            self.series_visible_checks.append(series_visible_check)
            visibility_layout.addWidget(series_visible_check)
            if _qt_version_info_ >= (6, 7):
                series_visible_check.checkStateChanged.connect(
                    partial(self.on_series_visibility_changed, index)
                )
            else:
                series_visible_check.stateChanged.connect(
                    partial(self.on_series_visibility_changed, index)
                )
            series_visible_check.setChecked(True)
            for receiver in RECEIVERS:
                self.charts[receiver].series(index).setName(name)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, visibility_dock)
        menu_view.addAction(visibility_dock.toggleViewAction())

        voltage_dock: QDockWidget = QDockWidget(self.tr("Voltage"), self)
        voltage_dock.setObjectName("VoltageDock")
        self.voltage_table: TableWidget = TableWidget(
            self.settings.angles, visibility_dock
        )
        voltage_dock.setWidget(self.voltage_table)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, voltage_dock)
        menu_view.addAction(voltage_dock.toggleViewAction())

        controls_dock: QDockWidget = QDockWidget(self.tr("Controls"), self)
        controls_dock.setObjectName("ControlsDock")
        controls_widget: QWidget = QWidget(controls_dock)
        controls_dock.setWidget(controls_widget)
        controls_layout: QHBoxLayout = QHBoxLayout()
        controls_widget.setLayout(controls_layout)
        self.stop_button: QPushButton = QPushButton(self.tr("&Stop"), self)
        controls_layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self._on_stop_button_clicked)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, controls_dock)
        menu_view.addAction(controls_dock.toggleViewAction())

        menu_help: QMenu = menu_bar.addMenu(self.tr("&Help"))
        if _qt_version_info_ >= (6, 3):
            menu_help.addAction(
                self.tr("&About…"),
                QKeySequence.StandardKey.HelpContents,
                self.about,
            )
        else:
            menu_help.addAction(
                self.tr("&About…"),
                self.about,
                QKeySequence.StandardKey.HelpContents,
            )
        menu_help.addAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMenuButton),
            self.tr("About &Qt…"),
            partial(QMessageBox.aboutQt, self),
        )

        self.status_bar: QStatusBar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.progress_bar: QProgressBar = QProgressBar(self.status_bar)
        self.status_bar.addPermanentWidget(self.progress_bar)

        self.settings.restore_widget(self)

        self.thread_hm.finished.connect(self._on_thread_finished)
        self.thread_hm.dataFileChanged.connect(self._on_thread_data_file_changed)
        self.thread_hm.stateChanged.connect(self._on_thread_state_changed)
        self.thread_hm.absorptionCalculated.connect(
            self._on_thread_absorption_calculated
        )
        self.thread_hm.dataObtained.connect(self._on_thread_data_obtained)
        self.thread_hm.start(QThread.Priority.TimeCriticalPriority)

    def about(self) -> None:
        QMessageBox.about(
            self,
            self.tr("About..."),
            """<h1>HMeter</h1>
© Oleg Bolshakov, 2010-2011<br>
<a href='mailto:obolshakov@mail.ru'>obolshakov@mail.ru</a>
""",
        )

    @Slot()
    def _on_thread_finished(self) -> None:
        self.stop_button.setDisabled(True)
        self.status_bar.showMessage(self.tr("Measurement ended."))

    @Slot()
    def _on_stop_button_clicked(self) -> None:
        self.setDisabled(True)
        self.stop_button.setDisabled(True)
        self.thread_hm.requestInterruption()
        self.thread_hm.quit()
        self.thread_hm.wait()
        self.setEnabled(True)

    @Slot(str)
    def _on_thread_data_file_changed(self, filename: str) -> None:
        self.setWindowTitle(QApplication.applicationName() + " — " + filename)

    @Slot(str, int, int)
    def _on_thread_state_changed(self, msg: str, pos: int, max_pos: int) -> None:
        self.status_bar.showMessage(msg)
        self.progress_bar.setMaximum(max_pos)
        self.progress_bar.setValue(pos)
        self.progress_bar.setVisible(
            self.progress_bar.minimum() != self.progress_bar.maximum()
        )

    @Slot(RECEIVER_MARK_TYPE, int, float)
    def _on_thread_data_obtained(
        self,
        receiver: RECEIVER_MARK_TYPE,
        angle_index: int,
        data_mean: float,
    ) -> None:
        self.voltage_table.setItem(
            angle_index,
            int(receiver),
            QTableWidgetItem(self.locale().toString(data_mean, "g", 4)),
        )
        self.voltage_table.resizeColumnsToContents()

    @Slot(QDateTime, RECEIVER_MARK_TYPE, float, float)
    def _on_thread_absorption_calculated(
        self,
        time: QDateTime,
        receiver: RECEIVER_MARK_TYPE,
        data_res: float,
        tau0: float,
    ) -> None:
        if not isnan(data_res) and not isnan(tau0):
            self.charts[receiver].series(0).append(time.toMSecsSinceEpoch(), data_res)
            self.charts[receiver].series(1).append(time.toMSecsSinceEpoch(), tau0)
            self.charts[receiver].chart().update()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.thread_hm.requestInterruption()
        self.thread_hm.quit()
        self.thread_hm.wait()
        self.settings.save_widget(self)
        self.settings.sync()
        return super().closeEvent(event)

    def on_series_visibility_changed(self, index: int, state: Qt.CheckState) -> None:
        for receiver in RECEIVERS:
            self.charts[receiver].series(index).setVisible(
                state == Qt.CheckState.Checked
            )


def run_gui() -> int:
    from qtpy import PYQT_VERSION
    from qtpy.QtWidgets import QApplication

    if PYQT_VERSION:
        # noinspection PyShadowingNames
        class QApplication(QApplication):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.__class__._instance = QApplication.instance()

    QApplication(sys.argv)
    QApplication.setApplicationName("HM")
    w: MainWindow = MainWindow()
    w.show()
    return QApplication.exec()
