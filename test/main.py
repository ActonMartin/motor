import serial
from lianji_control.function import lianjicontrol
from lianji_control.function import TouchScreen
import time
import threading
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

class StatusThread(threading.Thread):
    pass



def main():
    PORT = 'COM4'
    slave_addr = '01'
    # slave = serial.Serial(port=PORT, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0)
    slave = serial.Serial(port=PORT, baudrate=115200, bytesize=8, parity='N', stopbits=1)

    master = modbus_rtu.RtuMaster(slave)
    master.set_timeout(2.0)
    logger = modbus_tk.utils.create_logger("console")

    lianjimode = lianjicontrol(slave_addr).switchmode('01')
    line_code_0 = lianjicontrol(slave_addr).straight_interpolation(15,0,0,0)

    changespeed_0 = lianjicontrol(slave_addr).changespeedandacceleration(25000,50)
    changespeed_1 = lianjicontrol(slave_addr).changespeedandacceleration(50000,150)

    line_code_1 = lianjicontrol(slave_addr).straight_interpolation(45, 0, 0, 0)
    gozero_code = lianjicontrol(slave_addr).gozero('x')



    slave.write(lianjimode)
    time.sleep(0.1)
    slave.write(changespeed_0)
    time.sleep(0.1)
    slave.write(line_code_0)
    time.sleep(5)


    logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 41, 1))


    time.sleep(0.1)
    slave.write(changespeed_1)
    time.sleep(0.1)
    slave.write(line_code_1)
    time.sleep(5)


    logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 41, 1))


    time.sleep(0.1)
    # slave.write(gozero_code)
    slave.close()


def byte2hex(code):
    return code.hex()

if __name__ == "__main__":
    main()