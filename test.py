from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from pathlib import Path
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


class extendWidget(QtWidgets.QWidget):
    def __init__(self, parentWidget):
        super().__init__()
        self.parent = parentWidget
        self.setFixedWidth(50)
        self.setFixedHeight(30)
        self.shrunk = True


        # Refresh Timer Definition
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(100)          # every 1000 ms
    
    def refresh(self):
        self.update()

    def update(self):
        pass

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            if self.shrunk:
                self.parent.setFixedWidth(400)
                self.shrunk = False
                print("clicked")
            elif not self.shrunk:
                
                self.parent.setFixedWidth(75)
                self.shrunk = True
                print("clicked")
        # return super().mousePressEvent(event)
    
    def shrink_anim(self):
        pass


class DockedWidget(QtWidgets.QWidget):
    def __init__(self, app=QtWidgets.QApplication, dock_side="right", theme=Path('default_theme.qss').read_text()):
        super().__init__()
        self.app = app
        self.main_screen = self.app.primaryScreen()
        self.screen_h = self.main_screen.geometry().height()
        self.screen_w = self.main_screen.geometry().width()
        self.dock_side = dock_side
        self.align = Qt.AlignCenter | (Qt.AlignBottom if dock_side=="right" or dock_side=="left" else Qt.AlignLeft if dock_side=="top" else None)
        
        self.widget_h = self.screen_h * 8 // 10
        self.widget_w = 75
        
        self.resize(self.widget_w, self.widget_h)
        self.move(QtCore.QPoint(self.screen_w-self.widget_w, self.screen_h // 10))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumWidth(self.widget_w)
        self.setMouseTracking(True)
        self.setStyleSheet(theme)


        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(extendWidget(self), 0, self.align)


        '''
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(edgeHandle(self, Qt.LeftEdge), 0, Qt.AlignLeft)
        '''

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

        # Code to extrude the dock on contact
        if self.underMouse():
            self.show_dock()
        else:
            self.hide_dock()

    


if __name__ == "__main__":

    app = mainApp()

    right = DockedWidget(app, "right")
    app.exec()