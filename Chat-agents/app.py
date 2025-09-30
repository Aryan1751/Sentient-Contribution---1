import streamlit as st
from transformers import pipeline

# --- Initialize text generator ---
generator = pipeline("text-generation", model="distilgpt2")

# --- Planner agent ---
def planner_agent(task):
    prompt = f"Planner, make a plan for this task: {task}"
    result = generator(prompt, max_new_tokens=50)
    return result[0]['generated_text']

# --- Executor agent ---
def executor_agent(plan):
    prompt = f"Executor, follow this plan: {plan}"
    result = generator(prompt, max_new_tokens=50)
    return result[0]['generated_text']

# --- Streamlit UI ---
st.set_page_config(page_title="Cloud Agent Chat", page_icon="🤖")
st.title("🤖 Planner & Executor Chat Demo")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

task = st.text_input("Enter a task for the agents:")

if st.button("Start Conversation") and task:
    planner_msg = planner_agent(task)
    st.session_state.chat_history.append(f"Planner: {planner_msg}")

    executor_msg = executor_agent(planner_msg)
    st.session_state.chat_history.append(f"Executor: {executor_msg}")

# Display chat history
for msg in st.session_state.chat_history:
    st.text(msg)
