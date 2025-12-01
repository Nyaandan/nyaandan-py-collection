class Item:
    def __init__(self, name, look, feel, odor):
        self.name = name
        self.appearance = look
        self.feel = feel
        self.odor = odor

    def look(self):
        return f"You observe the {self.name}. {self.appearance}"

    def touch(self):
        return f"You touch the {self.name}. {self.feel}"

    def smell(self):
        return f"You smell the {self.name}. {self.odor}"