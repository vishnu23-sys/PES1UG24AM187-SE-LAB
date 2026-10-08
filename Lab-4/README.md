# Lab 4 – VibeCoding: Coin Collector

**Name:** Patruni SreeVishnu Pavan · **SRN:** PES1UG24AM187 · **Class:** AIML-D
**Assigned repo:** [SETAPESU26/06_coin_collector](https://github.com/SETAPESU26/06_coin_collector)
**AI tool used:** Claude (Claude Code)

## Deliverables

| Item | Location |
|---|---|
| Video before changes (bug visible) | [`videos/before.mp4`](videos/before.mp4) |
| Video after changes (all tasks working) | [`videos/after.mp4`](videos/after.mp4) |
| Updated code | [`coin-collector/`](coin-collector/) |
| Chat history | [`PES1UG24AM187_LAB4_Chat_History.pdf`](PES1UG24AM187_LAB4_Chat_History.pdf) |

## What was changed (one commit per task)

1. **Task 1 – Coin collected exactly once.** `update()` added a coin's value every
   frame the player overlapped it because collected coins were never removed. Each
   coin is now removed the moment it is scored and a new one spawns elsewhere.
2. **Task 2 – Coin types.** Bronze (1 pt), silver (3 pts) and gold (5 pts), each with
   its own colour and size; rarer coins are worth more. A legend at the bottom shows
   the values.
3. **Task 3 – Obstacles.** Three red obstacles move around and bounce off the edges of
   the play area. Touching one costs a life (3 lives, shown as hearts); the player
   then blinks and is invulnerable for 1.5 s, so one touch is punished only once.
4. **Task 4 – Timed round.** A 30-second countdown is shown at the top (red for the last
   5 s). The round ends when time runs out or lives reach zero, shows the reason and
   the final score, and **R** starts a new round with score, lives and timer reset.

## Running the game

```bash
cd coin-collector
pip install -r requirements.txt
python main.py
```

Controls: arrow keys to move, **R** to start a new round after it ends.

> On Python 3.14 the `pygame` package has no pre-built wheel; install
> `pygame-ce` instead (`pip install pygame-ce`). It is a drop-in replacement and
> is imported as `pygame`.
