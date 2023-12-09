from lianji_control.rtu_master import Slave
from fit.cal_r import cal_circle,cal_equation


def control_shengjiangji(slave_id,height, axis):
    """
    :param slave_id: 从机id
    :param height: 想上升的线性高度
    :param axis:移动那个轴
    :return: 返回从机id, 上升的高度
    """
    height_low = height-5
    if height_low < 0:
        slave_id.go_origin(2, 1, 0) # 升降台反转<2> 采集1号端口信号，低电平0有效 回零
    height_low_noxianxing = cal_circle(cal_equation(),height_low)
    height_noxianxing = cal_circle(cal_equation(), height)
    if axis == 'x':
        slave_id.go_straight(height_low_noxianxing, 0, 0, 0)
        slave_id.go_straight(height_noxianxing, 0, 0, 0)


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
    # print(slave1.read_cils(1,3))
    equation = cal_equation() # 计算拟合方程式
    flag = 0  # flag = 1,返回原点，flag = 0,上升到具体位置
    if flag:
        slave1.go_origin(2, 1, 0)  # 升降台反转<2> 采集1号端口信号，低电平0有效 回零
        slave1.turnoff_serial()
    else:
        # 10.8 检查油墨
        # 10.5 检查小面伤痕
        # 11.9 检查底座不良
        # 内污看不清楚
        # 12.5 检查溢胶
        # height_list = [8,10.5,10.8,11.9,12.5]
        height_list = [8,11,12,13,14]
        import time
        while True:
            for i in height_list:
                distance = cal_circle(equation,i)  # 计算上升10.8mm，转换线性距离,检查油墨
                print(i)
                slave1.go_straight(distance,None,None,None)
                time.sleep(3)
        slave1.turnoff_serial()
