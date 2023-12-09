from ui.ui_new_settings import Ui_Settings
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QImage,QCloseEvent
from PyQt5.QtCore import QSettings,pyqtSignal
import sys
import serial
import serial.tools.list_ports
from hikvision.utilty.camera import Camera
import cv2
from lianji_control.rtu_master import Slave


class SettingsGUI(QWidget):
    close_signal = pyqtSignal(str)
    def __init__(self):
        super(SettingsGUI, self).__init__()
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon(':/setting/setting.ico'))
        self.settings_file = QSettings("defections_detect.ini",
                                       QSettings.IniFormat)
        self.ui.setxifen_pushButton.clicked.connect(self.save_xifen)
        self.ui.setluoju_pushButton.clicked.connect(self.save_luoju)
        self.ui.pushButton_save_front.clicked.connect(self.save_front)
        self.ui.pushButton_save_back.clicked.connect(self.save_back)
        self.ui.checkPort_pushButton.clicked.connect(self.checkUSBport)
        self.ui.checkxifen_pushButton.setEnabled(0)
        self.ui.checkxifen_pushButton.setText('***')
        self.ui.checkluoju_pushButton.setEnabled(0)
        self.ui.checkluoju_pushButton.setText('***')
        self.ui.connect_pushButton.setEnabled(0)
        self.ui.connect_pushButton.setText("***")
        self.restore()

    # def save_port(self):
    #     self.settings_file.setValue('port',self.ui.port_comboBox.currentText())
    def restore(self):
        if self.settings_file.value('xifen_flag'):
            try:
                self.ui.xxifen_comboBox.setCurrentText(
                    self.settings_file.value('x_xifen'))
                self.ui.yxifen_comboBox.setCurrentText(
                    self.settings_file.value('y_xifen'))
                self.ui.zxifen_comboBox.setCurrentText(
                    self.settings_file.value('z_xifen'))
            except:
                pass
        if self.settings_file.value('luoju_flag'):
            try:
                self.ui.xluoju_lineEdit.setText(
                    self.settings_file.value('x_luoju'))
                self.ui.yluoju_lineEdit.setText(
                    self.settings_file.value('y_luoju'))
                self.ui.zluoju_lineEdit.setText(
                    self.settings_file.value('z_luoju'))
            except:
                pass
        if self.settings_file.value('front_flag'):
            try:
                self.ui.front_x.setText(self.settings_file.value('front_x'))
                self.ui.front_y.setText(self.settings_file.value('front_y'))
                self.ui.front_z.setText(self.settings_file.value('front_z'))
            except:
                pass
        if self.settings_file.value('back_flag'):
            try:
                self.ui.back_x.setText(self.settings_file.value('back_x'))
                self.ui.back_y.setText(self.settings_file.value('back_y'))
                self.ui.back_z.setText(self.settings_file.value('back_z'))
            except:
                pass

    def save_front(self):
        self.settings_file.setValue('front_flag', '1')
        self.settings_file.setValue('front_x', self.ui.front_x.text())
        self.settings_file.setValue('front_y', self.ui.front_y.text())
        self.settings_file.setValue('front_z', self.ui.front_z.text())

    def save_back(self):
        self.settings_file.setValue('back_flag', '1')
        self.settings_file.setValue('back_x', self.ui.back_x.text())
        self.settings_file.setValue('back_y', self.ui.back_y.text())
        self.settings_file.setValue('back_z', self.ui.back_z.text())

    def save_xifen(self):
        # self.settings_file.beginGroup('xifen')
        self.settings_file.setValue('xifen_flag', '1')
        self.settings_file.setValue('x_xifen',
                                    self.ui.xxifen_comboBox.currentText())
        self.settings_file.setValue('y_xifen',
                                    self.ui.yxifen_comboBox.currentText())
        self.settings_file.setValue('z_xifen',
                                    self.ui.zxifen_comboBox.currentText())
        # self.settings_file.endGroup()

    def save_luoju(self):
        self.settings_file.setValue('luoju_flag', '1')
        self.settings_file.setValue('x_luoju', self.ui.xluoju_lineEdit.text())
        self.settings_file.setValue('y_luoju', self.ui.yluoju_lineEdit.text())
        self.settings_file.setValue('z_luoju', self.ui.zluoju_lineEdit.text())

    def checkUSBport(self):
        scomList = list(serial.tools.list_ports.comports())
        print(scomList)

        def funcCom(arrContent):
            return "USB Serial Port" in arrContent.description

        b = list(filter(funcCom, scomList))
        # print(b)
        num = len(b)
        usb = []
        while num:
            num -= 1
            # usb.append(b[num].device)
            self.ui.port_comboBox.addItem(b[num].device)
            for i in range(self.ui.port_comboBox.count()):
                item = self.ui.port_comboBox.itemText(i)
                usb.append(item)
            usb = sorted(set(usb), key=usb.index)
            self.ui.port_comboBox.clear()
            self.ui.port_comboBox.addItems(usb)
        # print(usb)

    def checkCamera(self):
        try:
            self.cam = Camera()
            numbers = self.cam.getnumbersofcamera()
            items = [i for i in range(numbers)]
            items = [str(i) for i in items]
            self.ui.camera_comboBox.addItems(items)
            self.ui.checkcamera_pushButton.setEnabled(False)
        except:
            QMessageBox.about(self, '相机', '没有检测到相机，请检查相机是否插入')

    def connectUSB(self):
        try:
            self.current_port = self.ui.port_comboBox.currentText()
            if self.current_port:
                self.slave1 = Slave(self.current_port, '01')
            if self.slave1:
                QMessageBox.about(self, "端口连接", "端口连接成功")
        except:
            QMessageBox.about(self, "端口连接", "请先检测端口")

    def previewCamera(self):
        # print('windowState', int(self.windowState()))
        try:
            currentCameraIndex = int(self.ui.camera_comboBox.currentText())
            self.cam.activatecamera(currentCameraIndex)
            self.cam_flag = 1
        except:
            self.cam_flag = 0
            QMessageBox.about(self, '相机启动失败', '相机启动失败')
        try:
            if self.cam_flag:
                if int(self.windowState()) == 0:
                    width, height = 512, 384
                elif int(self.windowState()) == 2:
                    width, height = 640, 480
                self.image = self.cam.show_thread()
                show = cv2.resize(
                    self.image,
                    (int(width), int(height)))  # 把读到的帧的大小重新设置为 640x480
                show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
                showImage = QImage(show.data, show.shape[1], show.shape[0],
                                   QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
                self.ui.preview_label.setPixmap(
                    QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
        except:
            QMessageBox.about(self, '相机预览失败', '相机预览失败')

    def closePreviewCamera(self):
        try:
            self.cam.closedevice()
            self.ui.preview_label.clear()
        except:
            QMessageBox.about(self, "关闭相机预览", "关闭相机预览失败")

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.close_signal.emit('1')

if __name__ == "__main__":
    App = QApplication(sys.argv)
    settingWindow = SettingsGUI()
    settingWindow.show()
    sys.exit(App.exec_())
