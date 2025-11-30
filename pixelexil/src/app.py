import tkinter as tk
from tkinter import messagebox
from tkinter import colorchooser
import app_config as cf
import app_state as state
import event_handler as handler
import resources
import save_handler as savester
from PIL import Image, ImageTk
from datetime import datetime

def prepare_root():
    root = tk.Tk()
    root.title(cf.app_title)
    root.configure(bg=cf.app_color_bg)
    root.resizable(cf.app_resizable, cf.app_resizable)
    cf.app_geometry_max = (root.winfo_screenwidth(), root.winfo_screenheight())
    root.maxsize(*cf.app_geometry_max)
    root.minsize(*cf.app_geometry_min)
    root.configure(cursor="cross")
    return root

def grid_place_next(widget: tk.Widget, row = -1):
    parent = widget.master
    dims = parent.grid_size()
    col = 0

    if row == -1:
        row = dims[0]
    else:
        col = dims[1]
        
    widget.grid(row=row, column=col, sticky="nsew")
    
def setup_canvas(root: tk.Tk):
    canvas = tk.Canvas(root, name="canvas", bg=cf.app_color_bg, highlightthickness=0,
            width=state.canvas_width * cf.cell_size_default, height=state.canvas_height * cf.cell_size_default)
    canvas.grid(row=1, column=1, rowspan=2, sticky="nsew")
    state.canvas = canvas
    state.canvas_grid = [[None for _ in range(state.canvas_width)] for _ in range(state.canvas_height)]

    canvas.bind("<Button-3>", lambda event:canvas.scan_mark(event.x, event.y))
    canvas.bind("<B3-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))
    canvas.bind("<MouseWheel>", lambda event: canvas.scale("all", event.x, event.y, 1.1 if event.delta > 0 else 0.9, 1.1 if event.delta > 0 else 0.9))

    draw_canvas(canvas)

def draw_canvas(canvas: tk.Canvas):
    """Draw the grid on the canvas."""
    for i in range(state.canvas_height):
        for j in range(state.canvas_width):
            x1 = j * cf.cell_size_default
            y1 = i * cf.cell_size_default
            x2 = x1 + cf.cell_size_default
            y2 = y1 + cf.cell_size_default
            color = state.canvas_grid[i][j] or cf.cell_color_empty  # Default to empty color if not set
            cell = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=0.4)

            canvas.tag_bind(cell, "<Enter>", lambda e, cell=cell: handler.event_cell_enter(e, cell))  # Change color on hover
            canvas.tag_bind(cell, "<Leave>", lambda e, cell=cell: handler.event_cell_leave(e, cell))  # Reset color on leave
            canvas.tag_bind(cell, "<Button-1>", lambda e, cell=cell: handler.event_cell_click(e, cell))

def setup_tools_panel(root: tk.Tk):
    """Setup the command panel with buttons and tools."""
    panel = tk.Frame(root, width=120, name="command_panel", bg=cf.app_color_bg, pady=24)
    panel.grid(row=1, column=0, sticky="ns")

    pack_opts = {
        "fill": tk.X, "side": tk.TOP, "padx": 8, "pady": 4 }
    btn_options = {
        "border": 8, "compound": tk.CENTER, "relief": tk.RAISED }

    for i, tool in enumerate(resources.available_tools):
        btn = tk.Button(panel, name=f"tool_{tool}", image=resources.tool_icons[tool], **btn_options,
                command=lambda i=i, t=tool: click_tool_button(panel, i, t))
        btn.pack(**pack_opts)
        
    btn_color_picker = tk.Button(panel, image=resources.color_picker_icon, **btn_options,
            command=lambda: handler.event_select_color(colorchooser.askcolor()[1], main=True))
    btn_color_picker.pack(pack_opts)

def click_tool_button(panel:tk.Widget, i: int, tool: str):
    """Simulate a click on a tool button."""
    buttons = [c for c in panel.winfo_children() if isinstance(c, tk.Button) and c.winfo_name().startswith("tool_")]
    for btn in buttons:
        btn.config(relief=tk.RAISED)
    buttons[i].config(relief=tk.SUNKEN)
    handler.event_tool_select(tool)

