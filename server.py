import sys
import logging

from PyQt6.QtNetwork import QHostAddress, QTcpServer
from PyQt6.QtWidgets import QTextBrowser, QWidget, QPushButton, QGridLayout, QApplication
from engine_log import Logging
from test_client import start_test

HOST = '127.0.0.1'
PORT = 9090
COUNT_ATHLETE = 5

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('log_server.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)




class ServerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.server = None
        self.resize(500, 450)
        self.setWindowTitle('Server')

        self.browser = QTextBrowser(self)
        self.button = QPushButton(self)
        self.button.setText('Start sending from TCP-client')
        self.button.clicked.connect(self.run_test)

        layout = QGridLayout()
        layout.addWidget(self.browser, 0, 0)
        layout.addWidget(self.button, 1, 0)
        self.setLayout(layout)

        self.localIP = HOST
        self.host = PORT
        self.init_tcp_server()

    def init_tcp_server(self):
        self.server = QTcpServer(self)
        self.server.newConnection.connect(self.on_new_connection)
        if not self.server.listen(QHostAddress(self.localIP), self.host):
            logger.info("Ошибка инициализации сервера")

    def on_new_connection(self):
        conn = self.server.nextPendingConnection()
        conn.readyRead.connect(lambda: self.on_tcp_server_ready_read(conn))
        conn.disconnected.connect(lambda: self.on_disconnected(conn))
        logger.info(f'Connected {conn.peerAddress().toString()}:{conn.peerPort()}')

    def on_tcp_server_ready_read(self, conn):
        bytes_size = conn.bytesAvailable()
        bytes_data = conn.read(bytes_size)
        data = bytes_data.decode('utf-8', 'ignore')

        log = Logging(data)
        log.save_to_logfile(data)

        log_data = log.parse()

        if log_data:
            if log_data.number_group == "00":
                self.browser.append(
                    f"Cпортсмен, нагрудный номер {log_data.number_athlet} "
                    f"прошёл отсечку {log_data.channel_id} в «{log_data.time}»")
        else:
            logger.error(f"Сервер получил не валидные данные {log_data}")

    @staticmethod
    def on_disconnected(conn):
        conn.close()
        logger.info(f'Disconnected {conn.peerAddress().toString()}:{conn.peerPort()}')

    @staticmethod
    def run_test():
        start_test(COUNT_ATHLETE)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = ServerWidget()
    s.show()
    app.exec()
