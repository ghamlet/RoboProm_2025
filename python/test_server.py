import socket


def udp_sender():
    # Запрашиваем у пользователя IP и порт назначения
    target_ip = "192.168.42.22"
    target_port = 3163

    # Создаем UDP-сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            # Получаем сообщение от пользователя
            message = input(
                "Введите сообщение для отправки (или 'exit' для выхода): "
            )

            if message.lower() == "exit":
                break

            # Отправляем сообщение
            sock.sendto(message.encode("utf-8"), (target_ip, target_port))
            print(
                f"Отправлено сообщение на {target_ip}:{target_port}: {message}"
            )

    except KeyboardInterrupt:
        print("\nСервер остановлен по запросу пользователя.")
    finally:
        sock.close()


if __name__ == "__main__":
    udp_sender()
