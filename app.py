import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import uuid
import logging

from utils.llm_utils import check_prompt_safety, generate_response_with_retry
from components.sidebar import render_sidebar

# Configure logging
logger = logging.getLogger(__name__)

# --- Configuration & Setup ---
load_dotenv()

st.set_page_config(
    page_title="Election Guide AI Assistant",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass

if not GEMINI_API_KEY:
    st.error("Missing Gemini API Key. Please set GEMINI_API_KEY in .env or Streamlit Secrets.")
    st.stop()

# --- Gemini Setup ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- Load Initial State ---
if "chats" not in st.session_state:
    st.session_state.chats = {} 

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if st.session_state.current_chat_id is None and not st.session_state.chats:
    new_chat_id = str(uuid.uuid4())
    st.session_state.chats[new_chat_id] = {
        "title": "New Chat",
        "messages": [
            {"role": "assistant", "content": "Hello! I am your Election Guide Assistant. How can I help you understand elections today?"}
        ]
    }
    st.session_state.current_chat_id = new_chat_id

def get_current_messages():
    if st.session_state.current_chat_id and st.session_state.current_chat_id in st.session_state.chats:
        return st.session_state.chats[st.session_state.current_chat_id]["messages"]
    return []

# --- UI: Sidebar ---
selected_language, myth_buster_mode = render_sidebar()

# --- UI: Main Chat Area ---
st.title("Election Guide AI Assistant")

# Inject hidden Semantic HTML and ARIA roles for accessibility screen readers
st.markdown("""
<div aria-live="polite" class="sr-only">
    <header aria-label="Election Guide Header"></header>
    <main aria-label="Main Chat Interface">
        <nav aria-label="Election Navigation and FAQ"></nav>
    </main>
</div>
<style>
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("Ask me anything about the election process, voting, or democracy in India!")

for message in get_current_messages():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input & Processing ---
prompt = st.chat_input("Ask a question...")
if "quick_prompt" in st.session_state:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt

if prompt:
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    if current_chat["title"] == "New Chat":
        chat_title = " ".join(prompt.split()[:5])
        if len(prompt.split()) > 5:
            chat_title += "..."
        current_chat["title"] = chat_title

    with st.chat_message("user"):
        st.markdown(prompt)
    
    current_chat["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Security Check using modular util
        logger.info(f"Checking prompt security...")
        is_safe = check_prompt_safety(prompt, GEMINI_API_KEY)
        if not is_safe:
            st.error("⚠️ Your prompt was flagged for potential policy violations or malicious intent. Please rephrase.")
            st.stop()
        
        SYSTEM_PROMPT = """
        You are an Election Guide Assistant that explains elections in India in a simple, step-by-step, beginner-friendly way. 
        Stay neutral, avoid political bias, and guide users interactively.
        """
        
        if selected_language != "English":
             SYSTEM_PROMPT += f"\nCRITICAL INSTRUCTION: You MUST respond to all user queries exclusively in {selected_language}."
             
        if myth_buster_mode:
             SYSTEM_PROMPT += "\nMYTH BUSTER MODE IS ON: The user will provide a claim or rumor. You must rigorously fact-check it against official Election Commission of India guidelines. State clearly if it is TRUE, FALSE, or MISLEADING, and provide the actual facts."

        history_text = SYSTEM_PROMPT + "\n\nChat History:\n"
        recent_messages = current_chat["messages"][-7:-1] if len(current_chat["messages"]) > 6 else current_chat["messages"][:-1]
        for msg in recent_messages: 
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
        
        full_prompt = history_text + f"User: {prompt}\nAssistant:"

        try:
            # Use modular generate_response_with_retry
            logger.info("Generating response...")
            response_stream = generate_response_with_retry(model, full_prompt)
            full_response = ""
            
            for chunk in response_stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            current_chat["messages"].append({"role": "assistant", "content": full_response})
            
            if current_chat["title"] != "New Chat" and len(current_chat["messages"]) == 3: 
                st.rerun()

        except Exception as e:
            logger.error(f"API Error during response generation: {e}")
            error_msg = f"Sorry, I encountered an error: {e}"
            message_placeholder.error(error_msg)
