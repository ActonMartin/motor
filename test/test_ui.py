
from ui.ui_new_feature import Ui_MainWindow
from PyQt5.QtCore import QObject, QSettings, QTimer, Qt, pyqtSignal,QEvent,QThread
from PyQt5.QtGui import QCursor, QIcon, QImage, QPixmap, QTextCursor
from PyQt5.QtWidgets import (QApplication, QFileSystemModel, QGraphicsPixmapItem, QGraphicsScene, QMainWindow, QMenu,QMessageBox,QLabel)
import sys
import cv2


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)
        self.showlabel()

    def showlabel(self):
        pix = QPixmap('../ll.png')
        print(type(pix))
        self.label1 = self.ui.label_1
        self.label1.setPixmap(pix)
        self.label1.show()

        self.label2 = self.ui.label_2
        self.label2.setPixmap(pix)
        self.label2.show()


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    mainwindows = MainWindow()
    # mainwindows.setWindowState(Qt.WindowMaximized)
    mainwindows.show()
    sys.exit(APP.exec_())
