questions = [
    ["Which language was used to create Facebook?", "Python", "French", "JavaScript", "Php", 4],
    ["Which is the capital of France?", "London", "Berlin", "Paris", "Rome", 3],
    ["Which planet is known as the Red Planet?", "Earth", "Mars", "Jupiter", "Venus", 2],
    ["What is the chemical symbol for water?", "O2", "H2O", "CO2", "NaCl", 2],
    ["Who wrote 'Hamlet'?", "Shakespeare", "Charles Dickens", "Mark Twain", "Jane Austen", 1],
    ["Which animal is known as the King of the Jungle?", "Elephant", "Tiger", "Lion", "Bear", 3],
    ["What is the national sport of India?", "Football", "Hockey", "Cricket", "Kabaddi", 2],
    ["Which gas do plants absorb?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Helium", 3],
    ["What is the square root of 64?", "6", "8", "10", "7", 2],
    ["Which continent is the Sahara Desert located in?", "Asia", "South America", "Australia", "Africa", 4]
]

levels = [1000, 2000, 3000, 5000, 10000, 20000, 40000, 80000, 160000, 320000]
money = 0

# Define money lock levels
safe_levels = {4: 10000, 9: 320000}

for i in range(len(questions)):
    question = questions[i]
    print(f"\nQuestion for ₹{levels[i]}:")
    print(f"a. {question[1]}")
    print(f"b. {question[2]}")
    print(f"c. {question[3]}")
    print(f"d. {question[4]}")

    while True:
        try:
            reply = int(input("Enter your answer (1-4) or 0 to quit: "))
            if reply in [0, 1, 2, 3, 4]:
                break
            else:
                print("Please enter a valid option: 1, 2, 3, 4, or 0 to quit.")
        except ValueError:
            print("Invalid input! Please enter a number.")

    if reply == 0:
        if i == 0:
            money = 0
        else:
            money = levels[i - 1]
        print("You chose to quit.")
        break

    if reply == question[5]:
        print(f"✅ Correct! You've won ₹{levels[i]}")
        money = levels[i]
    else:
        print("❌ Wrong answer!")
        # Determine last safe level passed
        money = 0
        for key in safe_levels:
            if i > key:
                money = safe_levels[key]
        break

print(f"\n💰 Your take-home money is ₹{money}")
