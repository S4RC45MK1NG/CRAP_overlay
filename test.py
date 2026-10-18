from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

import sys


class mainApp(QtWidgets.QApplication):

    def __init__(self):
        super().__init__()
        

class edgeHandle(QtWidgets.QWidget):
    def __init__(self, parentWidget, edge):
        super().__init__()
        self.edge = edge
        self.setFixedWidth(5)
        self.setCursor(Qt.SizeHorCursor)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.window().windowHandle().startSystemResize(self.edge)

        # return super().mousePressEvent(event)


class DockedWidget(QtWidgets.QWidget):
    def __init__(self, app=QtWidgets.QApplication):
        super().__init__()
        self.app = app
        self.main_screen = self.app.primaryScreen()
        self.screen_h = self.main_screen.geometry().height()
        self.screen_w = self.main_screen.geometry().width()
        
        self.widget_h = self.screen_h * 8 // 10
        self.widget_w = 75
        
        self.resize(self.widget_w, self.widget_h)
        self.move(QtCore.QPoint(self.screen_w-self.widget_w, self.screen_h // 10))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumWidth(self.widget_w)
        self.setMaximumWidth(300)
        self.setMouseTracking(True)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(edgeHandle(self, Qt.LeftEdge), 0, Qt.AlignLeft)
        
        self.show()

        # Refresh Timer Definition
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(100)          # every 1000 ms

    def refresh(self):
        self.update()

    def hide_dock(self):
        while self.pos().x() < self.screen_w-10:
            self.move(self.pos().x() + 1, self.pos().y())

    def show_dock(self):
        while self.pos().x() > self.screen_w - self.widget_w:
            self.move(self.pos().x() - 1, self.pos().y())


    def update(self):
        self.widget_w, self.widget_h = self.size().width(), self.size().height()
        if self.underMouse():
            self.show_dock()
        else:
            self.hide_dock()



if __name__ == "__main__":

    app = mainApp()

    right = DockedWidget(app)
    app.exec()