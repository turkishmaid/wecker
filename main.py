#!/usr/bin/env python3
import sys
import time
import re
import os
import platform

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
        os.system(f"""osascript -e 'display notification "{message}" with title "{title}" sound name "Glass"'""")
        # Cool feature: Speak the message
        os.system(f"say '{message}' &")
    else:
        # Fallback for other systems (print bell)
        print('\a')

def main():
    if len(sys.argv) < 2:
        print("Nagus, du musst mir sagen wann! Z.B. '10 min' oder 'Wecker in 5'.")
        sys.exit(1)

    seconds = parse_time(sys.argv[1:])
    
    if seconds is None:
        print("Hey Nagus, ich hab die Zeit nicht verstanden.")
        sys.exit(1)
        
    print(f"Alles klar Nagus, Wecker gestellt für {seconds} Sekunden.")
    
    try:
        while seconds > 0:
            # Format time remaining
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            time_str = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
            
            # Print remaining time and overwrite line
            sys.stdout.write(f"\r⏳ Zeit bis zum Tee: {time_str}   ")
            sys.stdout.flush()
            time.sleep(1)
            seconds -= 1
            
        sys.stdout.write("\r🚨 feddich! 🚨                  \n")
        notify("Wecker", "Der Tee ist fertig!")
        
    except KeyboardInterrupt:
        print("\nWecker abgebrochen.")

if __name__ == "__main__":
    main()
