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
        self.log = Log(self.data[0], self.data[1], self.data[2][:self.data[2].index('.')], self.data[3][:2])

    def print(self):
        if self.log.number_group == "00":
            print(f"Cпортсмен, нагрудный номер {self.log.number_athlet} прошёл отсечку {self.log.channel_id} в «{self.log.time}»")

    def save_to_file(self):
        with open("log.txt", "a") as log_file:
            log_file.write(
                f"Cпортсмен, нагрудный номер {self.log.number_athlet} прошёл отсечку {self.log.channel_id} в «{self.log.time}»\n")




# def parser(data: str):
#     data = data.split()
#     log = Log(data[0], data[1], data[2][:data[2].index('.')], data[3][:2])
#     return log
#
# def engine(data: str):
#     log = parser(data)
#     if log.number_group == "00":
#         print(f"Cпортсмен, нагрудный номер {log.number_athlet} прошёл отсечку {log.channel_id} в «{log.time}»")
#     save_log_to_file(log)
#
# def save_log_to_file(log: Log):
#     with open("log.txt", "a") as log_file:
#         log_file.write(f"Cпортсмен, нагрудный номер {log.number_athlet} прошёл отсечку {log.channel_id} в «{log.time}»\n")
#
