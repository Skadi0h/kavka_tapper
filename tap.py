import random
import sys
import threading
import time

import pyautogui

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QMouseEvent, QResizeEvent, QKeyEvent, QIcon
from PyQt5.QtWidgets import QApplication, QWidget

import window

class SelectionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('KavkaTapper')
        self.setWindowIconText('KavkaTapper')
        self.setWindowIcon(QIcon('./assets/kavka_256x256x32.png'))
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.MaximizeUsingFullscreenGeometryHint | Qt.FramelessWindowHint)
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

    def clicker(self) -> None:
        x1, y1 = self.selection_start.x(), self.selection_start.y()
        x2, y2 = self.selection_end.x(), self.selection_end.y()
        box_width = 80
        offset = 3
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        click_box = (
            (center_x + box_width, center_y + box_width),
            (center_x - box_width, center_y - box_width)
        )
        pyautogui.moveTo(center_x, center_y)
        window.focus_app_by_name('Chrome')
        i = 0
        while 'Chrome' in window.get_active_window():
            for _ in range(random.randint(1, 4)):
                pyautogui.click()
            time.sleep(random.uniform(0.05, 0.20))
            pyautogui.move(
                random.randint(-offset, offset),
                random.randint(-offset, offset)
            )
            if not i % random.randint(13, 52):
                scroll_random = random.randint(1, 5)
                pyautogui.scroll(scroll_random)
                pyautogui.scroll(-scroll_random)
                time.sleep(random.uniform(0.01, 0.5))
                i = 0
            if pyautogui.position()[0] < click_box[1][0] or pyautogui.position()[0] > click_box[0][0]:
                pyautogui.move(
                    center_x+random.randint(-offset, offset),
                    center_y+random.randint(-offset, offset)
                )
            i += 1
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
