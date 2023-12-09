# from crc.CRC16 import CRC
from lianji_control.utils import bytecoding
from lianji_control.utilty.CRC16 import CRC


class TouchScreen:
    def __init__(self,slave_addr):
        self.slave_addr = slave_addr
        self.crc = CRC()

    @staticmethod
    def change_style(start_addr,number):
        if isinstance(start_addr,int):
            port_addr = hex(start_addr-1)[2:]
            port_addr = (number-len(port_addr))*'0' + port_addr
            return port_addr
        if isinstance(start_addr,str):
            convert_data = hex(int(start_addr))[2:]
            convert_data = (number-len(convert_data))*'0' + convert_data
            return convert_data

    @staticmethod
    def reverselowhigh(data_in,type):
        """
        传入data = '00059540'
        if type = 4 返回 95400005
        if type = 2 返回 40950500
        """
        data_temp = []
        for i in range(0, len(data_in), type):
            data_temp.append(data_in[i:i + type])
        datareversal = ''.join(data_temp[::-1])
        return datareversal

    @bytecoding
    def readcoilstatus(self,start_addr,number):
        """
        功能码01 读取线圈（端子）状态
        :param start_addr:读取端口开始
        :param number:读取开始端口后多少数量
        :return:需要读取状态的命令
        """
        assert number <= 140,print("查看数量只能是1到140之间的")
        assert start_addr+number <=140,print('状态查看的范围有误，查看端口过多超出140')

        function_code = '01'
        port_addr = hex(start_addr-1)[2:]
        port_addr = (4-len(port_addr))*'0' + port_addr

        number_addr = (4-len(str(number)))*'0' + str(number)

        code = self.slave_addr+function_code+port_addr+number_addr
        # print()
        crc_code = self.crc.crc16(code)
        return code+crc_code

    def encodereadstatus(self,code):
        """
        解析 读取线圈（端子）状态 接收到的命令
        code = 01 01 02 ff 01 39 cc
        type(code) str
        02是接收到的字节
        ff 01是后面收到的数据
        :param code:
        :return:
        """
        code = code.strip().replace(' ','')
        timebyte = int(code[4:6])
        data = code[6:timebyte*2+6]

        def hex2bin(data_hex):
            binary = bin(int(data_hex,16))[2:]
            binary = '0'*(timebyte*8-len(binary))+binary # # 不足8位补齐
            binary = binary[::-1]
            return binary

        data = self.reverselowhigh(data,2) #type hex
        result = hex2bin(data)
        return result

    @bytecoding
    def readregister(self,variable,number):
        """
        功能码03 读取寄存器命令
        :param variable_addr: 变量地址
        :param number: 读取几个
        :return: 读取命令
        """
        function_code = '03'
        # variable_addr可以使用change_style进行计算，下面两行是旧方法
        # variable_addr = hex(variable-1)[2:]
        # variable_addr = (4-len(variable_addr))*'0'+variable_addr
        variable_addr = self.change_style(variable,4)
        number_addr = number*2
        number_addr = self.change_style(number_addr+1,4)
        # number_addr = (4-len(str(number_addr)))*'0'+str(number_addr)
        code = self.slave_addr+function_code+variable_addr+number_addr
        crc_code = self.crc.crc16(code)
        return code+crc_code

    def encoderegister(self,num,code):
        """
        解析寄存器
        :param num:几个变量
        :return:返回一个列表，
        """
        try:
            if code[4:6] == '08':
                pass
        except:
            raise

        def reverselowhigh(data_in):
            """将返回的数据高低位还原回去"""
            data_temp = []
            for i in range(0, len(data_in), 4):
                data_temp.append(data_in[i:i + 4])
            datareversal = ''.join(data_temp[::-1])
            return datareversal

        code = code[6:-4]
        data_num = [code[i*8:(i+1)*8] for i in range(num)]
        result = []
        for i in range(num):
            res = reverselowhigh(data_num[i])
            res = int(res,16)
            result.append(res)
        return result

    @bytecoding
    def writecoilstatus(self,addr,data):
        """
        功能码05 写线圈（端子）状态
        :param addr:
        :param data:
        :return:
        """
        function_code = '05'
        addr_ = hex(addr-1)[2:]
        addr_ = (4-len(str(addr)))*'0' + str(addr_)
        if addr == 129 and data == 1:
            data_ = 'FF00H'
        elif addr ==129 and data == 0:
            data_ = '0000H'
        else:
            # todo 没有写完data_
            data_ = (8-len(str(data)))*'0'+str(data)
        code = self.slave_addr + function_code+ addr_+data_
        crc_code = self.crc.crc16(code)
        return code+crc_code

    @bytecoding
    def write_multi_registers(self,start_addr,data):
        """
        功能码16 写多个寄存器
        :param start_addr:
        :param data: 多个数据用分号隔开, 以此来获取数量
        :return:
        """
        function_code = '10'
        start_addr = self.change_style(start_addr,4)
        data = data.split(';')
        howmany = self.change_style(2*len(data)+1,4)
        databyte = self.change_style(4*len(data)+1,2)
        data_ = ''
        for each in data:
            i = self.change_style(each,8)
            data_ += self.reverselowhigh(i,4)
        code = self.slave_addr + function_code + start_addr+howmany+databyte+data_
        crc_code = self.crc.crc16(code)
        return code + crc_code


