import socket
import threading

# 客户端类
class GameClient:
    def __init__(self, server_host, port=12345):
        self.server_host = server_host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.client.connect((self.server_host, self.port))
            print(f"已连接到服务器 {self.server_host}:{self.port}")
            while True:
                message = input("输入消息（输入 'exit' 退出）：")
                if message.lower() == "exit":
                    break
                self.client.sendall(message.encode('utf-8'))
                response = self.client.recv(1024)
                print(f"服务器回复: {response.decode('utf-8')}")
        except Exception as e:
            print(f"连接到服务器失败: {e}")
        finally:
            self.client.close()