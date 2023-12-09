import sys

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer,Qt,pyqtSignal

from ui.ui_new_images_viewer import Ui_images_viewer



class IMG_WIN(QWidget):
    def __init__(self, graphicsView):
        super().__init__()
        self.graphicsView = graphicsView
        self.graphicsView.setStyleSheet(
            "padding: 0px; border: 0px;")  # 内边距和边界去除
        self.scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeft |
                                       QtCore.Qt.AlignTop)  # 改变对齐方式

        self.graphicsView.setSceneRect(
            0, 0,
            self.graphicsView.viewport().width(),
            self.graphicsView.height())  # 设置图形场景大小和图形视图大小一致
        # self.graphicsView.setSceneRect(0, 0,self.graphicsView.width(),self.graphicsView.height())  # 设置图形场景大小和图形视图大小一致
        self.graphicsView.setScene(self.scene)

        self.scene.mousePressEvent = self.scene_MousePressEvent  # 接管图形场景的鼠标点击事件
        # self.scene.mouseReleaseEvent = self.scene_mouseReleaseEvent
        self.scene.mouseMoveEvent = self.scene_mouseMoveEvent  # 接管图形场景的鼠标移动事件
        self.scene.wheelEvent = self.scene_wheelEvent  # 接管图形场景的滑轮事件

        self.ratio = 1  # 缩放初始比例
        self.zoom_step = 0.2  # 缩放步长
        self.zoom_max = 4  # 缩放最大值
        self.zoom_min = 0.2  # 缩放最小值
        self.pixmapItem = None

    def addScenes(self, img):  # 绘制图形
        self.org = img
        if self.pixmapItem != None:
            originX = self.pixmapItem.x()
            originY = self.pixmapItem.y()
        else:
            originX, originY = 0, 0  # 坐标基点

        self.scene.clear()  # 清除当前图元
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        self.pixmap = QtGui.QPixmap(
            QtGui.QImage(img[:], img.shape[1], img.shape[0], img.shape[1] * 3,
                         QtGui.QImage.Format_RGB888))  # 转化为qlbel格式

        self.pixmapItem = self.scene.addPixmap(self.pixmap)
        self.pixmapItem.setScale(self.ratio)  # 缩放
        self.pixmapItem.setPos(originX, originY)

    def scene_MousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:  # 左键按下
            # print("鼠标左键单击")  # 响应测试语句
            # print(event.scenePos())
            self.preMousePosition = event.scenePos()  # 获取鼠标当前位置
        # if event.button() == QtCore.Qt.RightButton:  # 右键按下
        #     print("鼠标右键单击")  # 响应测试语句

    def scene_mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # print("左键移动")  # 响应测试语句
            self.MouseMove = event.scenePos(
            ) - self.preMousePosition  # 鼠标当前位置-先前位置=单次偏移量
            self.preMousePosition = event.scenePos()  # 更新当前鼠标在窗口上的位置，下次移动用
            self.pixmapItem.setPos(self.pixmapItem.pos() +
                                   self.MouseMove)  # 更新图元位置

    # 定义滚轮方法。当鼠标在图元范围之外，以图元中心为缩放原点；当鼠标在图元之中，以鼠标悬停位置为缩放中心
    def scene_wheelEvent(self, event):
        angle = event.delta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        if angle > 0:
            # print("滚轮上滚")
            self.ratio += self.zoom_step  # 缩放比例自加
            if self.ratio > self.zoom_max:
                self.ratio = self.zoom_max
            else:
                w = self.pixmap.size().width() * (self.ratio - self.zoom_step)
                h = self.pixmap.size().height() * (self.ratio - self.zoom_step)
                x1 = self.pixmapItem.pos().x()  # 图元左位置
                x2 = self.pixmapItem.pos().x() + w  # 图元右位置
                y1 = self.pixmapItem.pos().y()  # 图元上位置
                y2 = self.pixmapItem.pos().y() + h  # 图元下位置
                if x1 < event.scenePos().x() < x2 and y1 < event.scenePos().y(
                ) < y2:  # 判断鼠标悬停位置是否在图元中
                    # print('在内部')
                    self.pixmapItem.setScale(self.ratio)  # 缩放
                    a1 = event.scenePos() - self.pixmapItem.pos()  # 鼠标与图元左上角的差值
                    a2 = self.ratio / (self.ratio - self.zoom_step) - 1  # 对应比例
                    delta = a1 * a2
                    self.pixmapItem.setPos(self.pixmapItem.pos() - delta)
                    # ----------------------------分维度计算偏移量-----------------------------
                    # delta_x = a1.x()*a2
                    # delta_y = a1.y()*a2
                    # self.pixmapItem.setPos(self.pixmapItem.pos().x() - delta_x,
                    #                        self.pixmapItem.pos().y() - delta_y)  # 图元偏移
                    # -------------------------------------------------------------------------

                else:
                    # print('在外部')  # 以图元中心缩放
                    self.pixmapItem.setScale(self.ratio)  # 缩放
                    delta_x = (self.pixmap.size().width() *
                               self.zoom_step) / 2  # 图元偏移量
                    delta_y = (self.pixmap.size().height() * self.zoom_step) / 2
                    self.pixmapItem.setPos(self.pixmapItem.pos().x() - delta_x,
                                           self.pixmapItem.pos().y() -
                                           delta_y)  # 图元偏移
        else:
            # print("滚轮下滚")
            self.ratio -= self.zoom_step
            if self.ratio < self.zoom_min:
                self.ratio = self.zoom_min
            else:
                w = self.pixmap.size().width() * (self.ratio + self.zoom_step)
                h = self.pixmap.size().height() * (self.ratio + self.zoom_step)
                x1 = self.pixmapItem.pos().x()
                x2 = self.pixmapItem.pos().x() + w
                y1 = self.pixmapItem.pos().y()
                y2 = self.pixmapItem.pos().y() + h
                # print(x1, x2, y1, y2)
                if x1 < event.scenePos().x() < x2 and y1 < event.scenePos().y(
                ) < y2:
                    # print('在内部')
                    self.pixmapItem.setScale(self.ratio)  # 缩放
                    a1 = event.scenePos() - self.pixmapItem.pos()  # 鼠标与图元左上角的差值
                    a2 = self.ratio / (self.ratio + self.zoom_step) - 1  # 对应比例
                    delta = a1 * a2
                    self.pixmapItem.setPos(self.pixmapItem.pos() - delta)
                    # ----------------------------分维度计算偏移量-----------------------------
                    # delta_x = a1.x()*a2
                    # delta_y = a1.y()*a2
                    # self.pixmapItem.setPos(self.pixmapItem.pos().x() - delta_x,
                    #                        self.pixmapItem.pos().y() - delta_y)  # 图元偏移
                    # -------------------------------------------------------------------------
                else:
                    # print('在外部')
                    self.pixmapItem.setScale(self.ratio)
                    delta_x = (self.pixmap.size().width() * self.zoom_step) / 2
                    delta_y = (self.pixmap.size().height() * self.zoom_step) / 2
                    self.pixmapItem.setPos(self.pixmapItem.pos().x() + delta_x,
                                           self.pixmapItem.pos().y() + delta_y)


