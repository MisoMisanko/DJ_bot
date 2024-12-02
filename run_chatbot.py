from dj_bot import DJBot

if __name__ == "__main__":
    bot = DJBot()
    bot.greeting()  # Initial greeting
    print("How are you feeling today? (type 'exit' to quit):")  # Updated initial prompt

    while True:  # Simplified loop, always runs unless the user types 'exit'
        user_input = input("You: ").strip()  # Get user input
        if user_input.lower() in ["exit", "quit"]:  # Exit condition
            bot.farewell()  # Goodbye message
            break  # Exit the loop
        else:
            mood = bot.process_input(user_input)  # Process the input
            response = bot.generate_response(mood)  # Generate a response
            print(f"DJ Bot: {response}")  # Print the bot's response
            
            # Follow-up question to make it more conversational
            print("DJ Bot: Did that match your mood, or should I try something else? How are you feeling now?")
