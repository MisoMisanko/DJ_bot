import sys
import time
import random
from dj_bot import DJBot

def main():
    if len(sys.argv) != 3:
        print("Usage: python run_chatbot.py <client_id> <client_secret>") #provided in the submitted zip file. Added this, based on google search of the best practices on how to handle using api credentials while sharing code to public repositories
        sys.exit(1)

    client_id = sys.argv[1]
    client_secret = sys.argv[2]

    bot = DJBot(client_id=client_id, client_secret=client_secret)
    special_depleted = False

    bot.greeting()
    print("How are you feeling today? (type 'exit' to quit):")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            bot.farewell()
            break
        else:
            processed_input = bot.process_input(user_input)
            general_mood = processed_input["general_mood"]
            emotions = processed_input["emotions"]

            if general_mood == "positive":
                positive_responses = [
                    "That’s great to hear! (^_^)",
                    "Amazing! I’m so happy for you! \(^o^)/",
                    "Fantastic! Let’s keep the good vibes rolling! (^_~)"
                ]
                print(f"DJ Bot: {random.choice(positive_responses)}")
                time.sleep(1)
                activity_prompts = [
                    "What are you up to right now? Relaxing, working out, or something else?",
                    "What’s on your schedule? Chilling, exercising, or anything else?",
                    "What are you doing at the moment? Taking it easy, hitting the gym, or something else?"
                ]
                context = input(f"DJ Bot: {random.choice(activity_prompts)}\nYou: ").strip().lower()
            else:
                negative_responses = [
                    "I’m sorry to hear that. (T_T)",
                    "Oh no, that sounds rough. (._.)",
                    "I’m here for you. Let’s make it better. (>_<)"
                ]
                print(f"DJ Bot: {random.choice(negative_responses)}")
                time.sleep(1)
                mood_prompts = [
                    "Should we stick with this mood or try to brighten things up?",
                    "Do you want to stay in this feeling or find something uplifting?",
                    "Would you prefer to keep this vibe or try to turn it around?"
                ]
                mood_action = input(f"DJ Bot: {random.choice(mood_prompts)}\nYou: ").strip().lower()
                if any(keyword in mood_action for keyword in ["uplift", "better", "happy", "improve", "change"]):
                    general_mood = "positive"
                elif any(keyword in mood_action for keyword in ["stick", "keep", "stay", "same"]):
                    general_mood = "negative"
                context = "relaxing" 

            response = bot.generate_response({"general_mood": general_mood, "emotions": emotions}, context=context)
            print(f"DJ Bot: {response}")

            while True:
                if not special_depleted:
                    special_prompts = [
                        "Want to explore another playlist, or check out something special I’ve curated just for you?",
                        "Would you like another playlist, or something unique I’ve crafted especially for you?",
                        "Ready for another playlist, or want to see something truly special?"
                    ]
                    next_step = input(f"DJ Bot: {random.choice(special_prompts)} Type 'another', 'special', or 'exit'.\nYou: ").strip().lower()
                else:
                    followup_prompts = [
                        "Want to explore another playlist based on your mood?",
                        "Would you like to try another playlist?",
                        "Ready to explore a new playlist for your vibe?"
                    ]
                    next_step = input(f"DJ Bot: {random.choice(followup_prompts)} Type 'another' or 'exit'.\nYou: ").strip().lower()

                if next_step == "another":
                    reset_prompts = [
                        "Let’s start fresh! How are you feeling now?",
                        "Let’s try again! What’s your mood now?",
                        "Okay! What’s the vibe you’re feeling now?"
                    ]
                    print(f"DJ Bot: {random.choice(reset_prompts)}")
                    break
                elif next_step == "special" and not special_depleted:
                    special_intro = [
                        "I’ve got something special for you. (^_^)",
                        "Here’s something truly unique I’ve made for you. \\(^o^)/",
                        "I’ve prepared something one-of-a-kind just for you. (^_~)"
                    ]
                    print(f"DJ Bot: {random.choice(special_intro)}")
                    time.sleep(1)
                    special_description = [
                        "It’s a playlist made just for you, tuned to your recent vibes.",
                        "This playlist perfectly matches what you need right now.",
                        "Here’s a playlist I’ve tailored specifically to your current vibe."
                    ]
                    print(f"DJ Bot: {random.choice(special_description)}")
                    time.sleep(1)
                    wrapped_playlist = bot.mini_spotify_wrapped()
                    print(f"DJ Bot: You’re going to love this one: {wrapped_playlist}")
                    special_depleted = True
                elif next_step in ["exit", "quit"]:
                    bot.farewell()
                    sys.exit(0)
                else:
                    retry_prompts = [
                        "I didn’t catch that. Please type 'another', 'special', or 'exit'.",
                        "Hmm, I didn’t get that. Try typing 'another', 'special', or 'exit'.",
                        "Not sure what you meant. Type 'another', 'special', or 'exit' to continue."
                    ]
                    if not special_depleted:
                        print(f"DJ Bot: {random.choice(retry_prompts)}")
                    else:
                        print("DJ Bot: I didn’t catch that. Please type 'another' or 'exit'.")

if __name__ == "__main__":
    main()
