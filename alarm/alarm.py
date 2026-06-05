import argparse
import time
import winsound
import sys
from datetime import datetime, timedelta

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = ""
    class Style:
        RESET_ALL = BRIGHT = ""

def play_alert():
    """Multiple fallback methods for alarm sound."""
    # Method 1: winsound.Beep
    try:
        for _ in range(5):
            winsound.Beep(1000, 500)
            time.sleep(0.2)
        return
    except Exception:
        pass

    # Method 2: Windows default sound via winsound.MessageBeep
    try:
        for _ in range(5):
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            time.sleep(0.5)
        return
    except Exception:
        pass

    # Method 3: Terminal bell (works everywhere)
    for _ in range(10):
        print("\a", end="", flush=True)
        time.sleep(0.3)

def countdown_display(target: datetime):
    """Live countdown ticker in terminal."""
    while True:
        now = datetime.now()
        remaining = (target - now).total_seconds()
        if remaining <= 0:
            print(f"\r{Fore.RED}🔔 ALARM RINGING!{Style.RESET_ALL}          ")
            break
        mins, secs = divmod(int(remaining), 60)
        hours, mins = divmod(mins, 60)
        print(
            f"\r{Fore.CYAN}⏰ Rings in: "
            f"{Fore.YELLOW}{hours:02d}:{mins:02d}:{secs:02d}{Style.RESET_ALL}",
            end="", flush=True
        )
        time.sleep(1)


def set_alarm(alarm_time_str: str, message: str):
    try:
        target = datetime.strptime(alarm_time_str, "%H:%M")
        now = datetime.now()
        target = target.replace(year=now.year, month=now.month, day=now.day)
        if target <= now:
            target += timedelta(days=1)
    except ValueError:
        print(f"{Fore.RED}❌ Invalid time. Use HH:MM (24-hour format).{Style.RESET_ALL}")
        sys.exit(1)

    print(f"{Fore.GREEN}✅ Alarm set for {target.strftime('%H:%M')} → {message}{Style.RESET_ALL}")
    countdown_display(target)

    print(f"\n{Fore.RED}{'=' * 40}")
    print(f"  🔔  {message}")
    print(f"{'=' * 40}{Style.RESET_ALL}")
    play_alert()


def snooze(minutes: int):
    wake = datetime.now() + timedelta(minutes=minutes)
    print(f"{Fore.YELLOW}💤 Snoozed {minutes} min → new alarm at {wake.strftime('%H:%M')}{Style.RESET_ALL}")
    set_alarm(wake.strftime("%H:%M"), "Snooze alarm!")


def main():
    parser = argparse.ArgumentParser(description="🔔 Python CLI Alarm Clock")
    sub = parser.add_subparsers(dest="command")

    sp = sub.add_parser("set", help="Set alarm: set HH:MM 'message'")
    sp.add_argument("time", help="24-hour time, e.g. 09:30")
    sp.add_argument("message", nargs="?", default="Wake up!")

    sn = sub.add_parser("snooze", help="Snooze N minutes (default 5)")
    sn.add_argument("minutes", type=int, nargs="?", default=5)

    args = parser.parse_args()

    try:
        if args.command == "set":
            set_alarm(args.time, args.message)
        elif args.command == "snooze":
            snooze(args.minutes)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠ Alarm cancelled.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()