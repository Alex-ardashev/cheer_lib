import json
import random
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Cheerish:
    def __init__(self, ai_client, config_path="config.json"):
        """
        Initialize Cheerish with an AI client and an optional configuration.
        If config_path is not found, the default shipped configuration is used.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            try:
                from importlib import resources
                self.config = json.load(resources.open_text("ai_cheerish", "config.example.json"))
            except Exception as e:
                raise FileNotFoundError(
                    "Neither the private config.json nor the default config.example.json could be loaded."
                ) from e

        self.settings = self.config.get("settings", {})
        self.motivational_messages = self.config.get("motivational_messages", {})
        self.human_nature = self.config.get("human_nature", "")
        self.message_count = 0
        self.ai_client = ai_client

    def enhance_message(self, user_message: str) -> tuple:
        """
        Enhances the user's message by optionally adding a system note.
         - For the first message, prepends the "human nature" note.
         - For every nth message (defined by `motivational_frequency`), prepends a motivational note.
        Returns a tuple of (enhanced_message, system_note).
        """
        system_note = ""
        if self.message_count == 0 and self.human_nature:
            system_note = self.human_nature
        elif (self.message_count + 1) % self.settings.get("motivational_frequency", 3) == 0:
            system_note = random.choice(
                self.motivational_messages.get("cheering", ["Keep going!"])
            )
        self.message_count += 1

        if system_note:
            enhanced_message = f"System Note: {system_note}\n{user_message}"
        else:
            enhanced_message = user_message

        return enhanced_message, system_note

    def log_interaction(self, user_message: str, system_note: str, ai_response: str):
        """Logs the interaction details with a timestamp to chat_logs.csv."""
        timestamp = datetime.now().isoformat()
        with open("chat_logs.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, user_message, system_note, ai_response])

    def __call__(self, user_message: str) -> str:
        """
        Enables the Cheerish instance to be called like a function.
        It enhances the user message, retrieves the AI response using the provided ai_client,
        logs the transaction, and then returns the response.
        """
        enhanced_message, sys_note = self.enhance_message(user_message)
        try:
            # If ai_client is a callable (like a function), call it directly.
            if callable(self.ai_client):
                response = self.ai_client([{"role": "user", "content": enhanced_message}])
            # Otherwise, assume it has a get_response method.
            elif hasattr(self.ai_client, "get_response"):
                response = self.ai_client.get_response([{"role": "user", "content": enhanced_message}])
            else:
                raise ValueError("Provided AI client must be a callable or have a 'get_response' method.")
        except Exception as e:
            response = f"Error generating response: {str(e)}"

        self.log_interaction(user_message, sys_note, response)
        return response