"""
Simple realisation of UR dashboard interface
"""
import logging
import socket
import traceback
from threading import Thread
import time

class Dashboard(Thread):

    def __init__(self, host):
        Thread.__init__(self)
        self.logger = logging.getLogger("dashboard")
        self.host = host
        self.dashboard_port = 29999    # Dashboard client interface on Universal Robots
        self.socket_connected = False
        self.timeout = 2
        self.connect()
        self._trystop = False  # to stop thread
        self.running = False  # True when robot is on and listening
        self.lastpacket_timestamp = 0

        self.start()

    def connect(self):
        try:
            self.dashboard = socket.create_connection((self.host, self.dashboard_port), timeout=self.timeout)
            self.socket_connected = True
        except Exception as ex:
            self.socket_connected = False
            traceback.format_exc()

    def run(self):
        while not self._trystop:
            try:
                time.sleep(0.1)
                if self.socket_connected == False:
                    self.connect()
                else:
                    try:
                        tmp = self.dashboard.recv(1024)
                        print(tmp)
                    except socket.timeout:
                        pass

            except:
                traceback.print_exc()

    def send_command(self, cmd):
        try:
            cmd += '\n'
            cmd = cmd.encode('ascii')
            self.dashboard.send(cmd)
            print(cmd)
        except:
            traceback.print_exc()

    def send_stop(self):
        try:
            self.dashboard.send('stop\n'.encode('ascii'))
        except:
            traceback.print_exc()