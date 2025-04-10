import socket
import re


class NanoPi:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.socket.bind((self.ip, self.port))
        print(f"Server started on {self.ip}:{self.port}")
        return self

    def send_message(self, message, udp_ip, udp_port):
        self.socket.sendto(message, (udp_ip, udp_port))

    # @staticmethod
    # def get_start_arguments(message):
    #     args_input = re.fullmatch(r'start:(\d+):(\d{1})#', message)
    #     iteration = args_input.group(1)
    #     object_is_found = args_input.group(2)
    #     return iteration, object_is_found

    # @staticmethod
    # def is_start_msg(message: str) -> bool:
    #     return bool(re.fullmatch(r"start:(\d+):(1|3)#", message))

    # @staticmethod
    # def is_sonar_data(message: str) -> bool:
    #     return bool(re.fullmatch(r"\d+", message))

    def close(self):
        self.socket.close()
        print("Socket closed")
