from generator import generate
import socket
from datetime import datetime

from client import INIT_VALUE
from client import NO_OFF_T
from client import LN_OFF_T
from client import PACK_SIZE

TIMEOUT = 10

class Server:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = port

        self.total_time = None
        self.total_received = None

        self.clientInfo = None

    def measure(self):
        self.total_time = 0
        self.total_received = 0

        data, self.clientInfo = self.sock.recvfrom(PACK_SIZE)

        start_time = last_time = datetime.now()

        try:

            while 1:
                req = self.sock.recvfrom(PACK_SIZE)
                self.total_received += 1
                last_time = datetime.now()

                req = int.from_bytes(req, byteorder='little')

        except socket.timeout:
            print("------------------")

        self.total_time = last_time - start_time

    def send_result(self):
        self.total_time = self.total_time.seconds * 10**6 + self.total_time.microseconds
        self.total_time = 1 if self.total_time == 0 else self.total_time

        result = "Packets received:\t{}/{}\n".format(self.total_received, self.packets_count)
        result += "Packets lost:\t{}\n".format(self.packets_count - self.total_received)

        full_size = self.packet_size * self.packets_count
        result += "Overall size:\t{} bytes\n".format(full_size)
        result += "Overall time:\t{} mcsec\n".format(self.total_time)

        speed = ((full_size // 1024) / self.total_time) * 10**6  # in KB/sec
        result += "Speed:\t~{0:.2f} KB/sec\n".format(speed)

        print(result)

        result = bytearray(result, encoding='utf-8')

    def start(self):
        print("Server started")

        self.sock.bind(("", self.port))

        try:
            self.measure()
            self.send_result()

        finally:
            self.sock.close()
            print("\n<=========================\n")
