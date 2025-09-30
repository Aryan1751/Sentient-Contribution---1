import streamlit as st
import requests

# --- Hugging Face Inference API setup ---
API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Free model, no download
HEADERS = {"Authorization": "Bearer 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"}  # Replace with your HF token

def query_hf(prompt):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 100}}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# --- Streamlit UI ---
st.set_page_config(page_title="Cloud Agent Chat", page_icon="🤖")
st.title("🤖 Cloud Agent Chat Demo")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

task = st.text_input("Enter a task for the agents:")

if st.button("Start Conversation") and task:
    # Planner generates a plan
    planner_prompt = f"Plan the task: {task}"
    planner_msg = query_hf(planner_prompt)
    st.session_state.chat_history.append(f"Planner: {planner_msg}")

    # Executor executes the plan
    executor_prompt = f"Execute the plan: {planner_msg}"
    executor_msg = query_hf(executor_prompt)
    st.session_state.chat_history.append(f"Executor: {executor_msg}")

# Show chat history
for msg in st.session_state.chat_history:
    st.text(msg)
