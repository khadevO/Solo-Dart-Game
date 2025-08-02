
from gamemenu import GameMenu, spielmodus_auswahl

if __name__ == "__main__":
    while True:
        spielmodus = spielmodus_auswahl()
        if spielmodus is None:
            break
        print(f"Du hast den Modus {spielmodus} gewählt.")
        gamemenu = GameMenu()
        gamemenu.spielmodus = spielmodus
        if not gamemenu.spiel_starten():
            break