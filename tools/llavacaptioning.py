import base64
import requests
import os
import json

CONTEXT = "You are LLaVA, a large language and vision assistant trained by UW Madison WAIV Lab. You are able to understand the visual content that the user provides, and assist the user by using natural language. Follow the instructions carefully and explain your answers in detail.### Human: Hi!### Assistant: Hi! I am your assistant, please let me know how I can help.\n"

# Folder containing your images and captions
folder_path = 'path/to/folder'

# Initialize the counter for processed images
processed_count = 0

# Count the total number of images in the folder (excluding .txt files)
total_images = sum(1 for file in os.listdir(folder_path) if file.endswith('.jpg'))

# List of words to check in the description
words_to_check = ['LLaVA', 'cannot', 'text-based', 'acceptable', 'language', 'appropriate']

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg'):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)

        # Initialize description length and presence of specified words to enter the loop
        description_length = 0
        has_specified_words = False

        while description_length < 100 or has_specified_words:
            with open(file_path, 'rb') as f:
                img_str = base64.b64encode(f.read()).decode('utf-8')

            # Read existing caption from the corresponding .txt file
            caption_file_path = os.path.splitext(file_path)[0] + '.txt'
            with open(caption_file_path, 'r') as caption_file:
                text = caption_file.read().strip()
            

            prompt = CONTEXT + f'### Human: Evaluate the accuracy of your previous response and provide a revised image caption, describing the image in detail. The current caption is {text}: \n<img src="data:image/jpeg;base64,{img_str}">### Assistant: '
                
            # Make the API request
            response = requests.post('http://127.0.0.1:5000/v1/completions', json={'prompt': prompt, 'max_tokens': 200, 'stop': ['\n###']})
                
            # Parse the JSON response
            response_data = response.json()

            # Extract the description from the response
            description = response_data['choices'][0]['text']

            # Update the description length
            description_length = len(description)

            # Check for the presence of specified words
            has_specified_words = any(word in description.lower() for word in words_to_check)

            if description_length < 100 or has_specified_words:
                print(f'Reprocessing {filename} as the description is less than 100 characters or contains specified words.')

        # Save the description in a text file with the same filename
        output_file_path = os.path.splitext(file_path)[0] + '.txt'
        with open(output_file_path, 'w') as output_file:
            output_file.write(description)

        processed_count += 1
        initial_description = text
#        print(f'Initial description: {initial_description}')
        print(f'Processed {filename} and saved the description in {output_file_path}\nInitial description: {initial_description}\nDescription: {description}\n ({processed_count}/{total_images} images processed)')

