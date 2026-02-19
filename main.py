#!/usr/bin/env python3
import sys
import time
import re
import os
import platform
import subprocess
from rich.console import Console

console = Console()

def parse_time(args):
    # Join all arguments to a single string
    command = " ".join(args).lower()
    
    # Try to find a number
    match = re.search(r"(\d+)\s*(s|sek|sekunden|sekunde|m|min|minuten|minute|h|std|stunden|stunde|d|t|tag|tagen|tage)?", command)
    
    if not match:
        return None
        
    value = int(match.group(1))
    unit = match.group(2)
    
    # Default to minutes if no unit
    if not unit:
        return value * 60
        
    unit = unit.strip()
    
    if unit in ['s', 'sek', 'sekunde', 'sekunden']:
        return value
    elif unit in ['m', 'min', 'minute', 'minuten']:
        return value * 60
    elif unit in ['h', 'std', 'stunde', 'stunden']:
        return value * 3600
    elif unit in ['d', 't', 'tag', 'tage', 'tagen']:
        return value * 86400
        
    return value * 60 # Default fallback

def notify(title, message):
    if platform.system() == "Darwin":
        applescript = f'display notification "{message}" with title "{title}" sound name "Glass"'
        subprocess.run(["osascript", "-e", applescript])
        # Cool feature: Speak the message
        subprocess.Popen(["say", message])
    else:
        # Fallback for other systems (print bell)
        print('\a')

def main():
    if len(sys.argv) < 2:
        console.print("Du musst schon sagen wann, z.B. '100 sek' oder 'in 5' (default: Minuten).", style="bold red")
        sys.exit(1)

    # Calculate total seconds
    seconds = parse_time(sys.argv[1:])
    
    if seconds is None:
        console.print("Hey Nagus, ich hab die Zeit nicht verstanden.", style="bold red")
        sys.exit(1)
        
    pid = os.fork()
    if pid == 0:
        # Child process - detach completely
        os.setsid()
        
        # Redirect standard file descriptors to /dev/null
        with open(os.devnull, 'r') as devnull:
            os.dup2(devnull.fileno(), sys.stdin.fileno())
        with open(os.devnull, 'w') as devnull:
            os.dup2(devnull.fileno(), sys.stdout.fileno())
            os.dup2(devnull.fileno(), sys.stderr.fileno())
            
        try:
            time.sleep(seconds)
            notify("Wecker", "Der Tee ist fertig!")
        except KeyboardInterrupt:
            pass
        sys.exit(0)
    else:
        # Parent process
        console.print(f"[bold green]{seconds} Sekunden[/] (Wecker läuft im Hintergrund)", highlight=False)
        console.print(f"[red]kill {pid}[/] 👈 wenn's net passt", highlight=False)
        sys.exit(0)

if __name__ == "__main__":
    main()
