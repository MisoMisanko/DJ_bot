from chatbot_base import ChatbotBase
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random


class DJBot(ChatbotBase):
    def __init__(self, name="DJBot", client_id=None, client_secret=None):
        super().__init__(name)
        self.spotify = None
        if client_id and client_secret:
            self.spotify = self.get_spotify_client(client_id, client_secret)

        self.emotion_to_keywords = {
            "happy": ["happy", "joyful", "cheerful", "elated", "content", "grateful"],
            "excited": ["excited", "thrilled", "pumped", "ecstatic"],
            "calm": ["calm", "relaxed", "peaceful", "serene"],
            "sad": ["sad", "down", "heartbroken", "blue", "unhappy"],
            "angry": ["angry", "mad", "furious", "annoyed", "frustrated"],
            "stressed": ["stressed", "anxious", "overwhelmed", "nervous"]
        }

    def process_input(self, user_input: str):
        analysis = TextBlob(user_input)
        polarity = analysis.sentiment.polarity
        general_mood = "positive" if polarity > 0 else "negative"
        detected_emotions = []
        for emotion, keywords in self.emotion_to_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                detected_emotions.append(emotion)
        return {"general_mood": general_mood, "emotions": detected_emotions}

    def generate_response(self, processed_input: dict, context=None) -> str:
        emotions = processed_input["emotions"]
        general_mood = processed_input["general_mood"]

        if context:
            query = f"{general_mood} {context}"
        elif general_mood == "negative" and not context:
            query = "sad relaxing music" #I had to add this, because the search often failed when I provided only "negative" with no context
        else:
            query = general_mood

        playlist = self.search_playlist(query)
        if playlist:
            responses = [
                f"This feels just right for your vibe. Here’s your playlist: {playlist}",
                f"I think you'll enjoy this! Here's the playlist: {playlist}",
                f"Got the perfect tunes for you! Check it out: {playlist}",
                f"Here's something that matches your mood: {playlist}"
            ]
            return random.choice(responses)
        else:
            fallback_playlist = "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0"
            fallback_responses = [
                f"I couldn’t find the perfect match, but this playlist might still hit the spot: {fallback_playlist}",
                f"Couldn't locate the exact tunes, but give this a try: {fallback_playlist}",
                f"Here's a playlist you might like: {fallback_playlist}"
            ]
            return random.choice(fallback_responses)

    def search_playlist(self, query: str):
        if not self.spotify:
            return None
        try:
            results = self.spotify.search(q=query, type="playlist", limit=1)
            if results and results.get("playlists", {}).get("items"):
                return results["playlists"]["items"][0]["external_urls"]["spotify"]
            return None
        except Exception:
            return None

    def get_spotify_client(self, client_id, client_secret):
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        return spotipy.Spotify(auth_manager=auth_manager)

    def mini_spotify_wrapped(self):
        return "https://open.spotify.com/playlist/37i9dQZF1EP6YuccBxUcC1"
