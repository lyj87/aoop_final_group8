import socket
import threading

# 服务器类
class GameServer:
    def __init__(self, host="0.0.0.0", port=12345):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"服务器已启动，监听 {self.host}:{self.port}")
        try:
            while True:
                conn, addr = self.server.accept()
                print(f"客户端连接：{addr}")
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
        except KeyboardInterrupt:
            print("\n服务器已关闭")
        finally:
            self.server.close()

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"收到来自 {addr} 的消息: {data.decode('utf-8')}")
                conn.sendall(f"服务器收到: {data.decode('utf-8')}".encode('utf-8'))
        except Exception as e:
            print(f"处理客户端出错: {e}")
        finally:
            conn.close()