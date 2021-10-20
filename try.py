
import threading
import time

exitFlag = True


class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name)
        print ("退出线程：" + self.name)


def print_time(threadName):
    while exitFlag:
        print("Thread running")
        time.sleep(1)


thread1 = myThread(1, "Thread-1")

print("start")
thread1.start()
time.sleep(5)

print("ending")

exitFlag = False

time.sleep(5)
print("over")
