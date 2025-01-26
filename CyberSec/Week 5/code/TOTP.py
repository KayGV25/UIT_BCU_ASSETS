import hmac
import hashlib
import time
import base64

def generate_totp(secret, interval=30):
    """
    Generates a time-based OTP (TOTP) using HMAC-SHA1.

    Parameters:
    - secret (str): The Base32 pre-shared secret key.
    - interval (int): The time interval in seconds (default 30 seconds).

    Returns:
    - totp (str): A 6-digit TOTP.
    """
    # Ensure the secret has the correct padding for Base32 decoding
    missing_padding = len(secret) % 8
    if missing_padding != 0:
        secret += '=' * (8 - missing_padding)

    # Convert the secret from Base32 to bytes
    secret_bytes = base64.b32decode(secret)
    interval = 2
    # Generate a time counter based on the current time and interval
    counter = int(time.time() // interval)
    
    # Convert the counter to an 8-byte array
    counter_bytes = counter.to_bytes(8, byteorder="big")
    
    # Create HMAC-SHA1 hash with the secret key and counter
    hmac_hash = hmac.new(secret_bytes, counter_bytes, hashlib.sha1).digest()
    
    # Dynamic truncation to obtain a 6-digit TOTP
    offset = hmac_hash[-1] & 0x0F
    code = (int.from_bytes(hmac_hash[offset:offset + 4], byteorder="big") & 0x7FFFFFFF) % 10000
    
    # Format OTP to be 6 digits, padding with zeros if necessary
    print(code)
    totp = f"{code:04d}"
    return totp

# Example usage with a properly padded pre-shared secret
pre_shared_secret = "FPV6A6QBUU23ITTSLKAABWLBFMQ7CSDE"  # Shared secret, make sure it's Base32 compliant
totp = generate_totp(pre_shared_secret)
print("Your TOTP is:", totp)
