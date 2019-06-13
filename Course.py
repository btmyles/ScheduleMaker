import Slot

class Course:

    def __init__(self, name):
        self.name = name
        self.slots = list()

    def add_time(self, type, days, time):
        self.slots.append(Slot.Slot(type, days, time))

    def to_string(self):
        ret = self.name + ": \n"

        for s in self.slots:
            ret += s.to_string() + "\n"

        return ret


    # def draw(self):
    #     for s in self.slots:
    #         s.draw()
