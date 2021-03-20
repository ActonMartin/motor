# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 17:15:29 2018

@author: 18665
"""

import threading
import time


class Producer(threading.Thread):
    # 生产者函数
    def run(self):
        global count
        while True:
            if con.acquire():
                # 当count 小于等于1000 的时候进行生产
                if count > 1000:
                    con.wait()
                else:
                    count = count + 100
                    msg = self.name + ' produce 100, count=' + str(count)
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
            # 当count 大于等于100的时候进行消费
            if con.acquire():
                if count < 100:
                    con.wait()

                else:
                    count = count - 5
                    msg = self.name + ' consume 5, count=' + str(count)
                    print(msg)
                    con.notify()
                    # 完成生成后唤醒waiting状态的线程，
                    # 从waiting池中挑选一个线程，通知其调用acquire方法尝试取到锁
                con.release()
                time.sleep(1)


count = 500
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
