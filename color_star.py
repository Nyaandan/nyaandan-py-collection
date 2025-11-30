import turtle
import random

end  = False
length = 180
angle = 144
just = False
value = 1
colors = ["white", "black", "red", "orange", "yellow", "green", "blue", "purple", "brown"]

def star_color():
  global end, just, value
  
  turtle.pensize(2)
  turtle.begin_fill()
  while not end:
    turtle.color(random.choice(colors))
    
    if just:
      just = False
    else:
      turtle.right(angle * value)
      
    turtle.forward(length)
      
    if random.randint(0, len(colors)) < 2:
      turtle.color("darkgrey")
      turtle.end_fill()
      #clear()
      
      just = True
      turtle.left(180)
      value *= -1
      turtle.begin_fill()

star_color()
turtle.done()