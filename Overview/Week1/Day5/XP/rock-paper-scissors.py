from game import Game

def main_menu():
    # Awaited main menu dispaly
    print("\n=== Rock-Paper-Scissors ===")
    print("1. Play a new game")
    print("2. Show game statistics")
    print("3. Quit")

def get_user_menu_choice():
    # Choice of the menu validation
     while True:
        choice = input("\nEnter your choice (1-3): ")
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid input. Please enter 1, 2, or 3.")

def print_results(stats):
    # Awaited statistics display
    print("\n=== Game Summary ===")
    print(f"Games played: {stats['games_played']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print(f"Draws: {stats['draws']}")
    print("\nThank you for playing!")

def main():
    game = Game()
    stats = {'games_played': 0, 'wins': 0, 'losses': 0, 'draws': 0}
    
    while True:
        main_menu()
        choice = get_user_menu_choice()
        
        if choice == '1':
            # Played game
            result = game.play()
            stats['games_played'] += 1
            if result == 'win':
                stats['wins'] += 1
            elif result == 'loss':
                stats['losses'] += 1
            else:
                stats['draws'] += 1
        elif choice == '2':
            # Stats display
            print_results(stats)
        elif choice == '3':
            # Game exit
            print_results(stats)
            break

if __name__ == "__main__":
    main()
