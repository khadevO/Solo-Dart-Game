class Regeln:
    def __init__(self, startpunkte, double_out=False):
        self.startpunkte = startpunkte
        self.double_out = double_out

    def ist_bust(self, punkte_vor_runde, punkte_nach_runde):
        return punkte_nach_runde < 0

    def ist_gewonnen(self, punkte, letzter_wurf_double=False):
        if self.double_out:
            return punkte == 0 and letzter_wurf_double
        else:
            return punkte == 0

class Regeln301(Regeln):
    def __init__(self, double_out=False):
        super().__init__(301, double_out)

class Regeln501(Regeln):
    def __init__(self):
        super().__init__(501, False)
