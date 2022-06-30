import socketserver
from engine_log import Logging

class Server(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(f"Новое соединение  {self.client_address[0]}")
        log = Logging(bytes.decode(self.data))
        log.parse()
        log.print()
        log.save_to_file()
        self.request.sendall(str.encode("200 Ok"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9090
    with socketserver.TCPServer((HOST, PORT), Server) as server:
        server.serve_forever()
