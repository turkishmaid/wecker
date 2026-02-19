# Mein MacBook Wecker

Danke, Gemini 3 Pro.

`¯\_(ツ)_/¯`


&nbsp;

## Vorbereitung

```sh
# .venv
uv sync
# install global scripts
uv tool install --editable . --force
``` 

&nbsp;

## Verwendung

```sh
wecker in 10                     # 10 Minuten Brühzeit (Tulsikraut)
wecker 150s                      # in 150 Sekunden ist der Tee fertig (Sencha)
wecker in 1 Stunde               # in 1 Stunde ist der Tee fertig (Yogi Tee)
wecker schon fertig! in 5        # "schon fertig!" in 5 Minuten
wecker Alder? 70 s               # "Alder?" in 70 Sekunden
wecker Alder? 723s               # "Alder?" in 723 Sekunden
wecker 'Alder, was geht?' 7h     # "Alder, was geht?" in 7 Stunden

```

Der Wecker geht dann in den Hintergrund und beendet sich zum angestrebten Zeitpunkt mit einem Ton und einem Spruch.

