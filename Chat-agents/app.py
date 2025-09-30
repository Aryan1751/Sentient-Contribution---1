import streamlit as st
from transformers import pipeline

# CPU-friendly model
generator = pipeline("text-generation", model="gpt2")

def planner_agent(task):
    prompt = f"Planner: Break down this task into steps:\nTask: {task}"
    output = generator(prompt, max_new_tokens=50, do_sample=True, temperature=0.7)
    return output[0]["generated_text"].replace(prompt, "").strip()

def executor_agent(plan):
    prompt = f"Executor: Follow these steps and provide instructions:\n{plan}"
    output = generator(prompt, max_new_tokens=50, do_sample=True, temperature=0.7)
    return output[0]["generated_text"].replace(prompt, "").strip()

st.set_page_config(page_title="🤖 Two Agents Demo", page_icon="🤖")
st.title("🤖 Planner & Executor Demo")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

task = st.text_input("Enter a task for the agents:")

if st.button("Start Conversation") and task:
    planner_msg = planner_agent(task)
    st.session_state.chat_history.append(f"Planner:\n{planner_msg}")

    executor_msg = executor_agent(planner_msg)
    st.session_state.chat_history.append(f"Executor:\n{executor_msg}")

for msg in st.session_state.chat_history:
    st.text(msg)
