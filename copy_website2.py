import os
import subprocess

# Function to download the website using curl (instead of wget)
def download_website(url):
    # Create a new directory to store the downloaded website
    folder_name = 'downloaded_website'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Build the curl command
    command = [
        'curl', '-O', '--recursive', '--no-parent', '--convert-links', url
    ]

    # Run the curl command using subprocess
    try:
        subprocess.run(command, check=True)
        print(f"Website has been downloaded successfully into the folder: {folder_name}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while downloading the website: {e}")

# Example usage: specify the URL of the website to download
url = 'http://tiger-wil.com'  # Replace with the target URL
download_website(url)
