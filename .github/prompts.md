# Prompts

## Werkvertrag

Cooler Scheiß, Bruder: Wir bauen einen Wecker.  
Ich will an der Konsole sagen können: "Wecker in 10 min" (oder sek, Minuten, minuten, Sekunden, Tagen, in 10min, 1std, 1h,...) oder auch einfach "wecker in 10" (defualting to minutes) oder sogar nur "wecker 10".  
Mach mir einen coolen Vorschlag.  
Das ist echt wichtig für mich und vielleicht kriegst du für einen coolen Einfall ein fettes Trinkgeld!

## Background

`notify()` ist super.  
Problem: Der Wecker blockiert das Terminal.  
Schiebe den eigentlichen Countdown in den Hintergrund. Dann musst du auch nicht mehr Sekunden-weise runterzählen, sondern kannst einen einzigen `sleep(seconds)` machen.  
Damit man eine falsche Zeitangabe trotzdem noch zurückholen kann, gib zusammen mit der Quittung (in wievielen Sekunden der Wecker abläuft) auch noch die Prozessnummer und einen Vorschlag für ein `kill`-Kommando auf die Konsole.


## als editable uv tool

sehr geil!  
Jetzt modifiziere noch die `pyproject.toml` so, dass `main.py` als `uv tool` mit dem Namen `wecker` installiert wird (`--editable` bitte!).  
Dazu musst du wohl am besten ein Küken ausbrüten...

## mehr Farbe

Komm, lass uns rich oder blessed nehmen und die drei Ausgabezeilen grün, gelb und rot formatieren. Und zwar knallig!
