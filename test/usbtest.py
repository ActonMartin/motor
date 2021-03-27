import serial
import serial.tools.list_ports

scomList = list(serial.tools.list_ports.comports())
# print(scomList)
def funcCom(arrContent):
    return "USB Serial Port" in arrContent.description


b = list(filter(funcCom, scomList))
# print(b)
num = len(b)
usb = []
while num:
    num -= 1
    usb.append(b[num].device)
print(usb)
