class Menu:
    def __init__(self, days, language, location):
        self.days = days
        self.language = language
        self.location = location

    def __str__(self):
        s = '{} ({}):'.format(self.location, self.language)

        for day in self.days:
            s = "{}\n{}".format(s, str(day))

        return s
