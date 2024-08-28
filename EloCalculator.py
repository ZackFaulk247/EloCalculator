import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

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
    

class EloApp:
    def __init__(self, root):
        self.methods = Methods()
        self.methods.load_file()

        self.root = root
        self.root.title("ELO Ranking System")

        # Frame for Text Widget and Scrollbar
        frame = tk.Frame(root)
        frame.pack(fill='both', expand=True)

        # Text area to display output with Scrollbar
        self.output = tk.Text(frame, height=10, width=50)
        scrollbar = tk.Scrollbar(frame, command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame for Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(fill='x', padx=5, pady=5)

        # Add Player Button
        self.add_button = tk.Button(button_frame, text="Add Player", command=self.add_player)
        self.add_button.pack(side=tk.TOP, fill='x', pady=2)

        # Edit Player Button
        self.edit_button = tk.Button(button_frame, text="Edit Player", command=self.edit_player)
        self.edit_button.pack(side=tk.TOP, fill='x', pady=2)

        # Delete Player Button
        self.delete_button = tk.Button(button_frame, text="Delete Player", command=self.delete_player)
        self.delete_button.pack(side=tk.TOP, fill='x', pady=2)

        # Record Match Button
        self.match_button = tk.Button(button_frame, text="Record Match", command=self.record_match)
        self.match_button.pack(side=tk.TOP, fill='x', pady=2)

        # Save and Exit Button
        self.save_button = tk.Button(button_frame, text="Save and Exit", command=self.save_and_exit)
        self.save_button.pack(side=tk.TOP, fill='x', pady=2)

        # Initial Player List Display
        self.list_players()

    def log_action(self, action_description):
        """Log the action with a timestamp."""
        with open("actions.log", "a") as log_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"[{timestamp}] {action_description}\n")

    def list_players(self):
        self.output.delete(1.0, tk.END)  # Clear previous output
        self.methods.list_players()
        count = 0
        for player in self.methods.players:
            count += 1
            self.output.insert(tk.END, f"{count}. {player.get_name()} : {player.get_elo()}\n")

    def add_player(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Player")

        tk.Label(add_window, text="Name:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()
        name_entry.focus_set()  # Auto-focus on the name entry field

        tk.Label(add_window, text="Elo Rating:").pack()
        rating_entry = tk.Entry(add_window)
        rating_entry.pack()

        def submit():
            name = name_entry.get()
            try:
                rating = int(rating_entry.get())
                self.methods.add_player(name, rating)
                messagebox.showinfo("Success", f"Added player: {name} with Elo rating {rating}")
                self.list_players()  # Refresh the player list
                self.log_action(f"Added player: {name} with Elo rating {rating}")
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Elo rating must be a number")

        submit_button = tk.Button(add_window, text="Submit", command=submit)
        submit_button.pack()

        add_window.bind('<Return>', lambda event: submit())  # Bind Enter key to submit

    def edit_player(self):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Player")

        tk.Label(edit_window, text="Current Name:").pack()
        current_name_entry = tk.Entry(edit_window)
        current_name_entry.pack()
        current_name_entry.focus_set()  # Auto-focus on the current name entry field

        tk.Label(edit_window, text="New Name:").pack()
        new_name_entry = tk.Entry(edit_window)
        new_name_entry.pack()

        tk.Label(edit_window, text="New Elo Rating:").pack()
        new_rating_entry = tk.Entry(edit_window)
        new_rating_entry.pack()

        def submit():
            current_name = current_name_entry.get()
            player = self.methods.find_player(current_name)
            if player:
                new_name = new_name_entry.get() or player.get_name()
                try:
                    new_rating = int(new_rating_entry.get()) if new_rating_entry.get() else player.get_elo()
                    player.set_name(new_name)
                    player.set_elo(new_rating)
                    messagebox.showinfo("Success", f"Player {current_name} updated to {new_name} with Elo rating {new_rating}")
                    self.list_players()  # Refresh the player list
                    self.log_action(f"Edited player: {current_name} to {new_name} with new Elo rating {new_rating}")
                    edit_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Elo rating must be a number")
            else:
                messagebox.showerror("Error", f"Player {current_name} not found")

        submit_button = tk.Button(edit_window, text="Submit", command=submit)
        submit_button.pack()

        edit_window.bind('<Return>', lambda event: submit())  # Bind Enter key to submit

    def delete_player(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Player")

        tk.Label(delete_window, text="Name:").pack()
        name_entry = tk.Entry(delete_window)
        name_entry.pack()
        name_entry.focus_set()  # Auto-focus on the name entry field

        def submit():
            name = name_entry.get()
            player = self.methods.find_player(name)
            if player:
                self.methods.players.remove(player)
                messagebox.showinfo("Success", f"Player {name} deleted")
                self.list_players()  # Refresh the player list
                self.log_action(f"Deleted player: {name}")
                delete_window.destroy()
            else:
                messagebox.showerror("Error", f"Player {name} not found")

        submit_button = tk.Button(delete_window, text="Submit", command=submit)
        submit_button.pack()

        delete_window.bind('<Return>', lambda event: submit())  # Bind Enter key to submit

    def record_match(self):
        match_window = tk.Toplevel(self.root)
        match_window.title("Record Match")

        tk.Label(match_window, text="Winner's Name:").pack()
        winner_entry = tk.Entry(match_window)
        winner_entry.pack()
        winner_entry.focus_set()  # Auto-focus on the winner name entry field

        tk.Label(match_window, text="Loser's Name:").pack()
        loser_entry = tk.Entry(match_window)
        loser_entry.pack()

        def submit():
            winner_name = winner_entry.get()
            loser_name = loser_entry.get()
            winner = self.methods.find_player(winner_name)
            loser = self.methods.find_player(loser_name)

            if winner and loser:
                self.methods.calculate_elo(winner, loser)
                messagebox.showinfo("Success", "Match recorded and Elo ratings updated")
                self.list_players()  # Refresh the player list
                self.log_action(f"Recorded match: {winner_name} (winner) vs {loser_name} (loser)")
                match_window.destroy()
            else:
                messagebox.showerror("Error", "One or both players not found")

        submit_button = tk.Button(match_window, text="Submit", command=submit)
        submit_button.pack()

        match_window.bind('<Return>', lambda event: submit())  # Bind Enter key to submit

    def save_and_exit(self):
        self.methods.save_file()
        self.log_action("Saved player data and exited the program")
        messagebox.showinfo("Saved", "Player data saved successfully")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = EloApp(root)
    root.mainloop()