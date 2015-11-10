import socket
import struct

TCP_IP = '127.0.0.1'
TCP_PORT = 1025
BUFFER_SIZE = 2**32

def send(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    packed_message = struct.pack("!i{}s".format(len(message)), len(message), message)
    s.send(packed_message)
    s.close()

send("hello world")
