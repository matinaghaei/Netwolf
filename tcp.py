import socket
import threading

BUFFER = 1024


class TCP:

    def __init__(self):
        address = socket.gethostbyname(socket.gethostname())
        host_tcp_info = (address, 0)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(host_tcp_info)

    def get_host_tcp_info(self):
        return self.server.getsockname()

    def listen(self, file_address):
        self.server.listen()
        conn, address = self.server.accept()
        self.send_file(file_address, conn, address)

    @staticmethod
    def send_file(file_address, conn, address):
        # print("Got TCP connection from", address)
        f = open(file_address, 'rb')
        # print("Sending via TCP...")
        data = f.read(BUFFER)
        while data:
            # print("Sending via TCP...")
            conn.send(data)
            data = f.read(BUFFER)
        f.close()
        # print("Done Sending", file_address, "via TCP")

    @staticmethod
    def receive_file(file_address, host_information):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(host_information)
        # print("Got TCP connection from", host_information)
        f = open(file_address, 'wb')
        # print("Receiving via TCP...")
        data = client.recv(BUFFER)
        while data:
            # print("Receiving via TCP...")
            f.write(data)
            data = client.recv(BUFFER)
        f.close()
        # print("Done Receiving", file_address, "via TCP")
        client.close()

    def close_server(self):
        self.server.close()
