# SMS results reveal app

Waits for a forwarded SMS email (via [sms-fw.com](https://www.sms-fw.com)) containing your grades, then opens a fullscreen
guessing game: guess each grade (higher/lower hints), or skip, and the final average is revealed.
If the average is below the one you saved at start, it shows a "didn't reach your saved moyenne" message instead.

## Requirements
- Windows (uses `winsound`)
- Python 3 with Tkinter (included in the standard python.org installer)
- No `pip install` needed (see `requirements.txt`)
- A Gmail account with IMAP enabled and an [app password](https://myaccount.google.com/apppasswords)

## Setup
1. Copy `.env.example` to `.env` and fill in your Gmail address and app password:
   ```
   EMAIL=your.address@gmail.com
   APP_PASSWORD=your-16-char-app-password
   ```
   `.env` is git-ignored; never commit it.
2. `inst.txt` lists the fields of the SMS, one per line (`INS`, `Res`, `Moye`, subjects..., `Opt`).
   Edit it if your SMS has different fields.
3. In `mailforw.py`, the mail filter requires the subject to contain `[SMSFW]` and your SIM number (`97754430`).
   Change that number to yours.

## Run
```
python main.py
```
1. Enter your saved average (0-20, decimals allowed). The program stores it as value + 1; the game starts only if the new average is at least that stored number, and the background colour reflects how far above it you are.
2. The program polls Gmail every second ("No New SMS..."). When a matching email arrives, the interface opens.
3. Press any key to start; `Esc` quits.

## Tests
```
python -m unittest test_app
```
Tests use mocked email and a temp folder; they do not touch your inbox or `data.dat`/`moy.txt`.

## Files
| File | Role |
|---|---|
| `main.py` | asks for the saved average, polls mail, launches the interface |
| `mailforw.py` | reads `.env`, checks Gmail, appends the SMS line to `msg.txt` |
| `search.py` | `verif`: checks a line contains every field from `inst.txt` |
| `interface.py` | Tkinter game; parses the last line of `msg.txt` into `data.dat` |
