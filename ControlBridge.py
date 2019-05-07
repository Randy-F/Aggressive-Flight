import socket  
import time
import struct
import logging
import time
from threading import Thread

import cflib
from cflib.crazyflie import Crazyflie

logging.basicConfig(level=logging.ERROR)


class ControlBridge:

    def __init__(self, ip, port):
        print("init!!")
        cflib.crtp.init_drivers(enable_debug_driver=False)
        # Scan for Crazyflies and use the first one found
        print('Scanning interfaces for Crazyflies...')
        available = cflib.crtp.scan_interfaces()
        print('Crazyflies found:')
        self.cf_connected = False
        self.att_ctrl_init('radio://0/100/2M/E7E7E7E707')
        while( self.cf_connected == False ):
            time.sleep(1)
            print(self.cf_connected)
            print("waiting for crazyflie connected")
        print("crazyflie connected!")

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((ip, port))
        # self.s.bind(('127.0.0.1', 8001))
        print("Bind UDP on 8001...")

    # def __exit__(*exc_info)
    #     thrust_mult = 1
    #     thrust_step = 200
    #     start_thrust = 42000
    #     end_thrust = 10001
    #     thrust = start_thrust
    #     pitch = 1.05
    #     roll = 0.5
    #     yawrate = 0

    #     # Unlock startup thrust protection

    #     while thrust >= end_thrust:
    #         print("thrust: " + str(thrust))
    #         self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)

    #         time.sleep(0.05)
    #         thrust += -thrust_step

    #     for _ in range(10):
    #         self._cf.commander.send_setpoint(0, 0, 0, 0)
    #         time.sleep(0.01)

    def bridge_run(self):
        take_off = False
        while True:
            data, _ = self.s.recvfrom(40)
            # print(data)
            if data is not None:
                #建立链接后先起飞
                if take_off == False:
                    self.take_off_cmd()
                    take_off = True
                    print("takeoff done!")
                    time.sleep(0.01)
                else:
                    # print(data)
                    unpack_cmd = struct.unpack("<dddidi", data)
                    # print(unpack_cmd)
                    print(unpack_cmd[0])
                    pitch = 1.4
                    roll = 0.6
                    yawrate = 0.0
                    # pitch = 3
                    # roll = 0.6
                    # yawrate = 0.0
                    self._cf.commander.send_setpoint(unpack_cmd[0], unpack_cmd[1], yawrate, unpack_cmd[3])
                    # self._cf.commander.send_setpoint(roll, pitch, yawrate, 40000)
                    time.sleep(0.01)
            else:
                print("recive none!!")
            

    def att_ctrl_init(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

        self._cf = Crazyflie(rw_cache='./cache')

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        self._cf.open_link(link_uri)

        print('Connecting to %s' % link_uri)

    def _connected(self, link_uri):
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""

        # Start a separate thread to do the motor test.
        # Do not hijack the calling thread!
        print("conect")
        self.cf_connected = True

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)

    def take_off_cmd(self):
        thrust_mult = 1
        thrust_step = 200
        start_thrust = 20000
        end_thrust = 42000
        thrust = start_thrust
        pitch = 1.05
        roll = 0.3
        yawrate = 0


        # Unlock startup thrust protection
        for _ in range(10):
            self._cf.commander.send_setpoint(0, 0, 0, 0)
            time.sleep(0.01)

        while thrust >= start_thrust:
            print("thrust: " + str(thrust))
            self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)

            time.sleep(0.02)
            if thrust <= end_thrust:
                thrust += thrust_step * thrust_mult
            else:
                break

