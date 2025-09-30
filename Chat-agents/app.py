# app.py
import streamlit as st
from huggingface_hub import InferenceClient

# --- Hugging Face API setup ---
HF_TOKEN = "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"
MODEL_NAME = "MODEL_NAME = "tiiuae/falcon-7b-instruct"
client = InferenceClient(model=MODEL_NAME, token=HF_TOKEN)

# --- Planner agent ---
def planner_agent(task):
    prompt = f"You are a planner. Break down the following task into 3 numbered steps, clearly and concisely:\nTask: {task}"
    response = client.text_generation(prompt, max_new_tokens=150, temperature=0.3)
    return response.strip()

# --- Executor agent ---
def executor_agent(plan):
    prompt = f"You are an executor. For each step below, provide a practical, actionable explanation:\n{plan}"
    response = client.text_generation(prompt, max_new_tokens=200, temperature=0.3)
    return response.strip()

# --- Streamlit UI ---
st.set_page_config(page_title="🤖 Two Agents Demo", page_icon="🤖")
st.title("🤖 Interactive Planner & Executor Demo")

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

