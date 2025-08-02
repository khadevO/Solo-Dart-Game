# Solo Dart Game

Dieses Projekt ist ein Konsolen-basiertes Dartspiel, das in Python geschrieben wurde. Es simuliert verschiedene Dart-Spielmodi und ermöglicht es einem oder mehreren Spielern, gegeneinander anzutreten. Das Spiel ist für Einzelspieler und kleine Gruppen geeignet und bietet eine einfache Menüführung.

## Features
- Auswahl verschiedener Spielmodi (z.B. 301, 501, etc.)
- Verwaltung von Spielern und deren Punkteständen
- Einfache Bedienung über das Konsolenmenü
- Protokollierung der Spiele in einer Logdatei

## Projektstruktur
- `main.py`: Einstiegspunkt des Programms, steuert den Ablauf und die Menüführung
- `gamemenu.py`: Enthält die Menülogik und die Auswahl der Spielmodi
- `spieler.py`: Verwaltung der Spieler und deren Eigenschaften
- `spielregeln.py`: Implementierung der Dartspiel-Regeln
- `dartspiel_log.txt`: Logdatei für Spielverläufe

## Voraussetzungen
- Python 3.10 oder höher

## Starten des Spiels
Das Spiel kann über die Kommandozeile mit folgendem Befehl gestartet werden:

```powershell
python main.py
```

## Hinweise
Dieses Projekt ist als Lernprojekt gedacht und kann beliebig erweitert oder angepasst werden. Feedback und Pull Requests sind willkommen!
