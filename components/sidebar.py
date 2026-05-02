import streamlit as st
import uuid

def render_sidebar():
    """Renders the sidebar UI components."""
    with st.sidebar:
        st.title("🗳️ Election Guide")
        st.divider()
        
        # FEATURE 1: Multilingual Support
        st.subheader("🌍 Language Settings")
        selected_language = st.selectbox(
            "Choose your language:",
            ["English", "Hindi", "Telugu", "Tamil", "Bengali", "Marathi", "Gujarati", "Urdu"],
            help="Select your preferred language for the AI Assistant's responses. All answers will be translated automatically."
        )
        
        # FEATURE 2: Myth Buster Mode
        st.subheader("🛡️ Fact-Checking Mode")
        myth_buster_mode = st.toggle("Enable Myth Buster", help="Turn this on to rigorously verify claims or rumors about the election.")
        st.divider()

        # Chat History Section
        if st.button("➕ New Chat", use_container_width=True, help="Start a new, fresh conversation."):
            new_chat_id = str(uuid.uuid4())
            welcome_msg = f"Hello! I am ready to help you in {selected_language}." if selected_language != "English" else "Hello! I am your Election Guide Assistant. How can I help you understand elections today?"
            st.session_state.chats[new_chat_id] = {
                "title": "New Chat",
                "messages": [{"role": "assistant", "content": welcome_msg}]
            }
            st.session_state.current_chat_id = new_chat_id
            st.rerun()
            
        st.subheader("Recent Chats")
        if not st.session_state.chats:
             st.caption("No recent chats.")
        else:
            for chat_id, chat_data in reversed(list(st.session_state.chats.items())):
                is_active = (st.session_state.current_chat_id == chat_id)
                button_label = f"🟢 {chat_data['title']}" if is_active else f"💬 {chat_data['title']}"
                if st.button(button_label, key=chat_id, use_container_width=True):
                    st.session_state.current_chat_id = chat_id
                    st.rerun()

        st.divider()
        st.subheader("💡 Most Common FAQs")
        if st.button("I am a First-Time Voter", help="Get a complete beginner's guide on registering and voting."):
             st.session_state.quick_prompt = "I am a first-time voter. Can you give me a complete beginner's guide on what I need to do from registration to voting?"
        if st.button("Name missing from Voter List?", help="Steps to fix issues with your voter registration."):
             st.session_state.quick_prompt = "My name was removed or is missing from the voter list! What exact steps can I take to fix this and ensure I can vote?"
        if st.button("How to update Voter ID details?", help="Correct mistakes on your voter ID card."):
             st.session_state.quick_prompt = "There is a mistake on my Voter ID card (like spelling or address). How do I correct or update my details?"
        if st.button("Voting from another city?", help="Understand rules for voting outside your home constituency."):
             st.session_state.quick_prompt = "I live in a different city for work/studies. How can I cast my vote without traveling back to my home constituency?"
        if st.button("What is the NOTA option?", help="Learn about the 'None of the Above' voting option."):
             st.session_state.quick_prompt = "What exactly is the NOTA (None of the Above) option on the EVM, and what happens if NOTA gets the highest number of votes?"

        st.divider()
        st.subheader("🛠️ Smart Election Tools")
        
        if st.button("📄 Verify My Application", help="Have the AI evaluate if your voter registration documents will be accepted."):
             st.session_state.quick_prompt = "I want to apply for a voter ID. Act as an Application Evaluator. Ask me for my age, citizenship, and the documents I have, and evaluate if my application will be accepted."
        if st.button("📅 Generate Voting Checklist", help="Get a complete list of things to bring to the polling booth."):
             st.session_state.quick_prompt = "Provide a comprehensive Voting Day Checklist. What do I need to bring to the polling booth, what are the timings, and what is prohibited?"
        if st.button("🎮 Take a Quiz", help="Test your knowledge of the Indian election process."):
             st.session_state.quick_prompt = "Give me a quick 3-question multiple-choice quiz about Indian election rules and EVMs. Wait for my answer before revealing the correct ones."

        st.divider()
        st.subheader("🗺️ Find Polling Booths")
        city = st.text_input("Enter your city to find nearby booths:")
        if city:
            maps_url = f"https://www.google.com/maps?q=polling+booths+in+{city.replace(' ', '+')}&output=embed"
            st.components.v1.iframe(maps_url, height=300)

        st.divider()
        st.markdown("<div style='text-align: center; color: gray; font-size: 0.9em; margin-top: 20px;'>Developed by <b>Syed</b></div>", unsafe_allow_html=True)
        
    return selected_language, myth_buster_mode
