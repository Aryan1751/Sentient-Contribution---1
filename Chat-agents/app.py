import streamlit as st
from transformers import pipeline

# Initialize text-generation pipeline with a small HF model
generator = pipeline("text-generation", model="bigscience/bloom-560m")

# Planner agent
def planner_agent(task):
    prompt = f"Planner: Break down this task into clear steps:\nTask: {task}"
    output = generator(prompt, max_new_tokens=100, do_sample=True, temperature=0.5)
    return output[0]["generated_text"].strip()

# Executor agent
def executor_agent(plan):
    prompt = f"Executor: Follow these steps and provide instructions:\n{plan}"
    output = generator(prompt, max_new_tokens=100, do_sample=True, temperature=0.5)
    return output[0]["generated_text"].strip()

# Streamlit UI
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

# Display chat history
for msg in st.session_state.chat_history:
    st.text(msg)