class lianjicontrol:
    """
    :param slave_addr:
    :return:
    """
    def __init__(self,slave_addr):
        self.slave_addr = slave_addr
        self.function_code = "7f"
        self.byte_cal = "11"
        self.dir_dict = {1: "X",2: "Y",3: "YX",4: "Z",5: "ZX",6: "ZY",7: "ZYX",
                    8: "A",9: "AX",10: "AY",11: "AYX",12: "AZ",13: "AZX",14: "AZY",15: "AZYX",}
        self.crc = CRC()

    @staticmethod
    def change_style(command,number):
        """
        command 指令数字
        number 需要最后生成几位
        将十进制command转换为16进制
        """
        command = hex(command)[2:]
        # command = (number-len(command))*'0' + command
        command = "{0:0>{1}s}".format(command,number)
        return command

    @staticmethod
    def reverselowhigh(data_in,type):
        """
        传入data = '000003e8'
        返回 e8030000
        """
        data_temp = []
        for i in range(0, len(data_in), type):
            data_temp.append(data_in[i:i + type])
        datareversal = ''.join(data_temp[::-1])
        return datareversal


    @bytecoding
    def restart_controler(self):
        """功能码123（0x7b）
        从站地址 + 功能码+ crc
        """
        function_code = '7b'
        code = self.slave_addr+ function_code
        crc_code = self.crc.crc16(code)
        return code+crc_code

    @bytecoding
    def readversion(self):
        """
        功能码124（0x7c）
        :param slave_addr:从站地址
        :return:
        """
        function_code = '7c'
        code = self.slave_addr+function_code
        crc_code = self.crc.crc16(code)
        return code + crc_code

    @bytecoding
    def switchmode(self,mode):
        """
        功能码126（0x7e)
        :param mode: '01'是联机模式，'00'是自动模式
        :return:
        """
        function_code = '7e'
        code = self.slave_addr + function_code + mode
        crc_code = self.crc.crc16(code)
        return code + crc_code

    @bytecoding
    def straight_interpolation(self,x, y, z, a=None):
        """
        <1 直线插补>
        直线插补,字节计数11
        支持坐标小数点后三位，小数点后多于三位的会被舍去。
        """
        command = 1
        command = self.change_style(command,2)

        def get_hex(num):
            """直线插补中计算十六进制"""
            num_str = str(num)
            if "." in num_str:
                high = num_str.split(".")[0]
                low = num_str.split(".")[1]
                low_len = len(low)
                if low_len < 3:
                    low = low + (3 - low_len) * "0"
                else:
                    low = low[:3]
                all = high + low
            else:
                all = num_str + "000"
            all = int(all)
            if all < 0:
                hex_num = hex(all & 0xFFFFFFFF)[2:]
            else:
                hex_num = hex(all)[2:]
            length = len(hex_num)
            if length <= 8:
                res = (8 - length) * "0" + hex_num
            else:
                res = hex_num[-8:]
            # res = '{0:0>8s}'.format(hex_num) #与上述三行同义
            return res

        code = self.slave_addr+self.function_code+self.byte_cal+command
        x_hex, y_hex,z_hex,a_hex = get_hex(x),get_hex(y),get_hex(z),get_hex(a)
        x_hex, y_hex,z_hex,a_hex = self.reverselowhigh(x_hex,2),self.reverselowhigh(y_hex,2),self.reverselowhigh(z_hex,2),self.reverselowhigh(a_hex,2)
        code = code + x_hex+y_hex+z_hex+a_hex
        crc_code = self.crc.crc16(code)
        return code+crc_code

    @bytecoding
    def go_origin(self,direction,siginal_input,method):
        """
        <3 返回原点> 执行该指令后，指定的轴一直转动到信号输入端有触发信号，之后电机反转，到触发信号消失后停止，相应轴的内部坐标清零
        :param direction: 指定回到原点的轴与转动方向,int
        {1:x轴正传，2:x轴反转，3:y轴正转,4:y轴反转,5:z轴正转,6:z轴反转,7:a轴正转,8:a轴反转,}
        :param siginal_input: 指定触发信号的输入端
        :param method: 指定触发方式 0:低电平/接通/是 1:高电平/断开/否
        :return:
        """
        command = 3
        command = self.change_style(command,2)
        direction = hex(direction)[2:]
        siginal_input = hex(siginal_input)[2:]
        method = hex(method)[2:]

        direction = "{0:0>8s}".format(direction)
        siginal_input = "{0:0>8s}".format(siginal_input)
        method = "{0:0>8s}".format(method)

        direction = self.reverselowhigh(direction,2)
        siginal_input = self.reverselowhigh(siginal_input,2)
        method = self.reverselowhigh(method,2)

        code = self.slave_addr+self.function_code+self.byte_cal+command+direction+siginal_input+method+'0'*8
        crc_code = self.crc.crc16(code)
        return code+crc_code

    @bytecoding
    def go_zero(self, direction):
        """
        <5 回到坐标0>  指定需要返回零点的轴，返回命令
        解释：该指令以直线插补的方式回到0坐标。当执行该指令之前还没有执行过<3 返回原点>
        与<21 坐标清零>指令，则<5 回到坐标0>就是回到控制器通电时的点。
        如已经执行过上述两指令，则<5 回到坐标0>就是回到<3 返回原点>与<21 坐标清零>
        指令完成后时的点
        direction : str 1 X,2 Y,3 YX,4 Z,5 ZX,6 ZY,7 ZYX,8 A,9 AX,10 AY,11 AYX,12 AZ,13 AZX,14 AZY,15 AZYX
        """
        command = 5
        command = self.change_style(command,2)
        dir = sorted(direction.upper())

        for k, v in self.dir_dict.items():
            if dir == sorted(v):
                data1 = self.change_style(k,8)
                data1 = self.reverselowhigh(data1,2)
                code = self.slave_addr + self.function_code + self.byte_cal + command + data1 + "0" * 24
                crc_code = self.crc.crc16(code)
                return code + crc_code

    @bytecoding
    def turnoffmotor(self,direction):
        """
        关闭指定轴电机，如果是跟随关闭电机一起启动，也会被关闭
        :param direction:
        direction : str 1 X,2 Y,3 YX,4 Z,5 ZX,6 ZY,7 ZYX,8 A,9 AX,10 AY,11 AYX,12 AZ,13 AZX,14 AZY,15 AZYX
        :return:
        """
        command = 6
        command = self.change_style(command,2)
        dir = sorted(direction.upper())
        for k,v in self.dir_dict.items():
            if dir == sorted(v):
                data1 = self.change_style(k,8)
                data1 = self.reverselowhigh(data1,2)
                code = self.slave_addr + self.function_code + self.byte_cal + command + data1 + '0'* 24
                crc_code = self.crc.crc16(code)
                return code+crc_code

    @bytecoding
    def changespeedandacceleration(self,speed, acceleration):
        """
        :param speed: 单位hz,为0时，不改变速度的设置
        :param acceleration:为0时，不改变加速度的设置
        :return:
        """
        command = 34
        command = self.change_style(command,2)
        speed = self.change_style(speed,8)
        acceleration = self.change_style(acceleration,8)

        speed = self.reverselowhigh(speed,2)
        acceleration = self.reverselowhigh(acceleration,2)
        code = self.slave_addr + self.function_code + self.byte_cal+command + speed + acceleration + '0'*16
        crc_code = self.crc.crc16(code)
        return code + crc_code

    @bytecoding
    def engine_up_off_speed(self,up,off):
        """
        :param up: pulse frequency
        :param off: pulse frequency
        :return:
        """
        command = 36
        command = self.change_style(command,2)
        up = self.change_style(up,8)
        off = self.change_style(off,8)
        up = self.reverselowhigh(up,2)
        off = self.reverselowhigh(off,2)
        code = self.slave_addr + self.function_code+ self.byte_cal+command+up+off+'0'*16
        crc_code = self.crc.crc16(code)
        return code +crc_code

