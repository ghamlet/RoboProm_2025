#Импортируем нужные библиотеки и классы
import os
import time
from dynamixel_sdk import * #Библиотека до Dynamixel sdk !Стоит обратить внимание на маршрут библиотеки

os.system("rs485 /dev/ttyS2 1")#открываем порт Dynamixel

# Необходимые регистры и переменные 

ADDR_BUF_A                 = 26  
ADDR_DAC_ENABLE            = 29
ADDR_MODE_SELECT           = 28

# Protocol version
PROTOCOL_VERSION            = 2.0               

# Default setting
DXL_ID                      = 19               
BAUDRATE                    = 1000000             
DEVICENAME                  = '/dev/ttyS2'   

DAC_BUF_SIZE             = 20
DAC_ENABLE               = 2                 
DAC_DISABLE              = 1                 
MODE_DAC                 = 33



TYPES = {
    0: "black",  # оставить
    1 : "red"   
}


count_for_red = 0
count_for_white = 0
count_for_grey =0
count_for_black = 0


#Инициализуруем обработчик порта и обработчик пакетов
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




# def readAruco():
#     max_aruco_count = 5 #max 5
#     indx = 16

#     for i in range(0, max_aruco_count):
#         id, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, indx)
#         if dxl_comm_result == COMM_SUCCESS:
#             print(f"id: {id}")

#         indx+= 1
#         cx, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, indx)
#         if dxl_comm_result == COMM_SUCCESS:
#             print(f"cx: {cx}")

#         indx+= 2
#         cy, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, indx)
#         if dxl_comm_result == COMM_SUCCESS:
#             print(f"cy: {cy}")
        
#         indx+= 2



def readBlob():
    max_blob_count = 2 #Количетсво объектов на кадре max 10
    indx = 16
    
    camera_data = []
    
    for i in range(0, max_blob_count):  # только первое значение
        
        collect_data = []   # сбор данных с одного прохода
        
        # print(i)
        type, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, indx)
        if dxl_comm_result == COMM_SUCCESS:
           # print(f"type: {type}")
            collect_data.append(type)

        indx+= 1
        dummy, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, indx)
        # if dxl_comm_result == COMM_SUCCESS:
        #     print(f"dummy: {dummy}")
            

        indx+= 1
        cx, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, indx)
        if dxl_comm_result == COMM_SUCCESS:
            #print(f"cx: {cx}")
            collect_data.append(cx)


        indx+= 2
        cy, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, indx)
        if dxl_comm_result == COMM_SUCCESS:
            #print(f"cy: {cy}")
            collect_data.append(cy)


        indx+= 2
        area, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, indx)
        if dxl_comm_result == COMM_SUCCESS:
            #print(f"area: {area}")
            collect_data.append(area)


        indx+= 4
        left, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, indx)
        if dxl_comm_result == COMM_SUCCESS:
            #print(f"left: {left}")
            collect_data.append(left)


        indx+= 2
        right, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, indx)
        if dxl_comm_result == COMM_SUCCESS:
            #print(f"right: {right}")
            collect_data.append(right)


        indx+= 2
        top, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, indx)
        if dxl_comm_result == COMM_SUCCESS:
           # print(f"top: {top}")
            collect_data.append(top)

        indx+= 2
        bottom, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, indx)
        if dxl_comm_result == COMM_SUCCESS:
           # print(f"bottom: {bottom}")
            collect_data.append(bottom)



       # print(collect_data)
        camera_data.append(collect_data)

        indx+= 2
        time.sleep(0.2)
        
        
    print(camera_data)
    return analize_camera_data(camera_data)
    
        



# [[1,23,245,23,34,], [2,0,0,0,0,0]]


def data_reset():
    """Сброс счетчиков для всех обьектов"""
    
    global count_for_red
    global count_for_white
    global count_for_grey
    global count_for_black
    
    
    count_for_red = 0
    count_for_white = 0
    count_for_grey =0
    count_for_black = 0



def analize_camera_data(camera_data):
    global count_for_red
    global count_for_white
    global count_for_grey
    global count_for_black
    
    for blob in camera_data:
        if blob:
            
            if all(int(param) > 0 for param in blob[1:]):  # если блоб не пустой
                object_type = int(blob[0])
                print(object_type)
                
                
                if TYPES[object_type] == "red":
                    count_for_red +=1
                    
                    if count_for_red > 10:
                        count_for_red = 0
                        #data_reset()
                        print("---------RED-----------")
                        return 2
                    
                    
                # elif TYPES[object_type] == "white":
                #     count_for_white += 1
                #     if count_for_white > 10:
                #         count_for_white = 0
                #         print("--------------WHITE---------------")
                #         return 3
                    
                    
                # elif TYPES[object_type] == "grey":
                #     count_for_grey+=1
                #     if count_for_grey > 10:
                #         count_for_grey =0
                #         print("----------------GREY--------------------")
                #         return 3
                    
                    
                elif TYPES[object_type] == "black":
                    count_for_black +=1
                    
                    if count_for_black > 10:
                        count_for_black = 0
                        #data_reset()
                        
                        print("---------BLACK---------------")
                        return 3
                    
            
    return None





def check_camera():  # 1/2/3/4 None
    """ обработка видео"""
    
    start_time = time.time()  # Запоминаем время начала

    while True:
        
        
        try:
            
             # Проверяем, не истек ли таймаут
            if time.time() - start_time > 5:
                #print("Таймаут: данные не получены за 5 секунд")
                return 4
            
            
            result = readBlob() #-> blob reader
            if result:
                print(f"{result=}")
                
                return result
               
               
        except KeyboardInterrupt:
            # Закрываем порт
            portHandler.closePort()
            break
        



check_camera()

# if __name__ == "__main__":
    
    
#     while True:
        
        
#         try:
            
#             result = readBlob() #-> blob reader
#             if result:
#                 print(f"{result=}")
               
               
#         except KeyboardInterrupt:
#             # Закрываем порт
#             portHandler.closePort()
#             break