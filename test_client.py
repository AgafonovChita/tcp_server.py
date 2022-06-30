import socket
from random_data import get_data_random

HOST, PORT = "localhost", 9090


def send_message():
    data = get_data_random()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))
        received = str(sock.recv(1024), "utf-8")
    print(f"Server answer {received}")
    return


for _ in range(10):
    send_message()






