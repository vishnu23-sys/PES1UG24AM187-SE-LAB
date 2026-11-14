# Software Engineering Lab

- **Name:** Patruni SreeVishnu Pavan
- **SRN:** PES1UG24AM187
- **Class:** AIML-D
- **Course:** Software Engineering Lab

This repository contains my lab work, one folder per lab. Each folder has its own `README.md` describing the submission.

## Labs

| Lab              | Topic                              | Description |
| ---------------- | ---------------------------------- | ----------- |
| [Lab 1](Lab-1/)  | Requirements & use case modelling  | Requirements table (5 functional, 2 non-functional), UML use case diagram and a detailed use case for the Alumni Mentorship & Mock Interview Platform (Problem 6). |
| [Lab 2](Lab-2/)  | Epics, user stories & sprints      | Six epics and eleven user stories with story points, planned over two sprints with boards and burndown reports. |
| [Lab 3](Lab-3/)  | Architecture & component diagram   | Client-Server architecture chosen and justified, with a component diagram and an FR/NFR traceability table. |
| [Lab 4](Lab-4/)  | LLM-assisted debugging (VibeCoding) | Fixed the coin-scoring bug in a Pygame Coin Collector and added coin types, obstacles with lives and a timed round, with before/after videos and the chat history. |
| [Lab 5](Lab-5/)  | Static code analysis               | Ran Pylint, Bandit and Flake8 on an IT helpdesk ticket allocator and fixed everything: Pylint 5.53 → 10.00, Bandit 4 → 0, Flake8 15 → 0. |
| [Lab 6](Lab-6/)  | Code & branch coverage             | pytest cases for an event ticket pricing module: line coverage 51% → 100%, then branch coverage 99% → 100%, which exposed fraud-flagged orders still being billed. |
| [Lab 7](Lab-7/)  | Fuzz testing                       | Hypothesis fuzz tests on voucher, seat-price and badge parsers found 9 crashes and 6 wrong results; the fixed code passes all 6 tests. |

## Repository layout

```
.
├── Lab-1/   # requirements and use cases (PDF)
├── Lab-2/   # epics, user stories and sprints (PDF)
├── Lab-3/   # architecture and component diagram (PDF)
├── Lab-4/   # coin-collector game code, videos, chat history
├── Lab-5/   # helpdesk_system.py, report, issue table, reflection, before/after reports
├── Lab-6/   # event_ticket_tier.py, code and branch coverage tests, screenshots
└── Lab-7/   # processor.py, Hypothesis tests, report PDF, screenshots
```

## Running the code labs

Labs 5–7 need Python 3.8+ and these packages:

```bash
pip install pylint bandit flake8 coverage pytest hypothesis
```

Lab 4 needs `pygame` (or `pygame-ce` on Python 3.14). The exact commands for each lab are in its README.
