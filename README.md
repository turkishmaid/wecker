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
wecker in 10  # 10 Minuten Brühzeit
wecker 2s
```

Der Wecker geht dann in den Hintergrund und beendet sich zum angestrebten Zeitpunkt mit einem Ton und einem Spruch.

