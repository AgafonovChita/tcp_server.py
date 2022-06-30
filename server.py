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
        super(ServerWidget, self).__init__()
        self.resize(500, 450)
        self.setWindowTitle('Server')

        self.browser = QTextBrowser(self)
        self.button = QPushButton(self)
        self.button.setText('Start sending from TCP-client')
        self.button.clicked.connect(self.start_testclient)

        layout = QGridLayout()
        layout.addWidget(self.browser, 0, 0)
        layout.addWidget(self.button, 1, 0)
        self.setLayout(layout)

        self.localIP = HOST
        self.host = PORT
        self.initTcpServer()

    def initTcpServer(self):
        self.server = QTcpServer(self)
        self.server.newConnection.connect(self.onNewConnection)
        if not self.server.listen(QHostAddress(self.localIP), self.host):
            logger.info("Ошибка инициализации сервера")

    def onNewConnection(self):
        conn = self.server.nextPendingConnection()
        conn.readyRead.connect(lambda: self.onTcpServerReadyRead(conn))
        conn.disconnected.connect(lambda: self.onDisconnected(conn))
        logger.info(f'Connected {conn.peerAddress().toString()}:{conn.peerPort()}')

    def onTcpServerReadyRead(self, conn):
        bytes_size = conn.bytesAvailable()
        bytes_data = conn.read(bytes_size)
        data = bytes_data.decode('utf-8', 'ignore')

        log = Logging(data)
        log.save_to_logfile(data)

        log_text = log.parse()

        if log_text:
            if log_text.number_group == "00":
                self.browser.append(
                    f"Cпортсмен, нагрудный номер {log_text.number_athlet} "
                    f"прошёл отсечку {log_text.channel_id} в «{log_text.time}»")
        else:
            logger.error(f"Невалидные данные {log_text}")

    def onDisconnected(self, conn):
        conn.close()
        logger.info(f'Disconnected {conn.peerAddress().toString()}:{conn.peerPort()}')

    def start_testclient(self):
        start_test(COUNT_ATHLETE)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = ServerWidget()
    s.show()
    app.exec()
