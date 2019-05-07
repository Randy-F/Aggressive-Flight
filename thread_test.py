import threading
import time
import socket  
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        # self.threadID = threadID
        # self.name = name
        # self.counter = counter
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(('127.0.0.1', 8001))
        print("Bind UDP on 8001...")

    def run(self):
        while True:
            # 接收数据 自动阻塞 等待客户端请求:
            data, addr = s.recvfrom(48)
            print(data)
            print(struct.unpack("<dddddd", data))
            # time.sleep(1)

    
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'r-', animated=False)

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

def func():
    ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                        init_func=init, blit=True, interval=1)
    plt.show()

#FuncAnimation要在主线程里
func()

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread1.start()
thread1.join()

# thread2 = myThread(2, "Thread-2", 2)
# thread2.start()
# thread2.join()

print ("退出主线程")



