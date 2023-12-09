from lianji_control.rtu_master import *
from fit.cal_r import cal_circle,cal_equation
from path_planning.path_file2 import PathPlanning
from lianji_control.function import *
from lianji_control.utilty.numeration_convert import *
from hikvision.utilty.Camera_new_method import *
import cv2
import math
import datetime
import time
from PyQt5.QtCore import pyqtSignal
""" 绝对坐标模式"""

def choose_slave(port,slave_addr):
    # port :"COM4"
    # slave_addr: "01"
    slave = Slave(port,slave_addr)
    return slave

def config_xifen_luoju(slave):
    # 配置细分、螺距
    slave.write_single_register(90, 3200) # 设置x轴细分
    slave.write_single_register(92, 3200)  # 设置y轴细分
    slave.write_single_register(94, 3200)  # 设置z轴细分
    # slave.write_single_register(96, 3200)  # 设置a轴细分

    slave.write_single_register(98, 5) #设置x轴转一圈的螺距
    slave.write_single_register(100, 5) #设置y轴转一圈的螺距
    slave.write_single_register(102, 5) #设置z轴转一圈的螺距
    # slave1.write_single_register(104, 1) #设置a轴转一圈的螺距


def change_speed_acceleration(slave,speed,acceleration):
    slave.change_speed(speed, acceleration)


def change_startup_end_speed(slave,startup_speed,end_speed):
    slave.startup_end_speed(startup_speed,end_speed)


def go_origin(slave):
    slave.go_origin(direction=2, siginal_input=6, method=0)
    slave.go_origin(direction=4, siginal_input=7, method=0)
    slave.go_origin(direction=6, siginal_input=8, method=0)


def go_first_position(slave,x_origin,y_origin,z_origin):
    #x_origin,y_origin,z_origin = -108.337,-68.125,7.397
    # slave.go_straight(0,y_origin,0,a=None)
    # slave.go_straight(x_origin-5,y_origin-5,0,a=None)
    slave.go_straight(x_origin,y_origin,z_origin,a=None)

def move2switcher(slave):
    #转动到开关触发
    slave.move2switcher(direction=1,siginal_input=5,method=0)

    slave.move2switcher(direction=3,siginal_input=4,method=0)

    slave.move2switcher(direction=6,siginal_input=1,method=0)


def clear_axis_data(slave,direction):
    """
    清除轴坐标
    :param direction:
    1:x轴 2:y 3:yx 4:z 5:zx 6:zy 7:zyx 8:a 9:ax 10:ay 11:ayx 12:az 13:azx 14:azy 15:azyx
    :return:
    """
    slave.clera_axis_data(direction)


def main():
    equation = cal_equation() # 计算拟合方程式
    z_distance = cal_circle(equation,4)
    print(z_distance)
    slave1.go_straight(-30,-45,None,None)
    # import time
    # time.sleep(15)
    # x = slave1.read_holding_registers(42,1)
    # print(x[0]/1000)