def setup_settings_panel(root: tk.Tk):
    """Setup the settings panel with options for the application."""
    settings_panel = tk.Frame(root, name="settings_panel", bg=cf.app_color_bg, pady=4)
    settings_panel.grid(row=2, column=0, sticky="ns")

    # Add a button to change the theme
    # btn_change_theme = tk.Button(settings_panel, text="Change Theme", command=handler.event_change_theme)
    # btn_change_theme.grid(row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=4)

    label_options = { "bg": cf.app_color_bg, "fg": cf.app_color_text, "anchor": "w", "font":("Cambria", 10) }
    entry_options = { "width": 3, "justify": "right", "font":("Algerian", 11) }

    for element in ("width", "height"):
        index = 0 if element == "width" else 1
        label = tk.Label(settings_panel, text=f"Pixel {element.capitalize()}:", **label_options)
        label.grid(row=index+2, column=0, sticky="w", pady=4)
        entry = tk.Entry(settings_panel, **entry_options)
        entry.insert(0, str(cf.pixel_size_default[index]))
        entry.grid(row=index+2, column=1, sticky="e", padx=2, pady=4)
        entry.bind("<Return>", lambda e, el=element: handler.event_change_pixel_size(el, e.widget.get()))
        entry.bind("<FocusOut>", lambda e, el=element: handler.event_change_pixel_size(el, e.widget.get()))
    

def setup_menu_bar(root: tk.Tk):
    """Create a menu bar with File, Edit, and Help options."""
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    root.bind("<Control-n>", lambda e: new_project(root))
    root.bind("<Control-o>", lambda e: load_project(root))
    root.bind("<Control-s>", lambda e: save_project(root))
    root.bind("<Control-e>", lambda e: save_image(root))
    root.bind("<Control-q>", lambda e: root.quit())

    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New", command=lambda: new_project(root), accelerator="Ctrl+N")
    file_menu.add_command(label="Open", command=lambda: load_project(root), accelerator="Ctrl+O")
    file_menu.add_command(label="Save", command=lambda: save_project(root), accelerator="Ctrl+S")
    file_menu.add_command(label="Export", command=lambda: save_image(root), accelerator="Ctrl+E")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit, accelerator="Ctrl+Q")
    menubar.add_cascade(label="File", menu=file_menu)

    """
    # Edit menu
    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Undo", command=lambda: handler.event_undo(), accelerator="Ctrl+Z")
    edit_menu.add_command(label="Redo", command=lambda: handler.event_redo(), accelerator="Ctrl+Y")
    menubar.add_cascade(label="Edit", menu=edit_menu)
    """

    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Tkinter Application"))
    menubar.add_cascade(label="Help", menu=help_menu)

def setup_status_bar(root: tk.Tk):
    """Create a status bar at the bottom of the application."""
    status_bar = tk.Frame(root, name="status_bar", bg=cf.app_color_bg, bd=1, relief=tk.SUNKEN)
    status_bar.grid(row=3, column=0, columnspan=3, sticky="ew")

    # Status for the current tool
    var_current_tool = tk.StringVar(value=f"Current Tool: {state.current_tool}")
    tool_label = tk.Label(status_bar, name="status_tool", textvariable=var_current_tool, bg=cf.app_color_bg, fg=cf.app_color_text)
    tool_label.pack(side="left", padx=5, pady=5)

    root.bind("<Configure>", lambda e: var_current_tool.set(f"Current Tool: {state.current_tool}"))

    # Status for the current color
    var_current_color = tk.StringVar(value=f"Current Color: {state.current_color_primary}")
    color_label = tk.Label(status_bar, name="status_color", textvariable=var_current_color, bg=cf.app_color_bg, fg=cf.app_color_text)
    color_label.pack(side="left", padx=5, pady=5)
    
    root.bind("<Configure>", lambda e: var_current_color.set(f"Current Color: {state.current_color_primary}"))
    
    # Status for the current cell
    var_current_cell = tk.StringVar(value="Current Cell: (,)")
    status_label = tk.Label(status_bar, name="status_cell", textvariable=var_current_cell, bg=cf.app_color_bg, fg=cf.app_color_text)
    status_label.pack(side="left", padx=5, pady=5)
    
    state.canvas.bind("<Motion>", lambda e: var_current_cell.set(
        f"Current Cell: ({e.x // cf.cell_size_default}, {e.y // cf.cell_size_default})"))
    state.canvas.bind("<Leave>", lambda e: var_current_cell.set("Current Cell: (_, _)"))

    # Debugging
    # btn_debug = tk.Button(status_bar, text="Debugging", command=lambda: make_debugging_area(root))
    # btn_debug.pack(side=tk.RIGHT, fill=tk.Y, padx=8, pady=2)

