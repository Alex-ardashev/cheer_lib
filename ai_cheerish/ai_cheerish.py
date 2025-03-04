import json
import random
import csv
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Cheerish:
    def __init__(self, ai_client, config_path=None):
        """
        Initialize Cheerish with an AI client and an optional configuration.
        
        Args:
            ai_client: A callable or an object with a get_response method
            config_path: Path to a custom configuration file. If None, the default 
                         shipped configuration is used.
        """
        self.config = self._load_config(config_path)
        self.settings = self.config.get("settings", {})
        self.motivational_messages = self.config.get("motivational_messages", {})
        self.human_nature = self.config.get("human_nature", "")
        self.message_count = 0
        self.ai_client = ai_client
        
        # Logging settings
        self.enable_logging = self.settings.get("enable_logging", False)
        self.log_file = self.settings.get("log_file", "chat_logs.csv")

    def _load_config(self, config_path):
        """
        Load configuration from the specified path or use the default.
        
        Args:
            config_path: Path to a custom configuration file
            
        Returns:
            dict: The loaded configuration
        """
        # Try loading from the specified path
        if config_path:
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except FileNotFoundError:
                print(f"Warning: Config file not found at {config_path}, falling back to default")
        
        # Try loading from config.json in the current directory
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            pass
            
        # Fall back to the example config
        try:
            from importlib import resources
            return json.load(resources.open_text("ai_cheerish", "config.example.json"))
        except Exception as e:
            print(f"Warning: Could not load default config: {e}")
            # Return minimal default config
            return {
                "settings": {"motivational_frequency": 3},
                "motivational_messages": {"cheering": ["Keep going!"]},
                "human_nature": ""
            }

    def enhance_message(self, user_message: str) -> tuple:
        """
        Enhances the user's message by optionally adding a system note.
         - For the first message, prepends the "human nature" note.
         - For every nth message (defined by `motivational_frequency`), prepends a motivational note.
        
        Args:
            user_message: The original message from the user
            
        Returns:
            tuple: (enhanced_message, system_note)
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
        """
        Logs the interaction details with a timestamp to the configured log file.
        
        Args:
            user_message: The original message from the user
            system_note: The system note that was added (if any)
            ai_response: The response from the AI
        """
        if not self.enable_logging:
            return
            
        # Create directory for log file if it doesn't exist
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        timestamp = datetime.now().isoformat()
        with open(self.log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, user_message, system_note, ai_response])

    def __call__(self, user_message: str) -> str:
        """
        Enables the Cheerish instance to be called like a function.
        It enhances the user message, retrieves the AI response using the provided ai_client,
        logs the transaction, and then returns the response.
        
        Args:
            user_message: The message from the user
            
        Returns:
            str: The response from the AI
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