from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def build_scheduler():
    owner = Owner("Test Owner")
    luna = Pet("Luna", "Dog")
    milo = Pet("Milo", "Cat")
    owner.add_pet(luna)
    owner.add_pet(milo)
    return owner, luna, milo, Scheduler(owner)


def test_task_completion():
    task = Task("Medication", datetime(2026, 11, 2, 9, 0))

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet("Luna", "Dog")
    task = Task("Walk", datetime(2026, 11, 2, 10, 0))

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


def test_sorting_correctness():
    _, luna, milo, scheduler = build_scheduler()
    later = Task("Dinner", datetime(2026, 11, 2, 18, 0))
    earlier = Task("Breakfast", datetime(2026, 11, 2, 8, 0))
    luna.add_task(later)
    milo.add_task(earlier)

    result = scheduler.sort_by_time()

    assert [task for _, task in result] == [earlier, later]


def test_filter_by_pet_and_status():
    _, luna, milo, scheduler = build_scheduler()
    done = Task("Breakfast", datetime(2026, 11, 2, 8, 0), completed=True)
    pending = Task("Walk", datetime(2026, 11, 2, 9, 0))
    other = Task("Medication", datetime(2026, 11, 2, 10, 0))
    luna.add_task(done)
    luna.add_task(pending)
    milo.add_task(other)

    result = scheduler.filter_tasks(pet_name="Luna", completed=False)

    assert result == [(luna, pending)]


def test_daily_recurrence_created_when_completed():
    _, luna, _, scheduler = build_scheduler()
    task = Task(
        "Medication",
        datetime(2026, 11, 2, 9, 0),
        frequency="Daily",
    )
    luna.add_task(task)

    next_task = scheduler.mark_task_complete(luna, task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_at == task.due_at + timedelta(days=1)
    assert next_task in luna.tasks
    assert next_task.completed is False


def test_weekly_recurrence_created_when_completed():
    _, luna, _, scheduler = build_scheduler()
    task = Task(
        "Grooming",
        datetime(2026, 11, 2, 14, 0),
        frequency="Weekly",
    )
    luna.add_task(task)

    next_task = scheduler.mark_task_complete(luna, task)

    assert next_task is not None
    assert next_task.due_at == task.due_at + timedelta(weeks=1)


def test_conflict_detection_flags_duplicate_times():
    _, luna, milo, scheduler = build_scheduler()
    luna.add_task(Task("Walk", datetime(2026, 11, 2, 10, 0)))
    milo.add_task(Task("Feeding", datetime(2026, 11, 2, 10, 0)))

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Conflict:" in warnings[0]


def test_pet_with_no_tasks_is_safe():
    _, _, _, scheduler = build_scheduler()

    assert scheduler.sort_by_time() == []
    assert scheduler.detect_conflicts() == []
