import threading
import os.path
import time
from tcp import TCP
from udp import UDP

ENCODING = 'utf-8'


class TransferManager:

    def __init__(self, directory, max_clients, listener_info):
        self.directory = directory
        self.max_clients = max_clients
        self.tcp_server = TCP()
        self.udp_response = UDP(0)
        self.number_of_clients = 0
        self.listener_info = listener_info

    def send_file(self, receiver, file_name):
        if os.path.isfile(self.directory + file_name):
            if self.number_of_clients < self.max_clients:
                self.number_of_clients += 1

                server_info = self.tcp_server.get_host_tcp_info()
                message = 'server\n' + server_info[0] + ' ' + str(server_info[1]) + '\n' + file_name + '\n' \
                          + self.listener_info[0] + ' ' + str(self.listener_info[1])
                data = message.encode(ENCODING)

                sender_thread = threading.Thread(target=self.tcp_server.listen, args=(self.directory + file_name,))
                sender_thread.start()
                self.udp_response.send(data, receiver)

                sender_thread.join()
                print(file_name, "is sent")
                self.number_of_clients -= 1
            else:
                print("Maximum number of clients exceeded!")
        else:
            print("Requested file doesn't exist!")

    def receive_file(self, server_address, file_name):
        TCP.receive_file(self.directory + file_name, server_address)
        print(file_name, "is received from", server_address)

    def stop(self):
        time.sleep(1)
        self.tcp_server.close_server()
        self.udp_response.close()
