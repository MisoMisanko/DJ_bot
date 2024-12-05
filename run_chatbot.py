import sys
from dj_bot import DJBot

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <client_id> <client_secret>")
        sys.exit(1)

    client_id = sys.argv[1]
    client_secret = sys.argv[2]

    bot = DJBot(client_id=client_id, client_secret=client_secret)
    bot.greeting()
    print("How are you feeling today? (type 'exit' to quit):")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            bot.farewell()
            break
        else:
            moods = bot.process_input(user_input)
            main_mood = moods["main"]
            secondary_moods = moods["secondary"]

            response = bot.generate_response(moods)
            print(f"DJ Bot: {response}")

if __name__ == "__main__":
    main()