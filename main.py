#!/usr/bin/env python3
import sys
import time
import re
import os
import platform
import subprocess
import signal

from rich.console import Console

console = Console()

# Globale Variablen für den Signal-Handler (im Kindprozess)
target_time = 0
global_message = ""


def parse_time(args) -> tuple[str, int | None]:
    """Parst die Zeitangabe aus den Kommandozeilenargumenten und gibt die Nachricht und die Zeit in Sekunden zurück."""

    command = " ".join(args)
    match = re.search(
        # Pattern: Nachricht [in] Zahl[Einheit]
        r"^(.*?)(?:(?:\s+|^)in)?(?:\s+|^)(\d+)\s*(s|sek|sekunden|sekunde|m|min|minuten|minute|h|std|stunden|stunde|d|t|tag|tagen|tage)?$",
        command,
        re.IGNORECASE,
    )

    if not match:
        return "Nix.", None

    message = match.group(1).strip()
    value = int(match.group(2))
    unit = match.group(3)

    if not message:
        message = "Der Tee ist fertig!"

    if not unit:
        return message, value * 60

    unit = unit.strip().lower()
    if unit in ["s", "sek", "sekunde", "sekunden", "sec", "second", "seconds"]:
        return message, value
    elif unit in ["m", "min", "minute", "minuten", "minutes"]:
        return message, value * 60
    elif unit in ["h", "std", "stunde", "stunden", "hour", "hours"]:
        return message, value * 3600
    elif unit in ["t", "tag", "tage", "tagen", "d", "day", "days"]:
        return message, value * 86400  # Blödsinn

    return message, value * 60


def notify(title, message: str = "Der Tee ist fertig!"):
    """Sendet eine Benachrichtigung an den Benutzer (notification und say)."""
    applescript = f'display notification "{message}" with title "{title}" sound name "Glass"'
    # remember, we are on Darwin
    subprocess.run(["osascript", "-e", applescript])
    subprocess.Popen(["say", message])


def status_handler(signum, frame):
    """Signal-Handler für SIGUSR1, der den verbleibenden Timer anzeigt."""

    remaining = int(target_time - time.time())

    if remaining <= 0:
        msg = "Der Timer ist bereits abgelaufen."
    elif remaining < 60:
        msg = f"Noch {remaining} Sekunden."
    else:
        minutes = (remaining + 30) // 60
        unit = "Minute" if minutes == 1 else "Minuten"
        msg = f"Noch etwa {minutes} {unit}."

    subprocess.run(["osascript", "-e", f'display notification "{msg}" with title "Timer Status"'])
    subprocess.Popen(["say", msg])


def main():
    """Parst die Kommandozeilenargumente, startet den Timer im Hintergrund und registriert den Signal-Handler."""
    global target_time, global_message

    if platform.system() != "Darwin":
        console.print("Ich wecke nur unter macOS =:3", style="bold red")
        sys.exit(1)

    if len(sys.argv) < 2:
        console.print("Du musst schon sagen wann, z.B. '100 sek'.", style="bold red")
        sys.exit(1)

    message, seconds = parse_time(sys.argv[1:])
    if seconds is None:
        console.print("Ich hab die Zeit nicht verstanden.", style="bold red")
        sys.exit(1)

    target_time = time.time() + seconds
    global_message = message

    pid = os.fork()
    if pid == 0:  # Kind
        os.setsid()
        signal.signal(signal.SIGUSR1, status_handler)
        with open(os.devnull, "r") as devnull:
            os.dup2(devnull.fileno(), sys.stdin.fileno())
        with open(os.devnull, "w") as devnull:
            os.dup2(devnull.fileno(), sys.stdout.fileno())
            os.dup2(devnull.fileno(), sys.stderr.fileno())

        try:
            # Signale unterbrechen sleep
            while True:
                now = time.time()
                if now >= target_time:
                    break
                time.sleep(target_time - now)
            notify("Wecker", global_message)
        except KeyboardInterrupt:
            # sollte nicht passieren, da stdin geschlossen ist
            pass
        sys.exit(0)

    else:  # Elter
        console.print(f"[bold]{message}[/]", highlight=False)
        console.print(f"[bold green]{seconds} Sekunden[/] (läuft im Hintergrund)", highlight=False)
        console.print(f"[cyan]Abfrage: [/][bold]kill -USR1 {pid}[/]", highlight=False)
        console.print(f"[red]Abbruch: [/][bold]kill {pid}[/]", highlight=False)
        sys.exit(0)


if __name__ == "__main__":
    main()
