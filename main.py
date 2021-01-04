import serial
from lianji_control.function import lianjicontrol
import time


def main():
    PORT = 'COM4'
    slave_addr = '01'
    slave = serial.Serial(port=PORT, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=0)
    lianjimode = lianjicontrol(slave_addr).switchmode('01')
    line_code_0 = lianjicontrol(slave_addr).straight_interpolation(15,0,0,0)

    changespeed_0 = lianjicontrol(slave_addr).changespeedandacceleration(50000,15000)
    changespeed_1 = lianjicontrol(slave_addr).changespeedandacceleration(90000,10000)

    line_code_1 = lianjicontrol(slave_addr).straight_interpolation(25, 0, 0, 0)
    gozero_code = lianjicontrol(slave_addr).gozero('x')

    slave.write(lianjimode)
    time.sleep(1)
    slave.write(changespeed_0)
    time.sleep(1)
    slave.write(line_code_0)
    time.sleep(1)
    slave.write(changespeed_1)
    time.sleep(1)
    slave.write(line_code_1)
    time.sleep(1)
    slave.write(gozero_code)
    slave.close()


if __name__ == "__main__":
    main()