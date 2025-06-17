import streamlit as st
import os
import pathlib
import random
from dj_bot import DJBot

# === Spotify credentials ===
client_id = os.environ["SPOTIPY_CLIENT_ID"]
client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]

# === Init bot ===
bot = DJBot(client_id=client_id, client_secret=client_secret)

# === Load external CSS ===
def load_css(css_file):
    css_path = pathlib.Path(css_file)
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/styles.css")

# === Session state ===
if 'step' not in st.session_state:
    st.session_state.step = 'mood'
    st.session_state.response = "Hey! I’m DJ Bot. How are you feeling today? 🎧"
    st.session_state.general_mood = ''
    st.session_state.emotions = []
    st.session_state.context = ''
    st.session_state.special_used = False

if "styledinput" not in st.session_state:
    st.session_state.styledinput = ""

# === Mood responses ===
emotion_responses = {
    "happy": [
        "That's wonderful to hear! 😊",
        "Yay! I'm glad you're feeling happy! 🎉",
        "Happiness suits you! 😄"
    ],
    "excited": [
        "Whoa, I can feel your energy from here! 🤩",
        "Let’s channel that excitement into some music! 🚀",
        "So much hype, I love it! 🔥"
    ],
    "calm": [
        "Peaceful vibes incoming. 🧘",
        "Let’s keep it nice and mellow. 🌿",
        "Staying zen — I like it. 🕊️"
    ],
    "sad": [
        "I'm sorry you're feeling down. 💙",
        "Let's find something to match or uplift your mood. 😔",
        "I’m here with you. 💫"
    ],
    "angry": [
        "Sounds like you need a release. 💥",
        "Let’s find something to help blow off steam. 🔥",
        "Deep breaths — and loud music? 😤"
    ],
    "stressed": [
        "Overwhelmed? Let’s unwind together. 💆",
        "We got this. 🎵",
        "Breathe in... music out. 🎧"
    ],
    "default": [
        "I feel you. Let’s vibe it out. ✨",
        "Got it — I’ve got a playlist for this. 🎶",
        "Let’s dive in with the right tracks. 💫"
    ]
}

# === Logic handler ===
def handle_input():
    user_input = st.session_state.styledinput.strip().lower()
    if not user_input:
        return

    # --- Special commands available globally ---
    if user_input == "special" and not st.session_state.special_used:
        st.session_state.response = f"Here’s something truly special I’ve curated just for you: {bot.mini_spotify_wrapped()}"
        st.session_state.special_used = True
        st.session_state.styledinput = ""
        return

    elif user_input == "exit":
        st.session_state.response = "Goodbye! Thanks for chatting 🎵"
        st.session_state.step = 'done'
        st.session_state.styledinput = ""
        return

    # --- Conversation flow ---
    if st.session_state.step == 'mood':
        processed = bot.process_input(user_input)
        st.session_state.general_mood = processed["general_mood"]
        st.session_state.emotions = processed["emotions"]

        mood_key = st.session_state.emotions[0] if st.session_state.emotions else "default"
        mood_message = random.choice(emotion_responses.get(mood_key, emotion_responses["default"]))
        st.session_state.response = f"{mood_message} What are you doing right now?"
        st.session_state.step = 'activity'

    elif st.session_state.step == 'activity':
        st.session_state.context = user_input
        playlist = bot.generate_response({
            "general_mood": st.session_state.general_mood,
            "emotions": st.session_state.emotions
        }, context=st.session_state.context)

        followup = "Type 'another' for a new playlist, 'special' for your special one, or 'exit'."
        st.session_state.response = f"{playlist}\n\n{followup}"
        st.session_state.step = 'post_playlist'

    elif st.session_state.step == 'post_playlist':
        if 'another' in user_input:
            st.session_state.step = 'mood'
            st.session_state.response = "Okay! How are you feeling now?"
        elif 'special' in user_input and not st.session_state.special_used:
            st.session_state.response = f"Here’s something truly special I’ve curated just for you: {bot.mini_spotify_wrapped()}"
            st.session_state.special_used = True
        elif 'exit' in user_input:
            st.session_state.response = "Goodbye! Thanks for chatting 🎵"
            st.session_state.step = 'done'
        else:
            st.session_state.response = "Type 'another' for a new playlist, 'special' for your special one, or 'exit'."

    # --- Clear input field ---
    st.session_state.styledinput = ""

# === UI ===
st.title("🎧 DJ Bot – Your Mood-Based Music Companion")

st.text_input(
    "You:",
    key="styledinput",
    label_visibility="collapsed",
    on_change=handle_input
)

if st.session_state.response:
    st.markdown(f"**DJ Bot:** {st.session_state.response}")
