import re
import requests
import os
import argparse

def find_next_folder(base_directory, specified_folder=None):
    folder_base_name = "folder" if not specified_folder else specified_folder
    i = 1
    while True:
        folder_name = f"{folder_base_name}{i}" if not specified_folder else folder_base_name
        full_folder_path = os.path.join(base_directory, folder_name)
        if not os.path.exists(full_folder_path):
            os.makedirs(full_folder_path)
            return full_folder_path
        if specified_folder:  # If specified, don't loop for numbering
            return full_folder_path
        i += 1

def extract_and_download(url, base_directory, specified_directory=None):
    link_pattern = re.compile(r'https://(?:files|litter)\.catbox\.moe/[\w\-.]+(?:\.jpg|\.jpeg|\.png|\.webm)')
    
    save_directory = find_next_folder(base_directory, specified_directory)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        links = link_pattern.findall(html_content)
        
        for link in links:
            try:
                response = requests.get(link)
                response.raise_for_status()
                
                file_name = link.split('/')[-1]
                save_path = os.path.join(save_directory, file_name)
                
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"Downloaded and saved in '{save_directory}': {file_name}")
            except requests.RequestException as e:
                print(f"Failed to download {link}: {e}")
    except requests.RequestException as e:
        print(f"Failed to fetch URL {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from a website.")
    parser.add_argument("url", help="The URL of the website to scan for images.")
    parser.add_argument("-d", "--directory", help="The directory name where images will be saved.", default=None)
    args = parser.parse_args()

    base_directory = os.getcwd()
    extract_and_download(args.url, base_directory, args.directory)
