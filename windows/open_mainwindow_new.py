from ui.ui_mainwindow import Ui_MainWindow
from open_setting import Settings
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QMessageBox
from PyQt5.QtCore import Qt, QSettings, QTimer
from PyQt5.QtGui import QImage,QPixmap,QResizeEvent
import sys
import cv2
# from hikvision.utilty.camera import Camera,get_devices_list
from hikvision.utilty.csdn_test import *


class mainWindows(QMainWindow):

    def __init__(self):
        super(mainWindows, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('主程序')

        # self.setWindowState(Qt.WindowFullScreen)
        self.setWindowState(Qt.WindowMaximized)
        self.setting = Settings()
        self.ui.settingsaction.triggered.connect(self.opensetting)
        # self.setting.ui.setxifen_pushButton.clicked.connect(self.savexifen)
        # self.setting.ui.setluoju_pushButton.clicked.connect(self.saveluoju)
        # self.setting.ui.checkxifen_pushButton.clicked.connect(self.checkxifen)
        # self.setting.ui.checkluoju_pushButton.clicked.connect(self.checkluoju)
        # self.setting.ui.connect_pushButton.clicked.connect(self.saveport)
        self.ui.checkBox.stateChanged.connect(self.camera1_around)
        # self.ui.checkBox_2.clicked.connect(self.camera2_around)

        self.restoredata()
        try:
            self.devices_lists = enum_devices(device=0, device_way=False)
        except:
            pass

    def resizeEvent(self, a0: QResizeEvent) -> None:
        # 4是全屏的意思 2是最大化
        if int(self.windowState()) == 4:
            W = self.width()
            H = self.height()
            Wcheck1 = self.ui.checkBox.width()
            Hcheck1 = self.ui.checkBox.height()
            Wcheck2 = self.ui.checkBox_2.width()
            Hcheck2 = self.ui.checkBox_2.height()
            self.ui.checkBox.setGeometry((W/2)-100,30,Wcheck1,Hcheck1)
            self.ui.checkBox_2.setGeometry((W/2)-100,30,Wcheck2,Hcheck2)
        if int(self.windowState()) == 2:
            W = self.width()
            H = self.height()
            Wcheck1 = self.ui.checkBox.width()
            Hcheck1 = self.ui.checkBox.height()
            Wcheck2 = self.ui.checkBox_2.width()
            Hcheck2 = self.ui.checkBox_2.height()
            self.ui.checkBox.setGeometry((W/2)-100,30,Wcheck1,Hcheck1)
            self.ui.checkBox_2.setGeometry((W/2)-100,30,Wcheck2,Hcheck2)



    def restoredata(self):
        self.config = QSettings('motor_config.ini', QSettings.IniFormat)
        if self.config.value('restore') is None:
            self.xxifen, self.yxifen, self.zxifen = '12800', '12800', '12800'
            self.xluoju, self.yluoju, self.zluoju = '4', '4', '1'
            self.setting.ui.xxifen_comboBox.setCurrentIndex(5)
            self.setting.ui.yxifen_comboBox.setCurrentIndex(5)
            self.setting.ui.zxifen_comboBox.setCurrentIndex(5)
            self.setting.ui.xluoju_lineEdit.setText(self.xluoju)
            self.setting.ui.yluoju_lineEdit.setText(self.yluoju)
            self.setting.ui.zluoju_lineEdit.setText(self.zluoju)
        if self.config.value('restore') is not None:
            self.config.beginGroup('xifen')
            self.xxifen = self.config.value('xxifen')
            self.yxifen = self.config.value('yxifen')
            self.zxifen = self.config.value('zxifen')
            self.config.endGroup()

            self.config.beginGroup('luoju')
            self.xluoju = self.config.value('xluoju')
            self.yluoju = self.config.value('yluoju')
            self.zluoju = self.config.value('zluoju')
            self.config.endGroup()

            self.config.beginGroup('port')
            self.port = self.config.value('port')
            self.config.endGroup()

            # self.setting.ui.xxifen_comboBox.setCurrentText(self.xxifen)
            # self.setting.ui.yxifen_comboBox.setCurrentText(self.yxifen)
            # self.setting.ui.zxifen_comboBox.setCurrentText(self.zxifen)
            # self.setting.ui.xluoju_lineEdit.setText(self.xluoju)
            # self.setting.ui.yluoju_lineEdit.setText(self.yluoju)
            # self.setting.ui.zluoju_lineEdit.setText(self.zluoju)
            # self.setting.ui.port_comboBox.addItem(self.port)
            # self.setting.ui.port_comboBox.setCurrentText(self.port)

    def opensetting(self):
        self.setting.show()

    def savexifen(self):
        self.config.setValue('restore', '1')
        self.config.beginGroup('xifen')
        self.config.setValue('xxifen',
                             self.setting.ui.xxifen_comboBox.currentText())
        self.config.setValue('yxifen',
                             self.setting.ui.yxifen_comboBox.currentText())
        self.config.setValue('zxifen',
                             self.setting.ui.zxifen_comboBox.currentText())
        self.config.endGroup()
        # todo 传输数据到控制器，进行设置相应数据
        # 传输数据到控制器进行相应参数设置
        try:
            self.setting.slave1.write_single_register(
                90, int(self.setting.ui.xxifen_comboBox.currentText()))
            self.setting.slave1.write_single_register(
                92, int(self.setting.ui.yxifen_comboBox.currentText()))
            self.setting.slave1.write_single_register(
                94, int(self.setting.ui.zxifen_comboBox.currentText()))
        except:
            QMessageBox.warning(self.setting, '警告', '细分设置出错')

    def checkxifen(self):
        try:
            self.xxifen = str(
                self.setting.slave1.read_holding_registers(90, 1)[0])
            self.yxifen = str(
                self.setting.slave1.read_holding_registers(92, 1)[0])
            self.zxifen = str(
                self.setting.slave1.read_holding_registers(94, 1)[0])
            print(self.xxifen, self.yxifen, self.zxifen)
        except:
            QMessageBox.about(self.setting, '错误', '是否已经检查可连接串口,并已经连接')
        try:
            self.setting.ui.xxifen_comboBox.setCurrentText(self.xxifen)
            self.setting.ui.yxifen_comboBox.setCurrentText(self.yxifen)
            self.setting.ui.zxifen_comboBox.setCurrentText(self.zxifen)
        except:
            pass

    def saveluoju(self):
        self.config.setValue('restore', '1')
        self.config.beginGroup('luoju')
        self.config.setValue('xluoju', self.setting.ui.xluoju_lineEdit.text())
        self.config.setValue('yluoju', self.setting.ui.yluoju_lineEdit.text())
        self.config.setValue('zluoju', self.setting.ui.zluoju_lineEdit.text())
        self.config.endGroup()
        # todo 传输数据到控制器，进行设置相应数据
        try:
            self.setting.slave1.write_single_register(
                98, int(self.setting.ui.xluoju_lineEdit.text()))
            self.setting.slave1.write_single_register(
                100, int(self.setting.ui.yluoju_lineEdit.text()))
            self.setting.slave1.write_single_register(
                102, int(self.setting.ui.zluoju_lineEdit.text()))
        except:
            QMessageBox.warning(self.setting, '警告', '螺距设置出错')

    def checkluoju(self):
        try:
            self.xluoju = str(
                self.setting.slave1.read_holding_registers(98, 1)[0])
            self.yluoju = str(
                self.setting.slave1.read_holding_registers(100, 1)[0])
            self.zluoju = str(
                self.setting.slave1.read_holding_registers(102, 1)[0])
            print(self.xluoju, self.yluoju, self.zluoju)
        except:
            QMessageBox.about(self.setting, '错误', '是否已经检查可连接串口,并已经连接')
        try:
            self.setting.ui.xluoju_lineEdit.setText(self.xluoju)
            self.setting.ui.yluoju_lineEdit.setText(self.yluoju)
            self.setting.ui.zluoju_lineEdit.setText(self.zluoju)
        except:
            pass

    def saveport(self):
        self.config.setValue('restore', '1')
        self.config.beginGroup('port')
        self.config.setValue('port',
                             self.setting.ui.port_comboBox.currentText())
        self.config.endGroup()


    def camera1_around(self):
        if self.ui.checkBox.isChecked():
            print('0033')
            try:
                # self.cam1 = Camera(self.devices_lists)
                self.cam1, _= creat_camera(self.devices_lists, 0, log=False)
            except:
                QMessageBox.warning(self,'警告','检查一号相机是否插入')
            try:
                open_device(self.cam1)
            except:
                print('here error')
            try:
                start_grab_and_get_data_size(self.cam1)
            except:
                print('start_grab error')
            try:
                set_Value(self.cam1, param_type="enum_value", node_name="TriggerMode", node_value=1)
                set_Value(self.cam1, param_type="enum_value", node_name="TriggerSource", node_value=0)
            except:
                pass
            try:
                self.startQtimer1()
            except:
                pass

    # def camera2_around(self):
    #     if self.ui.checkBox_2.isChecked():
    #         try:
    #             self.cam2 = Camera(self.devices_lists)
    #             self.cam2.activatecamera(1)
    #             self.cam2.set_trigger(trigger_source=1)
    #         except:
    #             QMessageBox.warning(self,'警告','检查二号相机是否插入')
    #         try:
    #             self.startQtimer2()
    #         except:
    #             pass

    def startQtimer1(self):
        self.timer_camera1 = QTimer()
        self.timer_camera1.timeout.connect(self.show_on_main_page1)
        self.timer_camera1.start(20)

    def startQtimer2(self):
        self.timer_camera2 = QTimer()
        self.timer_camera2.timeout.connect(self.show_on_main_page2)
        self.timer_camera2.start(20)

    def show_on_main_page1(self):
        try:
            if self.ui.checkBox.isChecked():
                self.flag = 1
                try:
                    image = access_get_image(self.cam1, active_way="getoneframetimeout")
                    # print(type(image),image.shape) # <class 'numpy.ndarray'> (1944, 2592, 1)
                    if image is not None:
                        show1 = cv2.resize(image, (int(512), int(384)))  # 把读到的帧的大小重新设置为 640x480
                        show1 = cv2.cvtColor(show1, cv2.COLOR_BGR2RGB)
                        showImage1 = QImage(show1.data, show1.shape[1], show1.shape[0],
                                            QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
                        self.ui.firstcamera_label.setPixmap(QPixmap.fromImage(showImage1))  # 往显示视频的Label里 显示QImage
                except:
                    pass
            if not self.ui.checkBox.isChecked() and self.flag == 1:
                pass
                self.ui.firstcamera_label.clear()
                self.flag = 0
                close_and_destroy_device(self.cam1)
        except:
            pass

    def show_on_main_page2(self):
        try:
            if self.ui.checkBox_2.isChecked():
                self.flag2 = 1
                image2 = self.cam2.show_thread()
                show2 = cv2.resize(image2, (int(512), int(384)))  # 把读到的帧的大小重新设置为 640x480
                show2 = cv2.cvtColor(show2, cv2.COLOR_BGR2RGB)
                showImage2 = QImage(show2.data, show2.shape[1], show2.shape[0],
                                    QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
                self.ui.secondcamera_label.setPixmap(QPixmap.fromImage(showImage2))  # 往显示视频的Label里 显示QImage
            if not self.ui.checkBox_2.isChecked() and self.flag2 == 1:
                self.ui.secondcamera_label.clear()
                self.flag2 = 0
                self.cam2.stopgrabimage()
                self.cam2.closedevice()
        except:
            pass


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    mainPageWindow = mainWindows()
    mainPageWindow.show()
    sys.exit(APP.exec_())
