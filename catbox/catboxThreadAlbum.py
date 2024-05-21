import re
import requests
import argparse

def fetch_content_and_extract_filenames(url, seen_albums, seen_filenames):
    # Regex to detect file and potential album links
    file_link_pattern = re.compile(r'https://files\.catbox\.moe/[\w\-.]+(?:\.jpg|\.jpeg|\.png|\.webm)')
    album_link_pattern = re.compile(r'https://catbox\.moe/c/[\w\-.]+')  # Corrected album URL pattern

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        content = response.text
        
        # Extract all file links
        file_links = file_link_pattern.findall(content)
        filenames = []
        for link in file_links:
            filename = link.split('/')[-1]
            if filename not in seen_filenames:
                seen_filenames.add(filename)
                filenames.append(filename)

        # Debugging output to show found filenames
        #print(f"Fetched from {url}: {filenames}")

        # Check for album links within the content, recurse if found
        album_links = album_link_pattern.findall(content)
        for album_link in album_links:
            if album_link not in seen_albums:
                seen_albums.add(album_link)
                additional_filenames = fetch_content_and_extract_filenames(album_link, seen_albums, seen_filenames)
                filenames.extend(additional_filenames)
                
                # Debugging output to show filenames from nested albums
                #print(f"Fetched from album {album_link}: {additional_filenames}")

        return filenames
    except requests.RequestException as e:
        print(f"Failed to fetch URL {url}: {e}")
        return []

def create_album_with_filenames(url):
    # Extract identifier from the URL
    identifier = url.split('/')[-1]
    board_id = url.split('/')[-3]

    seen_filenames = set()
    seen_albums = set(url)

    # Fetch content from the URL and extract filenames
    filenames = fetch_content_and_extract_filenames(url, seen_albums, seen_filenames)
    
    # Debugging output before creating the album
    print(f"Total unique filenames to create album: {filenames}")

    # URL and data for creating the album
    album_url = "https://catbox.moe/user/api.php"
    data = {
        'reqtype': 'createalbum',
        'title': f"Album for /{board_id}/{identifier}",
        'desc': f"Album for /{board_id}/{identifier}",
        'files': ' '.join(filenames)
    }

    # Send request to create the album
    try:
        album_response = requests.post(album_url, data=data)
        if album_response.status_code == 200:
            print("=====================")
            print(f"Detected Unique Filenames: {len(seen_filenames)}")
            print(f"Album created successfully: {album_response.text}")
            print("=====================")
        else:
            print("Failed to create album")
    except requests.RequestException as e:
        print(f"Failed to send album creation request: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an album from images and nested albums within a thread or album with debugging output, ensuring no duplicate filenames while maintaining order.")
    parser.add_argument("url", help="The URL of the thread or album to create an album from.")
    args = parser.parse_args()

    create_album_with_filenames(args.url)
