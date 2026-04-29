import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import uuid

# --- Configuration & Setup ---

# Load environment variables from .env file (if present)
load_dotenv()

# Streamlit Page Config
st.set_page_config(
    page_title="Election Guide AI Assistant",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Retrieve keys from environment variables or Streamlit secrets
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

SYSTEM_PROMPT = """
You are an Election Guide Assistant that explains elections in India in a simple, 
step-by-step, beginner-friendly way. Stay neutral, avoid political bias, and guide users interactively.
"""

# --- Load Initial State ---
# Store all chats in memory for this session
if "chats" not in st.session_state:
    st.session_state.chats = {} # chat_id -> {"title": str, "messages": list}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# Create a default chat if none exists
if st.session_state.current_chat_id is None and not st.session_state.chats:
    new_chat_id = str(uuid.uuid4())
    st.session_state.chats[new_chat_id] = {
        "title": "New Chat",
        "messages": [
            {"role": "assistant", "content": "Hello! I am your Election Guide Assistant. How can I help you understand elections today?"}
        ]
    }
    st.session_state.current_chat_id = new_chat_id

# Function to get messages for current chat
def get_current_messages():
    if st.session_state.current_chat_id and st.session_state.current_chat_id in st.session_state.chats:
        return st.session_state.chats[st.session_state.current_chat_id]["messages"]
    return []

# --- UI: Sidebar ---
with st.sidebar:
    st.title("🗳️ Election Guide")
    
    # Chat History Section
    if st.button("➕ New Chat", use_container_width=True):
        new_chat_id = str(uuid.uuid4())
        st.session_state.chats[new_chat_id] = {
            "title": "New Chat",
            "messages": [
                {"role": "assistant", "content": "Hello! I am your Election Guide Assistant. How can I help you understand elections today?"}
            ]
        }
        st.session_state.current_chat_id = new_chat_id
        st.rerun()
        
    st.subheader("Recent Chats")
    
    # List chats
    if not st.session_state.chats:
         st.caption("No recent chats.")
    else:
        for chat_id, chat_data in reversed(list(st.session_state.chats.items())):
            # Highlight the currently active chat
            is_active = (st.session_state.current_chat_id == chat_id)
            button_label = f"💬 {chat_data['title']}"
            if is_active:
                button_label = f"🟢 {chat_data['title']}"
                
            if st.button(button_label, key=chat_id, use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.rerun()

    st.divider()
    st.subheader("Quick Topics")
    if st.button("First-time voter guide"):
        st.session_state.quick_prompt = "I am a first-time voter. Can you guide me step-by-step?"
    if st.button("How to register to vote?"):
        st.session_state.quick_prompt = "How do I register to vote in India?"
    if st.button("What is EVM and VVPAT?"):
        st.session_state.quick_prompt = "Explain EVM and VVPAT simply."

# --- UI: Main Chat Area ---
st.title("Election Guide AI Assistant")
st.markdown("Ask me anything about the election process, voting, or democracy in India!")

# Display chat messages from history on app rerun
for message in get_current_messages():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input & Processing ---
# Check if a quick prompt was clicked in the sidebar
prompt = st.chat_input("Ask a question...")
if "quick_prompt" in st.session_state:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt

if prompt:
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    # Update title if it's the first user message
    if current_chat["title"] == "New Chat":
        chat_title = " ".join(prompt.split()[:5])
        if len(prompt.split()) > 5:
            chat_title += "..."
        current_chat["title"] = chat_title
        # Sidebar will automatically reflect title change on rerun or next interactions

    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Add User Message to Session State
    current_chat["messages"].append({"role": "user", "content": prompt})

    # 3. Generate AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Build context for Gemini
        history_text = SYSTEM_PROMPT + "\n\nChat History:\n"
        for msg in current_chat["messages"][:-1]: # exclude the latest prompt
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
        
        full_prompt = history_text + f"User: {prompt}\nAssistant:"

        try:
            with st.spinner("Thinking..."):
                response = model.generate_content(full_prompt)
                ai_response = response.text
                message_placeholder.markdown(ai_response)
                
                # 4. Add AI Message to Session State
                current_chat["messages"].append({"role": "assistant", "content": ai_response})
                
                # If the title changed, rerun to update sidebar immediately
                if current_chat["title"] != "New Chat" and len(current_chat["messages"]) == 3: # 1 welcome, 1 user, 1 assistant
                    st.rerun()

        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {e}"
            message_placeholder.error(error_msg)
