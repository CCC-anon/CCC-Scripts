import tkinter as tk
from tkinter import scrolledtext, Menu
import pyperclip
import re  # Import regular expressions for checks

# List of words to check against
words_to_remove = ['patreon', 'twitter', 'artist name', 'commentary', 'bad id', 'bad pixiv id']

def is_alphanumeric_first_char(s):
    """Check if the first character of the string is alphanumeric."""
    return bool(re.match(r'^[a-zA-Z0-9]', s))

def get_alphanumeric_prefix(s):
    """Extract the leading alphanumeric part of the string."""
    match = re.match(r'\w+', s)
    return match.group() if match else ""

def find_reset_point(tags):
    """Find the reset point where alphanumeric order is reset, considering only alphanumeric prefixes."""
    last_prefix = ""
    for i, tag in enumerate(tags):
        current_prefix = get_alphanumeric_prefix(tag)
        if current_prefix < last_prefix:
            return i
        last_prefix = current_prefix
    return -1

def process_and_display_input():
    """Process the input manually, check against a list of words, rearrange based on reset point, and display it in the output box."""
    input_text = input_box.get("1.0", tk.END).strip()
    tags = [item.replace("_", " ").replace("(", r"\(").replace(")", r"\)") for item in input_text.split()]

    # Filter out tags that do not start with an alphanumeric character
    tags = [tag for tag in tags if is_alphanumeric_first_char(tag)]

    # Further filter out tags containing any of the words to remove
    filtered_tags = [tag for tag in tags if not any(word in tag for word in words_to_remove)]

    # Find the reset point in the alphanumeric order
    reset_point = find_reset_point(filtered_tags)

    # Rearrange tags if a reset point is found
    if reset_point != -1:
        filtered_tags = filtered_tags[reset_point:] + filtered_tags[:reset_point]

    processed_text = ', '.join(filtered_tags)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.INSERT, processed_text)

def copy_output_to_clipboard():
    """Copy the text from the output box to the clipboard."""
    output_text = output_box.get("1.0", tk.END).strip()
    pyperclip.copy(output_text)

def clear_and_paste_from_clipboard():
    """Clear the input box and then paste the clipboard content into it."""
    input_box.delete("1.0", tk.END)  # Clear the input box
    clipboard_content = pyperclip.paste()
    input_box.insert(tk.INSERT, clipboard_content)

# Create the main window
root = tk.Tk()
root.title("Input/Output Processor")

# Create a Text box for input
input_label = tk.Label(root, text="Input:")
input_box = scrolledtext.ScrolledText(root, height=5, width=40)

# Create a Text box for output
output_label = tk.Label(root, text="Output:")
output_box = scrolledtext.ScrolledText(root, height=5, width=40, bg="light grey")

# Create a frame for the buttons to organize them horizontally
button_frame = tk.Frame(root)

# Initialize buttons within the button frame
clear_paste_button = tk.Button(button_frame, text="Clear & Paste", command=clear_and_paste_from_clipboard)
process_button = tk.Button(button_frame, text="Process", command=process_and_display_input)
copy_button = tk.Button(root, text="Copy Output", command=copy_output_to_clipboard)

# Pack everything in the desired order
input_label.pack()
input_box.pack()
button_frame.pack(fill=tk.X, padx=5, pady=5)
clear_paste_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
process_button.pack(side=tk.LEFT, expand=True, fill=tk.X)
output_label.pack()
output_box.pack()
copy_button.pack()

root.mainloop()
