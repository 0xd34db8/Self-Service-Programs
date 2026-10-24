# Importing necessary libraries
import qrcode
from PIL import Image

def generate_qr_code(link, filename):
    
    # Create a new QR code object with the specified data and error correction level
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
        error_correction=qrcode.constants.ERROR_CORRECT_L
    )

    # Add the given link as encoded data to the QR code object
    qr.add_data(link)
    qr.make(fit=True)

    # Create an image from the QR code object
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the generated QR code as an image file
    img.save(filename)


# Usage:
if __name__ == "__main__":
    link = input("Enter a URL: ")
    filename = input("Enter the Filename: ")

    generate_qr_code(link, filename)

    print(f"QR code saved to {filename}")
