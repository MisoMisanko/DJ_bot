import streamlit as st
import os
import pathlib
from dj_bot import DJBot

# === Load external CSS ===
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/styles.css")
load_css(css_path)

# === Load credentials ===
client_id = os.environ["SPOTIPY_CLIENT_ID"]
client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]

# === Init bot ===
bot = DJBot(client_id=client_id, client_secret=client_secret)

# === State setup ===
if 'step' not in st.session_state:
    st.session_state.step = 'mood'
    st.session_state.response = "Hey! I’m DJ Bot. How are you feeling today? 🎧"
    st.session_state.special_used = False
    st.session_state.general_mood = ''
    st.session_state.emotions = []

if "input" not in st.session_state:
    st.session_state.input = ""

# === Title ===
st.title("🎧 DJ Bot – Your Mood-Based Music Companion")

# === Input form ===
with st.form("chat_form"):
    st.text_input("You:", value=st.session_state.input, label_visibility="collapsed", key="styledinput")
    submitted = st.form_submit_button("Send", use_container_width=False, key="sendbutton")

# === Handle logic ===
def handle_input(text):
    if st.session_state.step == 'mood':
        processed = bot.process_input(text)
        st.session_state.general_mood = processed["general_mood"]
        st.session_state.emotions = processed["emotions"]

        if st.session_state.general_mood == "positive":
            st.session_state.response = "That’s great to hear! 😊 What are you doing right now?"
            st.session_state.step = 'activity'
        else:
            st.session_state.response = "Sorry to hear that 💙 Would you like to stay in that mood or feel better?"
            st.session_state.step = 'intent'

    elif st.session_state.step == 'intent':
        if any(word in text.lower() for word in ['uplift', 'change', 'better', 'happy']):
            st.session_state.general_mood = 'positive'
        elif any(word in text.lower() for word in ['stick', 'stay', 'keep']):
            st.session_state.general_mood = 'negative'
        st.session_state.response = "Got it. What are you doing right now?"
        st.session_state.step = 'activity'

    elif st.session_state.step == 'activity':
        reply = bot.generate_response({
            "general_mood": st.session_state.general_mood,
            "emotions": st.session_state.emotions
        }, context=text)
        st.session_state.response = reply
        st.session_state.step = 'post_playlist'

    elif st.session_state.step == 'post_playlist':
        if 'special' in text.lower() and not st.session_state.special_used:
            st.session_state.response = f"Here’s something truly special I’ve curated just for you: {bot.mini_spotify_wrapped()}"
            st.session_state.special_used = True
        elif 'another' in text.lower():
            st.session_state.step = 'mood'
            st.session_state.response = "Okay! How are you feeling now?"
        elif 'exit' in text.lower():
            st.session_state.response = "Goodbye! Thanks for chatting 🎵"
            st.session_state.step = 'done'
        else:
            st.session_state.response = "Type 'another' for a new playlist, 'special' for your special one, or 'exit'."

# === Execute ===
if submitted and st.session_state.input.strip():
    handle_input(st.session_state.input.strip())
    st.session_state.input = ""

# === Show reply ===
if st.session_state.response:
    st.markdown(f"**DJ Bot:** {st.session_state.response}")
