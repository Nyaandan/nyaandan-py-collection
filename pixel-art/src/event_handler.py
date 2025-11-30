import app_config as cf
import app_state as state
from resources import available_tools
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

def convert_color_from_hex(hex_color: str) -> tuple:
    """Convert a hex color string to an RGB tuple."""
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]  # Remove the '#' character
    if len(hex_color) == 6:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b, 255)  # Return RGB with full opacity
    else:
        raise ValueError("Invalid hex color format. Expected format: #RRGGBB")

def event_cell_click(event, cell):
    """Handle cell click events to change the background color of the clicked cell."""
    x = (cell - 1) % state.canvas_width
    y = (cell - 1) // state.canvas_width
    # print(f"Cell clicked at ({x}, {y}) with ID {cell}")

    match state.current_tool:
        case "pen":
            color = state.current_color_primary
            state.canvas.itemconfig(cell, fill=color)
            state.canvas_grid[x][y] = color
            state.current_cell = cell

        case "del":
            color = cf.cell_color_empty
            state.canvas.itemconfig(cell, fill=color)
            state.canvas_grid[x][y] = None
            state.current_cell = cell

        case "fll":
            color = state.current_color_primary
            # Flood fill algorithm
            target_color = state.canvas_grid[x][y]
            if target_color == color:
                return  # No need to fill if the color is the same

            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if (
                    0 <= cx < state.canvas_width and
                    0 <= cy < state.canvas_height and
                    state.canvas_grid[cx][cy] == target_color
                ):
                    cell_id = cy * state.canvas_width + cx + 1
                    state.canvas.itemconfig(cell_id, fill=color)
                    state.canvas_grid[cx][cy] = color
                    stack.extend([
                        (cx + 1, cy),
                        (cx - 1, cy),
                        (cx, cy + 1),
                        (cx, cy - 1)
                    ])
            state.current_cell = cell

        case _:
            print(f"Unknown tool: {state.current_tool}")
    
    
def event_cell_enter(event, cell):
    """Handle cell hover events to change the background color of the hovered cell."""
    state.canvas.itemconfig(cell, fill="lightgrey")
    state.current_cell = cell

def event_cell_leave(event, cell):
    """Handle cell leave events to reset the background color of the cell."""
    x = (cell - 1) % state.canvas_width
    y = (cell - 1) // state.canvas_width
    color = state.canvas_grid[x][y] or cf.cell_color_empty
    state.canvas.itemconfig(cell, fill=color)
    state.current_cell = None

def event_select_color(color, main: bool = True):
    """Handle color selection events to change the current tool's color."""
    if not color:
        print("No color selected.")
        return
    if main:
        state.current_color_primary = color
    else:
        state.current_color_secondary = color
    print(f"Selected {'main' if main else 'secondary'} color: {color}")

def event_tool_select(tool: str):
    """Handle tool selection events to change the current tool."""
    if tool in available_tools:
        state.current_tool = tool
        print(f"Selected tool: {tool}")
    else:
        print(f"Tool '{tool}' is not available.")

def event_change_pixel_size(dim: str, new_size: str):
    try:
        size = int(new_size)
        if size <= 0:
            raise ValueError("Pixel size must be a positive number.")
        if dim == "width":
            cf.pixel_size = (size, cf.pixel_size[1])
        elif dim == "height":
            cf.pixel_size = (cf.pixel_size[0], size)
        else:
            raise ValueError("Invalid dimension specified.")
        print(f"Changed pixel size to {cf.pixel_size}.")
    except ValueError as e:
        messagebox.showerror("Invalid Entry", "Pixel height must be a positive number.")
        print(f"Invalid pixel height: {e}")

def event_undo():
    """Handle undo events."""
    print("Undo action triggered. Not yet implemented.")

def event_redo():
    """Handle redo events."""
    print("Redo action triggered. Not yet implemented.")

"""No longer needed, as it's the same as creating a new project."""
def event_clear_canvas():
    """Handle clear canvas events to reset the canvas grid."""
    for i in range(state.canvas_height):
        for j in range(state.canvas_width):
            state.canvas_grid[i][j] = None
            x = j * cf.cell_size_default
            y = i * cf.cell_size_default
            cell = state.canvas.find_closest(x, y)
            state.canvas.itemconfig(cell[0], fill=cf.cell_color_empty)
    print("Canvas cleared.")

"""Unused for now."""
def event_change_theme():
    print( "Changing theme..." )
    """Handle theme change events."""
    if cf.current_theme == "light":
        cf.current_theme = "dark"
        cf.app_color_bg = "#555555"
        cf.app_color_text = "#55aa55"
        cf.app_color_highlight = "#aa4343"
    else:
        cf.current_theme = "light"
        cf.app_color_bg = "#ddddff"
        cf.app_color_text = "#000000"
        cf.app_color_highlight = "#881177"
    
    print(f"Theme changed to {cf.current_theme}.")
    # Update the UI elements to reflect the new theme