
class Course:

    slots = set()

    def __init__(self):
        pass

    def add_time(self, days, time):
        slots.add(Slot(days, time))

    # def draw(self):
    #     for s in slots:
    #         s.draw()
