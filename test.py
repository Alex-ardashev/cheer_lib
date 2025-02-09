from ai_cheerish import Cheerish

def dummy_get_response(messages):
    return "Dummy response: " + messages[0]["content"]

# Pass the function directly instead of creating a custom class instance.
cheerish = Cheerish(dummy_get_response)

response = cheerish("Hello, how are you?")
print(response)