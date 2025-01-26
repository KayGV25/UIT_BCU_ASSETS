import secrets
import base64

def generate_strong_base32_secret(length=20):
    """
    Generates a secure Base32-encoded secret.
    
    Parameters:
    - length (int): Length of the byte sequence to generate before Base32 encoding.
    
    Returns:
    - secret (str): A Base32-encoded string.
    """
    random_bytes = secrets.token_bytes(length)
    return base64.b32encode(random_bytes).decode('utf-8').rstrip("=")

# Example of generating a valid Base32 secret
pre_shared_secret = generate_strong_base32_secret()
print("Generated Base32-compliant secret:", pre_shared_secret)
