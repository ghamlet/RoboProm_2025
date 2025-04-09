import time
import socket

if __name__ == "__main__":
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpPort = 8888
    id = 5
    Q = 8
    server = "192.168.31.185"

    while True:
        try:
            udp.sendto(str.encode(f"start:{id}:{Q}#"), (server, udpPort))
            time.sleep(2)
        except KeyboardInterrupt as e:
            print("Interrupted")
            break
    exit()