def go_around(cam,slave,x_origin,y_origin,z_origin,path_lines):
    child_images_list = []
    count_flag = 0 # 每一个物体xy都需要变换四次完成拍照
    for x_xd,y_xd in path_lines:
        count_flag += 1
        # todo 加一个for z in z_lines
        x_xd,y_xd = x_xd*1000,y_xd*1000
        x_this =x_origin*1000+x_xd
        y_this = y_origin*1000+y_xd
        x_this = x_this/1000
        y_this = y_this/1000
        # print("目标位置 x:{},y:{}".format(x_this,y_this))
        slave.go_straight(x_this,y_this,z_origin,None)
        while True:
            x,y,z = get_x_y_z(slave1)
            # print("------目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this,y_this,x,y))
            if math.isclose(x_this,x,rel_tol=5e-5) and math.isclose(y_this,y,rel_tol=5e-5):
                print("目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this,y_this,x,y))
                try:
                    set_Value(cam, param_type='command_value',node_name="TriggerSoftware")
                except:
                    pass
                kjh0 = access_get_image(cam,"getImagebuffer")
                if kjh0 is not None:
                    child_images_list.append(kjh0)
                if count_flag == 4:
                    # 数到四次之后，一个物体拍摄完成，就可以将这一组拍摄的图片加到images_list里面，然后将子list清空
                    count_flag = 0

                    child_images_list = []
            break

def operation_camera():
    # 枚举设备
    deviceList = enum_devices(device=0, device_way=False)

    # 创建相机实例并创建句柄,(设置日志路径)
    cam, stDeviceList = creat_camera(deviceList, 0, log=False)

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
        set_Value(cam,param_type="enum_value",node_name="PixelFormat",node_value=17301505)
    except:
        pass
    # 设置曝光时间 5000
    try:
        set_Value(cam,param_type="float_value",node_name="ExposureTime",node_value=5000)
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
    #开始取流
    try:
        start_grab_and_get_data_size(cam)
    except:
        pass
    return cam


def get_x_y_z(slave):
    positions = slave.read_holding_registers(42,6)
    # print(positions)
    x_low,x_high = positions[0],positions[1]
    y_low,y_high = positions[2],positions[3]
    z_low,z_high = positions[4],positions[5]
    def convert(low,high):
        low_bin,high_bin = bin(low)[2:],bin(high)[2:]
        low_bin,high_bin = '{0:0>16s}'.format(low_bin),'{0:0>16s}'.format(high_bin)
        value_bin = high_bin+low_bin
        bin2dec = Bin2Dec()
        value_signed = bin2dec.bin2dec_auto(value_bin)
        value_signed = value_signed/1000
        return value_signed
    x_position = convert(x_low,x_high)
    y_position = convert(y_low,y_high)
    z_position = convert(z_low,z_high)

    return x_position,y_position,z_position

def test_wucha(cam,slave,x_origin,y_origin,z_origin):
    #x_origin,y_origin,z_origin = -108.337,-68.125,7.397
    path_lines = [(0.0,0.0),(96.504,0)]
    image_count = 1
    run_count = 0
    for ii in range(1000):
        for x_xd,y_xd in path_lines:
            # x_xd,y_xd = i
            x_xd,y_xd = x_xd*1000,y_xd*1000
            x_this =x_origin*1000-x_xd
            y_this = y_origin*1000+y_xd
            x_this = x_this/1000
            y_this = y_this/1000
            # print("目标位置 x:{},y:{}".format(x_this,y_this))
            slave.go_straight(x_this,y_this,z_origin,None)
            print('run_count value',run_count)
            # x_list = [999,888]
            while True:
                x,y,z = get_x_y_z(slave1)
                # x_list.append(x)
                # print(x_list)
                # print("目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this,y_this,x,y))
                # if x_this==x and y_this==y:
                # if x_list[-1] == x_list[-2] and x_list[-1]!=0.0:
                if math.isclose(x_this,x,rel_tol=2e-4) and math.isclose(y_this,y,rel_tol=2e-4):
                #     print("目标位置 x:{},y:{},目前位置x:{},y:{}".format(x_this,y_this,x,y))
                    print("到达指定位置")
                    # x_list=[999,888]
                    if run_count % 5 == 0 and y_xd==0 and x_xd!=0:
                        print("第{}个来回".format(run_count))
                        # 执行软触发
                        try:
                            set_Value(cam, param_type='command_value',node_name="TriggerSoftware")
                        except:
                            pass
                        kjh0 = access_get_image(cam,"getImagebuffer")
                        image_name = str(run_count)+".jpg"
                        image_path = os.path.join("D:/Projects/motor/images_saves/y",image_name)
                        cv2.imwrite(image_path,kjh0)
                    if y_xd==0 and x_xd!=0:
                        run_count += 1
                    break


if __name__ == '__main__':
    camera = operation_camera()
    slave1 = choose_slave("COM4","01")
    config_xifen_luoju(slave1)
    # change_startup_end_speed(slave1,800,800)
    change_startup_end_speed(slave1,1600,1600)
    change_speed_acceleration(slave1,20000,80)
    # go_origin(slave1)
    a_ = time.time()
    which_time_count = 0
    while True:
        if which_time_count % 50 == 0:
            b_ = time.time()
            print("50个板子平均时间为{}".format(b_-a_))
            a_ = time.time()
            # change_speed_acceleration(slave1,20000,60)
            go_origin(slave1)
            # change_speed_acceleration(slave1,25000,60)
            # move2switcher(slave1)
            # clear_axis_data(slave1,7)
        # while True:
        #     a,b,c = get_x_y_z(slave1)
        #     print(a,b,c)
        # go_first_position(slave1,x_origin=105.747,y_origin=-68.143,z_origin=7.543)
        # go_around(camera,slave1,x_origin=105.747,y_origin=-68.143,z_origin=7.543)
        # go_around(camera,slave1,x_origin=108.703,y_origin=-71.447,z_origin=7.67)
        # go_first_position(slave1,x_origin=-105.817,y_origin=-66.926,z_origin=7.843)
        # go_around(camera,slave1,x_origin=-105.817,y_origin=-66.926,z_origin=7.843,which_time_count=which_time_count)

        # go_first_position(slave1,x_origin=-106.491,y_origin=-64.798,z_origin=7.843)
        go_first_position(slave1,x_origin=22.242,y_origin=2.867,z_origin=23.82)
        go_around(camera,slave1,x_origin=22.242,y_origin=2.867,z_origin=23.82)
        # test_wucha(camera,slave1,x_origin=105.747,y_origin=-68.143,z_origin=7.543)
        which_time_count+=1




