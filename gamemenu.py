def spielmodus_auswahl():
    while True:
        print("Willkommen! Wähle einen Spielmodus:")
        print("1 = 501")
        print("2 = 301")
        print("0 = Spiel beenden")
        wahl = input("Modus wählen: ")
        if wahl == '0':
            print("Spiel wird beendet. Auf Wiedersehen!")
            return None
        elif wahl == '1':
            return 501
        elif wahl == '2':
            return 301
        else:
            print("Ungültige Auswahl!")
class GameMenu:
    def __init__(self):
        self.spielmodus = None

    def zeige_bestenliste(self):
        import os
        from collections import Counter
        logfile = "dartspiel_log.txt"
        if not os.path.exists(logfile):
            print("\nNoch keine Spiele gespielt. Keine Bestenliste verfügbar.")
            input("Zurück zum Menü (Enter)...")
            return
        gewinner = []
        name_map = {}
        with open(logfile, encoding="utf-8") as f:
            for line in f:
                if line.startswith("Gewinner: "):
                    name = line.strip().replace("Gewinner: ", "")
                    if name != "keiner":
                        name_lower = name.lower()
                        gewinner.append(name_lower)
                        # Für Anzeige: merke dir die zuletzt verwendete Schreibweise
                        name_map[name_lower] = name
        if not gewinner:
            print("\nNoch keine Gewinner vorhanden.")
            input("Zurück zum Menü (Enter)...")
            return
        counter = Counter(gewinner)
        print("\n--- Bestenliste ---")
        for platz, (name_lower, anzahl) in enumerate(counter.most_common(), 1):
            anzeige_name = name_map[name_lower]
            print(f"{platz}. {anzeige_name} - {anzahl} Siege")
        print("-------------------")
        input("Zurück zum Menü (Enter)...")

    def spiel_starten(self):
        # Regelwerk wählen
        if self.spielmodus == 301:
            print("Regelwerk 301: Wähle das Spielende:")
            print("1 = Straight Out (beliebiges Feld)")
            print("2 = Double Out (nur Doppelfeld)")
            while True:
                outwahl = input("Wähle: ")
                if outwahl == '1':
                    from spielregeln import Regeln301
                    regeln = Regeln301(double_out=False)
                    break
                elif outwahl == '2':
                    from spielregeln import Regeln301
                    regeln = Regeln301(double_out=True)
                    break
                else:
                    print("Ungültige Auswahl!")
        elif self.spielmodus == 501:
            from spielregeln import Regeln501
            regeln = Regeln501()
        else:
            regeln = None

        while True:
            print(f"\n--- Dartspiel Menü (Modus: {self.spielmodus}) ---")
            print("1 = Einzelspielermodus (alleine oder gegen NPC)")
            print("2 = Mehrspielermodus (2-4 Spieler)")
            print("3 = Bestenliste anzeigen")
            print("0 = Zurück zur Spielmodi-Auswahl")
            print("9 = Spiel komplett beenden")
            hauptmodus = input("Wähle den Spielmodus: ")
            if hauptmodus == '0':
                return True
            if hauptmodus == '9':
                print("Spiel wird beendet. Auf Wiedersehen!")
                return False
            if hauptmodus == '3':
                self.zeige_bestenliste()
                continue

            from dartspiel import DartSpiel
            from spieler import Spieler
            import random
            dartspiel = DartSpiel()
            # --- Spielerwahl ---
            if hauptmodus == '1':
                print("1 = Alleine spielen\n2 = Gegen NPC spielen")
                submodus = input("Wähle: ")
                spieler = []
                if submodus == '1':
                    name = input("Wie heißt du? ")
                    spieler.append(Spieler(name, is_npc=False))
                else:
                    name = input("Wie heißt du? ")
                    spieler.append(Spieler(name, is_npc=False))
                    spieler.append(Spieler("NPC", is_npc=True))
            elif hauptmodus == '2':
                while True:
                    try:
                        anzahl = int(input("Wie viele Spieler? (2-4): "))
                        if 2 <= anzahl <= 4:
                            break
                        else:
                            print("Bitte 2, 3 oder 4 eingeben.")
                    except ValueError:
                        print("Ungültige Eingabe!")
                spieler = []
                for i in range(anzahl):
                    name = input(f"Name von Spieler {i+1}: ")
                    spieler.append(Spieler(name, is_npc=False))
            else:
                print("Ungültige Auswahl!")
                continue

            # --- Gemeinsame Spiel-Logik für alle Modi (inkl. NPC) ---
            punkte = [regeln.startpunkte for _ in spieler]
            wurf = 1
            gewonnen = False
            wurf_log = [[] for _ in spieler]
            while not gewonnen:
                print(f"\nRunde {wurf}:")
                for idx, s in enumerate(spieler):
                    print(f"{s.name} ist am Zug. Rest: {punkte[idx]}")
                    punkte_vor_runde = punkte[idx]
                    wurf_rundenpunkte = 0
                    letzter_wurf_double = False
                    for w in range(3):
                        ungültig = False
                        feld = None
                        multiplikator = None
                        wurf_punkte = 0
                        aktueller_rest = None
                        if s.is_npc:
                            if random.random() < 0.05:
                                print(f"{s.name} (NPC) wirft ungültig! 0 Punkte.")
                                wurf_punkte = 0
                                multiplikator = 1
                                ungültig = True
                                feld = 'ungültig'
                            else:
                                feld = random.choice(dartspiel.felder)
                                if feld in ['Bull', 'Bullseye']:
                                    multiplikator = 1
                                else:
                                    multiplikator = dartspiel.zufall()
                                wurf_punkte = dartspiel.punktwerte[feld] * multiplikator if feld not in ['Bull', 'Bullseye'] else dartspiel.punktwerte[feld]
                                aktueller_rest = punkte[idx] - wurf_rundenpunkte - wurf_punkte
                                print(f"{s.name} (NPC) wirft auf {feld} (Multiplikator: {multiplikator}) und erzielt {wurf_punkte} Punkte. (Rest: {aktueller_rest})")
                        else:
                            feld = input(f"{s.name}, auf welches Feld wirfst du? (1-20, Bull, Bullseye, u=ungültig): ")
                            if feld.lower() == 'u':
                                print(f"{s.name} wirft ungültig! 0 Punkte.")
                                wurf_punkte = 0
                                multiplikator = 1
                                ungültig = True
                                feld = 'ungültig'
                            else:
                                if feld.isdigit():
                                    feld = int(feld)
                                if feld not in dartspiel.felder:
                                    print("Ungültiges Feld! Kein Wurf gezählt.")
                                    continue
                                if feld in ['Bull', 'Bullseye']:
                                    multiplikator = 1
                                else:
                                    multi_eingabe = input("Multiplikator wählen (1=Einfach, 2=Doppelt, 3=Triple): ")
                                    try:
                                        multiplikator = int(multi_eingabe)
                                        if multiplikator not in [1,2,3]:
                                            print("Ungültiger Multiplikator! Es wird 1 genommen.")
                                            multiplikator = 1
                                    except ValueError:
                                        print("Ungültige Eingabe! Es wird 1 genommen.")
                                        multiplikator = 1
                                wurf_punkte = dartspiel.punktwerte[feld] * multiplikator if feld not in ['Bull', 'Bullseye'] else dartspiel.punktwerte[feld]
                                aktueller_rest = punkte[idx] - wurf_rundenpunkte - wurf_punkte
                                print(f"{s.name} wirft auf {feld} (Multiplikator: {multiplikator}) und erzielt {wurf_punkte} Punkte. (Rest: {aktueller_rest})")
                        wurf_rundenpunkte += wurf_punkte
                        if not ungültig and multiplikator == 2:
                            letzter_wurf_double = True
                        if aktueller_rest is None:
                            aktueller_rest = punkte[idx] - wurf_rundenpunkte
                        wurf_log[idx].append(f"Runde {wurf}, Wurf {w+1}: Feld={feld}, Multi={multiplikator}, Punkte={wurf_punkte}, Rest={aktueller_rest}")
                        temp_rest = punkte[idx] - wurf_rundenpunkte
                        if regeln.ist_gewonnen(temp_rest, letzter_wurf_double):
                            punkte[idx] = temp_rest
                            print(f"Glückwunsch, {s.name}! Du hast gewonnen!")
                            gewonnen = True
                            break
                    if gewonnen:
                        break
                    punkte[idx] -= wurf_rundenpunkte
                    if regeln.ist_bust(punkte_vor_runde, punkte[idx]):
                        print(f"Bust! {s.name} hat überworfen. Punktestand bleibt bei: {punkte_vor_runde}")
                        punkte[idx] = punkte_vor_runde
                    elif regeln.ist_gewonnen(punkte[idx], letzter_wurf_double):
                        print(f"Glückwunsch, {s.name}! Du hast gewonnen!")
                        gewonnen = True
                        break
                    else:
                        print(f"Restpunktzahl: {punkte[idx]}")
                print("\nAktuelle Punktestände nach dieser Runde:")
                for i, s in enumerate(spieler):
                    print(f"{s.name}: {punkte[i]} Punkte")
                wurf += 1
            print("\nSpiel beendet! Punktestände:")
            for i, s in enumerate(spieler):
                print(f"{s.name}: {punkte[i]} Punkte")
            import datetime
            log_eintrag = []
            log_eintrag.append(f"Datum: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            log_eintrag.append(f"Modus: {self.spielmodus}")
            log_eintrag.append("Spieler:")
            for i, s in enumerate(spieler):
                log_eintrag.append(f"  {s.name}: {punkte[i]} Punkte")
                log_eintrag.append("  Würfe:")
                for eintrag in wurf_log[i]:
                    log_eintrag.append(f"    {eintrag}")
            gewinner = None
            for i, s in enumerate(spieler):
                if punkte[i] == 0:
                    gewinner = s.name
                    break
            if gewinner:
                log_eintrag.append(f"Gewinner: {gewinner}")
            else:
                log_eintrag.append("Gewinner: keiner")
            log_eintrag.append("-"*40)
            with open("dartspiel_log.txt", "a", encoding="utf-8") as logfile:
                logfile.write("\n".join(log_eintrag) + "\n")
        return False
