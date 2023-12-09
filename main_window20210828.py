import sys
import warnings
from PyQt5.QtGui import QPixmap,QIcon,QCloseEvent,QShortcutEvent
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow,QMessageBox,QWidget,QShortcut
from PyQt5.QtCore import QTimer,QSettings,QObject,pyqtSignal,QThread,Qt

from setting_window import SettingsGUI
from images_viewer import ImageViewerGUI
from ui.ui_new_mainwindow import Ui_MainWindow
import numpy as np
# from main_MoveAndTakeShot import choose_slave,config_xifen_luoju,change_startup_end_speed,change_speed_acceleration,operation_camera,go_first_position,go_around
from utilty.path_file2 import PathPlanning
from utilty.process_image_neiwu import process_neiwu,process_neiwu_all
from utilty.kill_thread import stop_thread
from lianji_control.rtu_master import *
from lianji_control.utilty.numeration_convert import *
from hikvision.utilty.Camera_new_method import *
import cv2
import math
import threading
import qdarkstyle


class DaoGuiAndCamera(QObject):
    finish_onething_shot = pyqtSignal(int)

    def __init__(self,usb_port:str,addr:str,start_speed:int,end_speed:int,running_speed:int,acceleration:int):
        super(DaoGuiAndCamera, self).__init__()
        self.usb_port = usb_port  # "COM4"
        self.addr = addr  # "01"
        self.start_speed = start_speed  # 1600
        self.end_speed = end_speed  # 1600
        self.running_speed = running_speed  # 1600
        self.acceleration = acceleration  # 80

        self.init_daogui()
        self._get_camera_list()
        self.init_camera()
        # self.choose_path(10.5,10.5,10,10,2)
        self.images_list = []

    def init_daogui(self):
        try:
            self.slave1 = self.choose_slave(self.usb_port, self.addr)
            self.config_xifen_luoju(self.slave1)
            # change_startup_end_speed(slave1,800,800)
            self.change_startup_end_speed(self.slave1, self.start_speed, self.end_speed)
            self.change_speed_acceleration(self.slave1, self.running_speed, self.acceleration)
        except:
            QMessageBox.warning(self)
            # pass

    def init_camera(self):
        try:
            self.camera1 = self._operation_camera(camera_index=0,exposuretime=5000)
        except:
            pass

    def choose_path(self,x_blank,y_blank,width,height,flag):
        # self.path_lines = PathPlanning(x_blank=10.5, y_blank=10.5, width=10, height=10, flag=1).get_path_planning()
        self.path_lines = PathPlanning(x_blank=x_blank, y_blank=y_blank, width=width, height=height, flag=flag).get_path_planning()

    def go_first_position_(self,x,y,z):
        self.go_first_position(self.slave1,x_origin=x,y_origin=y,z_origin=z)

    def go_around_normal(self,camera,x,y,height=[0,0]):
        self._go_around_front_normal(camera,self.slave1,x_origin=x,y_origin=y,path_lines=self.path_lines,images_list=self.images_list,height=height)

    def go_around_neiwu(self,camera,x,y,height=[0,0]):
        self._go_around_front_neiwu(camera,self.slave1,x_origin=x,y_origin=y,path_lines=self.path_lines,images_list=self.images_list,height=height)

    # @staticmethod
    def choose_slave(self,port, slave_addr):
        # port :"COM4"
        # slave_addr: "01"
        slave = Slave(port, slave_addr)
        return slave

    # @staticmethod
    def turnoff_motor(self,slave,direction):
        slave.turnoff_motor(direction)

    # @staticmethod
    def config_xifen_luoju(self,slave):
        # 配置细分、螺距
        slave.write_single_register(90, 3200)  # 设置x轴细分
        slave.write_single_register(92, 3200)  # 设置y轴细分
        slave.write_single_register(94, 3200)  # 设置z轴细分
        # slave.write_single_register(96, 3200)  # 设置a轴细分

        slave.write_single_register(98, 5)  # 设置x轴转一圈的螺距
        slave.write_single_register(100, 5)  # 设置y轴转一圈的螺距
        slave.write_single_register(102, 5)  # 设置z轴转一圈的螺距
        # slave1.write_single_register(104, 1) #设置a轴转一圈的螺距

    # @staticmethod
    def change_speed_acceleration(self,slave, speed, acceleration):
        slave.change_speed(speed, acceleration)

    # @staticmethod
    def change_startup_end_speed(self,slave, startup_speed, end_speed):
        slave.startup_end_speed(startup_speed, end_speed)

    # @staticmethod
    def go_origin(self,slave):
        slave.go_origin(direction=2, siginal_input=6, method=0)
        slave.go_origin(direction=4, siginal_input=7, method=0)
        slave.go_origin(direction=6, siginal_input=8, method=0)

    def go_first_position(self,slave, x_origin, y_origin, z_origin):
        # x_origin,y_origin,z_origin = -108.337,-68.125,7.397
        # slave.go_straight(0,y_origin,0,a=None)
        # slave.go_straight(x_origin-5,y_origin-5,0,a=None)
        slave.go_straight(x_origin, y_origin, z_origin, a=None)

    def go_around_front(self,cam, slave, x_origin, y_origin, z_origin, path_lines, images_list,flag=1):
        """
        deprecated
        flag为2的时候是添加的正常拍摄的照片
        flag为1的时候添加的是内污处理后的照片，例如拍摄内污，进行轮廓寻找
        """
        warnings.warn('代码不使用了，已经废除',DeprecationWarning)
        height_list_flag1 = [32.5,33.5]  # flag为1的时候添加的是内污处理后的照片，例如拍摄内污，进行轮廓寻找
        height_list_flag2 = [30,31]  # flag为2的时候是添加的正常拍摄的照片

        child_images_list = []
        count_flag = 0  # flag为1每一个物体xy都需要变换四次完成拍照
        which_flag = 0
        for x_xd, y_xd in path_lines:
            # count_flag += 1
            # print('count_flag',count_flag)
            x_xd, y_xd = x_xd * 1000, y_xd * 1000
            x_this = x_origin * 1000 + x_xd
            y_this = y_origin * 1000 + y_xd
            x_this = x_this / 1000
            y_this = y_this / 1000
            if flag == 1:
                for z_this in height_list_flag1:
                    count_flag += 1
                    # print("目标位置 x:{},y:{}".format(x_this,y_this))
                    slave.go_straight(x_this, y_this, z_this, None)
                    while True:
                        x, y, z = self.get_x_y_z(slave)
                        # print("------目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this,y_this,x,y))
                        if math.isclose(x_this, x, rel_tol=5e-5) and math.isclose(y_this, y, rel_tol=5e-5) and math.isclose(z_this, z, rel_tol=5e-5):
                            # print("目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this, y_this, x, y))
                            try:
                                set_Value(cam, param_type='command_value', node_name="TriggerSoftware")
                            except:
                                pass
                            imagebuffer = access_get_image(cam, "getImagebuffer")
                            if imagebuffer is not None:
                                imagebuffer = process_neiwu(imagebuffer, scale=0.5, min_area=80000, max_area=200000)
                                if imagebuffer is not None:
                                    child_images_list.append(imagebuffer)
                                else:
                                    child_images_list.append(np.zeros((800, 800, 1), dtype='uint8'))
                            if count_flag == 1*len(height_list_flag1):
                                # 对内污进行拍照时，只需要拍摄一个位置
                                count_flag = 0
                                which_flag += 1
                                self.finish_onething_shot.emit(which_flag)
                                images_list.append(child_images_list)
                                child_images_list = []
                                if which_flag == 100:
                                    which_flag = 0
                            break
            if flag == 2:
                # todo for 高度
                count_flag += 1
                # print("目标位置 x:{},y:{}".format(x_this,y_this))
                slave.go_straight(x_this, y_this, z_origin, None)
                while True:
                    x, y, z = self.get_x_y_z(slave)
                    # print("------目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this,y_this,x,y))
                    if math.isclose(x_this, x, rel_tol=5e-5) and math.isclose(y_this, y, rel_tol=5e-5):
                        # print("目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this, y_this, x, y))
                        try:
                            set_Value(cam, param_type='command_value', node_name="TriggerSoftware")
                        except:
                            pass
                        imagebuffer = access_get_image(cam, "getImagebuffer")
                        if imagebuffer is not None:
                            # flag为1的时候是添加的正常拍摄的照片
                            # flag为2的时候添加的是处理后的照片，例如拍摄内污，进行轮廓寻找
                            child_images_list.append(imagebuffer)
                        if count_flag == 4:
                            # 数到四次之后，一个物体拍摄完成，就可以将这一组拍摄的图片加到images_list里面，然后将子list清空
                            count_flag = 0
                            which_flag += 1
                            self.finish_onething_shot.emit(which_flag)
                            images_list.append(child_images_list)
                            # print('images_list',len(images_list),len(child_images_list))
                            child_images_list = []
                            if which_flag == 100:
                                which_flag = 0
                        break

    def _go_around_front_normal(self,cam, slave, x_origin, y_origin, path_lines, images_list,height):
        """
        为除了内污的拍照方法，背面也可以使用这个def，这里知识执行了在height的每一个高度值进行拍照
        """
        try:
            set_Value(cam, param_type="enum_value", node_name="TriggerMode", node_value=1)
            set_Value(cam, param_type="enum_value", node_name="TriggerSource", node_value=7)
        except:
            pass
        # height_list_flag2 = [30,31]  # flag为2的时候是添加的正常拍摄的照片,拍摄的是两个高度值的照片
        height_list_flag2 = height  # flag为2的时候是添加的正常拍摄的照片,拍摄的是两个高度值的照片

        child_images_list = []
        count_flag = 0  # flag为1每一个物体xy都需要变换四次完成拍照
        which_flag = 0
        for x_xd, y_xd in path_lines:
            count_flag += 1
            # print('count_flag',count_flag)
            x_xd, y_xd = x_xd * 1000, y_xd * 1000
            x_this = x_origin * 1000 + x_xd
            y_this = y_origin * 1000 + y_xd
            x_this = x_this / 1000
            y_this = y_this / 1000
            for z_this in height_list_flag2:
                # count_flag += 1
                # print("目标位置 x:{},y:{}".format(x_this,y_this))
                slave.go_straight(x_this, y_this, z_this, None)
                while True:
                    x, y, z = self.get_x_y_z(slave)
                    # print("------目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this,y_this,x,y))
                    if math.isclose(x_this, x, rel_tol=5e-5) and math.isclose(y_this, y, rel_tol=5e-5) and math.isclose(z_this, z, rel_tol=5e-5):
                        # print("目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this, y_this, x, y))
                        try:
                            set_Value(cam, param_type='command_value', node_name="TriggerSoftware")
                        except:
                            pass
                        imagebuffer = access_get_image(cam, "getImagebuffer")
                        if imagebuffer is not None:
                            child_images_list.append(imagebuffer)
                        if count_flag == 4:
                            count_flag = 0
                            which_flag += 1
                            self.finish_onething_shot.emit(which_flag)
                            images_list.append(child_images_list)
                            child_images_list = []
                            if which_flag == 100:
                                which_flag = 0
                        break

    def _go_around_front_neiwu(self,cam, slave, x_origin, y_origin, path_lines, images_list,height):
        """
        内污的拍照方法，这里执行了在height的两个高度值间进行拍照
        """
        try:
            set_Value(cam, param_type="enum_value", node_name="TriggerMode", node_value=0)
        except:
            pass
        # height_list_flag1 = [32.5,33.5]  # flag为1的时候添加的是内污处理后的照片，例如拍摄内污，进行轮廓寻找
        height_list_flag1 = height  # flag为1的时候添加的是内污处理后的照片，例如拍摄内污，进行轮廓寻找

        child_images_list = []
        count_flag = 0  # flag为1每一个物体xy都需要变换四次完成拍照
        which_flag = 0
        for x_xd, y_xd in path_lines:
            # count_flag += 1
            # print('count_flag',count_flag)
            x_xd, y_xd = x_xd * 1000, y_xd * 1000
            x_this = x_origin * 1000 + x_xd
            y_this = y_origin * 1000 + y_xd
            x_this = x_this / 1000
            y_this = y_this / 1000

            z_this = height_list_flag1[0]
            count_flag += 1
            # print("目标位置 x:{},y:{}".format(x_this,y_this))
            slave.go_straight(x_this, y_this, z_this, None)
            while True:
                x, y, z = self.get_x_y_z(slave)
                # print("------目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this,y_this,x,y))
                if math.isclose(x_this, x, rel_tol=5e-5) and math.isclose(y_this, y, rel_tol=5e-5) and math.isclose(z_this, z, rel_tol=5e-5):
                    # print("目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this, y_this, x, y))
                    move_flag = True
                    while True:
                        imagebuffer = access_get_image(cam, "getImagebuffer")
                        if imagebuffer is not None:
                            child_images_list.append(imagebuffer)
                        # else:
                        #     child_images_list.append(np.zeros((800, 800, 1), dtype='uint8'))
                        if move_flag:
                            self.change_speed_acceleration(slave, 1000, 50)
                            slave.go_straight(x_this, y_this, height_list_flag1[1], None)
                            move_flag = False
                        # if count_flag == 1*len(height_list_flag1):
                        #     # 对内污进行拍照时，只需要拍摄一个位置
                        #     count_flag = 0
                        #     which_flag += 1
                        #     self.finish_onething_shot.emit(which_flag)
                        #     images_list.append(child_images_list)
                        #     child_images_list = []
                        #     if which_flag == 100:
                        #         which_flag = 0
                        x, y, z = self.get_x_y_z(slave)
                        # print(x,y,z)
                        if math.isclose(height_list_flag1[1], z, rel_tol=5e-5):
                            self.change_speed_acceleration(slave, 10000, 50)
                            which_flag += 1
                            self.finish_onething_shot.emit(which_flag)
                            try:
                                child_images_list = process_neiwu_all(child_images_list)
                                images_list.append(child_images_list)
                            except:
                                pass
                            child_images_list = []
                            if which_flag == 100:
                                which_flag = 0
                            break
                    break

    def _get_camera_list(self):
        # 枚举设备
        try:
            self.deviceList = enum_devices(device=0, device_way=False)
        except:
            pass

    def _operation_camera(self,camera_index=0,exposuretime=5000):
        # 枚举设备
        # deviceList = enum_devices(device=0, device_way=False)

        # 创建相机实例并创建句柄,(设置日志路径)
        cam, stDeviceList = creat_camera(self.deviceList, camera_index, log=False)

        # decide_divice_on_line(cam)  ==============
        # 打开设备
        open_device(cam)
        # 设置软触发
        try:
            set_Value(cam, param_type="enum_value", node_name="TriggerMode", node_value=1)
            set_Value(cam, param_type="enum_value", node_name="TriggerSource", node_value=7)
        except:
            pass

        # 设置像素格式为Mono8
        try:
            set_Value(cam, param_type="enum_value", node_name="PixelFormat", node_value=17301505)
        except:
            pass
        # 设置曝光时间 5000
        try:
            set_Value(cam, param_type="float_value", node_name="ExposureTime", node_value=exposuretime)
        except:
            pass
        # 设置触发延迟
        # try:
        #     set_Value(cam,param_type="float_value",node_name="TriggerDelay",node_value=10000)
        # except:
        #     pass
        # 设置ROI区域
        # try:
        #     set_Value(cam,param_type="int_value",node_name="Width",node_value=1944)
        #     set_Value(cam,param_type="int_value",node_name="Height",node_value=1944)
        #     set_Value(cam,param_type="int_value",node_name="OffsetX",node_value=480)#496
        #     set_Value(cam,param_type="int_value",node_name="OffsetY",node_value=0)#176
        # except:
        #     pass
        # 开始取流
        try:
            start_grab_and_get_data_size(cam)
        except:
            pass
        return cam

    def get_x_y_z(self,slave):
        positions = slave.read_holding_registers(42, 6)
        # print(positions)
        x_low, x_high = positions[0], positions[1]
        y_low, y_high = positions[2], positions[3]
        z_low, z_high = positions[4], positions[5]

        def convert(low, high):
            low_bin, high_bin = bin(low)[2:], bin(high)[2:]
            low_bin, high_bin = '{0:0>16s}'.format(low_bin), '{0:0>16s}'.format(high_bin)
            value_bin = high_bin + low_bin
            bin2dec = Bin2Dec()
            value_signed = bin2dec.bin2dec_auto(value_bin)
            value_signed = value_signed / 1000
            return value_signed

        x_position = convert(x_low, x_high)
        y_position = convert(y_low, y_high)
        z_position = convert(z_low, z_high)

        return x_position, y_position, z_position


