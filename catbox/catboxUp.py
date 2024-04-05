import os
import requests
import argparse

def upload_files(directory_path):
    upload_url = "https://catbox.moe/user/api.php"
    uploaded_files_urls = []

    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            files = {'fileToUpload': (filename, open(os.path.join(directory_path, filename), 'rb'))}
            data = {'reqtype': 'fileupload'}
            response = requests.post(upload_url, files=files, data=data)
            if response.status_code == 200:
                print(f"Uploaded {filename}: {response.text}")
                uploaded_files_urls.append(response.text)
            else:
                print(f"Failed to upload {filename}")

    return uploaded_files_urls

def save_urls_to_file(directory_name, urls):
    with open(f"{directory_name}.txt", 'w') as file:
        for url in urls:
            file.write(url + '\n')

def extract_filenames(urls):
    filenames = [url.split('/')[-1] for url in urls]
    return filenames

def create_anonymous_album(filenames, album_title):
    album_url = "https://catbox.moe/user/api.php"
    data = {
        'reqtype': 'createalbum',
        'title': album_title,
        'desc': 'Automatically created album of uploaded files',
        'files': ' '.join(filenames)
    }
    response = requests.post(album_url, data=data)
    if response.status_code == 200:
        print("Album created successfully: " + response.text)
    else:
        print("Failed to create album")

def main(folder_path, create_album, album_title):
    directory_name = os.path.basename(folder_path.rstrip(os.sep))
    uploaded_files_urls = upload_files(folder_path)
    
    if uploaded_files_urls:
        save_urls_to_file(directory_name, uploaded_files_urls)
        if create_album:
            filenames = extract_filenames(uploaded_files_urls)
            create_anonymous_album(filenames, album_title)
        else:
            print("Album creation skipped.")
    else:
        print("No files were uploaded.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload files to Catbox and optionally create an album.")
    parser.add_argument("-f", "--folder", required=True, help="Path to the folder containing files to upload.")
    parser.add_argument("-a", "--album", action='store_true', help="Flag to create an anonymous album with uploaded files.")
    parser.add_argument("-t", "--title", default="My Uploaded Files", help="Title for the album, if album creation is enabled.")
    
    args = parser.parse_args()
    
    main(args.folder, args.album, args.title)