def configure_grid(root: tk.Tk):
    """Configure the grid layout for the root window."""
    root.grid_rowconfigure(0, weight=1)  # Title row
    root.grid_rowconfigure(1, weight=6)  # Main content area
    root.grid_rowconfigure(2, weight=1)  # Command panel
    root.grid_columnconfigure(0, weight=2)  # Command panel
    root.grid_columnconfigure(1, weight=6)  # Main canvas area
    root.grid_columnconfigure(2, weight=2)  # Details panel

def add_events(root: tk.Tk):
    """Add event bindings to the root window."""
    root.bind("<KeyPress>", lambda e: root.quit() if e.keysym == "Escape" else print(f"Key pressed: {e.keysym}"))  # Escape to quit
    #root.bind("<Configure>", lambda e: print(f"Window resized to: {e.width}x{e.height}"))  # Print window resize events

def make_debugging_area(root: tk.Tk):
    """Setup debugging features for the application."""
    debug_window = tk.Toplevel(root, name="debug_window", bg=cf.app_color_bg)
    debug_window.title("Debugging Area")
    debug_window.geometry("300x200")
    debug_window.resizable(False, False)
    debug_window.protocol("WM_DELETE_WINDOW", lambda: debug_window.withdraw())  # Hide instead of destroy

    debug_frame = tk.Frame(debug_window, name="debug_frame", bg=cf.app_color_bg)
    debug_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    debug_1 = tk.Label(debug_frame, text=f"Current Theme: {cf.current_theme}")
    var_1 = tk.StringVar(value=f"Current Theme: {cf.current_theme}")
    debug_1.configure(textvariable=var_1)
    debug_1.pack(side="top", fill=tk.X, padx=5, pady=5)

    debug_2 = tk.Label(debug_frame, text="Tool")
    var_2 = tk.StringVar(value="Tool: None")
    debug_2.configure(textvariable=var_2)
    debug_2.pack(side="top", fill=tk.X, padx=5, pady=5)

    root.bind("<Motion>", lambda e: var_1.set(f"Current Over: {e.widget.winfo_name()}"), '+')
    return debug_window

def new_project(root: tk.Tk):
    """Create a new project by resetting the canvas."""
    if messagebox.askyesno("New Project", "Are you sure you want to create a new project? This will clear the current canvas."):
        state.canvas_grid = [[None for _ in range(state.canvas_width)] for _ in range(state.canvas_height)]
        for y in range(state.canvas_height):
            for x in range(state.canvas_width):
                cell_id = (y * state.canvas_width) + x + 1
                state.canvas.itemconfig(cell_id, fill=cf.cell_color_empty)

def load_project(root: tk.Tk):
    """Load a project from a file."""
    try:
        savester.load_project(root)
    except Exception as e:
        messagebox.showerror("Load Error", f"Failed to load project: {e}")
        print(f"Error loading project: {e}")
        return
    
    for y in range(state.canvas_height):
        for x in range(state.canvas_width):
            cell_id = (y * state.canvas_width) + x + 1
            color = state.canvas_grid[x][y] or cf.cell_color_empty
            state.canvas.itemconfig(cell_id, fill=color)

def save_project(root: tk.Tk):
    """Save the current project."""
    if not state.canvas:
        messagebox.showerror("Error", "No canvas to save.")
        return
    if not state.canvas_grid:
        messagebox.showerror("Error", "Canvas is empty, nothing to save.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{timestamp}.png"
    try:
        savester.save_project(root)
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save project: {e}")
        print(f"Error saving canvas: {e}")

def save_image(root: tk.Tk):
    """Save the current canvas as an image."""
    if not state.canvas:
        messagebox.showerror("Error", "No canvas to save.")
        return
    if not state.canvas_grid:
        messagebox.showerror("Error", "Canvas is empty, nothing to save.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{timestamp}.png"
    try:
        savester.export_as_image(filename)
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save canvas: {e}")
        print(f"Error saving canvas: {e}")

def main():
    root = prepare_root()
    resources.load_resources()

    setup_canvas(root)
    setup_tools_panel(root)
    setup_settings_panel(root)
    setup_menu_bar(root)
    setup_status_bar(root)
    configure_grid(root)
    click_tool_button(root.nametowidget("command_panel"), 0, "pen")

    for widget in root.winfo_children():
        widget.configure()

    add_events(root)
    
    make_debugging_area(root).mainloop()
    root.mainloop()

if __name__ == "__main__":
    main()