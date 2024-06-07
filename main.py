import tkinter as tk
from tkinter import scrolledtext
import re

# Function to extract and sort reference designators
def extract_reference_designators():
    text = text_box.get("1.0", tk.END)
    lines = text.split("\n")
    references = []

    for line in lines:
        if '(property "Reference"' in line:
            parts = line.split('"')
            if len(parts) > 3:
                references.append(parts[3])

    # Sort references based on alphanumeric value
    def sort_key(ref):
        match = re.match(r"([A-Za-z]+)(\d+)", ref)
        if match:
            return match.group(1), int(match.group(2))
        return ref, 0  # default return in case there's no match

    references = sorted(set(references), key=sort_key)

    if references:
        result = "\n".join(references)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, result)
    else:
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "No reference designators found.")

# Function to clear the text box
def clear_text_box():
    text_box.delete("1.0", tk.END)

# Function to enable right-click copy functionality
def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)

# Create the main window
window = tk.Tk()
window.title("Reference Designator Extractor")

# Create and place the text box
text_box = scrolledtext.ScrolledText(window, width=100, height=20)
text_box.pack(padx=10, pady=10)

# Bind right-click to show context menu
text_box.bind("<Button-3>", show_context_menu)

# Create a context menu for right-click functionality
context_menu = tk.Menu(window, tearoff=0)
context_menu.add_command(label="Copy", command=lambda: window.focus_get().event_generate('<<Copy>>'))
context_menu.add_command(label="Cut", command=lambda: window.focus_get().event_generate('<<Cut>>'))
context_menu.add_command(label="Paste", command=lambda: window.focus_get().event_generate('<<Paste>>'))

# Create and place the buttons
extract_button = tk.Button(window, text="Extract Reference Designators", command=extract_reference_designators)
extract_button.pack(pady=5)

clear_button = tk.Button(window, text="Clear", command=clear_text_box)
clear_button.pack(pady=5)

# Start the GUI event loop
window.mainloop()
