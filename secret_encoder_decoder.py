import random
import string

def generate_random_string(length=3):
    """Generates a random alphanumeric string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def encode_word(word):
    """Encodes a single word using secret rules."""
    if len(word) >= 3:
        # Rotate first letter to the end
        transformed = word[1:] + word[0]
        # Wrap with random strings
        return generate_random_string() + transformed + generate_random_string()
    return word[::-1]  # Reverse short words

def decode_word(word):
    """Decodes a word encoded by encode_word()."""
    if len(word) < 9:
        return word[::-1]
    stripped = word[3:-3]  # Remove random prefix/suffix
    return stripped[-1] + stripped[:-1]  # Move last char to start

def process_message(message, operation):
    """Applies encoding or decoding to each word in a message."""
    words = message.split()
    if operation == 'encode':
        return ' '.join(encode_word(word) for word in words)
    elif operation == 'decode':
        return ' '.join(decode_word(word) for word in words)
    else:
        return "❌ Invalid operation. Choose 'encode' or 'decode'."

def main():
    print("🔐 Secret Message Encoder/Decoder 🔓")
    print("Type 'encode' to encrypt a message or 'decode' to reveal it.")

    operation = input("Operation (encode/decode): ").strip().lower()
    if operation not in ['encode', 'decode']:
        print("❌ Invalid input. Please choose either 'encode' or 'decode'.")
        return

    message = input("Enter the message: ").strip()
    if not message:
        print("⚠️ Message cannot be empty.")
        return

    result = process_message(message, operation)
    print(f"\n✅ Result:\n{result}")

# Run the app
if __name__ == "__main__":
    main()
