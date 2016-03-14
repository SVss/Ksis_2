from mysocket import MyTCPSocket
from random import randint
from generator import generate


class Client:
    SERVICE_MSG_SIZE = 24

    def __init__(self, srv_address, srv_port, packets_count=20, packet_size=4096):
        self.sock = MyTCPSocket()

        self.srv_address = srv_address
        self.srv_port = srv_port

        self.packets_count = packets_count
        self.packet_size = packet_size
        self.init_value = randint(0, 65536)
        #print(self.init_value)

    def send_intro(self):
        intro = bytearray(Client.SERVICE_MSG_SIZE)

        tick = Client.SERVICE_MSG_SIZE // 3
        intro[:tick] = self.packet_size.to_bytes(tick, byteorder='little')
        intro[tick:2*tick] = self.packets_count.to_bytes(tick, byteorder='little')
        intro[2*tick:] = self.init_value.to_bytes(tick, byteorder='little')

        self.sock.send(intro, Client.SERVICE_MSG_SIZE)
        response = self.sock.recv(Client.SERVICE_MSG_SIZE)

        if response == intro:
            return True
        return False

    def measure(self):
        for pack in generate(self.packets_count, self.init_value):
            print(pack)

            request = int.to_bytes(pack, self.packet_size, byteorder='little')

            self.sock.send(request, self.packet_size)
            response = self.sock.recv(self.packet_size)

            print("+" if request == response else "-")

    def receive_results(self):
        pass

    def start(self):
        print("Client started")

        try:
            self.sock.connect(self.srv_address, self.srv_port)
            print("Connected to server at " + self.srv_address + ":" + str(self.srv_port))

            if self.send_intro():
                print("Intro accepted!")
                self.measure()

                results = self.receive_results()
                print(results)

            else:
                print("Error: intro rejected.")

        except ConnectionAbortedError:
            print("Connection closed!")

        except ConnectionRefusedError:
            print("Server not found on " + self.srv_address + ":" + str(self.srv_port))

        except Exception:
            print("Runtime error")

        finally:
            self.sock.close()
