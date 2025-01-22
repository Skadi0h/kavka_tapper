import random
import sys
import threading
import time

import pynput
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QMouseEvent, QResizeEvent, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget

import window


class SelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('KavkaTapper')
        self.setWindowIconText('KavkaTapper')

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.selection_start = None
        self.selection_end = None
        self.is_selecting = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self.is_selecting:
            return
        if event.button() == Qt.RightButton:
            self.selection_start = event.pos()
            self.selection_end = self.selection_start
            self.is_selecting = True


    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self.is_selecting:
            return
        self.selection_end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if not self.is_selecting:
            return
        if event.button() == Qt.RightButton:
            self.is_selecting = False

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            self.is_selecting = False
            self.selection_start = None
            self.selection_end = None
            self.update()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key_T:
            if self.selection_start and self.selection_end:
                threading.Thread(target=self.clicker, daemon=True).start()
                self.hide()
        elif a0.key() == Qt.Key_Escape:
            self.close()

    def clicker(
        self
    ) -> None:
        x1, y1 = self.selection_start.x(), self.selection_start.y()
        x2, y2 = self.selection_end.x(), self.selection_end.y()
        box_width = 60
        offset = 5
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        click_box = (
            (center_x+box_width, center_y+box_width),
            (center_x-box_width, center_y-box_width)
        )
        mouse = pynput.mouse.Controller()
        mouse.position = (center_x, center_y)

        while window.get_active_window() != 'Google Chrome': time.sleep(0.1) # wait for focus Chrome
        while window.get_active_window() == 'Google Chrome':
            mouse.click(pynput.mouse.Button.left)
            delay = random.uniform(0.03, 0.1)
            time.sleep(delay)
            mouse.move(
                random.randint(-offset, offset),
                random.randint(-offset, offset)
            )
            if mouse.position[0] < click_box[1][0] or mouse.position[0] > click_box[0][0]:
                mouse.position = (center_x, center_y)
        self.reset()



    def paintEvent(self, event: QMouseEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        background_color = QColor(0, 0, 0, 50)
        painter.fillRect(self.rect(), background_color)

        if self.selection_start and self.selection_end:
            rect = QRect(self.selection_start, self.selection_end)

            painter.setPen(QColor(0, 0, 255, 128))
            painter.setBrush(QColor(0, 0, 255, 50))
            painter.drawRect(rect)
            painter.setPen(QColor(255, 0, 0))
        painter.end()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.update()

    def reset(self):
        self.selection_start = None
        self.selection_end = None
        self.is_selecting = False
        self.update()
        self.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SelectionWidget()
    widget.showMaximized()
    sys.exit(app.exec_())
