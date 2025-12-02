"""
Tufts University | CS 150 Algorithmic Music Composition
Fall 2025 | Final Project
Authors: Matthew Dacey (mdacey02), Sam Lev (slev01),
         Begüm Ugurlu (bugurl01), Kimaya Vaid (kvaid01)

Top-level global constants and functions
"""

C_MIDI = 60  # middle C in midi notation
ALL_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

BARS_PER_PHRASE = 8
PHRASES_PER_SECTION = 4
BARS_PER_SECTION = BARS_PER_PHRASE * PHRASES_PER_SECTION

    
#
# notes_to_midi: converts a note (letter) to its respective midi value
#
def notes_to_midi(note):
    if note == 'C':
        return 60
    elif note == 'D':
        return 62
    elif note == 'E':
        return 64
    elif note == 'F':
        return 65   
    elif note == 'G':
        return 67
    elif note == 'A':
        return 69
    elif note == 'B':
        return 71
