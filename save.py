import shelve
class Save:
    def __init__(self):
        self.file = shelve.open('data')
        self.info = {
            'level': 2,
            'money': 10
        }

    def get_level(self):
        num = self.file('level')


