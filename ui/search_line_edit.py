from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

class SearchLineEdit(QLineEdit):
    def __init__(self, parent=None, list_widget=None, on_enter_callback=None):
        super().__init__(parent)
        self.list_widget = list_widget
        self.on_enter_callback = on_enter_callback

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Down:
            self._move_selection(1)
        elif event.key() == Qt.Key.Key_Up:
            self._move_selection(-1)
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self._select_current_item()
        else:
            super().keyPressEvent(event)

    def _move_selection(self, direction):
        current_row = self.list_widget.currentRow()
        count = self.list_widget.count()

        if direction == 1 and current_row < count - 1:
            self.list_widget.setCurrentRow(current_row + 1)
        elif direction == -1 and current_row > 0:
            self.list_widget.setCurrentRow(current_row - 1)

    def _select_current_item(self):
        item = self.list_widget.currentItem()
        if item and self.on_enter_callback:
            self.on_enter_callback(item)
