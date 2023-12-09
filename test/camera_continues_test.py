from hikvision.utilty.Camera_new_method import *

def main():
    # 枚举设备
    deviceList = enum_devices(device=0, device_way=False)

    # 创建相机实例并创建句柄,(设置日志路径)
    cam, stDeviceList = creat_camera(deviceList, 0, log=False)

    # decide_divice_on_line(cam)  ==============
    # 打开设备
    open_device(cam)
    # 设置软触发
    try:
        set_Value(cam, param_type="enum_value", node_name="TriggerMode", node_value=0)
        # set_Value(cam, param_type="enum_value", node_name="TriggerSource", node_value=7)
    except:
        pass

    # 设置像素格式为Mono8
    try:
        set_Value(cam,param_type="enum_value",node_name="PixelFormat",node_value=17301505)
    except:
        pass
    #开始取流
    start_grab_and_get_data_size(cam)
    # 执行软触发
    # try:
    #     set_Value(cam, param_type='command_value',node_name="TriggerSoftware")
    # except:
    #     pass

    # kjh0 = access_get_image(cam,"getoneframetimeout")
    kjh0 = access_get_image(cam,"getImagebuffer")

    if kjh0 is not None:
        print('kjh0',kjh0.shape)