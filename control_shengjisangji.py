from lianji_control.rtu_master import Slave
import time
from fit.cal_r import calR

if __name__ == "__main__":
    slave1 = Slave('COM4','01')
    slave1.write_single_register(90,12800) # 设置x轴细分
    # slave1.write_single_register(92, 3200)  # 设置y轴细分
    # slave1.write_single_register(94, 3200)  # 设置z轴细分
    # slave1.write_single_register(96, 3200)  # 设置a轴细分

    slave1.write_single_register(98, 1) #设置x轴转一圈的螺距
    slave1.write_single_register(100, 1) #设置y轴转一圈的螺距
    slave1.write_single_register(102, 1) #设置z轴转一圈的螺距
    slave1.write_single_register(104, 1) #设置a轴转一圈的螺距

    slave1.change_speed(15000, 200)
    print(slave1.read_cils(1,3))

    flag = 0  # flag = 1,返回原点，flag = 0,上升到具体位置
    if flag:
        slave1.go_origin(2, 1, 0)  # 升降台反转<2> 采集1号端口信号，低电平0有效 回零
    # time.sleep(2)
    else:
        distance = calR(4.302283)  # 计算上升20mm，转换线性距离
        print(distance)
        slave1.go_straight(distance,0,0,0)
    slave1.turnoff_serial()
