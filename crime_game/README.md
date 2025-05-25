# 🔍 Crime Deduction Game

This is an interactive detective game where you interview suspects and try to catch the murderer.

---

## 🎯 Objective

- Interrogate suspects.
- Spot whose alibi is **not confirmed** by anyone else 
- Make your guess before or when running out of clues!

---

## 🧠 Game Logic

- 4 suspects are randomly selected.
- 3 innocents provide **mutually consistent testimonies**.
- 1 murderer gives a **false alibi**, unsupported by others.

> 🧩 Winning hint:
>
> ✅ Innocents always mutually confirm each other.  
> ❌ The murderer is alone in time/place, or not confirmed.  
> 🔍 Lower realiability can be a very useful hint.

---

## 📌 Notes

- The current program heavily relies on randomness, and there is still much room for improvement in aligning with human logical reasoning.
- This version serves as a conceptual prototype, showing only the structure and general direction, and may be enhanced in the future.

---

## ▶️ Run the Game

```bash
cd ~/crime_game
python main.py

