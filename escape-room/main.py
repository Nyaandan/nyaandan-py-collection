from game import *
from room import *

def read_room_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        sections = content.split('***\n')

        code = int(sections[0].strip())
        room_prompt = sections[1].strip()
        items_data = sections[2].strip().split('---\n')
        
        items = []
        for block in items_data:
            item_data = block.strip().split('\n')
            item = Item(*item_data)
            items.append(item)
    return code, items, room_prompt

# Main game loop
prompt = True
while True:
  if prompt:
    print("\nEnter level code (or 'leave' to exit):")
    prompt = False
  level = input("> ").strip().lower()
  if level == "leave":
    break
  
  try:   
    code, items, room_prompt = read_room_data(f'levels/{level}.txt')
  except FileNotFoundError:
    print("This level does not exist.")
    continue
  current_room = Room(code, items, room_prompt)
  game = Game(current_room)
  game.run_game()
  prompt = True