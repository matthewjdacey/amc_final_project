"""
answer.py
Tufts University | CS 150 Algorithmic Music Composition
Fall 2025 | Final Project
Authors: Matthew Dacey (mdacey02), Sam Lev (slev01),
         Begüm Ugurlu (bugurl01), Kimaya Vaid (kvaid01)

Generates an answer to the subject using serialism
"""

import random
from music21 import *

SER_ROT_COUNTER = 0

def generate_serialism(subject_sequence, subject_rhythm, notes_per_section, voice):
    """
    Generates and inserts the answer rhythm and pitches
    into its respective voice after using serialism transformations
    """
    transformation = random.randint(0,3)
    
    if transformation == 0:
        new_seq = serial_doublenote(subject_sequence)
        for i in range(0, len(new_seq)):
            voice.append(note.Note(new_seq[i], quarterLength = \
                                   (subject_rhythm[i % notes_per_section])/2))
    elif transformation == 1:
        new_seq = serial_doubletime(subject_sequence)
        for i in range(0, len(new_seq)):
            voice.append(note.Note(new_seq[i], quarterLength = \
                                   (subject_rhythm[i % notes_per_section])/2))
    elif transformation == 2:
        new_seq = serial_rotation_pitch(subject_sequence)
        for i in range(0, len(new_seq)):
            voice.append(note.Note(new_seq[i], quarterLength = \
                                   subject_rhythm[i]))
    else:
        new_rhythm = serial_rotation_rhythm(subject_rhythm)
        for i in range(0, len(new_rhythm)):
            voice.append(note.Note(subject_sequence[i], quarterLength = \
                                   new_rhythm[i]))


def serial_doubletime(subject_sequence):
    """
    transformation for serialism where the pitches are
    repeated twice (ABCD -> ABCDABCD)
    """  
    return subject_sequence * 2


def serial_doublenote(subject_sequence):
    """
    transformation for serialism where each pitch is
    repeated twice (ABCD -> AABBCCDD)
    """
    new_seq = []
    for i in subject_sequence:
        new_seq.append(i)
        new_seq.append(i)
    return new_seq
    

def serial_rotation_pitch(subject_sequence):
    """
    transformation for serialism where the pitch sequence
    is rotated by a certain value (SER_ROT_COUNTER)
    """
    global SER_ROT_COUNTER
    new_seq = []
    SER_ROT_COUNTER += 1
    for i in range(0, len(subject_sequence)):
        index = (i + SER_ROT_COUNTER) % len(subject_sequence)
        new_seq.append(subject_sequence[index])
    return new_seq


def serial_rotation_rhythm(subject_rhythm):
    """
    transformation for serialism where the rhythm sequence
    is rotated by a certain value (SER_ROT_COUNTE
    """
    global SER_ROT_COUNTER 
    new_seq = []
    SER_ROT_COUNTER += 1
    for i in range(0, len(subject_rhythm)):
        index = (i + SER_ROT_COUNTER) % len(subject_rhythm)
        new_seq.append(subject_rhythm[index])
    return new_seq