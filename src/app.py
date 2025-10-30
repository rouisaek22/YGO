# app.py
# Main application script for initializing image storage and retrieving images.
# Handles downloading images if not present locally.

# TODO : Add async functionality for image downloads
# TODO : Reading image IDs from a file instead of hardcoding
# TODO : Limit the number of concurrent downloads to avoid overwhelming the server

import os
import requests

def main():
    initialize_app()

    urls = [
        "10000.jpg",
        "10000000.jpg",
        "10000001.jpg",
        "10000002.jpg",
        "10000010.jpg",
        "100000101.jpg",
        "10000011.jpg",
        "10000012.jpg",
        "10000020.jpg",
        "10000021.jpg",
        "10000022.jpg",
        "10000030.jpg",
        "10000040.jpg",
        "10000080.jpg",
        "10000090.jpg",
        "10002346.jpg",
        "10004783.jpg",
        "10012614.jpg",
        "10019086.jpg",
        "10024317.jpg",
        "10026986.jpg",
        "10028593.jpg",
        "1003028.jpg",
        "10032958.jpg",
        "10035717.jpg",
        "1003840.jpg",
        "10040267.jpg",
        "100445001.jpg",
        "100445002.jpg",
        "100445003.jpg"
    ]
    
    for url in urls:
        get_image(url)

# Initialize application by creating necessary directories
def initialize_app():
        if not os.path.exists("./images"):
            print("Initializing application...")
            print("Setting up image storage directory...")
            print("Image storage directory is set to './images'")
            os.makedirs("./images")

# Retrieve image by ID, downloading if not present locally
def get_image(image_id)-> str:
    card_path = f"./images/{image_id}"
    card_id = os.path.basename(card_path)
    if not os.path.exists(card_path):
        print(f"Image {image_id} not found locally. Downloading...")
        get_image_from_source(image_id, card_path)
        get_image(image_id)
    else:
        print(f"Image {image_id} found locally at {card_path}")
    return card_id

# Download image from external source and save locally
def get_image_from_source(image_id, card_path):
    BASE_URL = "https://images.ygoprodeck.com/images/cards/"
    url = f"{BASE_URL}{image_id}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(card_path, 'wb') as f:
            f.write(response.content)
        print(f"Image {image_id} downloaded and saved to {card_path}")
    else:
        print(f"Failed to download image {image_id}. Status code: {response.status_code}")

# Append image references to a JavaScript file for gallery usage
def append_images_to_js(images_dir: str):
    for filename in os.listdir(images_dir):
        if filename.endswith(".jpg"):
            try:
                with open("../src/www/js/images.js", "a") as file:
                    file.write(f"// {filename[:-4]}\n")
                    file.write(f"galleryItems.push({{ src: '../{images_dir}/{filename}' }});\n")
            except FileNotFoundError:
                print("Error: The file 'images.js' was not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    append_images_to_js("images")