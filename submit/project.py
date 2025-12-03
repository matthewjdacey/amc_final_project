"""
project.py
Tufts University | CS 150 Algorithmic Music Composition
Fall 2025 | Final Project
Authors: Matthew Dacey (mdacey02), Sam Lev (slev01),
         Begüm Ugurlu (bugurl01), Kimaya Vaid (kvaid01)

This project generates a piece whose overall structure is inspired by that
of a Bach fugue and enforced by a grammar. The grammar assigns roles to 
different voices and sections throughout the piece, and each role is implemented
using a different algorithmic approach(es).
"""

import sys
import random
import numpy as np
from music21 import *
from top_level import *
from rhythm_gen import *
from grammar import *
from subject import generate_monte_carlo
from counter_subject import genetic_algorithm
from answer import generate_serialism
from chords import make_chord_voice

if "-fix" in sys.argv:
    print("fixing")
    random.seed(6)
    np.random.seed(6)

# global variables
# all voices
voice1 = stream.Part()    
voice2 = stream.Part()    
voice3 = stream.Part()
voice4 = stream.Part()

voice1.append(tempo.MetronomeMark(number=120))

notes_per_section, subject_rhythm = generate_subject_rhythm()


def insert_subject(subject_sequence, voice):
    """
    inserts the subject picthes and rhythms into the respective voice
    
    subject_sequence: list representing subject pitches
    voice: int in [1, 4]
    """
    for i in range(0, len(subject_sequence)):
        voice.append(note.Note(subject_sequence[i], quarterLength = \
                               subject_rhythm[i]))


def insert_rest(voice):
    """
    inserts 8 whole rests into the respective voice

    voice: an int in [1, 4]
    """
    for i in range(0, 8):
        voice.append(note.Rest(quarterLength = 4))


def each_part(i, voice, sub_seq):
    """
    appends pitch and rhythm sequence to respective voice
    """
    global subject_rhythm
    
    if i == 'S':
        insert_subject(sub_seq, voice)
    elif i == 'A':
        generate_serialism(sub_seq, subject_rhythm, notes_per_section, voice)
    elif i == 'C':
        # new_cs = genetic_algorithm(sub_seq) # change when rhythm done
        # cs_rhythm_len, new_cs_rhythm = generate_cs_rhythm(sub_seq)
        new_cs_pitches, new_cs_rhythm = genetic_algorithm(sub_seq, subject_rhythm)
        
        for j in range(0, len(new_cs_pitches)):
            voice.append(note.Note(new_cs_pitches[j], quarterLength = new_cs_rhythm[j]))
    else: # i == '_'
            insert_rest(voice)


def make_voice(v1, v2, v3, main_subject, dev_subject):
    """
    generates music for each voice to fill the appropriate role
    """

    for i in range(0, len(v1)):
        if PHRASES_PER_SECTION <= i < 2 * PHRASES_PER_SECTION:
            curr_subject = dev_subject
        else:
            curr_subject = main_subject

        each_part(v1[i], voice1, curr_subject)
        each_part(v2[i], voice2, curr_subject)
        each_part(v3[i], voice3, curr_subject)


def main(): 
    # derive structure from grammar
    grammar_seq = generate_grammar()
    v1 = []
    v2 = []
    v3 = []
    for roles in grammar_seq:
        v1.append(roles[0])
        v2.append(roles[1])
        v3.append(roles[2])

    print(grammar_seq)

    #generate subject melodies
    main_subject_sequence = generate_monte_carlo(notes_per_section)
    dev_subject_sequence = generate_monte_carlo(notes_per_section)

    make_voice(v1, v2, v3, main_subject_sequence, dev_subject_sequence)
    
    # transpose voice1 1 octave up
    for i in range(0, len(voice1)):
        if isinstance(voice1[i], note.Note):
            voice1[i].pitch.midi += 12
        
    # transpose voice3 1 octave down
    for i in range(0, len(voice3)):
        if isinstance(voice3[i], note.Note):
            voice3[i].pitch.midi -= 12

    make_chord_voice(voice4)

    #render to music21
    top_level = stream.Score()

    top_level.insert(0, voice1)
    top_level.insert(0, voice2)
    top_level.insert(0, voice3)
    top_level.insert(0, voice4)

    # Layout
    if top_level.metadata is None:
        top_level.metadata = metadata.Metadata()

    top_level.metadata.title = "Final"
    top_level.metadata.composer = "Matt, Sam, Kimaya and Begüm"

    # Play midi, output sheet music, or print the contents of the stream
    if ("-m" in sys.argv):
        top_level.write('midi', fp="out.midi")
    if ("-s" in sys.argv):
        top_level.write(fp="out.xml")
    else:
        top_level.show('text')

if __name__ == "__main__":
    main()