if __name__ == "__main__":
    slave = lianjicontrol('01') # 01号 从机
    lianji =slave.switchmode('01') #切换到联机模式
    zidong =slave.switchmode('00') #切换到自动模式
    # speed0 = slave.changespeedandacceleration(10,10) #修改速度，加速度
    # speed = slave.changespeedandacceleration(5000,5000) #修改速度，加速度
    # speed_ = slave.changespeedandacceleration(10000, 10000)  # 修改速度，加速度
    # line = slave.straight_interpolation(-10,0,0,0) #直线插补
    # line_ = slave.straight_interpolation(15,0,0,0) #直线插补
    # engingupoff = slave.engine_up_off(1000,1000) # 启动停止速度
    # engingupoff2 = slave.engine_up_off(500,500) # 启动停止速度
    # slave_screen = TouchScreen('01')
    # vr = slave_screen.readregister(29,1) #读取寄存器
    # go_origin = slave.go_origin(1,8,1)
    # print('go_origin',go_origin)
    # print(vr.hex())
    # print('联机',lianji)
    # print('自动',zidong)
    # print('速度0', speed0)
    # print('速度1',speed)
    # print('速度2',speed_)
    # print('直线插补1',line.hex())
    # print('直线插补2',line_)
    #
    # print('运行停止1',engingupoff)
    # print('运行停止2',engingupoff2)
    # print('vr',vr)
    # print('回零',slave.go_zero('x'))

    # line = slave.straight_interpolation(10, 5555555, 5555555, 5555555)  # 直线插补
    # print(line)
    codea = slave.turnoffmotor('XYZ')
    print(codea)



