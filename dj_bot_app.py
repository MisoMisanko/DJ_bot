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

# === Mood reaction prompts ===
mood_responses = {
    "happy": [
        "That’s wonderful to hear! 😄",
        "Yay! That made my circuits smile! 😊",
        "You’ve got the vibes today! ✨"
    ],
    "excited": [
        "Whoa! That’s the spirit! 🎉",
        "I can feel your energy through the screen! ⚡",
        "Let’s ride this wave of hype together! 🚀"
    ],
    "calm": [
        "Nice and chill — I like it. 🌿",
        "Peaceful vibes detected. 🧘",
        "Floating on calm waters, huh? 🛶"
    ],
    "sad": [
        "I’m really sorry you’re feeling that way. 💙",
        "Let’s find something that understands you. 😔",
        "Even when it’s rough, I’m here with tunes. 🎧"
    ],
    "angry": [
        "Yikes — sounds intense. 💢",
        "Want a playlist to scream into the void? 🔊",
        "Let’s redirect that fire with some fierce beats. 🔥"
    ],
    "stressed": [
        "Let’s breathe together. Deep in… deep out. 😮‍💨",
        "I’ve got just the thing to calm the storm. 🌪️",
        "Stress? Music might help soothe it. 🎶"
    ],
    "fallback": [
        "That’s an interesting mood. I’ll work with it. 🤔",
        "Whatever you’re feeling, I’ve got your back. 🤖",
        "Not sure how to label that — let’s find the right vibe anyway. 💫"
    ]
}

# === Logic handler ===
def handle_input():
    user_input = st.session_state.styledinput.strip()
    if not user_input:
        return

    if st.session_state.step == 'mood':
        processed = bot.process_input(user_input)
        st.session_state.general_mood = processed["general_mood"]
        st.session_state.emotions = processed["emotions"]

        mood = st.session_state.emotions[0] if st.session_state.emotions else "fallback"
        reaction = random.choice(mood_responses.get(mood, mood_responses["fallback"]))

        st.session_state.response = f"{reaction} What are you doing right now?"
        st.session_state.step = 'activity' if mood != 'fallback' else 'post_playlist_prep'

    elif st.session_state.step == 'activity':
        st.session_state.context = user_input
        reply = bot.generate_response({
            "general_mood": st.session_state.general_mood,
            "emotions": st.session_state.emotions
        }, context=st.session_state.context)

        upsell = "\n\nWant to explore another playlist, check out something special I’ve curated just for you, or exit?"
        st.session_state.response = reply + upsell
        st.session_state.step = 'post_playlist'

    elif st.session_state.step == 'post_playlist':
        if 'special' in user_input.lower() and not st.session_state.special_used:
            st.session_state.response = f"Here’s something truly special I’ve curated just for you: {bot.mini_spotify_wrapped()}"
            st.session_state.special_used = True
        elif 'another' in user_input.lower():
            st.session_state.step = 'mood'
            st.session_state.response = "Okay! How are you feeling now?"
        elif 'exit' in user_input.lower():
            st.session_state.response = "Goodbye! Thanks for chatting 🎵"
            st.session_state.step = 'done'
        else:
            st.session_state.response = "Type 'another' for a new playlist, 'special' for your special one, or 'exit'."

    # Clear input field
    st.session_state.styledinput = ""

# === Title ===
st.title("🎧 DJ Bot – Your Mood-Based Music Companion")

# === Input field ===
st.text_input("You:", key="styledinput", label_visibility="collapsed", on_change=handle_input)

# === Response ===
if st.session_state.response:
    st.markdown(f"**DJ Bot:** {st.session_state.response}")
