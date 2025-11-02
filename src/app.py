# app.py
# Main application script for initializing image storage and retrieving images.
# Handles downloading images if not present locally.

# [*] TODO : Add async functionality for image downloads
# [*] TODO : Reading image IDs from a file instead of hardcoding
# [*] TODO : Limit the number of concurrent downloads to avoid overwhelming the server (MAX 20 requests per second)
# [*] TODO : Error handling for failed downloads

import os
import requests
import time
import concurrent.futures

def main():
    initialize_app()
    ids = read_image_ids("ids.txt")

    def get_image_with_delay(image_id: int):
        get_image(image_id)
        time.sleep(0.1)  # Delay to limit request rate

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(get_image_with_delay, ids)

# Initialize application by creating necessary directories
def initialize_app():
    if not os.path.exists("./images"):
        print("Initializing application...")
        print("Setting up image storage directory...")
        print("Image storage directory is set to './images'")
        os.makedirs("./images")

# Read image IDs from a file, or use a default list if the file is not found (for testing)
def read_image_ids(filename: str) -> list[str]:
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Warning: {filename} not found, using default list")
        return [
            "10000000.jpg",
            "10000001.jpg",
            "10000002.jpg",
            "10000010.jpg",
            "100000101.jpg",
            "10000011.jpg",
            "10000012.jpg",
            "10000020.jpg",
            "10000021.jpg",
        ]

# Retrieve image by ID, downloading if not present locally
def get_image(image_id: int):
    card_path = f"./images/{image_id}"

    if not os.path.exists(card_path):
        print(f"Image {image_id} not found locally. Downloading...")
        get_image_from_source(image_id, card_path)
    else:
        print(f"Image {image_id} found locally at {card_path}")


# Download image from external source and save locally
def get_image_from_source(image_id: int, card_path: str):
    BASE_URL = "https://images.ygoprodeck.com/images/cards/"
    url = f"{BASE_URL}{image_id}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(card_path, "wb") as f:
                f.write(response.content)
            print(f"Image {image_id} downloaded and saved to {card_path}")
        else:
            print(
                f"Failed to download image {image_id}. Status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading image {image_id}: {e}")

# Append image references to a JavaScript file for gallery usage
def append_images_to_js(images_dir: str):
    for filename in os.listdir(images_dir):
        if filename.endswith(".jpg"):
            try:
                with open("../src/www/scripts/images.js", "a") as file:
                    file.write(f"// {filename[:-4]}\n")
                    file.write(
                        f"galleryItems.push({{ src: '../{images_dir}/{filename}' }});\n"
                    )
            except FileNotFoundError:
                print("Error: The file 'images.js' was not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    append_images_to_js("images")