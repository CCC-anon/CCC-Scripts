# CCC-Scripts

**Collection of scripts used for Stable Diffusion related activites like Dataset Manipulation, Caption pruning, etc**
* Most scripts have been created with the use of ChatGPT.
* They have been tested on Linux-only.
* If the Python scripts import modules at the beginning of the script, you might have to install those modules before being able to run the script
    * E.g.: If the .py file content starts with `from PIL import image` it might require you to first execute `pip install pillow` before running the script if it is not installed already.
* Feel free to fork, copy, use the scripts on your own projects as long as you do not ask me to fit your project's needs. (MIT License, no warranty).
* Some of the scripts work on the live files instead of creating a copy, therefore **ALWAYS** use them on a copy of your dataset instead of the real deal.

### **image_convert_and_resize.py**
Automatically parses all jpg/png files in a directory and resizes if their width/height are too big or converts them to jpeg 90% quality if their filesize is above >5mb. Set Input and Output path inside the script
### **remove_hair_and_eye_colors.py**
Parses a folder containing multiple .txt files with comma separated tags inside. Removes most instances of `<color> hair` or `<color> eyes`. If any colors slipped my set-up, feel free to change the list and include those colors in the hair or eye section.
### **combine_to_wildcard.py**
Parses the .txt files inside of a folder and combines them into a single file called `wildcards.txt`. The file will be made up of the contents of all of the other files merged into a single file, with each caption on a single line, ready to be used as a wildcard for prompting.
### **tagsUI.py**
Simple python tkinter interface that can translate from 'Grabber' tags to 'SD' tags ('blue_dress green_boots' becomes 'blue dress, green boots'). It can copy the output to clipboard.
Requires: 
* tkinter to be installed (https://tkdocs.com/tutorial/install.html - usually installed by default in python 3.1+) 
* pyperclip (`pip install pyperclip`). 
On Linux, pyperclip requires one of the following clipboard tools to be installed for the clipboard function to work:
   * xclip (`sudo apt-get install xclip`)
   * xsel (`sudo apt-get install xsel`)
   * gtk
   * qt
* Copy the tagsUI.py file somewhere on your computer
* Open a terminal/poweshell and go to the directory where you copied the file
* `python tagsUI.py`  
![tagsUI](https://github.com/CCC-anon/CCC-Scripts/assets/163057682/18e2ea79-3336-411a-a78b-d4c55dad5847)
