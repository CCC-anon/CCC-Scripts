# Catbox Scripts

## Disclaimer
The base functionality was initially tested in both Windows and Linux environments, however new edits to the scripts have only been tested on Linux.

## How to use:
* Download the two scripts individually from the release page https://github.com/CCC-anon/CCC-Scripts/releases/tag/v1
  * or copy their text and paste it inside a .py file
  * or clone the whole repository with `git clone https://github.com/CCC-anon/CCC-Scripts`
* open a terminal/cmd/powershell and install the `requests` library for python
  * `pip install requests`
    
## catboxDown.py
This Script has two functionalities:
* You can provide it the URL of a website, in which case it will attempt to parse the website, find any catbox URLs within the website ending in .png, .jpg, jpeg, .webm and then downlaoding them in a directory along the script named according to the last part of the URL. Attention should be paid when the URL contains special characters. The script will attempt to get rid of them but the name will be affected. `https://boards.website.org/x/thread/11111111` might generate a folder named `11111111#p122222222` instead of just `11111111`. Alternatively you can provide a directory name to be created with the arguments `-d` or `--directory`.
  * URL usage: `python catboxDown.py https://boards.website.org/x/thread/11111111`
  * URL usage with directory name provided: `python catboxDown.py https://boards.website.org/x/thread/11111111 -d downloads`

* You can provide it with a text file containing a list of Catbox URLs. The Catbox URLs have to be on a new line. The script will automatically download the images into a new directory based on the name of the text file that was provided.
  * File usage from the same folder: `python catboxDown.py -f links.txt`
  * File usage from another path: `python catboxDown.py -f /path/to/text/file/links.txt`
  * File usage from another path with directory naming: `python catboxDown.py -f /path/to/text/file/links.txt -d notLewds`
 
## catboxUp.py
This Script can take all the files found inside of a folder, upload them to catbox, return the URLs in both console and in a .txt file next to the script file. Optionally it can generate an album from the resulting URLs and provides the album URL as well.
**Do not end the directory path in a slash. Not sure what will happen but it might blow up.**
* Upload files from a folder without album: `python catboxUp.py -f /path/to/your/folder` 
* Upload files from a folder and create an album named 'My Pics': `python catboxUp.py -f /path/to/your/folder -a -t "My Pics"`

## catboxHover.user.js

* This is a userscript for Greasemonkey/Violentmonkey/*monkey
* It displays previews of images hosted on catbox or various sites that come in the form of a URL when hovering over the link.
  * ![preview](https://github.com/CCC-anon/CCC-Scripts/assets/163057682/9ae5a45d-c53d-4c8d-a799-66076932a867)
* It requires you to enable Linkify URLs in board settings ![linkify](https://github.com/CCC-anon/CCC-Scripts/assets/163057682/9ebb25fd-3100-41d7-b103-f789174a3236)
* Then save the contents of the script file in your Userscript extension, save it and reload the page.

## catboxThumbnails.user.js
* This is a userscript for Greasemonkey/Violentmonkey/*monkey
* It loads catbox and litter image links within the thread as clickable thumbnails
* It has a toggle to switch between Thumbnail and Plaintext view
* Before:
  * ![plain](https://github.com/CCC-anon/CCC-Scripts/assets/163057682/1c93bef2-3e9b-42ab-a661-78cd96a161f2)
* After:
  * ![thumbs](https://github.com/CCC-anon/CCC-Scripts/assets/163057682/f1b57833-ef23-44b0-91a4-2294a683929b)
