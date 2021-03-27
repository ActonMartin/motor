import serial

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from lianji_control.function import lianjicontrol
import time


class Slave:
    def __init__(self,port,slave_id):
        # logger = modbus_tk.utils.create_logger("console")
        self.slave_id = int(slave_id)
        self.serial = serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        self.master = modbus_rtu.RtuMaster(self.serial)
        self.master.set_timeout(3.0)
        self.master.set_verbose(True)

        self.lianji = lianjicontrol(slave_id)
        # 先进入联机模式
        self.lianji_()

    def lianji_(self):
        lianji_mode = self.lianji.switchmode('01')
        self.serial.write(lianji_mode)
        time.sleep(0.5)

    def read_cils(self,start,number):
        """
        读取线圈
        :param start:起始线圈端子
        :param number: 读取几个线圈
        :return: 结果
        """
        start = start-1
        data = self.master.execute(self.slave_id,cst.READ_COILS,start,number)
        return data

    def read_holding_registers(self,start,number):
        """
        读取寄存器
        if start==42,读取x轴坐标，需要除以1000
        :param start:
        :param number:
        :return:
        """
        start = start-1
        data = self.master.execute(self.slave_id,cst.READ_HOLDING_REGISTERS,start,number)
        return data

    def write_single_coil(self,start,value):
        """
        写单个线圈
        :param start:
        :param value:
        :return:
        """
        start = start -1
        data = self.master.execute(self.slave_id, cst.WRITE_SINGLE_COIL,start,output_value=value)
        return data

    def write_single_register(self,start,value):
        """
        写单个寄存器
        :param start:
        :param value:
        :return:
        """
        start = start-1
        data = self.master.execute(self.slave_id, cst.WRITE_SINGLE_REGISTER, start, output_value=value)
        return data

    def watch_metal_stopper(self):
        """
        检测金属感应器，作用不大
        :return:
        """
        while True:
            data = self.read_cils(8,1)
            time.sleep(0.5)

    def go_straight(self,x,y,z,a):
        code = self.lianji.straight_interpolation(x,y,z,a)
        self.serial.write(code)
        time.sleep(0.5)

    def change_speed(self,speed,acceleration):
        code = self.lianji.changespeedandacceleration(speed,acceleration)
        self.serial.write(code)
        time.sleep(0.5)

    def go_origin(self,direction,siginal_input,method):
        """
        <3 返回原点> 执行该指令后，指定的轴一直转动到信号输入端有触发信号，之后电机反转，到触发信号消失后停止，相应轴的内部坐标清零
        :param direction: 指定回到原点的轴与转动方向,int
        {1:x轴正传，2:x轴反转，3:y轴正转,4:y轴反转,5:z轴正转,6:z轴反转,7:a轴正转,8:a轴反转,}
        :param siginal_input: 指定触发信号的输入端
        :param method: 指定触发方式 0:低电平/接通/是 1:高电平/断开/否
        :return:
        """
        code = self.lianji.go_origin(direction,siginal_input,method)
        self.serial.write(code)
        time.sleep(0.5)

    def go_zero(self,direction):
        """
        <5 回到坐标0>  指定需要返回零点的轴，返回命令
        解释：该指令以直线插补的方式回到0坐标。当执行该指令之前还没有执行过<3 返回原点>
        与<21 坐标清零>指令，则<5 回到坐标0>就是回到控制器通电时的点。
        如已经执行过上述两指令，则<5 回到坐标0>就是回到<3 返回原点>与<21 坐标清零>
        指令完成后时的点
        direction : str 1 X,2 Y,3 YX,4 Z,5 ZX,6 ZY,7 ZYX,8 A,9 AX,10 AY,11 AYX,12 AZ,13 AZX,14 AZY,15 AZYX
        """
        code = self.lianji.go_zero(direction)
        self.serial.write(code)
        time.sleep(0.5)

    def turnoff_serial(self):
        "关闭串口"
        self.serial.close()

    def delay(self,frequency,xi_fen,step_length,distance):
        """
        :param frequency: 频率25000
        :param xi_fen: 细分数 12800
        :param step_length: 步进电机一圈走的步长 4mm
        :return: 需要的延时 s
        公式 frequency*60/((360/1.8)*(xi_fen/200)) 得到 转每分钟
        """
        speed = frequency/((360/1.8)*(xi_fen/200))*step_length #得到 mm每秒
        time = distance/speed
        return time


if __name__ == "__main__":
    slave1 = Slave('COM4','01')
    slave1.write_single_register(90,12800) # 设置x轴细分
    # slave1.write_single_register(92, 3200)  # 设置y轴细分
    # slave1.write_single_register(94, 3200)  # 设置z轴细分
    # slave1.write_single_register(96, 3200)  # 设置a轴细分

    slave1.write_single_register(98, 4) #设置x轴转一圈的螺距
    slave1.write_single_register(100, 4) #设置y轴转一圈的螺距
    slave1.write_single_register(102, 4) #设置z轴转一圈的螺距
    slave1.write_single_register(104, 4) #设置a轴转一圈的螺距

    slave1.change_speed(50000, 200)
    slave1.go_origin(1, 8, 0)
    time.sleep(2)
    # slave1.go_straight(-12, 0, 0, 0)
    import random
    for i in range(200):
        x = random.sample(range(10,35),3)
        x1,x2,x3 = x[0],x[1],x[2]
        dd = slave1.delay(50000,12800,4,x1)+3
        slave1.change_speed(50000, 200)

        slave1.go_straight(-x1, 0, 0, 0)

        print('sleep {}s'.format(dd))
        time.sleep(dd)

        slave1.go_zero('x')

        print('sleep {}s'.format(dd))
        time.sleep(dd)

        # print('第 {} 次,随机数{},{},{}'.format(i, x1, x2, x3))
        print('第 {} 次'.format(i))
        print('-'*30)
    # slave1.change_speed(50000, 200)
    # slave1.go_straight(-30, 0, 0, 0) #填写成30的话，就抵着了，控制器以为走了，往回走就会多走。
    # slave1.go_zero('x')

    # slave1.change_speed(10000, 200)
    # slave1.go_straight(-30, 0, 0, 0)
    # slave1.change_speed(3000, 200)
    # slave1.go_zero('x')
    slave1.turnoff_serial()


