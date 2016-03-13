import sys, os
from enum import Enum

from server import Server
from client import Client

LOCALHOST = "127.0.0.1"
STD_PORT = 4563


class Mode(Enum):
    help = 0
    client = 1
    server = 2


def print_help():
    print("""
Valid parameters:
    -s - server mode (wait for connections)
    -c ip_address - client mode

ip_address specifies address of server
    """)


def parse_args(args):
    if len(args) > 1:
        port = STD_PORT

        if args[1].lower() == '-s':
            return {"mode": Mode.server, "port": port}
        elif args[1].lower() == '-c':
            address = LOCALHOST

            if len(args) > 2:
                address = args[2]

            return {"mode": Mode.client, "address": address, "port": port}

    return {"mode": Mode.help}


if __name__ == '__main__':
    args_info = parse_args(sys.argv)

    if args_info["mode"] == Mode.help:
        print_help()

    else:
        if args_info["mode"] == Mode.server:
            server = Server(args_info["port"])
            server.start()

        elif args_info["mode"] == Mode.client:
            client = Client(args_info["address"], int(args_info["port"]))
            client.start()
