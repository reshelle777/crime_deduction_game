'''
main.py — Crime Deduction Game Launcher

Launches the interactive mystery game where players gather clues
and identify the murderer among suspects using testimonies.
'''

import re
from suspects import generate_suspects, display_suspects
from clues import generate_clues, get_clue_by_suspect


def ask_suspect(name, clues, log):
    # This function handles the 'ask' command. It retrieves the suspect's testimony
    clue = get_clue_by_suspect(name, clues) # Find the clue related to this suspect
    if clue:
        text = clue[1]
        reliability = clue[2]
        print(f"\n🗣️ {name} says: \"{text}\"")
        print(f"🧪 Reliability: {reliability}/100")

        # Use regex to extract the time and location from the testimony text
        time_match = re.search(r'at (\d+:\d+pm)', text)
        loc_match = re.search(r'in the (\w+)', text)
        time = time_match.group(1) if time_match else None
        location = loc_match.group(1) if loc_match else None

        # Record this testimony in the log and check for confirmation by others
        if time and location:
            if name not in log:
                log[name] = []
            log[name].append((time, location))

        # Compare this alibi with other suspects' testimonies
            for other, claims in log.items():
                if other == name:
                    continue
                for claim_time, claim_loc in claims:
                    if time == claim_time and location == claim_loc:
                        print(f"✅ Verified by {other}.")
                        return
    else:
        print(f"\n{name} says nothing useful.")


def guess_murderer(guess: str, murderer: str, detective: str) -> bool:
    # This function handles the 'guess' command.
    # It checks if the guess is correct and prints the result.
    print(f"\n🔎 Detective {detective} accuses {guess}.\n")
    if guess == murderer:
        print("✅ CORRECT! You solved the case.")
        return True
    else:
        print(f"❌ WRONG! The real murderer was {murderer}.")
        return False


def show_truth_log(clues, murderer):
    # Displays the full list of testimonies
    # Showing which were lies and their reliability scores.
    print("\n" + "=" * 95)
    print("🧾 FINAL TRUTH LOG".center(95))
    print("=" * 95)
    for speaker, text, reliability, is_misleading in clues:
        tag = "❌ LIE " if is_misleading else "✅ TRUE"
        print(f"{tag:<8}- {speaker:<10}: \"{text}\"  (Reliability: {reliability}/100)")
    print("=" * 95)
    print(f"🎯The murderer was: {murderer}\n")



def final_summary(detective: str, solved: bool):
    # Final message depending on whether the player guessed correctly
    if solved:
        print(f"\n🎓 Brilliant work, Detective {detective}. Evil had no place to hide.")
    else:
        print(f"\n🎓 The truth slipped through your fingers, Detective {detective}. Perhaps next time.")


def main():
    # Main function to run the game. Handles setup and command loop.
    print("🔍 Welcome to the Crime Deduction Game!")
    detective_name = input("Please enter your name, Detective: ").strip().title()
    print(f"\n🕵️ We look forward to justice prevailing under your watch, Detective {detective_name}.")

    # Generate suspects and clues
    suspects, murderer = generate_suspects()
    name_lookup = {name.lower(): name for name in suspects} # Support case-insensitive lookup
    clues = generate_clues(suspects, murderer)
    display_suspects(suspects) # Display suspect list with motive and behavior

    testimony_log = {} # Tracks all statements given by suspects
    clue_used = 0
    max_clues = len(clues)

    # Main command-processing loop
    while clue_used < max_clues:
        try:
            print(f"\nClues used: {clue_used}/{max_clues}")
            command = input("Enter command (ask <name> | guess <name> | exit): ").strip()

            if not command:
                raise ValueError("Empty command.")

            parts = command.split(maxsplit=1)
            if len(parts) < 2:
                if parts[0].lower() == 'exit':
                    print(f"\nYou left the case unsolved, Detective {detective_name}.")
                    final_summary(detective_name, solved=False)
                    return
                else:
                    raise ValueError("Invalid format. Use: ask <name> or guess <name>")

            action = parts[0].lower()
            name_input = parts[1].strip().lower()

            # Validate name
            if name_input not in name_lookup:
                raise ValueError("That person is not a suspect.")

            name = name_lookup[name_input] # Restore original casing

            if action == 'ask':
                ask_suspect(name, clues, testimony_log)
                clue_used += 1
            elif action == 'guess':
                if guess_murderer(name, murderer, detective_name):
                    final_summary(detective_name, solved=True)
                    show_truth_log(clues, murderer)
                    return
                else:
                    final_summary(detective_name, solved=False)
                    show_truth_log(clues, murderer)
                    return
            else:
                raise ValueError("Unknown command.")
        except ValueError as ve:
            print(f"⚠️ Input Error: {ve}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")

    
    # When all clues have been used, allow one final guess
    print("\n🧩You've used all clues. Make your final guess!")
    final_guess = input("Enter your final guess (guess <name>): ").strip()

    if final_guess.lower().startswith("guess "):
        name_input = final_guess[6:].strip().lower()
        if name_input in name_lookup:
            name = name_lookup[name_input]
            if guess_murderer(name, murderer, detective_name):
                final_summary(detective_name, solved=True)
            else:
                final_summary(detective_name, solved=False)
        else:
            print(f"❌ Invalid suspect: {name_input}")
            print(f"The real murderer was: {murderer}")
            final_summary(detective_name, solved=False)
    else:
        print("❌ Invalid format. You failed to make a final guess.")
        print(f"The real murderer was: {murderer}")
        final_summary(detective_name, solved=False)

    show_truth_log(clues, murderer)


if __name__ == '__main__':
    main()
