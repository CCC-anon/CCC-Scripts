import re
import requests
import os
import argparse

def find_next_folder(base_directory, name_source):
    # Determine if name_source is a URL or a file name
    if '/' in name_source:  # Likely a URL
        folder_base_name = name_source.split('/')[-1]
        # Remove any characters after a query (?) or hash (#) in URLs
        folder_base_name = re.split('\?|#', folder_base_name)[0]
    else:  # Likely a file name
        folder_base_name = os.path.splitext(name_source)[0]
    
    # Ensure the folder name is valid by removing characters not allowed in file names
    folder_base_name = re.sub(r'[<>:"/\\|?*]', '', folder_base_name)
    
    full_folder_path = os.path.join(base_directory, folder_base_name)
    if not os.path.exists(full_folder_path):
        os.makedirs(full_folder_path)
        return full_folder_path
    else:
        # If the folder exists, append a number to create a unique name
        i = 1
        while True:
            new_folder_name = f"{folder_base_name}_{i}"
            full_folder_path = os.path.join(base_directory, new_folder_name)
            if not os.path.exists(full_folder_path):
                os.makedirs(full_folder_path)
                return full_folder_path
            i += 1

def download_images(links, save_directory):
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

def extract_and_download(url=None, base_directory=None, specified_directory=None, url_list_file=None):
    link_pattern = re.compile(r'https://(?:files|litter)\.catbox\.moe/[\w\-.]+(?:\.jpg|\.jpeg|\.png|\.webm)')
    
    # Decide on save_directory based on the operation mode
    name_source = url if url else url_list_file if url_list_file else "downloaded_images"
    save_directory = find_next_folder(base_directory, name_source)

    if url_list_file:
        with open(url_list_file, 'r') as file:
            links = file.read().splitlines()
            download_images(links, save_directory)
    elif url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            links = link_pattern.findall(response.text)
            download_images(links, save_directory)
        except requests.RequestException as e:
            print(f"Failed to fetch URL {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from a website or a provided list of URLs.")
    parser.add_argument("url", nargs='?', help="The URL of the website to scan for images.", default=None)
    parser.add_argument("-d", "--directory", help="The base directory where images will be saved.", default=None)
    parser.add_argument("-f", "--file", help="Path to a text file containing URLs to download.", default=None)
    args = parser.parse_args()

    base_directory = os.getcwd() if not args.directory else args.directory
    extract_and_download(url=args.url, base_directory=base_directory, url_list_file=args.file)
