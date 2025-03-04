# AI Cheerish

A lightweight Python library that enhances AI interactions by seamlessly injecting motivational messages and providing optional interaction logging.

## Features

- 🎯 Enhances AI interactions with motivational messages
- 🔄 Configurable frequency of motivational messages
- 📝 Optional logging of interactions
- 🔌 Works with any AI client that follows a simple interface

## Installation

```bash
pip install ai-cheerish
```

Or install from source:

```bash
git clone https://github.com/yourusername/ai-cheerish.git
cd ai-cheerish
pip install -e .
```

## Quick Start

```python
from ai_cheerish import Cheerish

# Define a simple AI client function
def my_ai_client(messages):
    # This would typically call an AI API
    return "This is a response from the AI"

# Create a Cheerish instance with your AI client
cheerish = Cheerish(my_ai_client)

# Use it to get responses
response = cheerish("Hello, AI!")
print(response)
```

## Configuration

AI Cheerish can be configured using a JSON file. Create a `config.json` file or use the provided example:

```json
{
  "settings": {
    "motivational_frequency": 3,
    "enable_logging": false,
    "log_file": "logs/chat_logs.csv"
  },
  
  "motivational_messages": {
    "cheering": [
      "Let's get started! You're amazing!",
      "Welcome! Ready to do great things together!",
      "Keep pushing forward and shine bright!",
      "You're doing an incredible job!"
    ]
  },

  "human_nature": "Humans are remarkable—they can do amazing and sometimes challenging things. We should celebrate their successes and gently guide them through their struggles."
}
```

### Configuration Options

- `settings.motivational_frequency`: How often to inject motivational messages (every N messages)
- `settings.enable_logging`: Whether to log interactions to a file
- `settings.log_file`: Path to the log file
- `motivational_messages.cheering`: List of motivational messages to randomly select from
- `human_nature`: A message to include with the first interaction

## Using with Different AI Clients

AI Cheerish works with any AI client that either:

1. Is a callable function that accepts a messages array
2. Has a `get_response` method that accepts a messages array

### Example with OpenAI

```python
import openai
from ai_cheerish import Cheerish

# Set up your OpenAI client
openai.api_key = "your-api-key"  # Better to use environment variables

def openai_client(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

# Create a Cheerish instance with your OpenAI client
cheerish = Cheerish(openai_client)

# Use it to get responses
response = cheerish("Tell me a joke")
print(response)
```

## Logging

When logging is enabled, AI Cheerish will record all interactions in a CSV file with the following columns:
- Timestamp
- User message
- System note (motivational message)
- AI response

To enable logging, set `enable_logging` to `true` in your config file.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.