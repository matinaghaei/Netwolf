import threading
import time
from udp import UDP

ENCODING = 'utf-8'


class ClusterManager:

    def __init__(self, listener_info, cluster_list_address, discovery_period):
        self.discovery_period = discovery_period
        self.udp_discovery = UDP(0)
        self.udp_request = UDP(0)
        self.file_address = cluster_list_address
        self.cluster = self.read_cluster()
        self.listener_info = listener_info
        self.running = None

    def start(self):
        self.running = True
        threading.Thread(target=self.run_discovery).start()

    def stop(self):
        self.running = False
        self.udp_request.close()
        time.sleep(1)
        self.udp_discovery.close()

    def run_discovery(self):
        while self.running:
            time.sleep(self.discovery_period)
            if not self.running:
                break
            self.send_cluster()

    def read_cluster(self):
        cluster = []
        file = open(self.file_address, 'r')
        line = file.readline()
        while line:
            split_line = line.split()
            cluster.append((split_line[0], int(split_line[1])))
            line = file.readline()
        file.close()
        return cluster

    def send_cluster(self):
        file = open(self.file_address, 'rb')
        data = b'cluster\n' + file.read()
        file.close()
        for p in self.cluster:
            if p != self.listener_info:
                self.udp_discovery.send(data, p)

    def add_to_cluster(self, message):
        split_message = message.splitlines()
        for line in split_message:
            split_line = line.split()
            p = (split_line[0], int(split_line[1]))
            if p not in self.cluster:
                self.cluster.append(p)
        self.write_cluster()

    def write_cluster(self):
        file = open(self.file_address, 'w')
        for p in self.cluster:
            file.write(p[0] + ' ' + str(p[1]) + '\n')
        file.close()
        # print("wrote in", self.file_address)

    def send_request(self, file_name):
        message = 'request\n' + self.listener_info[0] + ' ' + str(self.listener_info[1]) + '\n' + file_name
        data = message.encode(ENCODING)
        for p in self.cluster:
            if p != self.listener_info:
                self.udp_request.send(data, p)

    def print_cluster(self):
        for p in self.cluster:
            print(p[0], p[1])
