from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import app_state as state
import app_config as config


def export_as_image(filename: str):
    """Save the current canvas as an image file."""
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        initialdir=config.last_save_directory or ".",
        initialfile=filename)
    if not path:
        print("Save operation cancelled.")
        return
    
    print(f"Saving canvas as {filename}...")
    cell_width = config.pixel_size[0]
    cell_height = config.pixel_size[1]
    width, height = state.canvas_width, state.canvas_height
    image = Image.new("RGBA", (width * cell_width, height * cell_height), "white")

    for y in range(height):
        for x in range(width):
            color = state.canvas_grid[x][y]
            cell = Image.new("RGBA", (cell_width, cell_height), color)
            image.paste(cell, (x * cell_width, y * cell_height))

    image.save(path)
    config.last_save_directory = path.rsplit('/', 1)[0]
    print(f"Canvas saved as {filename}")

def save_project(root: tk.Tk):
    """Save the current project state to a file."""
    filename = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        initialdir=config.last_save_directory or ".",
        initialfile="project.json")
    if not filename:
        print("Save operation cancelled.")
        return
    
    state_data = state.export_state()
    with open(filename, 'w') as f:
        import json
        json.dump(state_data, f, indent=4)
    
    config.last_save_directory = filename.rsplit('/', 1)[0]
    print(f"Project saved as {filename}")

def load_project(root: tk.Tk):
    """Load a project state from a file."""
    filename = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        initialdir=config.last_save_directory or ".")
    if not filename:
        print("Load operation cancelled.")
        return
    
    with open(filename, 'r') as f:
        import json
        state_data = json.load(f)
    
    state.import_state(state_data)
    print(f"Project loaded from {filename}")
    