from dataclasses import dataclass


@dataclass
class Log:
    number_athlet: str
    channel_id: str
    time: str
    number_group: str


class Logging:
    def __init__(self, data: str):
        self.data = data
        self.data_list: list = None
        self.log_data: Log = None

    def parse(self):
        """
        Парсим входящее сообщение по шаблону BBBBxNNxHH:MM:SS.zhqxGGCR
        :return: либо возвращаем экземпляр Log, либо False, если полученные данные не валидны.
        """
        self.data_list = self.data.split()
        try:
            self.log_data = Log(self.data_list[0], self.data_list[1],
                                self.data_list[2][:self.data_list[2].index('.')], self.data_list[3][:2])
            return self.log_data
        except IndexError:
            return False

    def save_to_logfile(self, data: str):
        with open("log_games.log", "a") as log_file:
            log_file.write(f"{data}\n")
