from contextlib import suppress
from typing import Any, Callable, ClassVar, Iterable, Iterator, Type, cast

from qtpy.QtCore import Signal, Slot
from qtpy.QtWidgets import QFormLayout, QLineEdit, QWidget

__all__ = ["ListInput", "ListByCategoriesInput"]


class ListInput[T](QLineEdit):
    changed: ClassVar[Signal] = Signal(list)

    def __init__(
        self,
        values: Iterable[T],
        value_type: Type[T],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._value_type: Type[T] = value_type
        self._values: list[T] = list(values)

        self.setText("; ".join(map(str, values)))
        self.editingFinished.connect(self._on_editing_finished)

    @Slot()
    def _on_editing_finished(self) -> None:
        values: list[T] = self.data()
        if not self.signalsBlocked() and values != self._values:
            self.changed.emit(values)
        self.blockSignals(True)
        self.setText("; ".join(map(str, values)))
        self.blockSignals(False)

    def data(self) -> list[T]:
        def silent_conversion[P](
            conversion: Callable[[P], T], items: Iterable[P]
        ) -> Iterator[T]:
            for item in items:
                with suppress(ValueError):
                    yield conversion(item)

        return list(silent_conversion(self._value_type, self.text().split(";")))


class ListByCategoriesInput[T](QWidget):
    changed: ClassVar[Signal] = Signal(dict)

    def __init__(
        self,
        data: dict[Any, Iterable[T]],
        value_type: Type[T],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._data: dict[Any, Iterable[T]] = data.copy()
        self._value_type: Type[T] = value_type

        layout: QFormLayout = QFormLayout()
        self.setLayout(layout)
        for key, values in self._data.items():
            text: ListInput[T] = ListInput(values, value_type, self)
            text.changed.connect(self._on_editing_finished)
            text.setProperty("key", key)
            layout.addRow(str(key), text)

    @Slot()
    def _on_editing_finished(self) -> None:
        self._data[self.sender().property("key")] = cast(
            ListInput[T], self.sender()
        ).data()
        self.changed.emit(self._data)

    def data(self) -> dict[Any, Iterable[T]]:
        return self._data.copy()
