from animation_class import Animation
from ViconBridge import ViconBridge

class Navigator:

    def __init__(self, ip, port):
        self.animation = Animation()
        self.vicon_bridge = ViconBridge(ip, port)