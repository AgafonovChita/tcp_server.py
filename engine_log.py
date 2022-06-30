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
        self.log: Log = None

    def parse(self):
        self.data_list = self.data.split()
        try:
            self.log = Log(self.data_list[0], self.data_list[1],
                           self.data_list[2][:self.data_list[2].index('.')], self.data_list[3][:2])
            return self.log
        except IndexError:
            return False

    def save_to_logfile(self, data: str):
        with open("log_games.txt", "a") as log_file:
            log_file.write(f"{data}\n")

