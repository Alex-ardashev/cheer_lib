# AI Cheerish

AI Cheerish is a lightweight Python library designed to enhance your AI chatbot's performance by injecting motivational and inspirational messages into conversation prompts. It integrates seamlessly with your existing AI client and automatically logs interactions for improved debugging and analysis.

## Key Features

- **Prompt Enhancement:** Automatically inject a custom "human nature" message on the first interaction and add motivational notes periodically (every nth message, as set in your configuration).
- **Easy Integration:** Works with any AI client that follows a conversational API pattern.
- **Logging:** Records conversation details including timestamps, original messages, enhanced prompts, and AI responses in a CSV file.

## Installation

Install the package via pip:

pip install ai-cheerish

## Configuration

Before you begin, copy the provided `config.example.json` file into your project root as `config.json` and adjust the settings as needed. This file is excluded from version control, so it's safe to store environment-specific configurations here.

## Usage Example

Below is a simple example showing how to integrate AI Cheerish with a dummy AI client:

from ai_cheerish import AICheerLib
class DummyAIClient:
def get_response(self, messages):
# For demonstration purposes, simply echo the prompt. Replace with your AI service integration.
return "Dummy response: " + messages[0]["content"]
Initialize your AI client
ai_client = DummyAIClient()
Create an instance of AICheerLib with your client
cheer_ai = AICheerLib(ai_client)
Process a user message to receive an enhanced AI response
response = cheer_ai.process_user_message("Hello, how are you?")
print(response)


## How It Works

1. **Message Enhancement:** 
   - On the first user message, the library can prepend a configured "human_nature" note.
   - Every nth message (by default, every 3rd message—modifiable via the `motivational_frequency` setting) gets an additional motivational note injected.
2. **Single API Call:** 
   - Instead of sending separate system and user messages, the system note is prepended directly to the user's message.
3. **Logging:** 
   - Each interaction is logged in a CSV file (`chat_logs.csv`) for later review or debugging.

## License

This project is licensed under the MIT License.