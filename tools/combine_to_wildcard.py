import os

# Define your folder path containing the text files
folder_path = 'path/to/your/folder'
# Define the path for the new combined file
combined_file_path = os.path.join(folder_path, 'wildcards.txt')

# Open the combined file in write mode
with open(combined_file_path, 'w', encoding='utf-8') as combined_file:
    # Process each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Ensure we are only reading .txt files
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()  # Read and strip whitespace from the content
                # Remove newline characters from the content
                content_no_newlines = content.replace('\n', ' ')
                # Write the modified content to the combined file, followed by a newline character
                combined_file.write(content_no_newlines + '\n')

print("All files have been combined into wildcards.txt.")
