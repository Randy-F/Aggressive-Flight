import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import multiprocessing

class Animation:

    def __init__(self, *disp_var_args):
        #输入('x', 'y', 'z', 'roll', 'pitch', 'yaw')确定画哪些参数
        print(disp_var_args)
        self.fig, self.ax = plt.subplots(figsize=(15, 10))
        
        self.ln1, = self.ax.plot([], [], 'r-', label='x' ,animated=False)
        self.ln2, = self.ax.plot([], [], 'b-', label='y' ,animated=False)
        self.ln3, = self.ax.plot([], [], 'k-', label='z' ,animated=False)
        self.ln4, = self.ax.plot([], [], 'g-', label='roll' ,animated=False)
        self.ln5, = self.ax.plot([], [], 'p-', label='pitch' ,animated=False)
        self.ln6, = self.ax.plot([], [], 'y-', label='yaw' ,animated=False)
        self.ax.legend(loc='upper left', fontsize=14);

        self.ln = self.geb_ln(disp_var_args)
        self.xdata, self.ydata = [], [[] for row in range(6)]
        self.time = 0

    def geb_ln(self, disp_var_args):
        # 根据传入参数决定画出哪些变量
        ln = []
        if 'x' in disp_var_args:
            ln.append(self.ln1)
        if 'y' in disp_var_args:
            ln.append(self.ln2)
        if 'z' in disp_var_args:
            ln.append(self.ln3)
        if 'roll' in disp_var_args:
            ln.append(self.ln4)
        if 'pitch' in disp_var_args:
            ln.append(self.ln5)
        if 'yaw' in disp_var_args:
            ln.append(self.ln6)
        return ln

    def anim_init(self):
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(-5, 5)
        return self.ln

    def anim_update(self, frame):
        if self.new_pose.value == 1:
            self.time += 1 
            # print("anim_pose " + str(self.pose[:]))
            self.xdata.append(self.time)
            self.ydata[0].append(self.pose[0])
            self.ydata[1].append(self.pose[1])
            self.ydata[2].append(self.pose[2])
            self.ydata[3].append(self.pose[3])
            self.ydata[4].append(self.pose[4])
            self.ydata[5].append(self.pose[5])
            # self.xdata.append(time)
            # self.ydata.append(self.pose[0])
            self.ln1.set_data(self.xdata, self.ydata[0])
            self.ln2.set_data(self.xdata, self.ydata[1])
            self.ln3.set_data(self.xdata, self.ydata[2])
            self.ln4.set_data(self.xdata, self.ydata[3])
            self.ln5.set_data(self.xdata, self.ydata[4])
            self.ln6.set_data(self.xdata, self.ydata[5])
            self.new_pose.value = 0

        return self.ln
        # return self.ln1, self.ln2, self.ln3, self.ln4, self.ln5, self.ln6

    def anim_run(self, pose, new_pose):
        self.pose = pose
        # print(self.pose)
        self.new_pose = new_pose
        # print(self.new_pose)
        ani = FuncAnimation(self.fig, self.anim_update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=self.anim_init, blit=True, interval=10)
        plt.show()  
