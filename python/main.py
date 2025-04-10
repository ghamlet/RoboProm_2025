from lamp import Lamp
from nano_pi import NanoPi

import re
import time


def get_start_arguments(message):
    args_input = re.fullmatch(r"start:(\d+):(\d{1})#", message)
    iteration = args_input.group(1)
    object_is_found = args_input.group(2)
    return iteration, object_is_found


def is_start_msg(message: str) -> bool:
    return bool(re.fullmatch(r"start:(\d+):(1|3)#", message))


def is_sonar_data(message: str) -> bool:
    return bool(re.fullmatch(r"(\d+)", message))


# Конфигурация сети
MAIN_IP = "192.168.42.120"  # nanopi
SERVER_CONTROL_IP = "192.168.42.22"
MAIN_PORT = 3163

LAMP_IP = "192.168.42.129"
LAMP_PORT = 8000

# айпи общего сервера разрабов
LOCAL_IP = "192.168.42.120"
LOCAL_PORT = 8888


# Для нормального считывания данных с сонара
MEASUREMENT_COUNT = 10  # количество замеров от сонара для анализа
DETECTION_THRESHOLD = 7  # порог для определения большинства (если >= 3 из 5  - объект есть)
MAX_DIST_TO_OBJECT = 15  # максимальная длина до детали

server = NanoPi(MAIN_IP, MAIN_PORT, LOCAL_IP, LOCAL_PORT)
server.start_global()
server.start_local()
signal_lamp = Lamp(LAMP_IP, LAMP_PORT)


signal_lamp.off()
signal_lamp.test_lamp()
signal_lamp.waiting_commands()

print("Ожидание стартового сообщения...")

while True:
    try:
        OBJECT_DETECTED = None
        sonar_counts = 0
        sonar_approve = 0
        signal_lamp.waiting_commands()

        data, addr = server.socket_serv.recvfrom(1024)
        message = data.decode("utf-8").strip()
        print(f"Received from {addr}: {message}")

        if is_start_msg(message):
            print("Получено стартовое сообщение")
            iteration, obj_is_found = get_start_arguments(message)
            print(f"{iteration=} {obj_is_found=}")
            signal_lamp.command_received()
            signal_lamp.off()

            while True:
                try:
                    data, addr = server.socket_sonar.recvfrom(1024)
                    message = data.decode("utf-8").strip()
                    print(f"Received from {addr}: {message}")

                    if is_sonar_data(message):
                        sonar_data = int(message)
                        print("Сонар: ", sonar_data)

                        if sonar_data <= MAX_DIST_TO_OBJECT

                        if len(current_measurements) >= MEASUREMENT_COUNT:
                            # Подсчитываем количество значений < 10
                            low_readings = sum(
                                1
                                for r in current_measurements
                                if r < MAX_DIST_TO_OBJECT
                            )

                            # Определяем наличие объекта по большинству
                            if low_readings >= DETECTION_THRESHOLD:
                                OBJECT_DETECTED = True
                                signal_lamp.defect()
                                server.send_final_mesage(
                                    iteration,
                                    3,
                                    2,
                                    SERVER_CONTROL_IP,
                                    MAIN_PORT,
                                )
                                #break

                            else:
                                OBJECT_DETECTED = False
                                signal_lamp.not_object()
                                server.send_final_mesage(
                                    iteration,
                                    3,
                                    1,
                                    SERVER_CONTROL_IP,
                                    MAIN_PORT,
                                )
                                #break

                except KeyboardInterrupt:
                    break

    except KeyboardInterrupt:
        print("\nServer stopped")
        server.close()
        break
