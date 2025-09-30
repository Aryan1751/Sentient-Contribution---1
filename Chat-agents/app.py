# app.py
import streamlit as st
from transformers import pipeline
import re
import time

# -------------------------
# Configuration
# -------------------------
MODEL_NAME = "google/flan-t5-small"  # small, cloud-friendly text2text model
ROUNDS = 4                          # how many back-and-forth turns to run
PLANNER_MAX_TOKENS = 80
EXECUTOR_MAX_TOKENS = 80

# -------------------------
# Initialize generator
# -------------------------
# We use text2text pipeline because flan-t5-small is text-to-text.
# do_sample + top_p reduces robotic repetition.
generator = pipeline(
    "text2text-generation",
    model=MODEL_NAME,
    do_sample=True,
    top_p=0.9,
)

# -------------------------
# Helper functions
# -------------------------
def clean_output(text: str, max_words: int = 120) -> str:
    """
    Simple post-processing:
    - Collapse repeating phrases (naive)
    - Trim to a reasonable length
    - Remove duplicated long fragments
    """
    if not text:
        return ""

    # Replace newlines with spaces
    s = re.sub(r"\s+", " ", text).strip()

    # Remove obvious repeated substrings like "foo foo foo"
    # Collapse groups of three or more repeats of the same token
    tokens = s.split()
    cleaned_tokens = []
    for t in tokens:
        if len(cleaned_tokens) >= 3 and t == cleaned_tokens[-1] == cleaned_tokens[-2] == cleaned_tokens[-3]:
            # skip extra repeated token
            continue
        cleaned_tokens.append(t)
    s = " ".join(cleaned_tokens)

    # Remove repeated long fragments (simple approach)
    # If the last half of the text equals the prior half, keep only first half
    mid = len(s) // 2
    if len(s) > 80:
        first = s[:mid].strip()
        second = s[mid:].strip()
        if first.endswith(second[:20]) or second.startswith(first[-20:]):
            s = first

    # Trim to max words
    words = s.split()
    if len(words) > max_words:
        s = " ".join(words[:max_words]) + " …"

    return s

def planner_agent(task: str) -> str:
    """
    Planner: create a short structured plan.
    We instruct the model to produce numbered steps.
    """
    prompt = (
        f"Planner: Create a concise 3-step plan (numbered) for this task. "
        f"Be explicit and short. Task: {task}"
    )
    out = generator(prompt, max_new_tokens=PLANNER_MAX_TOKENS)[0]["generated_text"]
    return clean_output(out, max_words=120)

def executor_agent(plan: str, step_hint: str = "") -> str:
    """
    Executor: produce a short, non-repetitive execution response for the given plan.
    Optionally a step_hint can be passed so executor can act on a particular step.
    """
    if step_hint:
        prompt = (
            f"Executor: You are executing a specific step. Follow this instruction concisely and say what you did: {step_hint}. "
            f"Plan summary: {plan}"
        )
    else:
        prompt = (
            f"Executor: Summarize what was executed for the plan in clear short sentences. "
            f"Plan summary: {plan}"
        )
    out = generator(prompt, max_new_tokens=EXECUTOR_MAX_TOKENS)[0]["generated_text"]
    return clean_output(out, max_words=120)

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Planner ⇄ Executor — Mini Agents", page_icon="🤖", layout="centered")
st.title("🤖 Planner ↔ Executor — Mini Agent Demo")

st.markdown(
    "Type a task, hit **Start Conversation**, and watch two agents (Planner and Executor) chat for a few turns."
)

if "chat" not in st.session_state:
    st.session_state.chat = []  # list of (role, text)

# Input row
with st.form("task_form", clear_on_submit=False):
    task_input = st.text_input("Enter a task for the agents:", key="task_input")
    submitted = st.form_submit_button("Start Conversation")

if submitted and task_input:
    # Clear previous chat for a fresh run
    st.session_state.chat = []
    st.session_state.chat.append(("system", f"Task: {task_input}"))

    # Run several back-and-forth rounds
    last_planner_text = ""
    for turn in range(ROUNDS):
        # Planner turn (uses full task for the first round, then may reference last exchange)
        planner_prompt_input = task_input if turn == 0 else f"{task_input} (previous exchange: {last_planner_text})"
        planner_msg = planner_agent(planner_prompt_input)
        st.session_state.chat.append(("Planner", planner_msg))

        # Executor turn
        # Optionally executor can run on a single step; we try to pick a short hint (first line or sentence)
        step_hint = ""
        # try extract first sentence or first line as a hint:
        if "." in planner_msg:
            step_hint = planner_msg.split(".")[0].strip()
        elif "\n" in planner_msg:
            step_hint = planner_msg.split("\n")[0].strip()
        else:
            step_hint = planner_msg[:120].strip()

        executor_msg = executor_agent(planner_msg, step_hint)
        st.session_state.chat.append(("Executor", executor_msg))

        # small pause for UX (in deployed app this just makes it feel live)
        time.sleep(0.2)

        # Keep last planner text for next round context
        last_planner_text = planner_msg

# Render chat nicely
for role, text in st.session_state.chat:
    if role == "Planner":
        st.markdown(f"**Planner:** {text}")
    elif role == "Executor":
        st.markdown(f"**Executor:** {text}")
    else:
        st.info(text)
