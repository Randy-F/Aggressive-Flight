import multiprocessing
from multiprocessing import Process
from ControlBridge import ControlBridge

def bridge_run():
    ctrl_bridge = ControlBridge('127.0.0.1', 8001)
    ctrl_bridge.bridge_run()

if __name__=='__main__':
    
    # new_pose = multiprocessing.Value('i', 0)
    # pose = multiprocessing.Array('d', range(6))
    
    # p1 = Process(target=animation.anim_run, args=(pose, new_pose))
    # p2 = Process(target=ctrl_bridge.bridge_run, args=(pose, new_pose))
    p2 = Process(target=bridge_run, args=())
    # p1.start()
    p2.start()
    # p.join()



