# Player.py

class Player:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    def get_elo(self):
        return self.rating

    def get_name(self):
        return self.name

    def set_elo(self, elo):
        self.rating = elo

    def set_name(self, name):
        self.name = name

    def swap_cont(self, name1, elo1):
        self.rating = elo1
        self.name = name1

    def __lt__(self, other):
        return self.rating < other.rating

    def __eq__(self, other):
        return self.name == other.name