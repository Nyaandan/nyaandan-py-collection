"""
PictoTurtle
A simple drawing program controlled with the keyboard.

Controls:
- Arrow keys to move the turtle
- 'a' to toggle pen up/down
- 's' to change speed
- 'd' to change pen size
- 'c' to change pen color
- 'Escape' to exit the program
"""

import sys
import turtle
from controls import *
import controls
from utils import vector_to_angle

def pressEnd():
  global end
  end = True

#region vars
colors = ["white", "black", "red", "orange", "yellow", "green", "blue", "purple", "brown"]
sizes = [1, 4, 8, 12, 16]
speeds = [1, 5, 10, 15]
#endregion

#region state
end  = False
current_color_idx = 1
current_size_idx = 1
current_speed_idx = 1
turtle_rotation = 0
target_rotation = 0
#endregion

def initialize_turtle():
  turtle.title("PictoTurtle")
  turtle.bgcolor("lightgrey")
  turtle.shape("turtle")
  set_pen_size()
  set_pen_color()
  set_speed()

  turtle.getscreen().getcanvas().winfo_toplevel().protocol(
    "WM_DELETE_WINDOW",
    lambda: (close_program(), turtle.bye())
  )

def addListeners():
  turtle.getscreen().onkeypress(pressRight, "Right")
  turtle.getscreen().onkeyrelease(releaseRight, "Right")
  turtle.getscreen().onkeypress(pressLeft, "Left")
  turtle.getscreen().onkeyrelease(releaseLeft, "Left")
  turtle.getscreen().onkeypress(pressUp, "Up")
  turtle.getscreen().onkeyrelease(releaseUp, "Up")
  turtle.getscreen().onkeypress(pressDown, "Down")
  turtle.getscreen().onkeyrelease(releaseDown, "Down")
  
  turtle.getscreen().onkeypress(toggle_pen, "a")
  turtle.getscreen().onkeypress(set_speed, "s")
  turtle.getscreen().onkeypress(set_pen_size, "d")
  turtle.getscreen().onkeypress(set_pen_color, "c")
  turtle.getscreen().onkeypress(pressEnd, "Escape")

  turtle.getscreen().listen()
  print("Controls ready...")

def process_movement_input():
  global turtle_rotation, target_rotation

  x = controls.input_x
  y = controls.input_y
  turtle_rotation = 180
  while not end:
    diff = 0
    if x != 0 or y != 0:
      target_rotation = vector_to_angle(x, y)
      diff = target_rotation - turtle_rotation
      turtle_rotation = target_rotation
      turtle.setheading(turtle_rotation)
      if diff == 0:
        turtle.forward(turtle_speed)
    turtle.update()
    x = controls.input_x
    y = controls.input_y

def set_speed():
  global current_speed_idx, turtle_speed
  current_speed_idx = (current_speed_idx + 1) % len(speeds)
  turtle_speed = speeds[current_speed_idx]
  print(f"Speed set to {turtle_speed}")

def set_pen_color():
  global current_color_idx
  current_color_idx = (current_color_idx + 1) % len(colors)
  new_color = colors[current_color_idx]
  turtle.pencolor(new_color)
  print(f"Pen color set to {new_color}")

def set_pen_size():
  global current_size_idx
  current_size_idx = (current_size_idx + 1) % len(sizes)
  new_size = sizes[current_size_idx]
  turtle.pensize(new_size)
  turtle.shapesize(max(new_size/8, 1))
  print(f"Pen size set to {new_size}")

def toggle_pen():
  if turtle.isdown():
    turtle.penup()
    print("Pen lifted.")
  else:
    turtle.pendown()
    print("Pen down.")

def close_program():
  global end
  end = True
  print("Exiting program...")

initialize_turtle()
addListeners()
process_movement_input()
sys.exit()
