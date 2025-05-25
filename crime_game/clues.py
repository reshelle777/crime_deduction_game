'''
clues.py — Clue Generation and Testimony Module

This module generates suspect testimonies for the Crime Deduction Game.
Innocents give consistent alibis that support each other.
The murderer gives an unverified or conflicting alibi with low reliability.
'''

import random

# Fixed sets of available times and locations
TIME_SLOTS = ['7:00pm', '8:00pm', '9:00pm']
LOCATIONS = ['hallway', 'café']


def generate_clues(suspects: dict, murderer: str, max_clues: int = 4) -> list:
    '''
    Innocents give overlapping, mutually consistent alibis.
    The murderer gives an unconfirmed alibi that no one supports.

    Returns:
        list of (speaker, clue_text, reliability, is_misleading)
    '''
    clues = []
    names = list(suspects.keys())
    innocent_names = [n for n in names if n != murderer]

    # Choose a shared time and location to be used by all innocent alibis
    shared_time = random.choice(TIME_SLOTS)
    shared_location = random.choice(LOCATIONS)

    assigned = {}
    available = innocent_names.copy()
    random.shuffle(available)

    used_pairs = set() # Track which innocent pairs have already been used

    for name in innocent_names:
        partner = None
        # Attempt to assign each innocent a unique partner (excluding self)
        for candidate in available:
            if candidate != name and (candidate, name) not in used_pairs and (name, candidate) not in used_pairs:
                partner = candidate
                break

        # If no unique partner available, assign a fallback
        if not partner:
            partner = random.choice([n for n in innocent_names if n != name])

        assigned[name] = partner
        used_pairs.add((name, partner))
        # Innocent testimony: mutually confirming location/time
        text = f"I was with {partner} in the {shared_location} at {shared_time}."
        reliability = random.randint(85, 100) # High reliability for innocents
        clues.append((name, text, reliability, False))

        # Murderer gives false testimony, unrelated to the above
        wrong_time = random.choice([t for t in TIME_SLOTS if t != shared_time])
        wrong_location = random.choice([l for l in LOCATIONS if l != shared_location])
        text = f"I was in the {wrong_location} at {wrong_time}."
        reliability = random.randint(0, 50)  # Low reliability to hint suspicion
        clues.append((murderer, text, reliability, True))

    random.shuffle(clues) # Randomize clue order to avoid bias
    return clues


def get_clue_by_suspect(suspect_name: str, clues: list) -> tuple | None:
    '''
    Return one clue spoken by a suspect.
    '''
    filtered = [c for c in clues if c[0] == suspect_name]
    return random.choice(filtered) if filtered else None

