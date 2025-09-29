import streamlit as st
import random

# Agents
def planner_agent(task, chat_history):
    ideas = [
        f"I think the steps for '{task}' are: 1) Break it down, 2) Work step by step.",
        f"To accomplish '{task}', first organize, then execute.",
        f"Let's tackle '{task}' by planning the easiest part first."
    ]
    return random.choice(ideas)

def executor_agent(plan, chat_history):
    actions = [
        f"Executing this plan: {plan}. Done ✅",
        f"Following the plan for '{plan}' carefully.",
        f"I've completed the steps for '{plan}'."
    ]
    return random.choice(actions)

# Streamlit UI
st.title("Mini Sentient-Style Chat Demo")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

task = st.text_input("Enter a task for the agents:")

if st.button("Send") and task:
    planner_msg = planner_agent(task, st.session_state.chat_history)
    st.session_state.chat_history.append(f"Planner: {planner_msg}")

    executor_msg = executor_agent(planner_msg, st.session_state.chat_history)
    st.session_state.chat_history.append(f"Executor: {executor_msg}")

# Display chat history
for msg in st.session_state.chat_history:
    st.text(msg)
