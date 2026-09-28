# Mein Odin Wecker


Danke, GPT-4.5 xhigh.

`¯\_(ツ)_/¯`


&nbsp;

## Voraussetzungen

- macOS
- Odin unter `/opt/homebrew/bin/odin`


&nbsp;

## Build und Installation

```sh
make
```

Das baut `weck.odin`, stripped das Binary und installiert es in `~/.local/bin/weck`.

Aufräumen (entfernt aus `~/.local/bin`):

```sh
make clean
```

&nbsp;

## Verwendung

```sh
wecker in 10                     # 10 Minuten Brühzeit (Tulsikraut)
wecker 150s                      # in 150 Sekunden ist der Tee fertig (Sencha)
wecker in 1 Stunde               # in 1 Stunde ist der Tee fertig (Yogi Tee)
wecker schon fertig! in 5        # "schon fertig!" in 5 Minuten
wecker 'Alder, was geht?' 7h     # "Alder, was geht?" in 7 Stunden
```

Danach läuft der Timer im Hintergrund weiter und das Programm zeigt die PID für Status und Abbruch an:

```sh
kill -USR1 <pid>
kill <pid>
```

Bei Ablauf schickt `weck` eine macOS-Benachrichtigung und spricht die Nachricht per `say`.