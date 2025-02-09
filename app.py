from openai import OpenAI
import os
from dotenv import load_dotenv
from ai_cheerish import Cheerish

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with Deepseek API key and base URL
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

def openai_get_response(messages):
    """
    Retrieve the AI response from the OpenAI client.
    Expects a list of messages where each message is a dict with 'role' and 'content' keys.
    """
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content

# Create an instance of Cheerish by directly passing in the OpenAI response function.
cheerish = Cheerish(openai_get_response)

# Start the chat loop
while True:
    user_input = input("You: ")
    response = cheerish(user_input)
    print(f"Assistant: {response}")
    
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Assistant: Goodbye!")
        break