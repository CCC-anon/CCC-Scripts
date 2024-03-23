import os

# Define your folder path containing the text files
folder_path = 'path/to/your/folder'

# Lists of common and uncommon hair and eye colors
hair_colors = ['aqua', 'black', 'brown', 'blonde', 'red', 'white', 'grey', 'gray', 'silver', 'blue', 'green', 'pink', 'purple', 'orange', 'yellow', 'cyan', 'magenta']
eye_colors = ['aqua', 'black', 'brown', 'blonde', 'red', 'white', 'grey', 'gray', 'silver', 'blue', 'green', 'pink', 'purple', 'orange', 'yellow', 'cyan', 'magenta', 'hazel', 'amber', 'red', 'violet']

# Function to remove hair and eye colors from a list of tags
def clean_tags(tags):
    cleaned_tags = []
    for tag in tags:
        tag_lower = tag.lower() # Convert to lowercase to ensure case-insensitive matching
        # Check if the tag contains any of the colors (for compound colors like 'green blue')
        if not any(color in tag_lower for color in hair_colors + eye_colors):
            cleaned_tags.append(tag)
    return cleaned_tags

# Process each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"): # Ensure we are only reading .txt files
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            tags = content.split(', ') # Split the content by comma to get the tags
            cleaned_tags = clean_tags(tags)
            cleaned_content = ', '.join(cleaned_tags)
        # Write the cleaned content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

print("Files have been processed.")
