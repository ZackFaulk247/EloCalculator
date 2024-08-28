from Player import Player
import os

class Methods:
    def __init__(self, filename='player.txt'):
        self.filename = filename
        self.players = []

    def load_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    name, rating = line.strip().split(';')
                    self.players.append(Player(name, int(rating)))
        else:
            print(f"File {self.filename} does not exist. Starting with an empty list of players.")

    def save_file(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            for player in self.players:
                file.write(f"{player.get_name()};{player.get_elo()}\n")

    def add_player(self, name, rating):
        new_player = Player(name, rating)
        self.players.append(new_player)
        print(f"Added player: {new_player.get_name()} with Elo rating {new_player.get_elo()}")

    def list_players(self):
        self.players.sort(reverse=True)
        count = 0
        for player in self.players:
            count += 1
            print(f"{count}. {player.get_name()} : {player.get_elo()}")

    def calculate_elo(self, winner, loser):
        k = 32  # K-factor, common in Elo rating systems
        winner_elo = winner.get_elo()
        loser_elo = loser.get_elo()

        expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        expected_loser = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))

        new_winner_elo = round(winner_elo + k * (1 - expected_winner))
        new_loser_elo = round(loser_elo + k * (0 - expected_loser))

        winner.set_elo(new_winner_elo)
        loser.set_elo(new_loser_elo)

        print(f"{winner.get_name()} wins! New Elo: {winner.get_elo()}")
        print(f"{loser.get_name()} loses! New Elo: {loser.get_elo()}")

    def find_player(self, name):
        for player in self.players:
            if player.get_name().lower() == name.lower():
                return player
        print(f"Player {name} not found.")
        return None