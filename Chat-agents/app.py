import streamlit as st
import random

# --------- Agents ---------

def planner_agent(task, chat_history):
    """Generates a plan for the given task."""
    ideas = [
        f"Break down '{task}' into smaller steps and handle them one by one.",
        f"To accomplish '{task}', first organize resources, then start execution.",
        f"Plan for '{task}': focus on easiest parts first, then move to harder ones."
    ]
    return random.choice(ideas)

def executor_agent(plan, chat_history):
    """Executes the plan and returns a readable response."""
    # Extract the task from Planner message
    if "'" in plan:
        try:
            task = plan.split("'")[1]  # gets the text inside the first pair of quotes
        except IndexError:
            task = plan
    else:
        task = plan

    actions = [
        f"Executing '{task}'… ✅ Done!",
        f"I've completed the task '{task}' successfully!",
        f"Task '{task}' is finished. All steps executed."
    ]
    return random.choice(actions)

# --------- Streamlit UI ---------

st.set_page_config(page_title="Mini Sentient Chat", page_icon="🤖")
st.title("🤖 Mini Sentient-Style Chat Demo")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Input box
task = st.text_input("Enter a task for the agents:")

if st.button("Send") and task:
    # Planner generates a plan
    planner_msg = planner_agent(task, st.session_state.chat_history)
    st.session_state.chat_history.append(f"Planner: {planner_msg}")

    # Executor responds to the plan
    executor_msg = executor_agent(planner_msg, st.session_state.chat_history)
    st.session_state.chat_history.append(f"Executor: {executor_msg}")

# Display chat history
for msg in st.session_state.chat_history:
    st.text(msg)
