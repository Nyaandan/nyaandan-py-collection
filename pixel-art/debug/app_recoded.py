import sys
import pygame
import tkinter as tk
from tkinter import simpledialog, colorchooser

# --- Config ---
TOOL_BRUSH = "Brush"
TOOL_ERASER = "Eraser"
TOOL_PICKER = "Picker"
TOOLS = [TOOL_BRUSH, TOOL_ERASER, TOOL_PICKER]
PANEL_WIDTH = 100
PREVIEW_WIDTH = 100
BG_COLOR = (40, 40, 40)
GRID_COLOR = (60, 60, 60)
PREVIEW_BG = (80, 80, 80)
PIXEL_SIZE = 20
MIN_ZOOM = 5
MAX_ZOOM = 60

# --- Helper functions ---
def ask_grid_size():
    root = tk.Tk()
    root.withdraw()
    w = simpledialog.askinteger("Grid Width", "Enter grid width (pixels):", minvalue=4, maxvalue=128)
    h = simpledialog.askinteger("Grid Height", "Enter grid height (pixels):", minvalue=4, maxvalue=128)
    root.destroy()
    return w or 16, h or 16

def ask_color(init_color):
    root = tk.Tk()
    root.withdraw()
    color = colorchooser.askcolor(color=init_color)
    root.destroy()
    if color[0]:
        return tuple(map(int, color[0]))
    return init_color

# --- Main App ---
class PixelArtApp:
    def __init__(self, grid_w, grid_h):
        pygame.init()
        self.grid_w, self.grid_h = grid_w, grid_h
        self.zoom = PIXEL_SIZE
        self.offset = [0, 0]
        self.dragging = False
        self.last_mouse = (0, 0)
        self.selected_tool = TOOL_BRUSH
        self.selected_color = (255, 0, 0)
        self.grid = [[None for _ in range(grid_h)] for _ in range(grid_w)]
        self.screen_w = PANEL_WIDTH + grid_w * PIXEL_SIZE + PREVIEW_WIDTH
        self.screen_h = max(400, grid_h * PIXEL_SIZE)
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Pixel Art App")
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)
            self.draw()
        pygame.quit()

    def handle_event(self, event):
        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mx < PANEL_WIDTH:
                self.handle_tools_panel_click(my)
            elif mx > self.screen_w - PREVIEW_WIDTH:
                pass  # Preview panel, do nothing
            elif event.button == 1:
                self.handle_canvas_click(mx, my)
            elif event.button == 3:
                self.dragging = True
                self.last_mouse = (mx, my)
            elif event.button == 4:  # Wheel up
                self.zoom = min(MAX_ZOOM, self.zoom + 2)
            elif event.button == 5:  # Wheel down
                self.zoom = max(MIN_ZOOM, self.zoom - 2)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx, dy = event.rel
                self.offset[0] += dx
                self.offset[1] += dy

    def handle_tools_panel_click(self, my):
        tool_height = 40
        idx = my // tool_height
        if idx < len(TOOLS):
            self.selected_tool = TOOLS[idx]
            if self.selected_tool == TOOL_BRUSH:
                self.selected_color = ask_color(self.selected_color)

    def handle_canvas_click(self, mx, my):
        gx, gy = self.screen_to_grid(mx, my)
        if 0 <= gx < self.grid_w and 0 <= gy < self.grid_h:
            if self.selected_tool == TOOL_BRUSH:
                self.grid[gx][gy] = self.selected_color
            elif self.selected_tool == TOOL_ERASER:
                self.grid[gx][gy] = None
            elif self.selected_tool == TOOL_PICKER:
                color = self.grid[gx][gy]
                if color:
                    self.selected_color = color

    def screen_to_grid(self, mx, my):
        x = mx - PANEL_WIDTH - self.offset[0]
        y = my - self.offset[1]
        gx = x // self.zoom
        gy = y // self.zoom
        return int(gx), int(gy)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_tools_panel()
        self.draw_canvas()
        self.draw_preview_panel()
        pygame.display.flip()

    def draw_tools_panel(self):
        pygame.draw.rect(self.screen, (30, 30, 30), (0, 0, PANEL_WIDTH, self.screen_h))
        font = pygame.font.SysFont(None, 24)
        for i, tool in enumerate(TOOLS):
            rect = pygame.Rect(0, i * 40, PANEL_WIDTH, 40)
            color = (70, 70, 70) if self.selected_tool == tool else (50, 50, 50)
            pygame.draw.rect(self.screen, color, rect)
            txt = font.render(tool, True, (255, 255, 255))
            self.screen.blit(txt, (10, i * 40 + 10))
        # Color preview
        pygame.draw.rect(self.screen, self.selected_color, (10, 140, 80, 30))

    def draw_canvas(self):
        ox, oy = self.offset
        for x in range(self.grid_w):
            for y in range(self.grid_h):
                px = PANEL_WIDTH + ox + x * self.zoom
                py = oy + y * self.zoom
                rect = pygame.Rect(px, py, self.zoom, self.zoom)
                color = self.grid[x][y]
                if color:
                    pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

    def draw_preview_panel(self):
        px = self.screen_w - PREVIEW_WIDTH
        pygame.draw.rect(self.screen, PREVIEW_BG, (px, 0, PREVIEW_WIDTH, self.screen_h))
        # Draw preview image (fit grid to preview panel)
        margin = 10
        w = PREVIEW_WIDTH - 2 * margin
        h = self.screen_h - 2 * margin
        scale = min(w / self.grid_w, h / self.grid_h)
        for x in range(self.grid_w):
            for y in range(self.grid_h):
                color = self.grid[x][y]
                if color:
                    rx = px + margin + int(x * scale)
                    ry = margin + int(y * scale)
                    pygame.draw.rect(self.screen, color, (rx, ry, int(scale), int(scale)))

if __name__ == "__main__":
    grid_w, grid_h = ask_grid_size()
    app = PixelArtApp(grid_w, grid_h)
    app.run()