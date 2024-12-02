from chatbot_base import ChatbotBase
from textblob import TextBlob

class DJBot(ChatbotBase):
    def __init__(self, name="DJBot"):
        super().__init__(name)
        self.mood_to_playlist = {
            "positive": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
            "negative": "https://open.spotify.com/playlist/7MEwraINsv80dmb7jTj9ke?si=b04aee63d5eb48c7",
            "neutral": "https://open.spotify.com/playlist/0NUtHPgeWm833NU14csQZi?si=f2066d3c8f064344"
        }

    def process_input(self, user_input: str):
        """Process user input and analyze sentiment."""
        analysis = TextBlob(user_input)
        if analysis.sentiment.polarity > 0.2:
            return "positive"
        elif analysis.sentiment.polarity < -0.2:
            return "negative"
        else:
            return "neutral"

    def generate_response(self, processed_input: str) -> str:
        """Generate a playlist recommendation based on the mood."""
        playlist = self.mood_to_playlist.get(processed_input, "No playlist found.")
        return f"I think you're feeling {processed_input}. Here's a playlist for you: {playlist}"
