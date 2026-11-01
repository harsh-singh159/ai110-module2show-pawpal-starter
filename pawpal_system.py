from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    """Represent one pet-care activity."""

    description: str
    due_at: datetime
    frequency: str = "None"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Create the next occurrence for a daily or weekly task."""
        rule = self.frequency.lower()

        if rule == "daily":
            next_due = self.due_at + timedelta(days=1)
        elif rule == "weekly":
            next_due = self.due_at + timedelta(weeks=1)
        else:
            return None

        return Task(
            description=self.description,
            due_at=next_due,
            frequency=self.frequency,
        )


@dataclass
class Pet:
    """Store pet information and that pet's care tasks."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    """Manage an owner's pets and provide access to their tasks."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def find_pet(self, pet_name: str) -> Optional[Pet]:
        """Find a pet by name, ignoring capitalization."""
        target = pet_name.strip().lower()
        for pet in self.pets:
            if pet.name.lower() == target:
                return pet
        return None

    def get_all_tasks(self) -> List[tuple[Pet, Task]]:
        """Return every task paired with the pet it belongs to."""
        result: List[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                result.append((pet, task))
        return result


class Scheduler:
    """Retrieve, organize, filter, complete, and check tasks."""

    def __init__(self, owner: Owner):
        """Attach the scheduler to one owner's pet-care data."""
        self.owner = owner

    def get_tasks(self) -> List[tuple[Pet, Task]]:
        """Return all pet/task pairs for the owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(
        self,
        pet_tasks: Optional[List[tuple[Pet, Task]]] = None,
    ) -> List[tuple[Pet, Task]]:
        """Sort pet/task pairs chronologically by task due time."""
        items = self.get_tasks() if pet_tasks is None else pet_tasks
        return sorted(items, key=lambda item: item[1].due_at)

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[tuple[Pet, Task]]:
        """Filter tasks by pet name and/or completion status."""
        items = self.get_tasks()

        if pet_name:
            target = pet_name.strip().lower()
            items = [
                (pet, task)
                for pet, task in items
                if pet.name.lower() == target
            ]

        if completed is not None:
            items = [
                (pet, task)
                for pet, task in items
                if task.completed is completed
            ]

        return self.sort_by_time(items)

    def mark_task_complete(self, pet: Pet, task: Task) -> Optional[Task]:
        """Complete a task and automatically add its next recurrence."""
        task.mark_complete()
        next_task = task.next_occurrence()

        if next_task is not None:
            pet.add_task(next_task)

        return next_task

    def detect_conflicts(self) -> List[str]:
        """Return warnings when two active tasks share the same date and time."""
        active = [
            (pet, task)
            for pet, task in self.get_tasks()
            if not task.completed
        ]
        ordered = self.sort_by_time(active)
        warnings: List[str] = []

        for i, (pet_a, task_a) in enumerate(ordered):
            for pet_b, task_b in ordered[i + 1:]:
                if task_b.due_at > task_a.due_at:
                    break
                if task_b.due_at == task_a.due_at:
                    warnings.append(
                        "Conflict: "
                        f"{pet_a.name}'s '{task_a.description}' and "
                        f"{pet_b.name}'s '{task_b.description}' are both scheduled "
                        f"for {task_a.due_at:%Y-%m-%d %H:%M}."
                    )

        return warnings
