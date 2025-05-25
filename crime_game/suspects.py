'''
suspects.py — Suspect Generation Module

This module handles the generation of suspects for the Crime Deduction Game.
Each suspect has a motive and behavior, and one is randomly chosen as the murderer.
'''

import random

# Predefined list of possible suspect names, behaviors, and motives
NAMES = ['Aria', 'Bobby', 'Chandler', 'Dr.Z', 'Evelen', 'Mishelle']
BEHAVIORS = ['nervous', 'calm', 'arrogant', 'silent']
MOTIVES = ['jealousy', 'money', 'revenge', 'competition']


def generate_suspects():
    selected = random.sample(NAMES, 4) # Randomly select 4 suspects from the full list
    murderer = random.choice(selected) # Randomly choose one of them to be the murderer

    suspects = {}
    for name in selected:
        # Each suspect is assigned a random motive and behavior
        suspects[name] = {
            'motive': random.choice(MOTIVES),
            'behavior': random.choice(BEHAVIORS),
            'is_murderer': name == murderer # True only for the selected killer
        }

    return suspects, murderer


def display_suspects(suspects: dict):
    # Print a table of suspects showing their name, motive, and behavior
    print("\n" + "=" * 50)
    print(f"{'SUSPECT PROFILES':^50}") 
    print("-" * 50)
    print(f"{'Name':<10} | {'Motive':<15} | {'Behavior':<10}")

    for name, info in suspects.items():
        print(f"{name:<10} | {info['motive']:<15} | {info['behavior']:<10}")

    print("=" * 50)

