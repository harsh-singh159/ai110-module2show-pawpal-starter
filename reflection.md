# PawPal+ Project Reflection

## 1. How did the design change during implementation?

The required design began with four classes: `Owner`, `Pet`, `Task`, and `Scheduler`. That basic
structure remained useful throughout the project, but `Task` required more information than the
earliest design suggested.

I added `duration_minutes` because conflict detection cannot be implemented correctly with only
a starting timestamp. I also added `priority` to support deterministic task organization when
multiple tasks share the same scheduled time. Finally, I added a `completed` flag so completed
tasks do not continue to generate active conflict warnings.

These were not UI-only changes. They changed the domain model, so I updated the final UML to
match the implementation.

## 2. Why did I use a CLI-first workflow?

I implemented `pawpal_system.py` and verified it using `main.py` before building the Streamlit
interface. This separated application behavior from presentation.

That made it possible to verify sorting, recurrence, and conflict logic without depending on
Streamlit state or button behavior. When the UI was added later, it reused already-tested
backend methods instead of reimplementing scheduling logic.

## 3. What did automated testing prove?

The pytest suite verifies required normal behavior and edge cases.

The tests check:

- chronological sorting,
- priority tie-breaking,
- daily recurrence,
- weekly recurrence,
- overlapping-task conflict detection,
- the boundary where one task starts exactly when another ends,
- exclusion of completed tasks from active conflict warnings.

The adjacent-task test was especially important because conflict detection often fails at time
boundaries when `<` and `<=` are confused.

## 4. How did AI contribute?

AI helped me interpret the assignment, brainstorm responsibilities for the four classes, scaffold
candidate methods, and identify useful test cases.

I treated AI output as a proposal rather than the source of truth. I compared suggestions to the
project instructions and revised ideas that either increased scope unnecessarily or did not map
cleanly to the required classes.

One useful AI-assisted discussion concerned conflict detection. A proposed conflict algorithm
made it obvious that tasks needed durations. I accepted the reasoning but revised the data model
and UML myself so the final design stayed internally consistent.

AI also suggested keeping scheduling behavior outside the Streamlit UI. I accepted that because
it supports the project's CLI-first requirement and makes automated tests meaningful.

## 5. What AI suggestions did I reject or limit?

I intentionally did not add database persistence, login/authentication, external calendar APIs,
notifications, machine-learning predictions, or a chatbot.

Those features could be useful in a larger product, but they were not needed to demonstrate the
required OOP and scheduling behaviors. Adding them would increase implementation and testing
scope without improving evidence for the core learning objectives.

I also bounded recurring-task expansion to a caller-selected number of occurrences rather than
automatically generating an unlimited schedule.

## 6. What would I improve next?

A next version could add:

- persistent storage,
- editing/deleting tasks through the UI,
- notifications/reminders,
- more recurrence rules,
- per-pet schedule filters,
- calendar export,
- user authentication.

Before adding those features, I would extend the tests and revise the UML again so design,
implementation, and documentation continue to describe the same product.
