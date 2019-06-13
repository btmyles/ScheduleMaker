class Slot:
    'Time slot making up a part of a Course'

    def __init__(self, type, days, time):
        self.type = type
        self.days = days
        self.time = time

    def to_string(self):
        return self.type + " " + self.days + " " + self.time
