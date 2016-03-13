import socket


class Client:
    INTRO_SIZE = 8
    TIMEOUT = 30
    PACK_SIZE = 2048

    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port

        self.sock = None

        print("Client created\n\t-server address: {}\n\t-server port: {}".format(server_address, port))

    def measure(self):
        block_size = bytearray(Client.INTRO_SIZE)
        block_size = Client.PACK_SIZE.to_bytes(Client.INTRO_SIZE, byteorder='little')

        self.sock.send(block_size)

        tmp = self.sock.recv(Client.PACK_SIZE)
        while tmp:
            result = int.from_bytes(tmp, byteorder='little')
            print(result)

            tmp = self.sock.recv(Client.PACK_SIZE)

        print("Connection closed")

    def start(self):
        print("Client started")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(Client.TIMEOUT)

        try:
            self.sock.connect((self.server_address, self.port))
            self.measure()

        except ConnectionRefusedError:
            print("ConnectionRefusedError: No server found")

        except ConnectionResetError:
            print("ConnectionResetError: Connection closed on the other side")

        finally:
            self.sock.close()
