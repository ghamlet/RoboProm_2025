import lamp
import UDPServer

# Конфигурация сети
MAIN_IP = "192.168.42.241"  # nanopi
MAIN_PORT = 8888
LAMP_IP = "192.168.42.129"
LAMP_PORT = 8000
sonar_data = 0

server = UDPServer.UDPServer(MAIN_IP, MAIN_PORT).start()

signal_lamp = lamp.Lamp(LAMP_IP, LAMP_PORT)


while True:
    try:
        data, addr = server.socket.recvfrom(1024)
        print("Waiting for messages...")
        signal_lamp.waiting_commands()
        message = data.decode("utf-8").strip()
        print(f"Received from {addr}: {message}")
        if server.is_start_msg(message):
            iteration, obj_is_found = server.get_start_arguments(message)
            signal_lamp.command_received()
            if sonar_data > 20:
                signal_lamp.not_object()
            # elif ....
            # остальная логика

        elif server.is_sonar_data(message):
            sonar_data = int(message)

    except KeyboardInterrupt:
        print("\nServer stopped")
        server.close()
        break
