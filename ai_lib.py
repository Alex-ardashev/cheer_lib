import json
import random
from openai import OpenAI

import csv
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AICheerLib:
    def __init__(self, config_path="config.json"):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.settings = self.config["settings"]
        self.motivational_messages = self.config["motivational_messages"]
        
        # Optional: If your config["motivational_messages"] is not a dict with key "cheering",
        # you could handle it here. For now we assume it is a dict.
        #
        # Initialize our state to track how many messages we've processed in the current chat.
        self.message_count = 0
        
        # Initialize OpenAI client using the API key from environment variables.
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def enhance_user_message(self, user_message: str) -> str:
        """
        Enhances the user's message with additional context based on the message count:
         - For the first message in a chat, appends the human_nature text.
         - For every third message (using motivational_frequency from settings) adds a cheering message.
         - For all other messages, returns the message as-is.
        """
        enhanced = user_message
        # First message: append "human_nature" from config.
        if self.message_count == 0:
            human_nature_text = self.config.get("human_nature", "")
            if human_nature_text:
                enhanced = f"{user_message}\n[System Note: {human_nature_text}]"
        # Every third message (ex: 3rd, 6th, ...) add a cheering note.
        elif (self.message_count + 1) % self.settings.get("motivational_frequency", 3) == 0:
            cheer_message = random.choice(
                self.motivational_messages.get("cheering", ["Keep going!"])
            )
            enhanced = f"{user_message}\n[System Note: {cheer_message}]"
        
        self.message_count += 1
        return enhanced

    def log_interaction(self, timestamp, user_message, enhanced_prompt, ai_response):
        """Improved logging with enhanced prompt"""
        with open(self.settings["log_file"], "a") as f:
            f.write(f"{timestamp}|{user_message}|{enhanced_prompt}|{ai_response}\n")

    def get_motivational_message(self) -> str:
        """Return a random cheering message from the configuration."""
        messages = self.config.get("motivational_messages", {})
        return random.choice(messages.get("cheering", ["Keep going!"]))

    def get_ai_response(self, prompt: str) -> str:
        """
        Simple wrapper for calling the OpenAI API with the chosen model.
        Now the model is obtained from the configuration settings.
        """
        model_name = self.settings.get("model_name", "gpt-3.5-turbo")
        # For chat models like gpt-3.5-turbo / gpt-4, use ChatCompletion
        if "gpt-3.5" in model_name or "gpt-4" in model_name:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        else:
            # For other models, use the Completion API
            response = self.client.completions.create(
                model=model_name,
                prompt=prompt,
                max_tokens=100,
                temperature=0.7
            )
            return response.choices[0].text.strip()

    def process_user_message(self, user_message: str) -> str:
        """
        Main interface function:
         1) Enhances the user message (adding human_nature on the first message or a motivational message every third message)
         2) Gets AI response from the model
         3) Logs the conversation details
         4) Returns the final answer
        """
        # 1) Enhance prompt with system notes if applicable.
        enhanced_prompt = self.enhance_user_message(user_message)
        
        # 2) Get AI response using the enhanced prompt
        try:
            ai_response = self.get_ai_response(enhanced_prompt)
        except Exception as e:
            ai_response = f"Error generating response: {str(e)}"
        
        # 3) Log the interaction details (including sentiment analysis for logging)
        timestamp = datetime.now().isoformat()
        self.log_interaction(
            timestamp=timestamp,
            user_message=user_message,
            enhanced_prompt=enhanced_prompt,
            ai_response=ai_response
        )
        
        # 4) Return final AI response
        return ai_response