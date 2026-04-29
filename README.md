# 🗳️ Election Guide AI Assistant

An intelligent, interactive, and unbiased AI chatbot built to help users navigate the Indian election process. Powered by the **Google Gemini API** and built with **Streamlit**, this application provides a modern, ChatGPT-style conversational interface to guide first-time voters and citizens through election timelines, voting registration, and democratic processes.

## ✨ Key Features
* **Advanced AI Intelligence**: Leverages `gemini-2.5-flash` with real-time text streaming to provide fast, beginner-friendly, and politically neutral guidance.
* **🌍 Instant Multilingual Support**: Seamlessly translates and interacts with users in multiple regional languages (Hindi, Telugu, Tamil, Bengali, etc.).
* **🛡️ Myth Buster Mode**: A dedicated fact-checking toggle that forces the AI to rigorously verify political rumors and claims against official Election Commission guidelines.
* **🛠️ Smart Election Tools**: Includes built-in hackathon features like an interactive Election Quiz, a Voting Day Checklist generator, and an AI-driven Voter Application Form Evaluator.
* **ChatGPT-Style Interface**: Seamlessly manage multiple distinct chat threads in a single session.
* **Smart Session Memory**: Built entirely on Streamlit's lightning-fast `session_state`, ensuring instant chat loading and 100% user privacy with zero database overhead.
* **First-Time Voter FAQs**: Quick-action buttons to instantly resolve major issues like missing voter list names, updating ID details, and understanding the NOTA option.

## 🚀 Quick Start
1. Clone the repository
2. Install the required libraries:
   `pip install -r requirements.txt`
3. Set your Google Gemini API key in your system environment variables or inside Streamlit Secrets (`GEMINI_API_KEY`).
4. Run the application:
   `streamlit run app.py`

## 🛠️ Tech Stack
* **Frontend/Backend**: Python & Streamlit
* **AI Model**: Google Gemini API
* **Architecture**: Stateless local session memory (Zero DB architecture)

**Developed by Syed**
