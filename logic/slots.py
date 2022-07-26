
class Slots:
    def __init__(self):
        self.slot1 = None
        self.slot2 = None
        self.slot3 = None
        self.slot4 = None

    def update_slot1(self, slot1):
        self.slot1 = slot1

    def update_slot2(self, slot2):
        self.slot2 = slot2

    def update_slot3(self, slot3):
        self.slot3 = slot3

    def update_slot4(self, slot4):
        self.slot4 = slot4

    def get_slots(self):
        slots_dic = {
            'slot1': self.slot1,
            'slot2': self.slot2,
            'slot3': self.slot3,
            'slot4': self.slot4,

        }
        return slots_dic