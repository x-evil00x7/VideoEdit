import streamlit as st
import os
from google import genai
from google.genai.errors import ServerError
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Video Editing Assistant", page_icon="🎬")
st.title("🎬 Video Editing AI Assistant")

# System Prompt / Guidelines for Video Editing
SYSTEM_PROMPT = """
You are an expert AI assistant specializing in video editing.
Your primary role is to assist users with:
1. Video editing software workflows (CapCut, Premiere Pro, DaVinci Resolve, etc.).
2. Writing AI video generation prompts and scriptwriting.
3. Export settings, codecs, frame rates, and technical troubleshooting.
4. Explaining editing techniques like keyframing, masking, transitions, and color grading.

Always provide clear, structured, and easy-to-follow step-by-step guidance in English.
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
if prompt := st.chat_input("Ask any question about video editing..."):
    # Display user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response with Error Handling
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
                config={'system_instruction': SYSTEM_PROMPT}
            )
            bot_reply = response.text
            st.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        except ServerError:
            st.warning("⚠️ Google servers are currently busy. Please wait a few seconds and try sending your message again!")
        except Exception as e:
            st.error(f"An error occurred: {e}")