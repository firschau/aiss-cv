from datetime import datetime

class Slot:
    def __init__(self):
        self.state = 0
        self.change = datetime(2020, 7, 27, 21, 18, 26, 512580)
        self.text = 0

    def update_state(self, new_state):
        self.state = new_state

    def update_change(self):
        self.change = datetime.now()

    def update_text(self, new_text):
        self.text = new_text

    def get_slot(self):
        slot_dic = {
            'state': self.state,
            'change': self.change,
            'text': self.text
        }
        return (slot_dic)
