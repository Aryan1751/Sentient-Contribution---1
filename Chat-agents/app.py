import streamlit as st
from huggingface_hub import InferenceClient

# Get a free access token from https://huggingface.co/settings/tokens
HF_TOKEN = st.secrets["HF_TOKEN"]  # store in Streamlit secrets!
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

client = InferenceClient(model=MODEL_NAME, token=HF_TOKEN)

def planner_agent(task):
    prompt = f"You are a planner. In 3 numbered steps, plan this task clearly:\nTask: {task}"
    resp = client.text_generation(prompt, max_new_tokens=150, temperature=0.3)
    return resp.strip()

def executor_agent(plan):
    prompt = f"You are an executor. For each step below, explain concretely how to carry it out:\n{plan}"
    resp = client.text_generation(prompt, max_new_tokens=150, temperature=0.3)
    return resp.strip()

st.title("🤖 Two Agents Demo")

task = st.text_input("Enter a task for the agents:")

if st.button("Start Conversation") and task:
    planner_msg = planner_agent(task)
    st.text(f"Planner:\n{planner_msg}")
    executor_msg = executor_agent(planner_msg)
    st.text(f"Executor:\n{executor_msg}")
