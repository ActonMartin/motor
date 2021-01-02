import serial
import serial.tools.list_ports


def ComAutoFind(self):
    # 先获取所以有USB串口挂载的设备
    self.scomList = list(serial.tools.list_ports.comports())

    if len(self.scomList) <= 0:
        self.ShowMessageBox("未发现Modbus接口，请检查线缆连接")
    else:
        comNum = len(self.scomList)
        print(str(comNum) + "Com is found")

    def funcCom(arrContent):
        return "USB-SERIAL" in arrContent.description

    # 通过filter函数筛选出设备描述里包含USB - SERIAL的设备
    b = list(filter(funcCom, self.scomList))
    comNum = len(b)
    print(str(comNum) + "USBCom is found")

    while comNum:
        comNum = comNum - 1
        self.usbComList.append(b[comNum].device)

    self.comboBox_Port.addItems(self.usbComList)
    print(self.usbComList)
