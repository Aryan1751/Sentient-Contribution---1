import streamlit as st
from huggingface_hub import InferenceClient

HF_TOKEN = "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"
client = InferenceClient(token=HF_TOKEN)

st.set_page_config(page_title="🤖 Two Agents Demo", page_icon="🤖")
st.title("🤖 Planner & Executor Demo")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def planner_agent(task):
    prompt = f"Planner: Break down this task into steps:\nTask: {task}"
    response = client.text_generation(
        model="bigscience/bloom-560m",
        inputs=prompt,
        max_new_tokens=50
    )
    return response.generated_text.strip()

def executor_agent(plan):
    prompt = f"Executor: Follow these steps and provide instructions:\n{plan}"
    response = client.text_generation(
        model="bigscience/bloom-560m",
        inputs=prompt,
        max_new_tokens=50
    )
    return response.generated_text.strip()

task = st.text_input("Enter a task for the agents:")

if st.button("Start Conversation") and task:
    planner_msg = planner_agent(task)
    st.session_state.chat_history.append(f"Planner:\n{planner_msg}")

    executor_msg = executor_agent(planner_msg)
    st.session_state.chat_history.append(f"Executor:\n{executor_msg}")

for msg in st.session_state.chat_history:
    st.text(msg)
