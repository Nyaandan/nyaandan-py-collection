import tkinter as tk

available_tools = ["pen", "del", "fll"] # Brush, Eraser, Fill

tool_icons: dict[str, tk.PhotoImage] = {}
tool_paths = [
    "assets/pixel_pen.png",
    "assets/pixel_towel.png",
    "assets/pixel_bucket.png"
]
color_picker_icon: tk.PhotoImage
color_picker_path = "assets/pixel_palette.png"

def load_resources():
    global tool_icons, color_picker_icon
    """Load all resources needed for the application."""
    for i, tool in enumerate(available_tools):
        try:
            tool_icons[tool] = tk.PhotoImage(file=tool_paths[i])
        except Exception as e:
            print(f"Error loading {tool} icon: {e}")
    try:
        color_picker_icon = tk.PhotoImage(file=color_picker_path)
    except Exception as e:
        print(f"Error loading resources: {e}")