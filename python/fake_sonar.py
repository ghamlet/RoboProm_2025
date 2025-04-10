import time
import socket


if __name__ == '__main__':
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpPort = 8888
    server = "192.168.0.69"

    dist = 22
    
    while True:
        try:
            udp.sendto(str.encode(f"{dist}"), (server, udpPort))
            time.sleep(1)
            
        except KeyboardInterrupt as e:
            print("Interrupted")
            break
    exit()