"""
chords.py
Tufts University | CS 150 Algorithmic Music Composition
Fall 2025 | Final Project
Authors: Matthew Dacey (mdacey02), Sam Lev (slev01),
         Begüm Ugurlu (bugurl01), Kimaya Vaid (kvaid01)

Generates chord progression for the full piece
"""

import random
from music21 import *

#constants
a_min = [45, 48, 52] # A minor
b_dim = [47, 50, 53] # B diminished
c_maj = [48, 52, 55] # C major
d_min = [50, 53, 57] # D minor
e_min = [52, 55, 59] # E minor
f_maj = [53, 57, 60] # F major
g_maj = [55, 59, 62] # G major

CHORD_LIST = [a_min, b_dim, c_maj, d_min, e_min, f_maj, g_maj]

def make_chord_voice(voice):
    """
    adds chords to the specified voice for the entire piece
    using a monte carlo method
    """
    for i in range(0, 96):
        prev = None
        
        # insert rules here... 
        while True:
            curr = random.choice(CHORD_LIST)
            # end each section w I chord
            if (i + 1) % 32 == 0 and curr != c_maj:
                continue
            
            # start w a safe chord
            if (i % 32 == 0) and (curr in [a_min, b_dim, d_min, e_min]):
                continue
           
                
            # "weirder" chords need stricter rules
            if prev is not None and (prev == a_min and curr in [a_min, b_dim, e_min]):
                continue
            if prev is not None and (prev == b_dim and curr not in [c_maj, a_min]):
                continue
            if prev is not None and (prev == e_min and curr not in [c_maj, a_min, f_maj]):
                continue
            
            break

        voice.append(chord.Chord(curr, quarterLength = 4))
        prev = curr