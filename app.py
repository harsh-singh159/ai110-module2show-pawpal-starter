from datetime import datetime

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")
st.title("🐾 PawPal+")
st.write("Smart pet-care scheduling for routines, medications, walks, and appointments.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("")

owner = st.session_state.owner

with st.sidebar:
    st.header("Owner")
    owner.name = st.text_input("Owner name", value=owner.name)

    st.header("Add Pet")
    new_pet_name = st.text_input("Pet name")
    new_pet_species = st.text_input("Species")

    if st.button("Add Pet", use_container_width=True):
        if not new_pet_name.strip() or not new_pet_species.strip():
            st.warning("Enter both a name and species.")
        elif owner.find_pet(new_pet_name):
            st.warning("A pet with that name already exists.")
        else:
            owner.add_pet(Pet(new_pet_name.strip(), new_pet_species.strip()))
            st.success(f"Added {new_pet_name.strip()}.")

if not owner.pets:
    st.info("Add a pet from the sidebar to start building a care schedule.")
    st.stop()

pet_name = st.selectbox("Choose pet", [pet.name for pet in owner.pets])
pet = owner.find_pet(pet_name)

left, right = st.columns([1, 1])

with left:
    st.subheader("Add Care Task")

    with st.form("task_form", clear_on_submit=True):
        task_name = st.text_input("Task")
        due_date = st.date_input("Date")
        due_time = st.time_input("Time")
        priority = st.selectbox(
            "Priority",
            [1, 2, 3],
            index=1,
            format_func=lambda p: {1: "1 - High", 2: "2 - Medium", 3: "3 - Low"}[p],
        )
        duration = st.number_input("Duration (minutes)", min_value=1, value=30, step=5)
        recurring = st.selectbox("Recurrence", ["None", "daily", "weekly"])

        submitted = st.form_submit_button("Add Task", use_container_width=True)

        if submitted:
            if not task_name.strip():
                st.warning("Enter a task name.")
            else:
                pet.add_task(
                    Task(
                        name=task_name.strip(),
                        due_at=datetime.combine(due_date, due_time),
                        priority=int(priority),
                        duration_minutes=int(duration),
                        recurring=None if recurring == "None" else recurring,
                    )
                )
                st.success("Task added.")

with right:
    st.subheader("Current Schedule")

    tasks = pet.get_tasks()
    if not tasks:
        st.info("No tasks yet.")
    else:
        for index, task in enumerate(tasks):
            recurring_text = f" • {task.recurring}" if task.recurring else ""
            complete_text = " ✅" if task.completed else ""
            st.markdown(
                f"**{task.due_at:%b %d, %Y %I:%M %p}**  \\"
                f"{task.name}{complete_text} — P{task.priority}, "
                f"{task.duration_minutes} min{recurring_text}"
            )

conflicts = Scheduler.find_conflicts(pet.tasks)

st.divider()
st.subheader("Schedule Analysis")

if conflicts:
    st.error(f"{len(conflicts)} conflict(s) detected.")
    for first, second in conflicts:
        st.write(
            f"⚠️ **{first.name}** ({first.due_at:%I:%M %p}-{first.end_at:%I:%M %p}) "
            f"overlaps **{second.name}** "
            f"({second.due_at:%I:%M %p}-{second.end_at:%I:%M %p})."
        )
else:
    st.success("No active schedule conflicts.")

recurring_tasks = [task for task in pet.tasks if task.recurring]
if recurring_tasks:
    st.subheader("Recurring Task Preview")
    selected = st.selectbox(
        "Recurring task",
        recurring_tasks,
        format_func=lambda task: task.name,
    )
    count = st.slider("Occurrences", 1, 7, 3)
    for item in Scheduler.expand_recurrence(selected, count):
        st.write(f"- {item.due_at:%A, %b %d at %I:%M %p} — {item.name}")
