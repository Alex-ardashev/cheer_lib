import sys
from ai_lib import AICheerLib
import os

def main():
    # Initialize our AI library with default settings
    cheer_ai = AICheerLib(config_path="config.json")

    print("Welcome to the Cheerful AI Chat! Type 'exit' to quit.")

    while True:
        user_message = input("\nYou: ")
        if user_message.lower() == "exit":
            print("Exiting the chat. Bye!")
            sys.exit(0)

        # Process the message through ai_lib
        response = cheer_ai.process_user_message(user_message)
        print(f"AI: {response}")

if __name__ == "__main__":
    main()