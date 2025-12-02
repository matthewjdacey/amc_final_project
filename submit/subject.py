"""
Tufts University | CS 150 Algorithmic Music Composition
Fall 2025 | Final Project
Authors: Matthew Dacey (mdacey02), Sam Lev (slev01),
         Begüm Ugurlu (bugurl01), Kimaya Vaid (kvaid01)

Generates pitchs sequence for the subject
"""

import random
from top_level import *


def generate_monte_carlo(notes_per_section):
    """
    Generates the pitch sequence for the subject
    """
    curr = 0
    prev = -1
    sequence = []

    while curr < notes_per_section:
        while True:
            next = random.randint(0,6)
            # chord tone must resolve to chord tone
            if prev in [2, 4, 6, 7] and next in [2, 4, 6, 7]:
                continue
            # no more than two consecutive notes
            if next == prev:
                continue
            # no more than two steps between consecutive notes
            if abs(next - prev) > 2:
                continue
            break 

        if curr == notes_per_section - 1 or curr == 0:
            next = 0

        sequence.append(ALL_NOTES[next])
        prev = next
        curr += 1
    
    return sequence