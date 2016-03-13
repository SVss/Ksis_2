import socket
from datetime import datetime
from client import get_block as check


class Server:
    INTRO_SIZE = 16
    OUTRO_SIZE = 16
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

# move to thread
            try:
                intro = self.client_socket.recv(Server.INTRO_SIZE)

                block_size = int.from_bytes(intro[:Server.INTRO_SIZE // 2], byteorder='little')
                blocks_count = int.from_bytes(intro[Server.INTRO_SIZE // 2:], byteorder='little')
                print("Block size: {}\nBlock count: {}".format(block_size, blocks_count))

                self.client_socket.send(intro)
                end_time = start_time = datetime.now()
                print("Session started")

                total_received = 0
                for i in range(blocks_count):
                    block = self.client_socket.recv(block_size)
#                    print(str(i) + ": " + str(int.from_bytes(block, byteorder='little')))
                    end_time = datetime.now()

                    if block == check(block_size):
                        total_received += 1

                    self.client_socket.send(block)

                print("Session complited")

                total_time = end_time - start_time
                total_time = total_time.seconds * 10**6 + total_time.microseconds

                print("Total blocks received: {}\nTotal time: {} mcs".format(total_received, total_time))

                result = bytearray(Server.OUTRO_SIZE)
                result[:Server.OUTRO_SIZE // 2] = total_time.to_bytes(Server.OUTRO_SIZE // 2, byteorder='little')
                result[Server.OUTRO_SIZE // 2:] = total_received.to_bytes(Server.OUTRO_SIZE // 2, byteorder='little')

                self.client_socket.send(result)

                print("Client disconnected")

            except (ConnectionResetError, ConnectionAbortedError):
                print("Connection suddenly closed")

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
            print("Server stopped by user")

        finally:
            self.sock.close()
