# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 17:15:29 2018

@author: 18665
"""

import threading
import time
from lianji_control.rtu_master import Slave


class Producer(threading.Thread):
    # 生产者函数
    def run(self):
        global count
        while True:
            if con.acquire():
                count = slave1.read_cils(8, 1)[0]
                # 当count 等于0时候，进行返回操作
                if count == 1:
                    con.wait()
                else:
                    slave1.go_zero('x')
                    msg = self.name + '_'+str(count)
                    print(msg)
                    # 完成生成后唤醒waiting状态的线程，
                    # 从waiting池中挑选一个线程，通知其调用acquire方法尝试取到锁
                    con.notify()
                con.release()
                time.sleep(1)


class Consumer(threading.Thread):
    # 消费者函数
    def run(self):
        global count
        while True:
            # 当count 大于0的时候进行移动
            if con.acquire():
                count = slave1.read_cils(8, 1)[0]
                if count == 0:
                    con.wait()
                else:
                    slave1.go_straight(15,0,0,0)
                    msg = self.name +'*'+str(count)
                    print(msg)
                    con.notify()
                    # 完成生成后唤醒waiting状态的线程，
                    # 从waiting池中挑选一个线程，通知其调用acquire方法尝试取到锁
                con.release()
                time.sleep(1)


slave1 = Slave('COM4','01')
count = slave1.read_cils(8,1)[0]
print(count,type(count))
con = threading.Condition()



def test():
    for i in range(1):
        p = Producer()
        p.start()
    for i in range(1):
        c = Consumer()
        c.start()


if __name__ == '__main__':
    test()
