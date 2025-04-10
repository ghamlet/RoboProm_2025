import socket
import time

"""
1 - красный (брак)
2 - оранж - wait
3 - хрупкая - зелён
4 - синий - не хрупкая
5 - син&зел - нету объекта
0 - orange OFF - all off
"""


class Lamp:
    def __init__(self, ip: str, port: int, state: int = 2):
        self.state = state
        self.lamp_ip = ip
        self.lamp_port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def set_state(self, state: int = 0):
        self.state = state
        bytes_to_send = str.encode(f"id:1:state:{self.state}")

        self.socket.sendto(bytes_to_send, (self.lamp_ip, self.lamp_port))

    def waiting_commands(self):
        self.set_state(2)

    def command_received(self):
        self.set_state(0)

    def defect(self):
        self.set_state(1)

    def delicate(self):
        self.set_state(3)

    def not_delicate(self):
        self.set_state(4)

    def not_object(self):
        self.set_state(5)

    def off(self):
        self.set_state(6)

    def test_lamp(self):
        self.off()
        for i in range(5):
            self.set_state(i)
            time.sleep(0.1)
        for i in range(5):
            self.set_state(4 - i)
            time.sleep(0.1)
        self.off()
