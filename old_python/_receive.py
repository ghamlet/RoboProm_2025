import time
import socket
import re

# Конфигурация сети
MAIN_IP = "192.168.42.241"  # nanopi
MAIN_PORT = 8888  # Порт для команд от сервера
CONTROLLER_IP = "192.168.42.128"  # IP второго контроллера
CONTROLLER_PORT = 8888
LAMPA_IP = "192.168.42.129"
LAMPA_PORT = 8000  # Порт для управления лампой
sonar_data = 0
was_start_message = False


def lamp_control(state):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpPort = 8000
    server = "192.168.42.129"
    udp.sendto(str.encode(f"id:1:state:{state}"), (server, udpPort))


def main():
    # Инициализация UDP сокета для команд от сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((MAIN_IP, MAIN_PORT))

    try:
        print(
            f"Main controller started. Waiting for server commands at {MAIN_IP}:{MAIN_PORT}"
        )
        while True:
            # Принимаем команды от сервера
            data, addr = server_socket.recvfrom(1024)
            data_str = data.decode("utf-8").strip()
            print(data_str)

            # Проверяем команду start
            args_input = re.fullmatch(r"start:(\d+):(\d{1})#", data_str)
            if args_input is not None:
                iter = args_input.group(1)
                Q = args_input.group(2)
                print(f"Received start command: {data_str}")
                print(f"iteration: {iter} \n obj: {Q}")

            else:
                sonar_data = int(data_str)
                print(sonar_data)

            if sonar_data is not None and sonar_data > 20:
                R = 1
                lamp_control(5)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")


if __name__ == "__main__":
    main()
