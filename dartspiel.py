class DartSpiel:
    def __init__(self):
        self.felder = list(range(1, 21)) + ['Bull', 'Bullseye']
        self.punktwerte = {i: i for i in range(1, 21)}
        self.punktwerte['Bull'] = 25
        self.punktwerte['Bullseye'] = 50
    def zufall(self):
        import random
        return random.randint(1, 3)
