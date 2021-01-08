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
        while True:
            data = self.read_cils(8,1)
            time.sleep(0.1)

    def go_straight(self,x,y,z,a):
        code = self.lianji.straight_interpolation(x,y,z,a)
        self.serial.write(code)
        time.sleep(0.1)

    def change_speed(self,speed,acceleration):
        code = self.lianji.changespeedandacceleration(speed,acceleration)
        self.serial.write(code)
        time.sleep(0.1)

    def go_origin(self,direction,siginal_input,method):
        """
        <3 返回原点> 执行该指令后，指定的轴一直转动到信号输入端有触发信号，之后电机反转，到触发信号消失后停止，相应轴的内部坐标清零
        :param direction: 指定回到原点的轴与转动方向,int
        {1:x轴正传，2:x轴反转，3:y轴正转,4:y轴反转,5:z轴正转,6:z轴反转,7:a轴正转,8:a轴反转,}
        :param siginal_input: 指定触发信号的输入端
        0:低电平/接通/是 1:高电平/断开/否
        :param method: 指定触发方式
        :return:
        """
        code = self.lianji.go_origin(direction,siginal_input,method)
        self.serial.write(code)
        time.sleep(0.1)

    def go_zero(self,direction):
        code = self.lianji.go_zero(direction)
        self.serial.write(code)
        time.sleep(0.1)

    def turnoff_serial(self):
        "关闭串口"
        self.serial.close()


if __name__ == "__main__":
    slave1 = Slave('COM4','01')

    print(slave1.read_holding_registers(42,1))
    slave1.go_origin(1,8,0)
    slave1.change_speed(12000,200)
    slave1.go_straight(-10.005,0,0,0)
    slave1.change_speed(25000,200)
    slave1.go_straight(-20,0,0,0)
    slave1.change_speed(45000, 200)
    slave1.go_straight(-40, 0, 0, 0)
    slave1.change_speed(50000, 200)
    slave1.go_straight(-50, 0, 0, 0)
    slave1.go_zero('x')
    slave1.turnoff_serial()
