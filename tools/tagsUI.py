import tkinter as tk
from tkinter import scrolledtext, Menu
import pyperclip

def process_and_display_input():
    """Process the input manually and display it in the output box."""
    input_text = input_box.get("1.0", tk.END).strip()
    processed_items = [item.replace("_", " ") for item in input_text.split()]
    processed_text = ', '.join(processed_items)
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
# Pack the buttons inside the frame with 'expand' and 'fill' to center them
clear_paste_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
process_button.pack(side=tk.LEFT, expand=True, fill=tk.X)
# This might leave a gap on the right; adjust padding or use another method for precise centering if needed

output_label.pack()
output_box.pack()
copy_button.pack()

root.mainloop()
