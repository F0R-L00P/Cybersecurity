from PIL import Image


def encode_message(image_path, message, output_path):
    """
    Hides a message inside an image using LSB steganography.
    """
    # Open the image
    img = Image.open(image_path)
    pixels = list(img.getdata())

    # Convert message to binary and add a stopping marker
    binary_message = (
        "".join(format(ord(char), "08b") for char in message) + "1111111111111110"
    )  # End marker

    # Encode message in pixels' least significant bits
    new_pixels = []
    message_index = 0

    for pixel in pixels:
        new_pixel = list(pixel)
        for i in range(3):  # Modify only RGB channels
            if message_index < len(binary_message):
                new_pixel[i] = (new_pixel[i] & 0xFE) | int(
                    binary_message[message_index]
                )
                message_index += 1
        new_pixels.append(tuple(new_pixel))

    # Create and save the new image
    img.putdata(new_pixels)
    img.save(output_path)
    return output_path


# File paths and message
input_image = r"forest.jpg"
output_image = "stego_image.png"
secret_message = "Steganography is fascinating!"

# Encode the message into the image
try:
    encoded_image_path = encode_message(input_image, secret_message, output_image)
    print(f"Message encoded successfully! Output: {encoded_image_path}")
except Exception as e:
    print(f"An error occurred: {e}")


def decode_message(image_path):
    """
    Decodes a hidden message from an image using LSB steganography.
    """
    # Open the image
    img = Image.open(image_path)
    pixels = list(img.getdata())

    # Extract the least significant bits from the pixels
    binary_message = ""
    for pixel in pixels:
        for i in range(3):  # Extract from RGB channels
            binary_message += str(pixel[i] & 1)

    # Split binary message into 8-bit chunks and decode characters
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i : i + 8]
        if byte == "11111110":  # End marker
            break
        message += chr(int(byte, 2))

    return message


# Decode the hidden message from the image
decoded_message = decode_message(output_image)
# Display the hidden message
print(f"Decoded message: {decoded_message}")
