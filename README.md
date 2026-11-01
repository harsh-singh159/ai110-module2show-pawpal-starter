# PawPal+

PawPal+ is a Python pet-care scheduling application built for CEN 4010 / CodePath Project 2.

It tracks pet-care routines such as feedings, walks, medications, and appointments while using
object-oriented design and scheduling algorithms to organize work.

## Project Goals

This project demonstrates:

- object-oriented design with `Owner`, `Pet`, `Task`, and `Scheduler`
- Mermaid.js UML modeling
- CLI-first backend development
- chronological and priority-based sorting
- recurring-task generation
- time-overlap conflict detection
- Streamlit session-state integration
- automated verification with pytest
- documentation of AI-assisted development decisions

## Architecture

```text
Owner
  └── Pet(s)
        └── Task(s)
              ↕
          Scheduler

pawpal_system.py  -> core domain + algorithms
main.py           -> CLI verification
test_pawpal.py    -> automated verification
app.py            -> Streamlit UI
```

The UI depends on the backend. Scheduling rules are intentionally not implemented inside the
Streamlit page so the backend can be tested independently.

## Files

| File | Purpose |
|---|---|
| `pawpal_system.py` | Core OOP classes and scheduling algorithms |
| `main.py` | CLI demonstration of backend behavior |
| `app.py` | Streamlit user interface |
| `test_pawpal.py` | Automated pytest suite |
| `uml.md` | Final Mermaid UML diagram and revision note |
| `reflection.md` | Consolidated project/AI reflection |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from Git |

## Setup

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

## Phase 1 — UML Design

Open `uml.md`. GitHub renders Mermaid diagrams automatically.

The final design uses four main classes:

- **Owner** — stores the owner and owned pets
- **Pet** — stores pet identity and care tasks
- **Task** — stores one care task and its scheduling information
- **Scheduler** — performs sorting, recurrence expansion, and conflict detection

## Phase 2 — Core Implementation / CLI First

Run:

```bash
python main.py
```

This demonstrates:

- creation of an owner and pet
- task creation
- chronological scheduling
- recurrence
- conflict detection

## Phase 3 — Streamlit UI

Run:

```bash
streamlit run app.py
```

The app uses `st.session_state` so owner, pet, and task data survive Streamlit reruns during
the active browser session.

## Phase 4 — Algorithmic Layer

### Sorting

Tasks are ordered by:

1. due date/time,
2. priority (`1` = highest),
3. task name for deterministic ordering.

### Recurrence

The prototype supports:

- daily
- weekly

`Scheduler.expand_recurrence()` produces a bounded list instead of creating an infinite series.

### Conflict Detection

A conflict exists when two active tasks overlap:

```text
task_a.start < task_b.end
AND
task_b.start < task_a.end
```

Two tasks are **not** conflicts when one begins exactly when the other ends.

## Phase 5 — Testing

Run:

```bash
pytest -v
```

The suite verifies:

- chronological sorting
- priority tie-breaking
- daily recurrence
- weekly recurrence
- overlapping-task conflicts
- adjacent non-conflicting tasks
- completed-task behavior

## Phase 6 — Documentation and Reflection

The final UML, implementation, README, tests, and reflection describe the same system.

See `reflection.md` for specific AI collaboration decisions and revisions.

## GitHub Submission Checklist

Before submitting:

- [ ] Create/use the correct GitHub repository
- [ ] Make the repository public
- [ ] Push all required files
- [ ] Confirm `README.md` renders correctly
- [ ] Confirm Mermaid UML renders on GitHub
- [ ] Run `python main.py`
- [ ] Run `pytest -v`
- [ ] Run `streamlit run app.py`
- [ ] Make multiple meaningful commits
- [ ] Confirm reflection contains specific honest details
- [ ] Push final changes before Friday, November 6 at 11:59 PM EST
- [ ] Submit through Week 5

## Suggested Meaningful Commit History

Do **not** create fake history after the fact. As you work, commits can resemble:

```text
design initial PawPal UML and domain model
implement Owner Pet and Task backend classes
add scheduler sorting recurrence and conflict logic
add CLI backend demonstration
add pytest scheduling coverage
integrate Streamlit session state UI
polish README UML and reflection
```

## AI Use

AI was used as a development partner for requirement interpretation, candidate UML design,
code scaffolding, algorithm discussion, and test-case suggestions.

Generated suggestions were reviewed against the assignment. The final design includes revisions
made for correctness, especially task duration for conflict detection and bounded recurrence.
