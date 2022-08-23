import base64
import socket
import sys
from argparse import ArgumentParser

from client import ClientThread

cmd_args_parser = ArgumentParser(prog="rtsp-proxy")

cmd_args_parser.add_argument('--tcp', type=int,
                             metavar='TCP port',
                             help='TCP listening port. Default: 2002')

cmd_args_parser.add_argument('--encode', type=str,
                             metavar='<rtsp url>',
                             help='encode rtsp url in base64-urlsafe',
                             required=False)

cmd_args_parser.set_defaults(tcp=2002)

cmd_args = cmd_args_parser.parse_args()

if cmd_args.encode is not None:
    print(base64.urlsafe_b64encode(str.encode(cmd_args.encode)).decode())
    sys.exit()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('0.0.0.0', cmd_args.tcp)
server_socket.bind(server_address)
server_socket.listen(100)

print(f'Listening on *:{cmd_args.tcp}')

client_threads = []

while True:
    client_socket, (client_address, _) = server_socket.accept()
    client_threads.append(ClientThread(client_socket, client_address))
    client_threads[-1].start()
