from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random


class DJBot:
    def __init__(self, name="DJBot", client_id=None, client_secret=None):
        self.name = name
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

        # Build search priorities: use the first detected emotion or general fallback
        emotion = emotions[0] if emotions else general_mood
        query_options = self.build_query_variants(emotion, context)

        playlist = self.search_multiple_queries(query_options)
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

    def build_query_variants(self, emotion, context=None):
        if context:
            return [
                f"{emotion} {context} playlist",
                f"{emotion} music for {context}",
                f"{emotion} {context} songs",
                f"{emotion} {context}",
                f"{context} {emotion}",
                f"{context} music",
                f"{emotion} playlist"
            ]
        else:
            return [f"{emotion} playlist", f"{emotion} music"]

    def search_multiple_queries(self, query_list):
        for query in query_list:
            result = self.search_playlist(query)
            if result:
                return result
        return None

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
