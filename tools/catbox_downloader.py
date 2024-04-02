import re
import requests
import os

def find_next_folder():
    folder_base_name = "folder"
    i = 1
    while True:
        folder_name = f"{folder_base_name}{i}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            return folder_name
        i += 1

def extract_and_download(file_name, base_directory):
    # Modified regex to match specific file types
    link_pattern = re.compile(r'https://(?:files|litter)\.catbox\.moe/[^ \n]*(?:\.jpg|\.jpeg|\.png|\.webm)')
    
    # Determine the save directory based on existing folders
    save_directory = find_next_folder()
    full_save_directory = os.path.join(base_directory, save_directory)
    
    # Read the file and extract URLs
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        links = link_pattern.findall(content)
    
    # Download and save each file
    for link in links:
        try:
            response = requests.get(link)
            response.raise_for_status()  # Check for HTTP request errors
            
            # Extracting file name from the URL for saving
            file_name = link.split('/')[-1]
            save_path = os.path.join(full_save_directory, file_name)
            
            # Save the content to a file
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded and saved in '{save_directory}': {file_name}")
        except requests.RequestException as e:
            print(f"Failed to download {link}: {e}")

# Usage
base_directory = os.getcwd()  # Use the current working directory of the script
file_name = os.path.join(base_directory, 'content.txt')  # The text file is expected to be in the same directory
extract_and_download(file_name, base_directory)
