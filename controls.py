"""Controls module for handling keyboard input for movement."""

input_x = 0
input_y = 0
end = False
keys_pressed = [False, False, False, False]

def pressRight():
    global input_x, keys_pressed
    if keys_pressed[0]:
        return

    #print("+R")
    keys_pressed[0] = True
    input_x = 1 if input_x == 0 else 0
    

def releaseRight():
    #print("-R")
    global input_x, keys_pressed
    keys_pressed[0] = False
    input_x = -1 if input_x == 0 else 0


def pressLeft():
    global input_x, keys_pressed
    if keys_pressed[1]:
        return

    #print("+L")
    keys_pressed[1] = True
    input_x = -1 if input_x == 0 else 0
    
    
def releaseLeft():
    #print("-L")
    global input_x, keys_pressed
    keys_pressed[1] = False
    input_x = 1 if input_x == 0 else 0
    
    
def pressUp():
    global input_y, keys_pressed
    if keys_pressed[2]:
        return

    #print("+U")
    keys_pressed[2] = True
    input_y = 1 if input_y == 0 else 0
    
    
def releaseUp():
    #print("-U")
    global input_y, keys_pressed
    keys_pressed[2] = False
    input_y = -1 if input_y == 0 else 0
    
    
def pressDown():
    global input_y, keys_pressed
    if keys_pressed[3]:
        return

    #print("+D")
    keys_pressed[3] = True
    input_y = -1 if input_y == 0 else 0
    
    
def releaseDown():
    #print("-D")
    global input_y, keys_pressed
    keys_pressed[3] = False
    input_y = 1 if input_y == 0 else 0
