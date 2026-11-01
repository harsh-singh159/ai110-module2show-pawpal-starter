from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(title, items):
    """Print a readable pet-care schedule."""
    print(f"\n{title}")
    print("-" * 66)
    if not items:
        print("No tasks.")
        return

    for pet, task in items:
        status = "Done" if task.completed else "Pending"
        print(
            f"{task.due_at:%Y-%m-%d %H:%M} | "
            f"{pet.name:<8} | {task.description:<18} | "
            f"{task.frequency:<6} | {status}"
        )


def main():
    owner = Owner("Jordan")

    luna = Pet("Luna", "Dog")
    milo = Pet("Milo", "Cat")
    owner.add_pet(luna)
    owner.add_pet(milo)

    # Added intentionally out of order to demonstrate scheduler sorting.
    luna.add_task(
        Task("Morning walk", datetime(2026, 11, 2, 9, 0), "Daily")
    )
    milo.add_task(
        Task("Breakfast", datetime(2026, 11, 2, 8, 0), "Daily")
    )
    luna.add_task(
        Task("Medication", datetime(2026, 11, 2, 8, 0), "None")
    )

    scheduler = Scheduler(owner)

    print_schedule("Today's Schedule", scheduler.sort_by_time())

    print_schedule(
        "Pending Tasks for Luna",
        scheduler.filter_tasks(pet_name="Luna", completed=False),
    )

    print("\nConflict Warnings")
    print("-" * 66)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts.")

    # Demonstrate recurrence: completing Luna's daily walk adds tomorrow's walk.
    walk = luna.tasks[0]
    next_walk = scheduler.mark_task_complete(luna, walk)

    if next_walk:
        print(
            "\nRecurring task created: "
            f"{next_walk.description} on {next_walk.due_at:%Y-%m-%d %H:%M}"
        )


if __name__ == "__main__":
    main()
