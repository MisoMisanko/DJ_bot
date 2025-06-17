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

# === Helper prompt variations ===
positive_responses = [
    "That’s great to hear! 😄",
    "Amazing! I’m so happy for you! 🥳",
    "Fantastic! Let’s keep the good vibes rolling! ✨"
]

activity_prompts = [
    "What are you up to right now? Relaxing, working out, or something else?",
    "What’s on your schedule? Chilling, exercising, or anything else?",
    "What are you doing at the moment? Taking it easy, hitting the gym, or something else?"
]

negative_responses = [
    "I’m sorry to hear that. 😔",
    "Oh no, that sounds rough. 💔",
    "I’m here for you. Let’s make it better. 🌧️"
]

intent_prompts = [
    "Should we stick with this mood or try to brighten things up?",
    "Do you want to stay in this feeling or find something uplifting?",
    "Would you prefer to keep this vibe or try to turn it around?"
]

another_prompts = [
    "Want to explore another playlist, or check out something special I’ve curated just for you?",
    "Would you like another playlist, or something unique I’ve crafted especially for you?",
    "Ready for another playlist, or want to see something truly special?"
]

retry_prompts = [
    "Type 'another' for a new playlist, 'special' for your special one, or 'exit'.",
    "Let me know if you want 'another', something 'special', or just 'exit'.",
    "Need more music? Say 'another', 'special', or 'exit'."
]

# === Logic handler ===
def handle_input():
    user_input = st.session_state.styledinput.strip()
    if not user_input:
        return

    if st.session_state.step == 'mood':
        processed = bot.process_input(user_input)
        st.session_state.general_mood = processed["general_mood"]
        st.session_state.emotions = processed["emotions"]

        if st.session_state.general_mood == "positive":
            st.session_state.response = f"{random.choice(positive_responses)}\n{random.choice(activity_prompts)}"
            st.session_state.step = 'activity'
        else:
            st.session_state.response = f"{random.choice(negative_responses)}\n{random.choice(intent_prompts)}"
            st.session_state.step = 'intent'

    elif st.session_state.step == 'intent':
        if any(word in user_input.lower() for word in ['uplift', 'change', 'better', 'happy']):
            st.session_state.general_mood = 'positive'
        elif any(word in user_input.lower() for word in ['stick', 'stay', 'keep']):
            st.session_state.general_mood = 'negative'
        st.session_state.response = random.choice(activity_prompts)
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
            st.session_state.response = f"Here’s something truly special I’ve curated just for you: {bot.mini_spotify_wrapped()}"
            st.session_state.special_used = True
        elif 'another' in user_input.lower():
            st.session_state.step = 'mood'
            st.session_state.response = "Let’s try again! What’s your mood now?"
        elif 'exit' in user_input.lower():
            st.session_state.response = "Goodbye! Thanks for chatting 🎵"
            st.session_state.step = 'done'
        else:
            st.session_state.response = random.choice(retry_prompts)

    # Clear input field
    st.session_state.styledinput = ""

# === Title ===
st.title("🎧 DJ Bot – Your Mood-Based Music Companion")

# === Input field ===
st.text_input("You:", key="styledinput", label_visibility="collapsed", on_change=handle_input)

# === Response ===
if st.session_state.response:
    st.markdown(f"**DJ Bot:** {st.session_state.response}")