"""
其中data_biaoqian是一个numpy数组，10*10*(每一组拍摄的图片张数)*(缺陷种类数目)
在这个地方，现在的缺陷种类数目有6种，也就是numpy数组的维度是10*10*(每一组拍摄的图片张数)*6
self.index就是每一组拍摄的图片张数的索引
六种缺陷的索引分别是：dizuobuliang:0,neiwu:1,xiaomianshang:2,youwu:3,kuangshang:4,yijiao:5
"""


class ImageViewerGUI(QWidget):
    emit2main_page = pyqtSignal(int,int,int,int)
    emit2main_page_defection = pyqtSignal(int)
    right_arrow_signal = pyqtSignal(int)
    left_arrow_signal = pyqtSignal(int)

    def __init__(self, neiwu_value, dizuobuliang_value, xiaomianshang_value,
                 youwu_value, kuangshang_value, yijiao_value):
        super().__init__()

        self.ui = Ui_images_viewer()
        self.ui.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowIcon(QIcon(':/setting/setting.ico'))
        self.graphic = IMG_WIN(self.ui.graphicsView)  # 实例化IMG_WIN类
        self.timer_a = QTimer()
        self.timer_a.start(200)
        self.timer_a.timeout.connect(self.deal_emit_defection_signal)
        self.ui.pushButton.clicked.connect(self.select_img)
        self.ui.pushButton_a.clicked.connect(self.preview_image)
        self.ui.pushButton_b.clicked.connect(self.next_image)
        self.left_arrow_signal.connect(self.left_arrow)
        self.right_arrow_signal.connect(self.right_arrow)
        # self.HK_right = SystemHotkey()
        # self.HK_left = SystemHotkey()
        # self.HK_right.register(('control','0'),callback=lambda x:self.right_send_event(1))
        # self.HK_left.register(('control','9'),callback=lambda x:self.left_send_event(1))
        self.index = 0

        self.dizuobuliang = dizuobuliang_value
        self.neiwu = neiwu_value
        self.xiaomianshang = xiaomianshang_value
        self.youwu = youwu_value
        self.kuangshang = kuangshang_value
        self.yijiao = yijiao_value

        self.ui.checkBox_dizuobuliang.clicked.connect(self.dizuobuliang_func)
        self.ui.checkBox_neiwu.clicked.connect(self.neiwu_func)
        self.ui.checkBox_xiaomianshang.clicked.connect(self.xiaomianshang_func)
        self.ui.checkBox_youwu.clicked.connect(self.youwu_func)
        self.ui.checkBox_kuangshang.clicked.connect(self.kuangshang_func)
        self.ui.checkBox_yijiao.clicked.connect(self.yijiao_func)

        self.ui.checkBox_dizuobuliang.stateChanged.connect(
            self.change_data_biaoqian_dizuobuliang)
        self.ui.checkBox_neiwu.stateChanged.connect(
            self.change_data_biaoqian_neiwu)
        self.ui.checkBox_xiaomianshang.stateChanged.connect(
            self.change_data_biaoqian_xiaomianshang)
        self.ui.checkBox_youwu.stateChanged.connect(
            self.change_data_biaoqian_youwu)
        self.ui.checkBox_kuangshang.stateChanged.connect(
            self.change_data_biaoqian_kuangshang)
        self.ui.checkBox_yijiao.stateChanged.connect(
            self.change_data_biaoqian_yijiao)

    def add_images_list(self, images_list):
        self.images_list = images_list
        self.indexs = len(images_list) - 1
        self.set_default_image()

    def add_data_biaoqian(self, data_biaoqian):
        self.data_biaoqian = data_biaoqian
        # self.watch_data_biaoqian_timer = QTimer()
        # self.watch_data_biaoqian_timer.start(200)
        # self.watch_data_biaoqian_timer.timeout.connect(self.change_data_biaoqian)
        self.data_biaoqian_cell = self.data_biaoqian[self.row][self.col]
        if self.data_biaoqian_cell[0] == 1:
            self.ui.checkBox_dizuobuliang.setChecked(1)
        if self.data_biaoqian_cell[1] == 1:
            self.ui.checkBox_neiwu.setChecked(1)
        if self.data_biaoqian_cell[2] == 1:
            self.ui.checkBox_xiaomianshang.setChecked(1)
        if self.data_biaoqian_cell[3] == 1:
            self.ui.checkBox_youwu.setChecked(1)
        if self.data_biaoqian_cell[4] == 1:
            self.ui.checkBox_kuangshang.setChecked(1)
        if self.data_biaoqian_cell[5] == 1:
            self.ui.checkBox_yijiao.setChecked(1)

    def change_data_biaoqian_dizuobuliang(self):
        if self.ui.checkBox_dizuobuliang.isChecked():
            self.dizuobuliang_flag = 1
        else:
            self.dizuobuliang_flag = 0
        # 六种缺陷的索引分别是：dizuobuliang:0,neiwu:1,xiaomianshang:2,youwu:3,kuangshang:4,yijiao:5
        self.data_biaoqian[self.row][self.col][0] = self.dizuobuliang_flag

    def change_data_biaoqian_neiwu(self):
        if self.ui.checkBox_neiwu.isChecked():
            self.neiwu_flag = 1
        else:
            self.neiwu_flag = 0
        # 六种缺陷的索引分别是：dizuobuliang:0,neiwu:1,xiaomianshang:2,youwu:3,kuangshang:4,yijiao:5
        self.data_biaoqian[self.row][self.col][1] = self.neiwu_flag

    def change_data_biaoqian_xiaomianshang(self):
        if self.ui.checkBox_xiaomianshang.isChecked():
            self.xiaomianshang_flag = 1
        else:
            self.xiaomianshang_flag = 0
        # 六种缺陷的索引分别是：dizuobuliang:0,neiwu:1,xiaomianshang:2,youwu:3,kuangshang:4,yijiao:5
        self.data_biaoqian[self.row][self.col][2] = self.xiaomianshang_flag

    def change_data_biaoqian_youwu(self):
        if self.ui.checkBox_youwu.isChecked():
            self.youwu_flag = 1
        else:
            self.youwu_flag = 0
        # 六种缺陷的索引分别是：dizuobuliang:0,neiwu:1,xiaomianshang:2,youwu:3,kuangshang:4,yijiao:5
        self.data_biaoqian[self.row][self.col][3] = self.youwu_flag

    def change_data_biaoqian_kuangshang(self):
        if self.ui.checkBox_kuangshang.isChecked():
            self.kuangshang_flag = 1
        else:
            self.kuangshang_flag = 0
        # 六种缺陷的索引分别是：dizuobuliang:0,neiwu:1,xiaomianshang:2,youwu:3,kuangshang:4,yijiao:5
        self.data_biaoqian[self.row][self.col][4] = self.kuangshang_flag

    def change_data_biaoqian_yijiao(self):
        if self.ui.checkBox_yijiao.isChecked():
            self.yijiao_flag = 1
        else:
            self.yijiao_flag = 0
        # 六种缺陷的索引分别是：dizuobuliang:0,neiwu:1,xiaomianshang:2,youwu:3,kuangshang:4,yijiao:5
        self.data_biaoqian[self.row][self.col][5] = self.yijiao_flag

    def add_zuobiao(self, row, col,images_index_in_images_list):
        """
        row,col是10*10这个的第一第二的索引
        """
        self.row = row
        self.col = col
        self.images_index_in_images_list = images_index_in_images_list

    def neiwu_func(self):
        if self.ui.checkBox_neiwu.isChecked():
            self.neiwu += 1
        else:
            self.neiwu -= 1

    def dizuobuliang_func(self):
        if self.ui.checkBox_dizuobuliang.isChecked():
            self.dizuobuliang += 1
        else:
            self.dizuobuliang -= 1

    def xiaomianshang_func(self):
        if self.ui.checkBox_xiaomianshang.isChecked():
            self.xiaomianshang += 1
        else:
            self.xiaomianshang -= 1

    def youwu_func(self):
        if self.ui.checkBox_youwu.isChecked():
            self.youwu += 1
        else:
            self.youwu -= 1

    def kuangshang_func(self):
        if self.ui.checkBox_kuangshang.isChecked():
            self.kuangshang += 1
        else:
            self.kuangshang -= 1

    def yijiao_func(self):
        if self.ui.checkBox_yijiao.isChecked():
            self.yijiao += 1
        else:
            self.yijiao -= 1

    def set_default_image(self):
        if self.images_list:
            self.graphic.addScenes(self.images_list[self.index])

    def preview_image(self):
        self.index -= 1
        if self.index < 0:
            self.index = 0
            # self.deal_emit_defection_signal()
            self.emit2main_page.emit(self.row, self.col, self.images_index_in_images_list, 0)
        self.graphic.addScenes(self.images_list[self.index])

    def next_image(self):
        self.index += 1
        if self.index > self.indexs:
            self.index = self.indexs
            # self.deal_emit_defection_signal()
            self.emit2main_page.emit(self.row, self.col, self.images_index_in_images_list,1)
        self.graphic.addScenes((self.images_list[self.index]))

    def deal_emit_defection_signal(self):
        if self.ui.checkBox_dizuobuliang.isChecked() \
                or self.ui.checkBox_neiwu.isChecked() \
                or self.ui.checkBox_xiaomianshang.isChecked()\
                or self.ui.checkBox_youwu.isChecked() \
                or self.ui.checkBox_kuangshang.isChecked() \
                or self.ui.checkBox_yijiao.isChecked():
            self.emit2main_page_defection.emit(1)
        else:
            self.emit2main_page_defection.emit(0)

    def select_img(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择你要上传的图片",  # 标题
            r"E:\picture\test",  # 起始目录
            "图片类型 (*.png *.jpg *.bmp)"  # 选择类型过滤项，过滤内容在括号中
        )
        if filePath == '':
            return
        else:
            img = cv2.imread(filePath)
            # print(type(img))
            self.graphic.addScenes(img)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            self.right_arrow_signal.emit(1)
        if event.key() == Qt.Key_A:
            self.left_arrow_signal.emit(1)
        if event.key() == Qt.Key_Right:
            self.right_arrow_signal.emit(1)
        if event.key() == Qt.Key_Left:
            self.left_arrow_signal.emit(1)

    # def right_send_event(self,num):
    #     self.right_arrow_signal.emit(num)
    #
    # def left_send_event(self,num):
    #     self.left_arrow_signal.emit(num)

    def right_arrow(self,num):
        self.next_image()

    def left_arrow(self,num):
        self.preview_image()

if __name__ == "__main__":
    import glob
    files = glob.glob("D:\\Projects\\motor\\test\\images\\*.png")
    image_list = []
    for i in files:
        image_list.append(cv2.imread(i))
    app = QApplication(sys.argv)
    window = ImageViewerGUI(0,0,0,0,0,0)
    window.add_images_list(image_list)
    window.show()
    sys.exit(app.exec_())
