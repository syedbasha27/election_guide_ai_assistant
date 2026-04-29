# 🗳️ Election Guide AI Assistant

An intelligent, interactive, and unbiased AI chatbot built to help users navigate the Indian election process. Powered by the **Google Gemini API** and built with **Streamlit**, this application provides a modern, Gemini-style conversational interface to guide first-time voters and citizens through election timelines, voting registration, and democratic processes.

## ✨ Features
* **Gemini-Powered Intelligence**: Leverages `gemini-2.5-flash` to provide fast, beginner-friendly, and politically neutral guidance.
* **ChatGPT-Style Interface**: Seamlessly manage multiple distinct chat threads in a single session.
* **Smart Session Memory**: Built entirely on Streamlit's lightning-fast `session_state`, ensuring instant chat loading and 100% user privacy with zero database overhead.
* **Auto-Generating Titles**: Dynamically creates chat thread titles based on your first question.
* **Quick Prompts**: One-click buttons to instantly ask common questions (e.g., "First-time voter guide", "Explain EVM and VVPAT").

## 🚀 Quick Start
1. Clone the repository
2. Install the required libraries:
   `pip install -r requirements.txt`
3. Set your Google Gemini API key in your system environment variables (`GEMINI_API_KEY`).
4. Run the application:
   `streamlit run app.py`

## 🛠️ Tech Stack
* **Frontend/Backend**: Python & Streamlit
* **AI Model**: Google Gemini API
