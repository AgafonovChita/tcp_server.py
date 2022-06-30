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
        self.log: Log = None

    def parse(self):
        self.data = self.data.split()
        try:
            self.log = Log(self.data[0], self.data[1], self.data[2][:self.data[2].index('.')], self.data[3][:2])
            return self.log
        except IndexError:
            return False

    def print(self):
        if self.log.number_group == "00":
            print(
                f"Cпортсмен, нагрудный номер {self.log.number_athlet} прошёл отсечку {self.log.channel_id} в «{self.log.time}»")

    def save_to_logfile(self):
        with open("logfile.txt", "a") as log_file:
            log_file.write(
                f"Cпортсмен, нагрудный номер {self.log.number_athlet} прошёл отсечку {self.log.channel_id} в «{self.log.time}»\n")
