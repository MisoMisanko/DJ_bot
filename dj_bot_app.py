import streamlit as st
import os
import pathlib
from dj_bot import DJBot

# === Spotify credentials ===
client_id = os.environ["SPOTIPY_CLIENT_ID"]
client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]

# === Init bot ===
bot = DJBot(client_id=client_id, client_secret=client_secret)

# === Session state ===
if 'step' not in st.session_state:
    st.session_state.step = 'mood'
    st.session_state.mood = ''
    st.session_state.context = ''
    st.session_state.general_mood = ''
    st.session_state.emotions = []
    st.session_state.special_used = False
    st.session_state.response = "Hey! I’m DJ Bot. How are you feeling today? 🎧"

if "input" not in st.session_state:
    st.session_state.input = ""

def load_css(css_file):
    css_path = pathlib.Path(css_file)
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ CSS file not found.")

load_css("assets/styles.css")

# === Title ===
st.title("🎧 DJ Bot – Your Mood-Based Music Companion")

# === Logic handler ===

def handle_input():
    user_input = st.session_state.styledinput
    if not user_input:
        return

    if st.session_state.step == 'mood':
        processed = bot.process_input(user_input)
        st.session_state.general_mood = processed["general_mood"]
        st.session_state.emotions = processed["emotions"]

        if st.session_state.general_mood == "positive":
            st.session_state.response = "That’s great to hear! 😊 What are you doing right now?"
            st.session_state.step = 'activity'
        else:
            st.session_state.response = "Sorry to hear that 💙 Would you like to stay in that mood or feel better?"
            st.session_state.step = 'intent'

    elif st.session_state.step == 'intent':
        if any(word in user_input.lower() for word in ['uplift', 'change', 'better', 'happy']):
            st.session_state.general_mood = 'positive'
        elif any(word in user_input.lower() for word in ['stick', 'stay', 'keep']):
            st.session_state.general_mood = 'negative'
        st.session_state.response = "Got it. What are you doing right now?"
        st.session_state.step = 'activity'

    elif st.session_state.step == 'activity':
        st.session_state.context = user_input
        reply = bot.generate_response({
            "general_mood": st.session_state.general_mood,
            "emotions": st.session_state.emotions
        }, context=st.session_state.context)
        st.session_state.response = reply
        st.session_state.step = 'post_playlist'

    elif st.session_state.step == 'post_playlist':
        if 'special' in user_input.lower() and not st.session_state.special_used:
            wrapped_link = bot.mini_spotify_wrapped()
            st.session_state.response = f"Here’s something truly special I’ve curated just for you: {wrapped_link}"
            st.session_state.special_used = True
        elif 'another' in user_input.lower():
            st.session_state.step = 'mood'
            st.session_state.response = "Okay! How are you feeling now?"
        elif 'exit' in user_input.lower():
            st.session_state.response = "Goodbye! Thanks for chatting 🎵"
            st.session_state.step = 'done'
        else:
            st.session_state.response = "Type 'another' for a new playlist, 'special' for your special one, or 'exit'."

    # Clear input after handling
    st.session_state["styledinput"] = ""

# === Input field ===
with st.form("chat_form", clear_on_submit=True):
    st.text_input("You:", label_visibility="collapsed", key="styledinput")
    submitted = st.form_submit_button("Send")

if submitted:
    handle_input()


# === Output ===
if st.session_state.response:
    st.markdown(f"**DJ Bot:** {st.session_state.response}")
