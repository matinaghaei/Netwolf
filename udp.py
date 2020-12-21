import socket

BUFFER = 1024


class UDP:

    def __init__(self, udp_port):
        address = socket.gethostbyname(socket.gethostname())
        self.host_udp_info = (address, udp_port)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(self.host_udp_info)

    def get_host_udp_info(self):
        return self.host_udp_info

    def receive(self):
        data, addr = None, None
        try:
            # print("Receiving via UDP...")
            data, addr = self.udp_socket.recvfrom(BUFFER)
            # print("Done Receiving via UDP")
        except socket.error:
            pass
        return data, addr

    def send(self, data, address):
        # print("Sending via UDP...")
        self.udp_socket.sendto(data, address)
        # print("Done Sending via UDP")

    def close(self):
        self.udp_socket.close()
