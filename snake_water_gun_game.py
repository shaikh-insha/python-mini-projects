import random

def display_welcome():
    print("\n🎮 Welcome to the Snake-Water-Gun Game!")
    print("Rules:")
    print("🐍 Snake drinks 💧 Water → Snake wins")
    print("💧 Water drowns 🔫 Gun → Water wins")
    print("🔫 Gun kills 🐍 Snake → Gun wins")
    print("Type 'quit' anytime to exit.\n")

def get_player_choice(options):
    while True:
        choice = input("Enter your choice (snake, water, gun): ").lower()
        if choice == 'quit':
            return 'quit'
        if choice in options:
            return choice
        print("❌ Invalid input. Please choose 'snake', 'water', or 'gun'.")

def get_winner(player, computer):
    win_conditions = {
        'snake': 'water',
        'water': 'gun',
        'gun': 'snake'
    }
    if player == computer:
        return 'tie'
    elif win_conditions[player] == computer:
        return 'player'
    else:
        return 'computer'

def show_result(player, computer, winner):
    emojis = {'snake': '🐍', 'water': '💧', 'gun': '🔫'}
    print(f"\nYou chose: {player} {emojis[player]} | Computer chose: {computer} {emojis[computer]}")
    
    if winner == 'tie':
        print("🤝 It's a tie!")
    elif winner == 'player':
        print("🎉 You win this round!")
    else:
        print("💻 Computer wins this round!")

def snake_water_gun_game():
    options = ['snake', 'water', 'gun']
    player_score = 0
    computer_score = 0
    
    display_welcome()

    while True:
        player = get_player_choice(options)
        if player == 'quit':
            print("\n🏁 Game Over!")
            print(f"Final Score → You: {player_score} | Computer: {computer_score}")
            print("Thanks for playing!")
            break
        
        computer = random.choice(options)
        winner = get_winner(player, computer)
        show_result(player, computer, winner)

        if winner == 'player':
            player_score += 1
        elif winner == 'computer':
            computer_score += 1

        print(f"📊 Scoreboard → You: {player_score} | Computer: {computer_score}\n")

# Start the game
if __name__ == "__main__":
    snake_water_gun_game()
