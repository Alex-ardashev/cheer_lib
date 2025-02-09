import json
import random
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AICheerLib:
    def __init__(self, ai_client, config_path="config.json"):
        # Try to load the private configuration from config.json
        try:
            with open(config_path) as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # If config.json is not found, fall back to the default configuration shipped with the package
            try:
                from importlib import resources
                self.config = json.load(resources.open_text("ai_cheerish", "config.example.json"))
            except Exception as e:
                raise FileNotFoundError("Neither the private config.json nor the default config.example.json could be loaded.") from e

        self.settings = self.config["settings"]
        self.motivational_messages = self.config["motivational_messages"]

        # Initialize our state to track how many messages we've processed in the current chat.
        self.message_count = 0

        # Use the provided AI client (model agnostic) supplied by the user
        self.ai_client = ai_client

    def enhance_user_message(self, user_message: str) -> tuple:
        """
        Enhances the user's message with additional context based on the message count:
         - For the first message in a chat, appends the human_nature text.
         - For every third message (using motivational_frequency from settings) adds a cheering message.
         - For all other messages, returns the message as-is.
        Returns a tuple: (user_message, system_note)
        """
        system_note = ""
        # First message: append "human_nature" from config.
        if self.message_count == 0:
            human_nature_text = self.config.get("human_nature", "")
            if human_nature_text:
                system_note = human_nature_text
        # Every third message (ex: 3rd, 6th, ...) add a cheering note.
        elif (self.message_count + 1) % self.settings.get("motivational_frequency", 3) == 0:
            system_note = random.choice(
                self.motivational_messages.get("cheering", ["Keep going!"])
            )
        
        self.message_count += 1
        return user_message, system_note

    def log_interaction(self, timestamp, user_message, enhanced_prompt, ai_response):
        """Improved logging with enhanced prompt"""
        with open("chat_logs.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, user_message, enhanced_prompt, ai_response])

    def get_motivational_message(self) -> str:
        """Return a random cheering message from the configuration."""
        messages = self.config.get("motivational_messages", {})
        return random.choice(messages.get("cheering", ["Keep going!"]))

    def get_ai_response(self, user_message: str, system_note: str = "") -> str:
        """
        Get the AI response using the provided ai_client.
        The ai_client should be model agnostic and implement a method get_response(prompt) that returns the response as a string.
        """
        try:
            # Prepare the messages for the AI model
            messages = [
                {"role": "system", "content": system_note} if system_note else None,
                {"role": "user", "content": user_message},
            ]
            # Filter out None values (if no system note is provided)
            messages = [msg for msg in messages if msg is not None]
            
            # Get the AI response
            response = self.ai_client.get_response(messages)
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def process_user_message(self, user_message: str) -> str:
        """
        Main interface function:
         1) Enhances the user message (adding human_nature on the first message or a motivational message every third message)
         2) Gets AI response from the model
         3) Logs the conversation details
         4) Returns the final answer
        """
        # 1) Enhance prompt with system notes if applicable.
        user_message, system_note = self.enhance_user_message(user_message)
        
        # 2) Get AI response using the enhanced prompt
        try:
            ai_response = self.get_ai_response(user_message, system_note)
        except Exception as e:
            ai_response = f"Error generating response: {str(e)}"
        
        # 3) Log the interaction details
        timestamp = datetime.now().isoformat()
        self.log_interaction(
            timestamp=timestamp,
            user_message=user_message,
            enhanced_prompt=system_note,  # Log the system note separately
            ai_response=ai_response
        )
        
        # 4) Return final AI response
        return ai_response