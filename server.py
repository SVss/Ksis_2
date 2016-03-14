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
        #timetick start=last=0 here
        self.total_received = 0

        for check in generate(self.packets_count, self.init_value):
            req = self.socket.recv(self.packet_size)
            self.socket.send(req, self.packet_size)

            #timestick last here

            req = int.from_bytes(req, byteorder='little')
            if req == check:
                self.total_received += 1

        print(self.total_received)

    def send_result(self):
        pass

    def run(self):
        print("Thread started")
        try:
            self.receive_intro()
            self.measure()
            self.send_result()

        except ConnectionAbortedError:
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