class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)
        self.ui.label_7.setPixmap(QPixmap("./resources/school_logo.png"))
        # self.setWindowIcon(QIcon(":"))
        self.flush_table_head()
        self.flush_table_row()
        self.changeTableWidgetSize()
        self.ui.tableWidget.currentCellChanged.connect(self.jump_new_window)
        self.ui.action_settings.triggered.connect(self.open_settings)
        self.ui.action_2.triggered.connect(self.turn_off_application)
        self.ui.init_daogui_camera.clicked.connect(self.init_daoguiandcamera)
        self.ui.close_motor.clicked.connect(self.turn_off_motor)

        self.ui.pushButton_front.clicked.connect(self.start_check)
        self.ui.pushButton_front.setEnabled(0)
        self.ui.pushButton_front_2.clicked.connect(self.start_check_neiwu)
        self.ui.pushButton_front_2.setEnabled(0)
        self.ui.pushButton_back.setEnabled(0)
        self.init_data()

        self.timer = QTimer()
        self.timer.start(200)
        self.timer.timeout.connect(self.check_data_in_image_viewer)
        self.timer.timeout.connect(self.display_lcd)

        self.ui.lcdNumber_neiwu.setStyleSheet("color: red;font:bold")
        self.ui.lcdNumber_dizuobuliang.setStyleSheet("color: red;font:bold")
        self.ui.lcdNumber_xiaomianshang.setStyleSheet("color: red;font:bold")
        self.ui.lcdNumber_youwu.setStyleSheet("color: red;font:bold")
        self.ui.lcdNumber_kuangshang.setStyleSheet("color: red;font:bold")
        self.ui.lcdNumber_yijiao.setStyleSheet("color: red;font:bold")

        # self.daoguiandcamera = DaoGuiAndCamera("COM4","01",1600,1600,20000,80)

        # self.ui.pushButton_front.clicked.connect(self.front_moving)

    def check_data_in_image_viewer(self):
        try:
            self.neiwu = self.imageviewerGUI.neiwu
            self.dizuobuliang = self.imageviewerGUI.dizuobuliang
            self.xiaomianshang = self.imageviewerGUI.xiaomianshang
            self.youwu = self.imageviewerGUI.youwu
            self.kuangshang = self.imageviewerGUI.kuangshang
            self.yijiao = self.imageviewerGUI.yijiao
            self.data_biaoqian = self.imageviewerGUI.data_biaoqian
        except:
            pass

    def display_lcd(self):
        self.ui.lcdNumber_neiwu.display(str(self.neiwu))
        self.ui.lcdNumber_dizuobuliang.display(str(self.dizuobuliang))
        self.ui.lcdNumber_xiaomianshang.display(str(self.xiaomianshang))
        self.ui.lcdNumber_youwu.display(str(self.youwu))
        self.ui.lcdNumber_kuangshang.display(str(self.kuangshang))
        self.ui.lcdNumber_yijiao.display(str(self.yijiao))

    def init_data(self):
        self.neiwu = 0
        self.dizuobuliang = 0
        self.xiaomianshang = 0
        self.youwu = 0
        self.kuangshang = 0
        self.yijiao = 0

        # import glob
        # files = glob.glob("D:\\Projects\\motor\\test\\images\\*.png")
        # self.image_list = []
        # for i in files:
        #     self.image_list.append(cv2.imread(i))
        self.data_biaoqian = np.zeros((10,10,6))
        self.settings_file = QSettings("defections_detect.ini",QSettings.IniFormat)
        # if self.settings_file.value():
        #     pass

    def flush_table_head(self):
        col = 10
        header_text = [str(i+1) for i in range(col)]
        self.ui.tableWidget.setColumnCount(len(header_text))
        self.ui.tableWidget.setHorizontalHeaderLabels(header_text)

    def flush_table_row(self):
        row = 10
        self.ui.tableWidget.setRowCount(row)

    def changeTableWidgetSize(self):
        destop = QApplication.desktop()
        value = int(0.08*destop.width())
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(value)
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(value)


    def jump_new_window(self):
        self.currentRow = self.ui.tableWidget.currentRow()
        self.currentColumn = self.ui.tableWidget.currentColumn()
        if self.currentRow in [1,3,5,7,9]:
            self.currentColumn = 9-self.currentColumn
        # images_index_in_images_list = (currentRow+1)*(currentColumn+1)-1
        images_index_in_images_list = self.currentRow*10+self.currentColumn
        self.ui.statusbar.showMessage(f"当前查看的是第{images_index_in_images_list+1}组照片")
        # print('len(self.daoguiandcamera.images_list)',len(self.daoguiandcamera.images_list))
        try:
            here_list = self.daoguiandcamera.images_list[images_index_in_images_list]
            # print('len(here_list)',len(here_list))
            # import glob
            # files = glob.glob("D:\\Projects\\motor\\test\\images\\*.png")
            # here_list = []
            # for i in files:
            #     here_list.append(cv2.imread(i))
        except:
            pass
        try:
            self.imageviewerGUI = ImageViewerGUI(self.neiwu,self.dizuobuliang,self.xiaomianshang,self.youwu,self.kuangshang,self.yijiao)
            self.imageviewerGUI.add_images_list(here_list)
            self.imageviewerGUI.add_zuobiao(self.currentRow, self.currentColumn,images_index_in_images_list)
            self.imageviewerGUI.add_data_biaoqian(self.data_biaoqian)
            self.imageviewerGUI.show()
            self.imageviewerGUI.emit2main_page.connect(self.deal_data)
            self.imageviewerGUI.emit2main_page_defection.connect(self.put_defection_image)
        except:
            QMessageBox.warning(self,"警告","请先拍摄图片")
        # try:
        #     self.put_gou_image(self.currentRow,self.currentColumn)
        # except:
        #     pass

    def deal_data(self,num1,num2,num3,num4):
        # print('num1,num2',num1,num2)
        # self.imageviewerGUI.destroy()
        show_vv_flag = True
        if num4 == 1:
            now_images_index_in_images_list = num3 + 1
            if now_images_index_in_images_list > 99:
                now_images_index_in_images_list = 99
                show_vv_flag = False
                QMessageBox.information(self,"检查完毕","检查完毕")
        else:
            now_images_index_in_images_list = num3 - 1
            if now_images_index_in_images_list < 0:
                now_images_index_in_images_list = 0
        self.currentRow = now_images_index_in_images_list//10
        self.currentColumn = now_images_index_in_images_list%10
        if self.currentRow in [1,3,5,7,9]:
            self.currentColumn = 9-self.currentColumn
        self.ui.statusbar.showMessage(f"当前查看的是第{now_images_index_in_images_list+1}组照片")
        try:
            here_list = self.daoguiandcamera.images_list[now_images_index_in_images_list]
            # import glob
            # files = glob.glob("D:\\Projects\\motor\\test\\images\\*.png")
            # here_list = []
            # for i in files:
            #     here_list.append(cv2.imread(i))
        except:
            pass
        try:
            if show_vv_flag:
                self.imageviewerGUI = ImageViewerGUI(self.neiwu,self.dizuobuliang,self.xiaomianshang,self.youwu,self.kuangshang,self.yijiao)
                self.imageviewerGUI.add_images_list(here_list)
                self.imageviewerGUI.add_zuobiao(self.currentRow, self.currentColumn,now_images_index_in_images_list)
                self.imageviewerGUI.add_data_biaoqian(self.data_biaoqian)
                self.imageviewerGUI.show()
                self.imageviewerGUI.emit2main_page.connect(self.deal_data)
                self.imageviewerGUI.emit2main_page_defection.connect(self.put_defection_image)
        except:
            QMessageBox.warning(self,"警告","请先拍摄图片")
        # try:
        #     self.put_gou_image(self.currentRow,self.currentColumn)
        # except:
        #     pass

    def open_settings(self):
        self.settings_page = SettingsGUI()
        # self.settings_page.close_signal.connect(self.test_close)
        self.settings_page.show()

    def test_close(self):
        print("close setting page")

    def Work1(self):
        try:
            self.daoguiandcamera = DaoGuiAndCamera("COM3","01",1600,1600,12000,80)  #创建线程对象
            self.daoguiandcamera.finish_onething_shot.connect(self.put_one_image_on_cell)
            self.ui.pushButton_front.setEnabled(1)
            self.ui.pushButton_front_2.setEnabled(1)
            self.ui.pushButton_back.setEnabled(1)
        except:
            QMessageBox.warning(self,"导轨初始化出错","请检查线缆是否连接")

    def Work2(self):
        # 正面除内污外缺陷拍照
        try:
            self.daoguiandcamera.images_list = []
            self.daoguiandcamera.choose_path(10.5, 10.5, 10, 10, flag=2)
            self.daoguiandcamera.go_origin(self.daoguiandcamera.slave1)
            self.daoguiandcamera.go_first_position_(10.273,10.128,25)
            self.daoguiandcamera.go_around_normal(self.daoguiandcamera.camera1,10.273,10.128,[30,31])
        except:
            pass

    def Work3(self):
        # 内污的拍摄线程
        self.daoguiandcamera.images_list = []
        self.daoguiandcamera.camera1.MV_CC_SetFloatValue("ExposureTime",50000) # todo 临时修改，有第二个相机的时候可以去掉这个
        self.daoguiandcamera.choose_path(12.175,11.48,6,9,flag=1)
        self.daoguiandcamera.go_origin(self.daoguiandcamera.slave1)
        self.daoguiandcamera.go_first_position_(10.273, 10.128, 25)
        self.daoguiandcamera.go_around_neiwu(self.daoguiandcamera.camera1,10.273, 10.128,[32.5,33.5])

    def init_daoguiandcamera(self):
        try:
            self.thread1 = threading.Thread(target=self.Work1,args=())
            self.thread1.start()
            self.ui.init_daogui_camera.setEnabled(0)
        except:
            # QMessageBox.warning(self,"请先打开设置设置参数","请先打开开始设置参数")
            self.ui.init_daogui_camera.setEnabled(1)

    def start_check(self):
        self.ui.tableWidget.clearContents()
        try:
            self.thread2 = threading.Thread(target=self.Work2,args=())
            self.thread2.start()
        except:
            pass

    def start_check_neiwu(self):
        self.ui.tableWidget.clearContents()
        try:
            self.thread3 = threading.Thread(target=self.Work3, args=())
            self.thread3.start()
        except:
            pass

    def put_gou_image(self,row,col):
        imagelabel = QLabel()
        imagelabel.setText("")
        imagelabel.setScaledContents(True)
        pixmap = QPixmap()
        # pixmap.load("./resources/gou.ico")
        pixmap.load(":/mainwindow/gou.ico")
        imagelabel.setPixmap(pixmap)
        self.ui.tableWidget.setCellWidget(row,col,imagelabel)

    def put_defection_image(self,num):
        if num == 1:
            imagelabel = QLabel()
            imagelabel.setText("")
            imagelabel.setScaledContents(True)
            pixmap = QPixmap()
            # pixmap.load("./resources/gou.ico")
            pixmap.load(":/mainwindow/gou_with_defections.ico")
            imagelabel.setPixmap(pixmap)
            self.ui.tableWidget.setCellWidget(self.currentRow, self.currentColumn, imagelabel)
        else:
            self.put_gou_image(self.currentRow,self.currentColumn)

    def put_one_image_on_cell(self,num):
        row_ = (num-1)//10
        if row_ in [1,3,5,7,9]:
            col_ = (num-1)%10
            col_ = 9-col_
        else:
            col_ = (num - 1) % 10
        imagelabel = QLabel()
        imagelabel.setText("")
        imagelabel.setScaledContents(True)
        pixmap = QPixmap()
        # pixmap.load("./resources/gou.ico")
        pixmap.load(":/mainwindow/picture.ico")
        imagelabel.setPixmap(pixmap)
        self.ui.tableWidget.setCellWidget(row_,col_,imagelabel)

    def closeEvent(self, event) -> None:

        reply = QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            try:
                self.daoguiandcamera.turnoff_motor(self.daoguiandcamera.slave1, 'XYZ')
            except:
                pass
            sys.exit(0)
        else:
            event.ignore()

    def turn_off_motor(self):
        try:
            if self.thread1.is_alive():
                stop_thread(self.thread1)
        except:
            pass
        try:
            if self.thread2.is_alive():
                stop_thread(self.thread2)
        except:
            pass
        try:
            if self.thread3.is_alive():
                stop_thread(self.thread3)
        except:
            pass
        try:
            self.daoguiandcamera.turnoff_motor(self.daoguiandcamera.slave1, 'XYZ')
        except:
            QMessageBox.warning(self, '停止电机运动失败', '电机停止运动失败')

    def turn_off_application(self):
        try:
            self.daoguiandcamera.turnoff_motor(self.daoguiandcamera.slave1,'X')
        except:
            pass
        reply = QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit(0)
        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = Mainwindow()
    window.show()
    sys.exit(app.exec_())