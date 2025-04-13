from typing import ClassVar, Collection

from qtpy.QtCore import QFileInfo, Signal, Slot
from qtpy.QtWidgets import QFileDialog, QHBoxLayout, QLineEdit, QToolButton, QWidget

__all__ = ["OpenDirectoryPathEntry"]


class OpenDirectoryPathEntry(QWidget):
    changed: ClassVar[Signal] = Signal(str, name="changed")

    def __init__(
        self,
        initial_filename: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._filename: str = ""
        self._name_filters: list[tuple[str, str | Collection[str]]] = []

        layout: QHBoxLayout = QHBoxLayout(self)

        self._label: QLineEdit = QLineEdit(self)
        self.setFilename(initial_filename)
        self._label.setReadOnly(True)
        self._label.setMinimumWidth(self._label.height() * 4)
        layout.addWidget(self._label)

        browse_button: QToolButton = QToolButton(self)
        browse_button.setText(self.tr("&Browse…"))
        browse_button.clicked.connect(self._on_browse_button_clicked)
        layout.addWidget(browse_button)

        self._dialog: QFileDialog = QFileDialog(self)
        self._dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self._dialog.setFileMode(QFileDialog.FileMode.Directory)

    def filename(self) -> str:
        return self._filename

    def setFilename(self, filename: str) -> None:
        filename_info: QFileInfo = QFileInfo(filename)
        if filename_info.exists() and not filename_info.isDir():
            self._filename = ""
            self._label.clear()
            self._label.setToolTip("")
        else:
            self._filename = filename_info.absoluteFilePath()
            self._label.setText(self._filename)
            self._label.setToolTip(self._filename)

    @Slot()
    def _on_browse_button_clicked(self) -> None:
        _space_before_extensions: str = " " * (
            not self._dialog.testOption(QFileDialog.Option.HideNameFilterDetails)
        )
        if self._name_filters:
            self._dialog.setNameFilter(
                ";;".join(
                    f[0]
                    + _space_before_extensions
                    + (f[1] if isinstance(f[1], str) else " ".join(f[1]))
                    for f in self._name_filters
                )
            )
        if self._filename:
            self._dialog.selectFile(str(self._filename))

        if self._dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files: list[str] = self._dialog.selectedFiles()
            if selected_files:
                if selected_files[0] != self._filename:
                    self.setFilename(selected_files[0])
                    self.changed.emit(self._filename)
