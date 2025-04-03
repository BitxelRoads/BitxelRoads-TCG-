# 🚗 Bitxel Roads: Trading Card Game (TCG)

**Bitxel Roads** is a fast-paced turn-based **Trading Card Game** where NFT racing cars battle using performance stats, gadgets, and unpredictable Nitro boosts. Build your deck, activate synergies, and outmaneuver your opponent!

---

## 🎮 How Does It Work?

Each player builds a deck of **3 cars** and receives **1 Gadget**. During each round:
- Cars battle using one of four variables: Acceleration, Top Speed, Fuel, or Brakes.
- Gadgets can be activated using Mana Points (MP).
- The player who reduces their opponent’s FP (Fight Points) to 0 wins the match.

---

## 🧩 Code Structure

The game engine is fully modular and divided into **15 core modules**:

| Module | Functionality |
|--------|-----------------------------|
| 1 | NFT Car Generator |
| 2 | Dual-mode Gadget Generator (Instant/Equipment) |
| 3 | Variable-Based Combat Logic |
| 4 | MP System + Gadget Activation |
| 5 | Synergies between Car Model + Protocol |
| 6 | Maneuverability & Tiebreaking |
| 7 | Full Round + Match Engine |
| 8 | Nitro System (Boosts with Risk) |
| 9 | Individual MP per Player |
|10 | Real Effects of Active Gadgets |
|11 | Alternative Defense (1 use per card) |
|12 | Full Rotation Mode (each card fights once per phase) |
|13 | Visual Enhancements (Print formatting) |
|14 | Batch Testing System for Balancing |
|15 | Game Modes Filter (Common, Diamond, Free) |

---

## 🚀 How to Run

```bash
python main.py
