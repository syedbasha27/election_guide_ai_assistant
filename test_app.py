import pytest
from streamlit.testing.v1 import AppTest
from unittest.mock import patch

def test_app_loads():
    at = AppTest.from_file("app.py")
    at.secrets["GEMINI_API_KEY"] = "mock_key"
    at.run(timeout=10)
    assert not at.exception
    assert at.title[0].value == "Election Guide AI Assistant"

def test_language_selection():
    at = AppTest.from_file("app.py")
    at.secrets["GEMINI_API_KEY"] = "mock_key"
    at.run(timeout=10)
    
    at.selectbox[0].set_value("Hindi").run(timeout=10)
    assert at.selectbox[0].value == "Hindi"

def test_myth_buster_toggle():
    at = AppTest.from_file("app.py")
    at.secrets["GEMINI_API_KEY"] = "mock_key"
    at.run(timeout=10)
    
    at.toggle[0].set_value(True).run(timeout=10)
    assert at.toggle[0].value == True

def test_faq_button_clicks():
    at = AppTest.from_file("app.py")
    at.secrets["GEMINI_API_KEY"] = "mock_key"
    at.run(timeout=10)
    
    # Click "I am a First-Time Voter"
    at.button[1].click().run(timeout=10) # Button 0 is New Chat, Button 1 is the first FAQ
    
    # After click, quick_prompt should be set and prompt handled
    # We just ensure it doesn't crash
    assert not at.exception
