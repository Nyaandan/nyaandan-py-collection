import tkinter as tk

canvas: tk.Canvas
status_bar: tk.Widget

canvas_width: int = 32  # Number of columns in the grid
canvas_height: int = 32  # Number of rows in the grid
canvas_grid: list[list[str | None]]  # 2D list to track the colors of each cell

current_tool = "pen"  # Track the currently selected tool
current_color_primary = "#000000"  # Default color for the main tool
current_color_secondary = "#441144"  # Default color for the secondary tool
current_cell = (0, 0)  # Track the currently selected cell

def export_state():
    """Export the current state of the application."""
    return {
        "canvas_width": canvas_width,
        "canvas_height": canvas_height,
        "canvas_grid": canvas_grid,
        "current_tool": current_tool,
        "current_color_primary": current_color_primary,
        "current_color_secondary": current_color_secondary,
        "current_cell": current_cell
    }

def import_state(state: dict):
    """Import a previously saved state into the application."""
    global canvas_width, canvas_height, canvas_grid, current_tool, current_color_primary, current_color_secondary, current_cell
    canvas_width = state.get("canvas_width", 32)
    canvas_height = state.get("canvas_height", 32)
    canvas_grid = state.get("canvas_grid", [[None] * canvas_height for _ in range(canvas_width)])
    current_tool = state.get("current_tool", "pen")
    current_color_primary = state.get("current_color_primary", "#000000")
    current_color_secondary = state.get("current_color_secondary", "#441144")
    current_cell = state.get("current_cell", (0, 0))

def reset_state():
    """Reset the application state to default values."""
    global canvas_width, canvas_height, canvas_grid, current_tool, current_color_primary, current_color_secondary, current_cell
    canvas_width = 32
    canvas_height = 32
    canvas_grid = [[None] * canvas_height for _ in range(canvas_width)]
    current_tool = "pen"
    current_color_primary = "#000000"
    current_color_secondary = "#441144"
    current_cell = (0, 0)