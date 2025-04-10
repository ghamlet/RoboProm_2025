# Импортируем нужные библиотеки и классы
import os
import time
from dynamixel_sdk import *  # Библиотека до Dynamixel sdk !Стоит обратить внимание на маршрут библиотеки

os.system("rs485 /dev/ttyS2 1")  # открываем порт Dynamixel

# Необходимые регистры и переменные

ADDR_BUF_A = 26
ADDR_DAC_ENABLE = 29
ADDR_MODE_SELECT = 28

# Protocol version
PROTOCOL_VERSION = 2.0

# Default setting
DXL_ID = 19
BAUDRATE = 1000000
DEVICENAME = "/dev/ttyS2"

DAC_BUF_SIZE = 20
DAC_ENABLE = 2
DAC_DISABLE = 1
MODE_DAC = 33


TYPES = {0: "black", 1: "red"}  # оставить


count_for_red = 0
count_for_white = 0
count_for_grey = 0
count_for_black = 0

# Инициализуруем обработчик порта и обработчик пакетов
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Открываем порт
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    quit()

# Устанавливаем скорость обмена данными
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    quit()


def readBlob():
    max_blob_count = 2  # Количетсво объектов max 10
    indx = 16

    camera_data = []

    for i in range(0, max_blob_count):  # только первое значение

        collect_data = []  # сбор данных с одного прохода

        # print(i)
        type, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(
            portHandler, DXL_ID, indx
        )
        if dxl_comm_result == COMM_SUCCESS:
            print(f"type: {type}")
            # camera_data[type].append(type)
            collect_data.append(type)

        indx += 1
        dummy, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(
            portHandler, DXL_ID, indx
        )
        # if dxl_comm_result == COMM_SUCCESS:
        #     print(f"dummy: {dummy}")

        indx += 1
        cx, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(
            portHandler, DXL_ID, indx
        )
        if dxl_comm_result == COMM_SUCCESS:
            print(f"cx: {cx}")
            # camera_data[type].append(cx)
            collect_data.append(cx)

        indx += 2
        cy, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(
            portHandler, DXL_ID, indx
        )
        if dxl_comm_result == COMM_SUCCESS:
            print(f"cy: {cy}")
            # camera_data[type].append(cy)
            collect_data.append(cy)

        indx += 2
        area, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(
            portHandler, DXL_ID, indx
        )
        if dxl_comm_result == COMM_SUCCESS:
            print(f"area: {area}")
            # camera_data[type].append(area)
            collect_data.append(area)

        indx += 4
        left, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(
            portHandler, DXL_ID, indx
        )
        if dxl_comm_result == COMM_SUCCESS:
            print(f"left: {left}")
            # camera_data[type].append(left)
            collect_data.append(left)

        indx += 2
        right, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(
            portHandler, DXL_ID, indx
        )
        if dxl_comm_result == COMM_SUCCESS:
            print(f"right: {right}")
            # camera_data[type].append(right)
            collect_data.append(right)

        indx += 2
        top, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(
            portHandler, DXL_ID, indx
        )
        if dxl_comm_result == COMM_SUCCESS:
            print(f"top: {top}")
            # camera_data[type].append(top)
            collect_data.append(top)

        indx += 2
        bottom, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(
            portHandler, DXL_ID, indx
        )
        if dxl_comm_result == COMM_SUCCESS:
            print(f"bottom: {bottom}")
            # camera_data[type].append(bottom)
            collect_data.append(bottom)

        print(collect_data)
        camera_data.append(collect_data)

        indx += 2
        time.sleep(0.2)

    print(camera_data)

    analize_camera_data(camera_data)


def analize_camera_data(camera_data):
    global count_for_red
    global count_for_white
    global count_for_grey
    global count_for_black

    for blob in camera_data:
        if blob:

            if all(int(param) > 0 for param in blob[1:]):
                object_type = int(blob[0])
                print(object_type)

                if TYPES[object_type] == "red":
                    count_for_red += 1

                # elif TYPES[object_type] == "white":
                #     count_for_white += 1

                # elif TYPES[object_type] == "grey":
                #     count_for_grey+=1

                elif TYPES[object_type] == "black":
                    count_for_black += 1


if __name__ == "__main__":

    while True:
        try:
            readBlob()  # -> blob reader

            if count_for_red > 5:
                print("-----------RED------------------")
                count_for_red = 0

            if count_for_black > 5:
                print("--------------BLACK-------------------")
                count_for_black = 0

        except KeyboardInterrupt:
            # Закрываем порт
            portHandler.closePort()
            break
