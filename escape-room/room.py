from item import *

class Room:
    def __init__(self, code: int, content: list[Item], prompt: str):
        self.code = code
        self.prompt = prompt
        self.content = {}
        for item in content:
            self.content[item.name.lower()] = item

    def check_code(self, entered_code: int):
        return entered_code == self.code

    def get_items(self):
        return [item for item in self.content]