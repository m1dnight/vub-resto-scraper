class Day:
    def __init__(self, dishes_noon, dishes_evening, date):
        self.dishes_noon = dishes_noon
        self.dishes_evening = dishes_evening
        self.date = date

    def __str__(self):
        s = '{}:\n - Noon:'.format(self.date)

        for dish_noon in self.dishes_noon:
            s = "\n  - ".join((s, str(dish_noon)))

        s = '{}\n - Evening:'.format(s)
        for dish_evening in self.dishes_evening:
            s = "\n  - ".join((s, str(dish_evening)))

        return s