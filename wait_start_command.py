import time
import socket
import re


class UDPServer:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    
    def start(self):
        """Start the UDP server and bind to the specified IP and port"""
        self.socket.bind((self.ip, self.port))
        print(f"Server started on {self.ip}:{self.port}")
        return self
    
    def receive_messages(self):
        """Main loop to receive and process messages"""
        print("Waiting for messages...")
        
        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
                self._process_message(data, addr)
                time.sleep(2)
                
            except KeyboardInterrupt:
                print("\nServer stopped")
                break
    
    
    def _process_message(self, data: bytes, addr: tuple):
        """Process incoming message"""
        message = data.decode().strip()
        print(f"Received from {addr}: {message}")
        
        if self._validate_message(message):
            print(f"Valid message received: {message}")
        else:
            print(f"Invalid message format: {message}")
    
    
    @staticmethod
    def _validate_message(message: str) -> bool:
        """Validate message format (start:\d{1}:\d{1}#)"""
        return bool(re.fullmatch(r'start:\d{1}:\d{1}#', message))
    
    
    def close(self):
        """Close the socket"""
        self.socket.close()
        print("Socket closed")


def main():
    server = UDPServer("192.168.31.185", 8888)
    try:
        server.start().receive_messages()
    finally:
        server.close()


if __name__ == "__main__":
    main()