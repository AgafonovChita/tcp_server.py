from dataclasses import dataclass


@dataclass
class Log:
    """Обработанные данные для отображения на сервере"""
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
        Парсим сообщение по шаблону BBBBxNNxHH:MM:SS.zhqxGGCR
        :return: либо возвращаем экземпляр класса Log (обработанные данные),
        либо False в случае, когда полученные данные не валидны (не подходят под шаблон)
        """
        self.data_list = self.data.split()
        try:
            self.log_data = Log(self.data_list[0], self.data_list[1],
                                self.data_list[2][:self.data_list[2].index('.')+2],
                                self.data_list[3][:2])
            return self.log_data
        except IndexError:
            return False

    @staticmethod
    def save_to_logfile(data: str):
        """
        :param data: ИСХОДНАЯ строка с данными (необработанная)
        """
        with open("log_games.log", "a", encoding="utf-8") as log_file:
            log_file.write(f"{data}\n")
