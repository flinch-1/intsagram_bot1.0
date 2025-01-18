from instagrapi import Client
from cryptography.fernet import Fernet
import os
import json

# Paths for saving encrypted credentials
CREDENTIALS_FILE = "credentials.json"
KEY_FILE = "secret.key"

# Generate or load encryption key
def load_or_generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
    return key

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()

# Save credentials securely
def save_credentials(username, password):
    key = load_or_generate_key()
    encrypted_credentials = {
        "username": encrypt_data(username, key),
        "password": encrypt_data(password, key)
    }
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(encrypted_credentials, f)

# Load credentials securely
def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        return None, None
    key = load_or_generate_key()
    with open(CREDENTIALS_FILE, 'r') as f:
        encrypted_credentials = json.load(f)
    username = decrypt_data(encrypted_credentials['username'], key)
    password = decrypt_data(encrypted_credentials['password'], key)
    return username, password

# Login to Instagram
def login_to_instagram():
    client = Client()
    username, password = load_credentials()

    if not username or not password:
        username = input("Enter your Instagram username: ")
        password = input("Enter your Instagram password: ")
        save_credentials(username, password)

    try:
        client.login(username, password)
        print("Login successful!")
        return client
    except Exception as e:
        print(f"Login failed: {e}")
        return None

# Access Chats (Placeholder)
def access_chats(client):
    try:
        inbox = client.direct_threads()  # Fetch direct messages
        for thread in inbox:
            print(f"Thread: {thread['thread_id']} with users {[user['username'] for user in thread['users']]}")
    except Exception as e:
        print(f"Failed to fetch chats: {e}")

# Download Reels from a given URL (Placeholder)
def download_reel(client, reel_url, save_path="reels"):
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        media = client.media_info_by_url(reel_url)
        filename = os.path.join(save_path, f"{media.pk}.mp4")
        client.video_download(media.id, filename)
        print(f"Reel downloaded to {filename}")
    except Exception as e:
        print(f"Failed to download reel: {e}")

# Main execution block
def main():
    client = login_to_instagram()
    if client:
        # Placeholder for accessing chats and downloading reels
        access_chats(client)
        # Example Reel URL (replace with an actual URL for testing)
        example_reel_url = "https://www.instagram.com/reel/example/"
        download_reel(client, example_reel_url)

if __name__ == "__main__":
    main()
