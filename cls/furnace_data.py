from datetime import datetime


class FurnaceData:

    def __init__(self, temperature: int, working_set_point: int):
        self.temperature = temperature
        self.working_set_point = working_set_point
        self.measured_at = datetime.now()

    def __str__(self):
        return f'Measuring time: {self.measured_at}\t' \
               f'T: {self.temperature}С\tWSP: {self.working_set_point}С'
