from PyQt5.QtCore import pyqtSignal,QObject,pyqtSlot
from PyQt5.QtWidgets import QWidget,QMainWindow,QApplication,QDialog
from ui.ui_new_settings import Ui_Settings
from ui.ui_new_mainwindow import Ui_MainWindow
import sys


class A(QMainWindow):
    def __init__(self):
        super(A, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_front.clicked.connect(self.opencc)

    def opencc(self):
        self.b = B()
        self.b.show()
        self.b.signal.connect(self.get_text)

    def get_text(self):
        print("strings")


class B(QWidget):
    signal = pyqtSignal(str)
    def __init__(self):
        super(B, self).__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)

        self.ui.connect_pushButton.clicked.connect(self.aaa)
    def aaa(self):
        self.signal.emit("88")



class aa(QObject):
    kk = pyqtSignal(int)
    def __init__(self):
        super(aa, self).__init__()
        # self.iou()

    def iou(self,age):
        self.kk.emit(age)

class bb(QObject):
    @pyqtSlot(int)
    def do_kk(self,j):
        print(j)

class wind(QMainWindow):
    def __init__(self):
        super(wind, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_front.clicked.connect(self.opencc)

    def opencc(self):
        self.b = aa()  #实例化
        self.b.kk.connect(self.get_text) #创建连接关系
        self.b.iou(10) #赋值

    @pyqtSlot(int)
    def get_text(self,ah):
        print(ah)
if __name__ == '__main__':
    # kkk = aa()
    # ll = bb()
    # kkk.kk.connect(ll.do_kk)
    # kkk.iou(10)
    app = QApplication(sys.argv)
    window = wind()
    window.show()
    sys.exit(app.exec_())



