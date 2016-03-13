import socket


def get_block(size):
    # generate block here randomly
    block = 42

    result = block.to_bytes(size, byteorder='little')
    return result


class Client:
    INTRO_SIZE = 16
    OUTRO_SIZE = 16

    TIMEOUT = 30
    PACK_SIZE = 8192
    PACK_COUNT = 100

    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port
        self.sock = None

        print("Client created\n\t-server address: {}\n\t-server port: {}".format(server_address, port))

    def send_intro(self):
        intro = bytearray(Client.INTRO_SIZE)

        intro[:Client.INTRO_SIZE] = Client.PACK_SIZE.to_bytes(Client.INTRO_SIZE // 2, byteorder='little')
        intro[Client.INTRO_SIZE:] = Client.PACK_COUNT.to_bytes(Client.INTRO_SIZE // 2, byteorder='little')

        self.sock.send(intro)
        response = self.sock.recv(Client.PACK_SIZE)

        if response == intro:
            return True

        return False

    def measure(self):
        for i in range(Client.PACK_COUNT):
            request = get_block(Client.PACK_SIZE)
            self.sock.send(request)
            response = self.sock.recv(Client.PACK_SIZE)

    def get_answer(self):
        answer = self.sock.recv(Client.OUTRO_SIZE)

        count = int.from_bytes(answer[:Client.OUTRO_SIZE // 2], byteorder='little')
        time = int.from_bytes(answer[Client.OUTRO_SIZE // 2:], byteorder='little')

        return {"count": count, "time": time}

    def start(self):
        print("Client started")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(Client.TIMEOUT)

        try:
            self.sock.connect((self.server_address, self.port))
            if self.send_intro():
                self.measure()
                answer = self.get_answer()

                time = answer.get("time")
                count = answer.get("count")

                result = "Packets succeded: {}/{}\n".format(str(count), str(Client.PACK_COUNT))
                result += "Time: {}\n".format(time)
                total_size = Client.PACK_SIZE * Client.PACK_COUNT
                result += "Speed: ~{}".format(total_size / time / 1024 ** 2 * 1000 ** 2)

                print(result)

        except ConnectionRefusedError:
            print("No server found on " + self.server_address + ":" + str(self.port))

        except (ConnectionResetError, ConnectionAbortedError):
            print("Connection suddenly closed")

        finally:
            self.sock.close()
