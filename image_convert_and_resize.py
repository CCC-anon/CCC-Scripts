import os
from shutil import copy2
from PIL import Image

def resize_and_convert_image(input_folder_path, output_folder_path):
    # Ensure the output folder exists
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(input_folder_path):
        # Check if the file is a .jpg or .png
        if filename.lower().endswith(('.jpg', '.png')):
            input_file_path = os.path.join(input_folder_path, filename)

            # Open the image
            with Image.open(input_file_path) as img:
                width, height = img.size
                original_mode = img.mode
                should_save = False  # Flag to determine if we need to save (resize or convert) the image

                # Resize if necessary
                if width > 2048 or height > 2048:
                    if width > height:
                        new_height = int((2048 / width) * height)
                        new_size = (2048, new_height)
                    else:
                        new_width = int((2048 / height) * width)
                        new_size = (new_width, 2048)

                    img = img.resize(new_size, Image.ANTIALIAS)
                    should_save = True

                # Convert "P" or "RGBA" mode images to "RGB"
                if img.mode in ['RGBA', 'P']:
                    img = img.convert('RGB')
                    should_save = True

                # Determine new file path in output folder
                new_filename = filename
                if original_mode in ['RGBA', 'P'] or os.path.getsize(input_file_path) > 5 * 1024 * 1024:
                    new_filename = os.path.splitext(filename)[0] + '.jpeg'
                output_file_path = os.path.join(output_folder_path, new_filename)

                # Save the image if it was resized or converted
                if should_save:
                    img.save(output_file_path, 'JPEG', quality=90)
                else:
                    # Copy the file as is
                    copy2(input_file_path, output_file_path)

# Replace these paths with the actual paths of your folders
input_folder_path = 'path_to_your_input_folder'
output_folder_path = 'path_to_your_output_folder'
resize_and_convert_image(input_folder_path, output_folder_path)
