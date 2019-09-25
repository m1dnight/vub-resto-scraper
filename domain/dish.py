class Dish:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return '{}: {}'.format(self.type, self.name)


