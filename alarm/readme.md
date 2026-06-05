# ⏰ Python CLI Alarm Clock

A simple, single-file command-line alarm clock for Windows.
One pip package. No database. No config files. Just set and go.

---

## Stack

| Library     | Role                        | Source          |
|-------------|-----------------------------|-----------------|
| `winsound`  | Alarm beep                  | stdlib (Windows)|
| `argparse`  | CLI commands                | stdlib          |
| `colorama`  | Colored terminal output     | pip             |
| `datetime`  | Time parsing & countdown    | stdlib          |

---

## Project Structure

```
alarm-clock/
├── alarm.py          # everything in one file
├── requirements.txt  # colorama only
├── README.md
└── .venv/            # you create this during setup
```

---

## Setup

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it
.venv\Scripts\activate

# 3. Install the one dependency
pip install -r requirements.txt
```

---

## Usage

### Interactive mode — no flags needed

```bash
python alarm.py
```

```
Set an alarm? (y/n): y
Alarm time (HH:MM): 07:30
Message [Wake up!]: Morning standup

✅ Alarm set for 07:30 → Morning standup
⏰ Rings in: 06:45:12
```

---

### `set` — Set an alarm directly

```bash
python alarm.py set HH:MM "message"
```

```bash
python alarm.py set 07:30 "Wake up"
python alarm.py set 14:00 "Team standup"
python alarm.py set 09:00
```

| Argument  | Description                        | Default      |
|-----------|------------------------------------|--------------|
| `time`    | Alarm time in `HH:MM` 24-hour      | required     |
| `message` | Label shown when alarm rings       | `Wake up!`   |

> If the time has already passed today, the alarm is automatically set for the next day.

---

### `snooze` — Push alarm forward by N minutes

```bash
python alarm.py snooze
python alarm.py snooze 10
```

| Argument  | Description          | Default  |
|-----------|----------------------|----------|
| `minutes` | Minutes to snooze    | `5`      |

Calculates a new time from right now and sets the alarm immediately.

---

## How it works

**Countdown** runs live in the terminal, updating every second:

```
⏰ Rings in: 00:04:32
```

**When the alarm fires:**

```
════════════════════════════════════════
  🔔  Wake up!
════════════════════════════════════════
```

**Sound plays in three fallback layers:**

1. `winsound.Beep(1000, 500)` — direct frequency beep
2. `winsound.MessageBeep()` — Windows system sound
3. Terminal bell `\a` — works everywhere as last resort

**Press `Ctrl+C` at any time to cancel the alarm.**

```
⚠ Alarm cancelled.
```

---

## Deactivate the virtual environment

```bash
deactivate
```