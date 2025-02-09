from openai import OpenAI
import os
from dotenv import load_dotenv
from ai_cheerish import AICheerLib

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with Deepseek API key and base URL
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# Initialize AI Cheerish
class AIClient:
    def get_response(self, messages):
        """
        Get the AI response using the provided messages.
        The messages should be a list of dictionaries with "role" and "content" keys.
        """
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content

# Initialize the AI client and AI Cheerish
ai_client = AIClient()
cheer_ai = AICheerLib(ai_client)

# Initialize the conversation with a system message
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
]

# Start the chat loop
while True:
    # Get user input
    user_input = input("You: ")
    
    # Append the user's message to the conversation history
    messages.append({"role": "user", "content": user_input})
    
    # Process the user's message with AI Cheerish. This internally logs the full interaction.
    response = cheer_ai.process_user_message(user_input)
    
    # Print the assistant's reply
    print(f"Assistant: {response}")
    
    # Append the assistant's reply to the conversation history
    messages.append({"role": "assistant", "content": response})
    
    # Optionally, you can add a condition to exit the loop
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Assistant: Goodbye!")
        break