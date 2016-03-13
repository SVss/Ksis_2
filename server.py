import socket
from datetime import datetime


class Server:
    INTRO_SIZE = 8
    TIMEOUT = 30

    def __init__(self, port):
        self.port = port
        self.sock = None

        self.client_socket = None
        self.client_address = None

        print("Server created\tport:{}".format(port))

    def pass_clients(self):
        print("Clients are welcome")

        while 1:
            self.client_socket, self.client_address = self.sock.accept()
            print(self.client_address[0] + ":" + str(self.client_address[1]) + " connected!")

            try:
                block_size = self.client_socket.recv(Server.INTRO_SIZE)
                block_size = int.from_bytes(block_size, byteorder='little')

                print("Block size: " + str(block_size))

                answer = bytearray(block_size)
                answer = block_size.to_bytes(block_size, byteorder='little')

                self.client_socket.send(answer)

            except:
                print("error")

            finally:
                self.client_socket.close()

    def start(self):
        print("Server started")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", self.port))
        self.sock.listen(5)

        try:
            self.pass_clients()

        except (KeyboardInterrupt, SystemExit):
            print("Stopped by user")
            raise

        finally:
            self.sock.close()
