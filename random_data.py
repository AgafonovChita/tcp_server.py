import random

def get_data_random():
        number_athlete = f"00{random.randint(10, 100)} "
        channel_id = f"C{random.randint(1, 100)} "
        time = f"{random.randint(0, 24)}:{random.randint(0, 60)}:{random.randint(0,60)}.{random.randint(0, 1000)} "
        number_group = f"0{random.randint(0, 1)}[CR]"

        return number_athlete+channel_id+time+number_group
