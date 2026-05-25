from qtpy.QtCore import QRect
from qtpy.QtWidgets import QBoxLayout, QWidget

__all__ = ["AutoBoxLayout"]


class AutoBoxLayout(QBoxLayout):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(QBoxLayout.Direction.LeftToRight, parent)

    def setGeometry(self, rect: QRect) -> None:
        children_height: int = (
            sum(
                child.minimumSize().height()
                for i in range(self.count())
                if (child := self.itemAt(i)) is not None
            )
            + self.spacing() * self.count()
        )
        children_width: int = (
            sum(
                child.minimumSize().width()
                for i in range(self.count())
                if (child := self.itemAt(i)) is not None
            )
            + self.spacing() * self.count()
        )
        if (
            self.direction() == QBoxLayout.Direction.TopToBottom
            and rect.width() - children_width > rect.height() - children_height
        ):
            self.setDirection(QBoxLayout.Direction.LeftToRight)
        elif (
            self.direction() == QBoxLayout.Direction.LeftToRight
            and rect.width() - children_width < rect.height() - children_height
        ):
            self.setDirection(QBoxLayout.Direction.TopToBottom)
        super().setGeometry(rect)
