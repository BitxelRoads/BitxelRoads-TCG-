# 🚗 Bitxel Roads: Trading Card Game (TCG)
(This is how we test the game)

 Bitxel Roads is a fast-paced turn-based Trading Card Game where NFT racing cars battle using performance stats, gadgets, and unpredictable Nitro boosts.
 Build your deck, activate synergies, and outmaneuver your opponent!

# 🎮 How Does It Work?

 Each player builds a deck of 3 cars and receives 1 Gadget. During each round:

 - Cars battle using one of four variables: Acceleration, Top Speed, Fuel, or Brakes.
 - Gadgets can be activated using Mana Points (MP).
 - The player who reduces their opponent’s FP (Fight Points) to 0 wins the match.

# 🧩 Code Structure

 The game engine is fully modular and divided into 15 core modules:

 | Module | Functionality |
 |--------|--------------|
 | 1 | NFT Car Generator |
 | 2 | Dual-mode Gadget Generator (Instant/Equipment) |
 | 3 | Variable-Based Combat Logic |
 | 4 | MP System + Gadget Activation |
 | 5 | Synergies between Car Model + Protocol |
 | 6 | Maneuverability & Tiebreaking |
 | 7 | Full Round + Match Engine |
 | 8 | Nitro System (Boosts with Risk) |
 | 9 | Individual MP per Player |
 | 10 | Real Effects of Active Gadgets |
 | 11 | Alternative Defense (1 use per card) |
 | 12 | Full Rotation Mode (each card fights once per phase) |
 | 13 | Visual Enhancements (Print formatting) |
 | 14 | Batch Testing System for Balancing |
 | 15 | Game Modes Filter (Common, Diamond, Free) |

# 🚀 How to Run

# 👉 1. Run a Single Match

 To play a single match and see live printed results:

 python main.py

# 👉 2. Run Batch Test for Balance (Recommended)

# To simulate multiple matches in batch mode, collect results in a CSV, and balance your game:

 - The tester will simulate 50 matches automatically.
 - It will print the cars and gadgets drawn by each player before every duel.
 - At the end, it will show a full summary table of wins, performance points, and decks used.
 - Results will be exported


 This is useful for:
 - Balancing car stats and gadget effects.
 - Observing performance trends between car models and protocols.
 - Preparing data for statistical analysis.

# 📂 Output Example:

 📊 Resultados del Test Batch:

 | Match | Winner | Player 1 FP | Player 2 FP | Player 1 Deck | Player 2 Deck |
 |-------|--------|-------------|-------------|---------------|---------------|
 | 1     | Player 1 | 18 | 12 | CarA ⭐2 | CarB ⭐3 |
 | 2     | Player 2 | 15 | 20 | CarC ⭐1 | CarD ⭐2 |
 ...

# 🎯 Pro Tip:

 You can modify the number of matches by changing this line in tester.py:

# n_matches = 50  # Change to any number you want!



