import streamlit as st
from transformers import pipeline

# --- Initialize the text-to-text generator ---
generator = pipeline("text2text-generation", model="google/flan-t5-small")

# --- Planner agent ---
def planner_agent(task):
    prompt = f"Planner: Create a clear 3-step plan for this task: {task}"
    result = generator(prompt, max_new_tokens=100)
    return result[0]['generated_text']

# --- Executor agent ---
def executor_agent(plan):
    prompt = f"Executor: Execute this plan step by step: {plan}"
    result = generator(prompt, max_new_tokens=100)
    return result[0]['generated_text']

# --- Streamlit UI ---
st.set_page_config(page_title="Planner & Executor Chat", page_icon="🤖")
st.title("🤖 Interactive Agent Chat Demo")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box for task
task = st.text_input("Enter a task for the agents:")

if st.button("Start Conversation") and task:
    # Planner generates a plan
    planner_msg = planner_agent(task)
    st.session_state.chat_history.append(f"Planner: {planner_msg}")

    # Executor executes the plan
    executor_msg = executor_agent(planner_msg)
    st.session_state.chat_history.append(f"Executor: {executor_msg}")

# Display chat history
for msg in st.session_state.chat_history:
    st.text(msg)
