# coding: utf8
import threading
import time


# 真正要执行的函数
def t1():
    print(1)
    return 1


# 每隔10秒钟执行
def t2():
    while 1:
        data = t1()
        time.sleep(1)


if __name__ == '__main__':
    t = threading.Thread(target=t2)
    t.setDaemon(True)
    t.start()

    t.join()