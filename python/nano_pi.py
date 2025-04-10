import socket


class NanoPi:
    def __init__(
        self, ip_global: str, port_global: int, ip_local: str, port_local: int
    ):
        self.ip_global = ip_global
        self.port_global = port_global
        self.ip_local = ip_local
        self.port_local = port_local
        self.socket_serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_sonar = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start_global(self):
        self.socket_serv.bind((self.ip_global, self.port_global))
        print(f"Global Server started on {self.ip_global}:{self.port_global}")
        return self

    def start_local(self):
        self.socket_sonar.bind((self.ip_local, self.port_local))
        print(f"Local Server started on {self.ip_local}:{self.port_local}")
        return self

    def send_message(self, message, udp_ip, udp_port):
        self.socket_serv.sendto(message, (udp_ip, udp_port))
    
    def send_final_mesage(self, iteration, team, result, udp_ip, udp_port):
        self.socket_serv.sendto(str.encode(f"{iteration}:t{team}:finish:{result}#", "utf-8"), (udp_ip, udp_port))

    def close(self):
        self.socket_serv.close()
        self.socket_sonar.close()
        print("Socket closed")
