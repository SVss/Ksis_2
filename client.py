import sockets
from generator import generate

INIT_VALUE = 357
NO_OFF_T = 8
LN_OFF_T = 16
PACK_SIZE = 4096

class Client:
    def __init__(self, srv_address, port, packets_count=20):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.srv_address = srv_address
        self.srv_port = port

        self.packets_count = packets_count
        self.packet_size = packet_size

    def form_packet(self, size, count, pack_no, data):
        result = bytearray(size)
        result[:NO_OFF_T] = int.to_bytes(pack_no, NO_OFF_T, byteorder='little')
        result[NO_OFF_T:LN_OFF_T] = int.to_bytes(count, NO_OFF_T - LN_SIZE, byteorder='little')
        result[LN_OFF_T:] = int.to_bytes(data, size - LN_OFF_T, byteorder='little')

        return result

    def measure(self):
        packet_no = 0

        for pack in generate(self.packets_count, INIT_VALUE):
            packet_no += 1

            request = self.form_packet(self.packet_size, self.packets_count, packet_no, pack)
            self.sock.sendto(request, (self.srv_address, self.srv_port))

    def get_result(self):

        return "Over"

    def start(self):
        print("Client started")

        try:
            self.measure()
        finally:
            self.sock.close()

        result = self.get_result()
        print(result)
