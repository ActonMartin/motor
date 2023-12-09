from serial.tools import list_ports

if __name__ == '__main__':
    # 获取端口列表，列表中为 ListPortInfo 对象
    port_list = list(list_ports.comports())

    num = len(port_list)

    if num <= 0:
        print("找不到任何串口设备")
    else:
        for i in range(num):
            # 将 ListPortInfo 对象转化为 list
            port = list(port_list[i])
            print(port[0])
