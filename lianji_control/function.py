from crc.CRC16 import CRC


def readcoilstatus(slave_addr,start_addr,number):
    """
    功能码01 读取线圈（端子）状态
    :param slave_addr:从机地址
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

    code = slave_addr+function_code+port_addr+number_addr
    print()
    crc_code = CRC().crc16(code)
    return code+crc_code


def encodereadstatus(code):
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

    def reverselowhigh(data_in):
        data_temp = []
        for i in range(0, len(data_in), 2):
            data_temp.append(data_in[i:i + 2])
        datareversal = ''.join(data_temp[::-1])
        return datareversal

    def hex2bin(data_hex):
        binary = bin(int(data_hex,16))[2:]
        binary = '0'*(timebyte*8-len(binary))+binary # # 不足8位补齐
        binary = binary[::-1]
        return binary

    data = reverselowhigh(data) #type hex
    result = hex2bin(data)
    return result


def restart_controler(slave_addr):
    """功能码123（0x7b）
    从站地址 + 功能码+ crc
    """
    function_code = '7b'
    code = slave_addr+ function_code
    crc_code = CRC().crc16(code)
    return code+crc_code


def readregister(slave_addr,variable,number):
    """
    功能码03 读取寄存器命令
    :param slave_addr: 从机地址
    :param variable_addr: 变量地址
    :param number: 读取几个
    :return: 读取命令
    """
    function_code = '03'
    variable_addr = hex(variable-1)[2:]
    variable_addr = (4-len(variable_addr))*'0'+variable_addr
    number_addr = number*2
    number_addr = (4-len(str(number_addr)))*'0'+str(number)
    code = slave_addr+function_code+variable_addr+number_addr
    crc_code = CRC().crc16(code)
    return code+crc_code


def encoderegister(slave_addr,num,code):
    """
    :param slave_addr:从机地址
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
        result.append(reverselowhigh(data_num[i]))
    return result

def writecoilstatus(slave_addr,addr,data):
    """
    写线圈（端子）状态
    :param slave_addr:
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
        print('其余条件没有写完')
        # todo 没有写完data_
        data_ = (8-len(str(data)))*'0'+str(data)
    code = slave_addr + function_code+ addr_+data_
    crc_code = CRC().crc16(code)
    return code+crc_code


def readversion(slave_addr):
    """
    功能码124（0x7c）
    :param slave_addr:从站地址
    :return:
    """
    function_code = '7c'
    code = slave_addr+function_code
    crc_code = CRC().crc16(code)
    return code + crc_code


def switchmode(slave_addr,mode):
    """
    功能码126（0x7e)
    :param slave_addr:
    :param mode: 01是联机模式，00是自动模式
    :return:
    """
    function_code = '7e'
    code = slave_addr + function_code + mode
    crc_code = CRC().crc16(code)
    return code + crc_code


def straightinterpolation(slave_addr,x,y,z,a):
    """
    功能码127（0x7f) 字节计数11
    直线插补
    :param slave_addr:
    :param x: 数值
    :param y: 数值
    :param z: 数值
    :param a: 数值
    :return:
    """
    function_code = "7f"
    byte_cal = "11"
    command = '01'
    def gethex(num):
        """直线插补中计算十六进制"""
        num_str = str(num)
        if "." in num_str:
            high = num_str.split(".")[0]
            low = num_str.split(".")[1]
            low_len = len(low)
            if low_len < 3:
                low = low + (3 - low_len) * "0"
            all = high + low
        else:
            all = num_str + "000"
        hex_num = hex(int(all))[2:]
        length = len(hex_num)
        if length < 8:
            res = (8 - length) * "0" + hex_num
        return res
    code = slave_addr+function_code+byte_cal+command
    x_hex, y_hex,z_hex,a_hex = gethex(x),gethex(y),gethex(z),gethex(a)
    code = code + x_hex+y_hex+z_hex+a_hex
    crc_code = CRC().crc16(code)
    return code+crc_code

def gethex(num):
    """直线插补中计算十六进制"""
    num_str = str(num)
    if "." in num_str:
        high = num_str.split(".")[0]
        low = num_str.split(".")[1]
        low_len = len(low)
        if low_len < 3:
            low = low + (3 - low_len) * "0"
        all = high + low
    else:
        all = num_str + "000"
    hex_num = hex(int(all))[2:]
    length = len(hex_num)
    if length < 8:
        res = (8 - length) * "0" + hex_num
    return res

def gozero(slave_addr, direction):
    """指定需要返回零点的轴，返回命令
    direction : str 1 X,2 Y,3 YX,4 Z,5 ZX,6 ZY,7 ZYX,8 A,9 AX,10 AY,11 AYX,12 AZ,13 AZX,14 AZY,15 AZYX
    """
    crc = CRC()

    def cal_hex(num):
        hex_num = hex(num)[2:]
        length = len(hex_num)
        if length < 8:
            res = (8 - length) * "0" + hex_num
        return res

    function_code = "7f"
    byte_cal = "11"
    gozero_code = "05"
    dir = sorted(direction.upper())

    dir_dict = {
        1: "X",
        2: "Y",
        3: "YX",
        4: "Z",
        5: "ZX",
        6: "ZY",
        7: "ZYX",
        8: "A",
        9: "AX",
        10: "AY",
        11: "AYX",
        12: "AZ",
        13: "AZX",
        14: "AZY",
        15: "AZYX",
    }
    for k, v in dir_dict.items():
        if dir == sorted(v):
            print(v)
            data1 = cal_hex(k)
            code = (slave_addr + function_code + byte_cal + gozero_code + data1 + "0" * 24)
            crc_code = crc.crc16(code)
            return code + crc_code


if __name__ == "__main__":
    # kk = readregister('01',42,2)
    kk = writestatus('01',73,00)
    print(kk)




