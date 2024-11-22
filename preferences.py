# coding=utf-8

from abc import abstractmethod
from functools import partial
from logging import Logger, getLogger
from math import ceil, floor
from typing import Any, ClassVar, Hashable, Self, cast

from qtpy.QtGui import QIcon
from qtpy.QtCore import QDateTime, QDir, Qt
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QListWidget,
    QListWidgetItem,
    QScrollArea,
    QSpinBox,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)

from list_by_categories_input import ListByCategoriesInput, ListInput
from open_directory_path_entry import OpenDirectoryPathEntry
from settings import Settings

__all__ = ["Preferences"]


class BaseLogger:
    logger: ClassVar[Logger]

    def __new__[**_P](cls, *args: _P.args, **kwargs: _P.kwargs) -> Self:
        cls.logger = getLogger(cls.__name__)
        return super().__new__(cls)

    @abstractmethod
    def __init__[**_P](self, *args: _P.args, **kwargs: _P.kwargs) -> None:
        pass


class PreferencePage(BaseLogger, QScrollArea):
    """A page of the Preferences dialog"""

    def __init__(
        self,
        value: dict[
            str,
            (
                Settings.CallbackOnly
                | Settings.SpinboxAndCallback
                | Settings.ComboboxAndCallback
                | Settings.EditableComboboxAndCallback
            ),
        ],
        settings: Settings,
        parent: QWidget | None = None,
    ) -> None:
        BaseLogger.__init__(self)
        QScrollArea.__init__(self, parent)

        widget: QWidget = QWidget(self)
        self.setWidget(widget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setFrameStyle(0)

        self._changed_settings: dict[str, Any] = {}

        # https://forum.qt.io/post/671245
        def _on_event(x: bool | int | float | str, *, callback: str) -> None:
            self._changed_settings[callback] = x

        def _on_combo_box_current_index_changed(
            _: int, *, sender: QComboBox, callback: str
        ) -> None:
            self._changed_settings[callback] = sender.currentData()

        if not (isinstance(value, dict) and value):
            raise TypeError(f"Invalid type: {type(value)}")
        layout: QFormLayout = QFormLayout(widget)
        layout.setLabelAlignment(
            layout.labelAlignment() | Qt.AlignmentFlag.AlignVCenter
        )
        key2: str
        value2: (
            Settings.CallbackOnly
            | Settings.SpinboxAndCallback
            | Settings.ComboboxAndCallback
            | Settings.EditableComboboxAndCallback
        )

        check_box: QCheckBox
        text_input: QLineEdit
        path_entry: OpenDirectoryPathEntry
        date_time_edit: QDateTimeEdit
        list_input: ListInput[float]
        list_by_categories_input: ListByCategoriesInput[float]
        spin_box: QSpinBox | QDoubleSpinBox
        combo_box: QComboBox

        for key2, value2 in value.items():
            current_value: Any = getattr(settings, value2.callback)
            if isinstance(value2, Settings.CallbackOnly):
                if isinstance(current_value, bool):
                    check_box = QCheckBox(settings.tr(key2), widget)
                    check_box.setChecked(current_value)
                    check_box.toggled.connect(
                        partial(_on_event, callback=value2.callback)
                    )
                    layout.addWidget(check_box)
                elif isinstance(current_value, str):
                    text_input = QLineEdit(current_value, widget)
                    text_input.textChanged.connect(
                        partial(_on_event, callback=value2.callback)
                    )
                    layout.addRow(key2, text_input)
                elif isinstance(current_value, list):
                    list_input = ListInput(current_value, float, widget)
                    list_input.changed.connect(
                        partial(_on_event, callback=value2.callback)
                    )
                    layout.addRow(key2, list_input)
                elif isinstance(current_value, dict):
                    list_by_categories_input = ListByCategoriesInput(
                        current_value, float, widget
                    )
                    list_by_categories_input.changed.connect(
                        partial(_on_event, callback=value2.callback)
                    )
                    layout.addRow(key2, list_by_categories_input)
                elif isinstance(current_value, QDir):
                    path_entry = OpenDirectoryPathEntry(current_value.path(), widget)
                    path_entry.changed.connect(
                        partial(_on_event, callback=value2.callback)
                    )
                    layout.addRow(key2, path_entry)
                elif isinstance(current_value, QDateTime):
                    date_time_edit = QDateTimeEdit(current_value, widget)
                    date_time_edit.dateTimeChanged.connect(
                        partial(_on_event, callback=value2.callback)
                    )
                    layout.addRow(key2, date_time_edit)
                else:
                    PreferencePage.logger.error(
                        f"The type of {value2.callback!r} is not supported"
                    )
            elif isinstance(value2, Settings.SpinboxAndCallback):
                if isinstance(current_value, int):
                    spin_box = QSpinBox(widget)
                    spin_box.setRange(floor(value2.range[0]), ceil(value2.range[1]))
                    spin_box.setSingleStep(
                        round(value2.range[2]) if len(value2.range) > 2 else 1
                    )
                elif isinstance(current_value, float):
                    spin_box = QDoubleSpinBox(widget)
                    spin_box.setRange(value2.range[0], value2.range[1])
                    spin_box.setSingleStep(
                        value2.range[2] if len(value2.range) > 2 else 1
                    )
                else:
                    PreferencePage.logger.error(
                        f"The type of {value2.callback!r} is not supported"
                    )
                    continue
                spin_box.setValue(current_value)
                spin_box.setPrefix(value2.prefix_and_suffix[0])
                spin_box.setSuffix(value2.prefix_and_suffix[1])
                spin_box.valueChanged.connect(
                    partial(_on_event, callback=value2.callback)
                )
                layout.addRow(key2, spin_box)
            elif isinstance(value2, Settings.ComboboxAndCallback):
                if not isinstance(current_value, Hashable):
                    PreferencePage.logger.error(
                        f"The type of {value2.callback!r} is not supported"
                    )
                    continue
                combo_box = QComboBox(widget)
                combobox_data: dict[Hashable, str]
                if isinstance(value2.combobox_data, dict):
                    combobox_data = value2.combobox_data
                else:
                    combobox_data = dict(enumerate(value2.combobox_data))
                for index, (data, item) in enumerate(combobox_data.items()):
                    combo_box.addItem(settings.tr(item), data)
                combo_box.setEditable(False)
                combo_box.setCurrentText(combobox_data[current_value])
                combo_box.currentIndexChanged.connect(
                    partial(
                        _on_combo_box_current_index_changed,
                        sender=combo_box,
                        callback=value2.callback,
                    )
                )
                layout.addRow(key2, combo_box)
            elif isinstance(value2, Settings.EditableComboboxAndCallback):
                if isinstance(current_value, str):
                    current_text: str = current_value
                else:
                    PreferencePage.logger.error(
                        f"The type of {value2.callback!r} is not supported"
                    )
                    continue
                combo_box = QComboBox(widget)
                combo_box.addItems(value2.combobox_items)
                if current_text in value2.combobox_items:
                    combo_box.setCurrentIndex(value2.combobox_items.index(current_text))
                else:
                    combo_box.insertItem(0, current_text)
                    combo_box.setCurrentIndex(0)
                combo_box.setEditable(True)
                combo_box.currentTextChanged.connect(
                    partial(_on_event, callback=value2.callback)
                )
                layout.addRow(key2, combo_box)
            else:
                PreferencePage.logger.error(f"{value2!r} is not supported")

    @property
    def changed_settings(self) -> dict[str, Any]:
        return self._changed_settings.copy()


class PreferencesBody(BaseLogger, QSplitter):
    """The main area of the GUI preferences dialog"""

    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        try:
            from qtawesome import icon  # import locally to avoid a circular import
        except ImportError:

            def icon(*_, **__) -> QIcon:
                return QIcon()

        BaseLogger.__init__(self)
        QSplitter.__init__(self, parent)
        self.setObjectName("preferencesBody")

        self.setOrientation(Qt.Orientation.Horizontal)
        self.setChildrenCollapsible(False)
        content: QListWidget = QListWidget(self)
        self._stack: QStackedWidget = QStackedWidget(self)
        key: (
            str
            | tuple[str, tuple[str, ...]]
            | tuple[str, tuple[str, ...], tuple[tuple[str, Any], ...]]
        )
        value: dict[
            str,
            (
                Settings.CallbackOnly
                | Settings.SpinboxAndCallback
                | Settings.ComboboxAndCallback
                | Settings.EditableComboboxAndCallback
            ),
        ]
        for key, value in settings.dialog().items():
            if not (isinstance(value, dict) and value):
                PreferencesBody.logger.error(f"Invalid value of {key!r}")
                continue
            new_item: QListWidgetItem
            if isinstance(key, str):
                new_item = QListWidgetItem(key)
            elif isinstance(key, tuple):
                if len(key) == 1:
                    new_item = QListWidgetItem(key[0])
                elif len(key) == 2:
                    new_item = QListWidgetItem(icon(*key[1]), key[0])
                else:
                    PreferencesBody.logger.error(f"Invalid key: {key!r}")
                    continue
            else:
                PreferencesBody.logger.error(f"Invalid key type: {key!r}")
                continue
            content.addItem(new_item)
            box: PreferencePage = PreferencePage(value, settings, self._stack)
            self._stack.addWidget(box)
        content.setMinimumWidth(content.sizeHintForColumn(0) + 2 * content.frameWidth())
        self.addWidget(content)
        self.addWidget(self._stack)

        if content.count() > 0:
            content.setCurrentRow(0)  # select the first page

        content.currentRowChanged.connect(self._stack.setCurrentIndex)

    @property
    def changed_settings(self) -> dict[str, Any]:
        changed_settings: dict[str, Any] = {}
        for index in range(self._stack.count()):
            changed_settings.update(
                cast(PreferencePage, self._stack.widget(index)).changed_settings
            )
        return changed_settings


class Preferences(QDialog):
    """GUI preferences dialog"""

    def __init__(self, settings: Settings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("preferencesDialog")

        self._settings: Settings = settings
        self.setModal(True)
        self.setWindowTitle(self.tr("Preferences"))
        if parent is not None:
            self.setWindowIcon(parent.windowIcon())

        layout: QVBoxLayout = QVBoxLayout(self)
        self._preferences_body: PreferencesBody = PreferencesBody(
            settings=settings, parent=parent
        )
        layout.addWidget(self._preferences_body)
        buttons: QDialogButtonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.close)
        layout.addWidget(buttons)

        self.adjustSize()
        self.resize(self.width() + 4, self.height())

        self._settings.restore_widget(self)
        self._settings.restore_widget(self._preferences_body)

    def reject(self) -> None:
        self._settings.save_widget(self)
        self._settings.save_widget(self._preferences_body)
        return super().reject()

    def accept(self) -> None:
        self._settings.save_widget(self)
        self._settings.save_widget(self._preferences_body)

        for key, value in self._preferences_body.changed_settings.items():
            setattr(self._settings, key, value)
        return super().accept()
