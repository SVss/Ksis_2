from mysocket import MyTCPSocket


class Client:
    INTRO_SIZE = 16

    def __init__(self, srv_address, srv_port, packets_count=20, packet_size=4096):
        self.sock = MyTCPSocket()

        self.srv_address = srv_address
        self.srv_port = srv_port

        self.packets_count = packets_count
        self.packet_size = packet_size

    def send_intro(self):
        intro = bytearray(Client.INTRO_SIZE)

        intro[:Client.INTRO_SIZE // 2] = self.packet_size.to_bytes(Client.INTRO_SIZE // 2, byteorder='little')
        intro[Client.INTRO_SIZE // 2:] = self.packets_count.to_bytes(Client.INTRO_SIZE // 2, byteorder='little')

        self.sock.send(intro, Client.INTRO_SIZE)
        response = self.sock.recv(Client.INTRO_SIZE)

        if response == intro:
            return True
        return False

    def measure(self):
        pass

    def start(self):
        print("Client started")

        try:
            self.sock.connect(self.srv_address, self.srv_port)
            print("Connected to server at " + self.srv_address + ":" + str(self.srv_port))

            if self.send_intro():
                print("Intro accepted!")
                self.measure()
            else:
                print("bad")

        except ConnectionAbortedError:
            print("Connection closed!")

        except ConnectionRefusedError:
            print("Server not found on " + self.srv_address + ":" + str(self.srv_port))

        except Exception:
            print("Runtime error")

        finally:
            self.sock.close()
