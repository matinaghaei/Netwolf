import threading
import time
from udp import UDP
from cluster_manager import ClusterManager
from transfer_manager import TransferManager

ENCODING = 'utf-8'


class NetWolf:

    def __init__(self, udp_listener_port, files_directory, cluster_list_address,
                 discovery_period, max_clients, free_ride_delay, request_timeout):
        self.udp_listener = UDP(udp_listener_port)
        listener_info = self.udp_listener.get_host_udp_info()
        self.cluster_manager = ClusterManager(listener_info, cluster_list_address, discovery_period)
        self.transfer_manager = TransferManager(files_directory, max_clients, listener_info)
        self.running = None
        self.requested = []
        self.prior_communications = []
        self.free_ride_delay = free_ride_delay
        self.request_timeout = request_timeout

    def start(self):
        self.running = True
        threading.Thread(target=self.run_receiver).start()
        self.cluster_manager.start()

    def stop(self):
        print("Terminating...")
        self.running = False
        self.cluster_manager.stop()
        self.transfer_manager.stop()
        time.sleep(1)
        self.udp_listener.close()
        print("Terminated!")

    def run_receiver(self):
        while self.running:
            data, sender = self.udp_listener.receive()
            if self.running and data:
                threading.Thread(target=self.handle_data, args=(data, sender,)).start()

    def handle_data(self, data, sender):
        message = data.decode(ENCODING)
        split_message = message.split('\n')

        if split_message[0] == 'cluster':
            self.cluster_manager.add_to_cluster(split_message[1])

        elif split_message[0] == 'request':
            print("Request received from", split_message[1], "for", split_message[2])
            if split_message[1] not in self.prior_communications:
                print("Delaying request of free rider for", self.free_ride_delay, "seconds")
                time.sleep(self.free_ride_delay)
            split_line = split_message[1].split()
            receiver = (split_line[0], int(split_line[1]))
            self.transfer_manager.send_file(receiver, split_message[2])

        elif split_message[0] == 'server':
            if split_message[2] in self.requested:
                self.requested.remove(split_message[2])
                print("TCP server listening at", split_message[1], "to send", split_message[2])
                split_line = split_message[1].split()
                server_address = (split_line[0], int(split_line[1]))
                self.prior_communications.append(split_message[3])
                self.transfer_manager.receive_file(server_address, split_message[2])
            else:
                print(split_message[2], "is not requested anymore!")

        else:
            print("The message is not supported!")

    def request_file(self, file_name):
        print("Requesting for", file_name)
        self.requested.append(file_name)
        self.cluster_manager.send_request(file_name)
        threading.Timer(self.request_timeout, self.check_request, (file_name,)).start()

    def check_request(self, file_name):
        if file_name in self.requested:
            print("File was not found in the cluster!")
            self.requested.remove(file_name)

    def print_list(self):
        self.cluster_manager.print_cluster()
