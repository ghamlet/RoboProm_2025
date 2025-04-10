from lamp import Lamp
from nano_pi import NanoPi

import re



def get_start_arguments(message):
    args_input = re.fullmatch(r'start:(\d+):(\d{1})#', message)
    iteration = args_input.group(1)
    object_is_found = args_input.group(2)
    return iteration, object_is_found


def is_start_msg(message: str) -> bool:
    return bool(re.fullmatch(r"start:(\d+):(1|3)#", message))


def is_sonar_data(message: str) -> bool:
    return bool(re.fullmatch(r"(\d+)", message))



# Конфигурация сети
MAIN_IP = "192.168.0.69"  # nanopi
MAIN_PORT = 8888

LAMP_IP = "192.168.42.129"
LAMP_PORT = 8000

# айпи общего сервера разрабов
EXTERNAL_SERVER_IP = "192.168.42.22"
EXTERNAL_SERVER_PORT = 3163


# Для нормального считывания данных с сонара
object_detected = False
sonar_readings = []
current_measurements = []
MEASUREMENT_COUNT = 5  # количество замеров от сонара для анализа
DETECTION_THRESHOLD = 3  # порог для определения большинства (если >= 3 из 5  - объект есть)
MAX_DIST_TO_OBJECT = 10   # максимальная длина до детали


OBJECT_DETECTED = None  # переменная для определения наличия обьекта на конвейере


server = NanoPi(MAIN_IP, MAIN_PORT).start()
signal_lamp = Lamp(LAMP_IP, LAMP_PORT)


WAS_START_MESSAGE = False  # флаг для отлова стартового сообщения



signal_lamp.waiting_commands()

print("Ожидание стартового сообщения...")

# Ловим стартовое сообщение
while not WAS_START_MESSAGE:
    try:
        data, addr = server.socket.recvfrom(1024)       
        message = data.decode("utf-8").strip()
        print(f"Received from {addr}: {message}")
        
        
        if is_start_msg(message): # если пришло сообщение от главного сервака разрабов в первый раз
            print("Получено стартовое сообщение")
            WAS_START_MESSAGE = True
            
            iteration, obj_is_found = get_start_arguments(message)
            print(f"{iteration=} {obj_is_found=}")
            
            print("Выключаем лампу")
            signal_lamp.command_received()
       
       
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.close()
        break     
            

# Цикл для считывания данных с сонара
while OBJECT_DETECTED is None:
    try:
            
        data, addr = server.socket.recvfrom(1024)       
        message = data.decode("utf-8").strip()
        print(f"Received from {addr}: {message}")

        if is_sonar_data(message):  # если пришло сообщение от сонара
            sonar_data = int(message)
            print("СОНАР: ", sonar_data)
            
            # Добавляем текущее показание в список последних значений
            current_measurements.append(sonar_data)
            
            # Когда накопили достаточное количество замеров
            if len(current_measurements) >= MEASUREMENT_COUNT:
                # Подсчитываем количество значений < 10
                low_readings = sum(1 for r in current_measurements if r < MAX_DIST_TO_OBJECT)
                
                # Определяем наличие объекта по большинству
                if low_readings >= DETECTION_THRESHOLD:
                    print(f"Объект обнаружен!")
                    OBJECT_DETECTED = True
                    
                else:
                    print(f"Объекта нет")
                    OBJECT_DETECTED = False
                
                # Сохраняем статистику и очищаем текущие замеры
                sonar_readings.extend(current_measurements)
                current_measurements = []
                print(f"Статистика: {len([r for r in sonar_readings if r < MAX_DIST_TO_OBJECT])} из {len(sonar_readings)} замеров < {MAX_DIST_TO_OBJECT}")
            
            

    except KeyboardInterrupt:
        break     
    
