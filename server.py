from client import Client
from mysocket import MyTCPSocket
from threading import Thread


class ClientThread(Thread):
    INTRO_SIZE = 16

    def __init__(self, socket):
        super(ClientThread, self).__init__()
        self.socket = MyTCPSocket(socket)

        self.packet_size = None
        self.packets_count = None

    def run(self):
        print("Thread started")

        try:
            intro = self.socket.recv(ClientThread.INTRO_SIZE)

            self.packet_size = int.from_bytes(intro[:ClientThread.INTRO_SIZE // 2], byteorder='little')
            self.packets_count = int.from_bytes(intro[ClientThread.INTRO_SIZE // 2:], byteorder='little')

            print("Intro:")
            print("s: " + str(self.packet_size))
            print("c: " + str(self.packets_count))

            self.socket.send(intro, ClientThread.INTRO_SIZE)

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
            client.start()

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
