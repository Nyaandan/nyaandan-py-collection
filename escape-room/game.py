"""
Escape Room Game
A simple text-based escape room game where the player must interact with objects in a room to find the correct code to escape.

How to Play:
- The player is presented with a room description and a list of objects.
- They can interact with objects using commands "look", "touch", and "smell" followed by the object name.
- They can attempt to guess the escape code with "guess <code>".
"""

# Messages
msg_invalid_input = "Am I... confused?"
msg_invalid_target = "No such object here..."
msg_invalid_action = "I can't do that..."
prompt_action = "\nWhat will you do next?\n-> "
msg_correct_code = "The code is correct. You may proceed..."
msg_wrong_code = "Wrong code, try again."
msg_defeat = "Yet another wrong code. The lock is broken..."
msg_options = "\nCertain objects catch your attention."
msg_quit = "It was just a dream, you wake up on the ground next to your bed."
msg_game_over = "Game over."

class Game:
    def __init__(self, room):
        self.over = False
        self.max_tries = 3
        self.tries = 0
        self.room = room

    """Parse and validate the command"""
    def get_player_action(self):
        move = input(prompt_action)

        # Shutdown command
        if move == "quit":
            print(msg_quit)
            self.over = True
            return

        move = move.split(' ', 2)
        if len(move) < 2:
            print(msg_invalid_input)
            return
        action = move[0].lower()
        target = move[1].lower()

        # Verify the code if player tries a guess
        if action == "guess":
            self.guess_code(int(target))
            return

        # Retrieve the target if it exists, write a message is not
        target = self.room.content.get(target)
        if target is None:
            print(msg_invalid_target)
            return
        
        # Perform the action on the target if the input is valid,
        # write a message if not (the action does not exist)
        if hasattr(target, action):
            print(getattr(target, action)())
        else:
            print(msg_invalid_action)

    """Verify the entered code"""
    def guess_code(self, code):
        if self.room.check_code(code):
            print(msg_correct_code)
            self.over = True
        else:
            self.tries += 1
            if self.tries == self.max_tries:
                print(msg_defeat)
                self.over = True
            else:
                print(msg_wrong_code)

    """Retrieve a list of the objects present in the room"""
    def get_options(self):
        options = msg_options
        for item in self.room.get_items():
            options += f"\n* {item.capitalize()}"
        return options

    """Game flow"""
    def run_game(self):
        print(self.room.prompt)
        print(self.get_options())
        while not self.over:
            self.get_player_action()