import serial

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu


class Slave:
    def __init__(self,port,slave_id):
        logger = modbus_tk.utils.create_logger("console")
        self.slave = serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        self.slave_id = slave_id
        self.master = modbus_rtu.RtuMaster(self.slave)
        self.master.set_timeout(3.0)
        self.master.set_verbose(True)

    def read_cils(self,start,number):
        """
        :param start
        :param number:
        :return:
        """
        start = start-1
        start = "%x"%start
        start = int(start)
        data = self.master.execute(self.slave_id,cst.READ_COILS,start,number)
        return data

    def read_holding_registers(self,start,number):
        start = start-1
        # start = '%04x'%start
        # start = int(start)
        number = number*2
        # number = '%04x'%number
        # number = int(number)
        data = self.master.execute(self.slave_id,cst.READ_HOLDING_REGISTERS,start,number)
        return data

    def write_single_coil(self):
        pass


if __name__ == "__main__":
    slave1 = Slave('COM4',1)
    # data = slave1.read_cils(8,1)
    # when I use the cst.READ_COILS, It is right. I have the same crc_code whth you.

    data = slave1.read_holding_registers(42,2)
    print(data)
    # when I use the cst.READ_HOLDING_REGISTERS, It is wrong .
    # 2021-01-04 13:11:04,600	DEBUG	modbus.execute	MainThread	-> 1-3-0-29-0-4-212-15
    # 2021-01-04 13:11:04,618	DEBUG	modbus.execute	MainThread	<- 1-3-8-0-0-0-0-0-0-0-0-149-215
    # but the right sending is 1-3-0-29-0-4-149-193
    # maybe here have something wrong.