from chatbot_base import ChatbotBase
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class DJBot(ChatbotBase):
    def __init__(self, client_id: str, client_secret: str, name="DJBot"):
        super().__init__(name)
        self.client_id = client_id
        self.client_secret = client_secret

    def process_input(self, user_input: str):
        analysis = TextBlob(user_input)
        polarity = analysis.sentiment.polarity

        if polarity > 0.2:
            main_mood = "positive"
        elif polarity < -0.2:
            main_mood = "negative"
        else:
            main_mood = "neutral"

        keywords = {
            "stressed": ["stressed", "anxious", "nervous", "overwhelmed"],
            "excited": ["excited", "thrilled", "ecstatic"],
            "calm": ["calm", "relaxed", "peaceful"],
        }

        secondary_moods = []
        for mood, words in keywords.items():
            if any(word in user_input.lower() for word in words):
                secondary_moods.append(mood)

        return {"main": main_mood, "secondary": secondary_moods}

    def generate_response(self, processed_input: dict) -> str:
        main_mood = processed_input["main"]
        secondary_moods = processed_input["secondary"]

        mood_description = main_mood
        if secondary_moods:
            mood_description += " and " + " and ".join(secondary_moods)

        context = input("DJ Bot: What are you currently doing? (e.g., studying, working out, relaxing): ").strip().lower()

        playlist = self.search_playlist(main_mood, context)
        if playlist:
            return f"Here is a playlist for {context} while feeling {mood_description}: {playlist}"
        else:
            return f"Sorry, I couldn't find a playlist for {context} while feeling {mood_description}."

    def get_spotify_client(self):
        auth_manager = SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret
        )
        return spotipy.Spotify(auth_manager=auth_manager)

    def search_playlist(self, mood: str, context: str):
        spotify = self.get_spotify_client()
        query = f"{mood} {context}"
        results = spotify.search(q=query, type="playlist", limit=1)

        if results["playlists"]["items"]:
            return results["playlists"]["items"][0]["external_urls"]["spotify"]
        else:
            return None