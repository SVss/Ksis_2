from generator import generate
from mysocket import MyTCPSocket
from datetime import datetime

#from threading import Thread

class ClientThread:#(Thread):
    SERVICE_MSG_SIZE = 24

    def __init__(self, socket):
        super(ClientThread, self).__init__()
        self.socket = MyTCPSocket(socket)
        self.socket.settimeout(5)

        self.packet_size = None
        self.packets_count = None
        self.init_value = 0

        self.total_received = 0
        self.total_time = 0

    def receive_intro(self):
        intro = self.socket.recv(ClientThread.SERVICE_MSG_SIZE)

        tick = ClientThread.SERVICE_MSG_SIZE // 3
        self.packet_size = int.from_bytes(intro[:tick], byteorder='little')
        self.packets_count = int.from_bytes(intro[tick:2*tick], byteorder='little')
        self.init_value = int.from_bytes(intro[2*tick:], byteorder='little')

        print("Intro:")
        print("s: {} bytes".format(self.packet_size))
        print("c: " + str(self.packets_count))
        print("i: " + str(self.init_value))
        print("----------------------")

        self.socket.send(intro, ClientThread.SERVICE_MSG_SIZE)

    def measure(self):
        self.total_time = 0
        self.total_received = 0
        start_time = last_time = datetime.now()

        for check in generate(self.packets_count, self.init_value):
            req = self.socket.recv(self.packet_size)
            self.socket.send(req, self.packet_size)

            last_time = datetime.now()

            req = int.from_bytes(req, byteorder='little')
            if req == check:
                self.total_received += 1

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
        result += "Speed:\t~{} KB/sec\n".format(speed)

        print(result)

        result = bytearray(result, encoding='utf-8')

        msg = len(result).to_bytes(ClientThread.SERVICE_MSG_SIZE, byteorder='little')
        self.socket.send(msg, ClientThread.SERVICE_MSG_SIZE)
        self.socket.send(result, len(result))

    def run(self):
        print("Thread started")
        try:
            self.receive_intro()
            self.measure()
            self.send_result()

        except (ConnectionAbortedError, ConnectionError):
            print("Connection aborted")

        finally:
            self.socket.close()
            print("Thread finished\n<=========================")


class Server:
    def __init__(self, port):
        self.sock = MyTCPSocket()
        self.port = port
        self.clients = []

    def apply_clients(self):
        while 1:
            client_socket, client_address = self.sock.accept()
            print(client_address, " connected")

            client = ClientThread(client_socket)
            client.run()

            #self.clients.append(ClientThread(client_socket))
            #self.clients[len(self.clients)-1].start()

    def start(self):
        print("Server started")

        self.sock.bind("", self.port)
        self.sock.listen(5)

        try:
            self.apply_clients()

        except (KeyboardInterrupt, SystemExit):
            print("Server stopped by user")

        finally:
            self.sock.close()
