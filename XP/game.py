import random

class Game:
    def __init__(self):
        # Possible choices 
        self.choices = ['rock', 'paper', 'scissors']
    
    def get_user_item(self):
        # Repeated asking till valid entry
        while True:
            user_input = input("Select rock, paper, or scissors: ").lower().strip()
            if user_input in self.choices:
                return user_input
            print("Invalid choice. Choose between: rock, paper, scissors. Please try again.")
    
    def get_computer_item(self):
        # Randomed selection
        return random.choice(self.choices)
    
    def get_game_result(self, user_item, computer_item):
        # Logic for determining the result
        if user_item == computer_item:
            return 'draw'
        winning_combinations = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }
        return 'win' if winning_combinations[user_item] == computer_item else 'loss'
    
    def play(self):
        # Sequencing of a game complète
        user_item = self.get_user_item()
        computer_item = self.get_computer_item()
        result = self.get_game_result(user_item, computer_item)
        
        # Messages regarding the results
        result_messages = {
            'win': 'You win!',
            'loss': 'You lose!',
            'draw': 'You drew!'
        }
        # Awaited display ffichage : "You selected X. The computer selected Y. Result!"
        print(f"\nYou selected {user_item}. The computer selected {computer_item}. {result_messages[result]}")
        
        return result