import qrcode

def generate_qr_code(secret):
    """
    Generates a QR code with the pre-shared secret for secure distribution.

    Parameters:
    - secret (str): The pre-shared secret to encode in the QR code.

    Returns:
    - None. Displays and saves the QR code as an image file.
    """
    # Create a QR code with the secret
    qr = qrcode.QRCode(
        version=10, # Can be use up to version 40
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add the secret to the QR code
    qr.add_data(secret)
    qr.make(fit=True)
    
    # Generate and display the QR code
    img = qr.make_image(fill="black", back_color="white")
    img.show()

    # Optionally, save the QR code as an image file
    img.save("pre_shared_secret_qr.png")
    print("QR code saved as 'pre_shared_secret_qr.png'.")

# Example usage
pre_shared_secret = "Q7ZEHZL5SQACT573QJKI25ZNYEV7CRC3"  # Replace with your actual secret
generate_qr_code(pre_shared_secret)
