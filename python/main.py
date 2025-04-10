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
    data = re.fullmatch(r"(\d+)", message)
    if data is not None:
        if int(data.group(1)) > 0:
            return True
    return False


# Конфигурация сети
MAIN_IP = "192.168.42.120"  # nanopi
SERVER_CONTROL_IP = "192.168.42.22"
MAIN_PORT = 3163

LAMP_IP = "192.168.42.129"
LAMP_PORT = 8000

SONAR_IP = "192.168.42.128"
SONAR_PORT = 8888

# айпи общего сервера разрабов
LOCAL_IP = "192.168.42.120"
LOCAL_PORT = 8888


# Для нормального считывания данных с сонара
MEASUREMENT_COUNT = 10  # количество замеров от сонара для анализа
DETECTION_THRESHOLD = (
    7  # порог для определения большинства (если >= 3 из 5  - объект есть)
)
MAX_FAIL_SONAR = MEASUREMENT_COUNT - DETECTION_THRESHOLD
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
        OBJECT_DETECTED = False
        sonar_counts = 0
        sonar_approve = 0
        signal_lamp.waiting_commands()
        time.sleep(1)
        data, addr = server.socket_serv.recvfrom(1024)
        message = data.decode("utf-8").strip()
        print(f"Received from {addr}: {message}")

        if is_start_msg(message):
            print("Получено стартовое сообщение")
            iteration, obj_is_found = get_start_arguments(message)
            print(f"{iteration=} {obj_is_found=}")
            signal_lamp.off()
            time.sleep(1)
            server.send_message(
                str.encode("get_sonar_data", "utf-8"), SONAR_IP, SONAR_PORT
            )

            while True:
                try:
                    data, addr = server.socket_sonar.recvfrom(1024)
                    message = data.decode("utf-8").strip()
                    print(f"Received from {addr}: {message}")

                    if is_sonar_data(message):
                        sonar_data = int(message)
                        print("Сонар: ", sonar_data)

                        if sonar_data <= MAX_DIST_TO_OBJECT:
                            OBJECT_DETECTED = True

                        if OBJECT_DETECTED:
                            signal_lamp.defect()
                            server.send_final_mesage(
                                iteration,
                                3,
                                2,
                                SERVER_CONTROL_IP,
                                MAIN_PORT,
                            )
                            break

                        else:
                            signal_lamp.not_object()
                            server.send_final_mesage(
                                iteration,
                                3,
                                1,
                                SERVER_CONTROL_IP,
                                MAIN_PORT,
                            )
                            break

                except KeyboardInterrupt:
                    break
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.close()
        break
