from binascii import unhexlify
from crcmod import mkCrcFun

"""
用的现成的库进行计算,速度没有CRC16.py使用的查表法速度快
"""
# CRC16/CCITT
def crc16_ccitt(s):
    crc16 = mkCrcFun(0x11021, rev=True, initCrc=0x0000, xorOut=0x0000)
    return get_crc_value(s, crc16)


# CRC16/CCITT-FALSE
def crc16_ccitt_false(s):
    crc16 = mkCrcFun(0x11021, rev=False, initCrc=0xFFFF, xorOut=0x0000)
    return get_crc_value(s, crc16)


# CRC16/MODBUS
def crc16_modbus(s):
    crc16 = mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    return get_crc_value(s, crc16)


# CRC16/XMODEM
def crc16_xmodem(s):
    crc16 = mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)
    return get_crc_value(s, crc16)


# common func
def get_crc_value(s, crc16):
    data = s.replace(' ', '')
    crc_out = hex(crc16(unhexlify(data))).upper()
    str_list = list(crc_out)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0
    crc_data = ''.join(str_list[2:])
    return crc_data[2:] + ' ' + crc_data[:2]


if __name__ == '__main__':
    jj = '01 7E 01'
    # jj = '01 03 00 29 00 04'
    import time
    frequency = 1
    start = time.time()
    for i in range(frequency):
        s3 = crc16_modbus(jj)
    end = time.time()
    print((end-start)/frequency)
    print('crc16_modbus: ' + s3)
