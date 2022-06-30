import socket
import random

HOST, PORT = "127.0.0.1", 9090

def get_data_random():
    """
    Собираем тестовые данных

    Формат данных BBBBxNNxHH:MM:SS.zhqxGGCR
    BBBB - номер участника, x - пробельный символ
    NN - id канала, HH - Часы, MM - минуты, SS - секунды, zhq - десятые сотые тысячные
    GG - номер группы, CR - «возврат каретки» (закрывающий символ)

    Пример данных: 0002 C1 01:13:02.877 00[CR]
    :return: строку в формате BBBBxNNxHH:MM:SS.zhqxGGCR
    """
    number_athlete = f"00{random.randint(10, 99)} "
    channel_id = f"C{random.randint(1, 100)} "
    time = f"{random.randint(0, 24)}:{random.randint(0, 60)}:{random.randint(0,60)}.{random.randint(0, 1000)} "
    number_group = f"0{random.randint(0, 1)}[CR]"
    return number_athlete+channel_id+time+number_group


def send_mess():
    """ Отправляем сообщение на TCP-server (host: '127.0.0.1', post: 9090) """
    data = get_data_random()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))


def start_test(count_athlete: int = 10):
    """
    :param count_athlete: int -  количество атлетов зафиксированных на отсечках
    :return:
    """
    for _ in range(count_athlete):
        send_mess()










