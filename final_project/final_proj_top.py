#!/usr/bin/env python3
# Purpose: <TODO>
#
# This program currently just provides some arbitrary starter code, plus
# the code for writing xml and midi files. Please remove this comment (and any
# unused starter code) and explain your actual program once you have a plan for
# your composition!
# 
# Author(s): <TODO>
# Date: <TODO>


import sys
import random
from music21 import *

C_MIDI = 60  # middle C in midi notation
ALL_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
NOTES_PER_SECTION = 20
SER_ROT_COUNTER = 0

subject = stream.Part()    
answer = stream.Part()    
c_subject = stream.Part()  
subject.append(tempo.MetronomeMark(number=150))

subject_rhythm = [1, 1, 0.5, 1, 0.5, 1, 1, 0.5, 1, 0.5, 1, 1, 0.5, 1, 0.5, 1, 1, 0.5, 1, 0.5]

def generate_monte_carlo():
    curr = 0
    prev = -1
    sequence = []

    while curr < NOTES_PER_SECTION:
        while True:
            next = random.randint(0,6)
            if prev in [2, 4, 6, 7] and next in [2, 4, 6, 7]:
                continue
            if next == prev:
                continue
            if abs(next - prev) > 2:
                continue
            break 

        if curr == NOTES_PER_SECTION-1 or curr == 0:
            next = 0

        sequence.append(ALL_NOTES[next])
        prev = next
        curr += 1
    
    return sequence

def insert_subject(subject_sequence):
    for i in range(0, len(subject_sequence)):
        subject.append(note.Note(subject_sequence[i], quarterLength = subject_rhythm[i]))
        
def insert_rest(voice):
    for i in range(0, 4):
        voice.append(note.Rest(quarterLength = 4))

def generate_serialism(subject_sequence, voice):
    transformation = random.randint(0,3)
    
    if transformation == 0:
        new_seq = serial_doublenote(subject_sequence)
        for i in range(0, len(new_seq)):
            voice.append(note.Note(new_seq[i], quarterLength = (subject_rhythm[i % 20])/2)) ## new_seq [i] gives note and we need midi value ??? 
    elif transformation == 1:
        new_seq = serial_doubletime(subject_sequence)
        for i in range(0, len(new_seq)):
            voice.append(note.Note(new_seq[i], quarterLength = (subject_rhythm[i % 20])/2)) ## new_seq [i] gives note and we need midi value ??? 
    elif transformation == 2:
        new_seq = serial_rotation_pitch(subject_sequence)
        for i in range(0, len(new_seq)):
            voice.append(note.Note(new_seq[i], quarterLength = subject_rhythm[i])) ## new_seq [i] gives note and we need midi value ??? 
    else:
        new_rhythm = serial_rotation_rhythm()
        for i in range(0, len(new_rhythm)):
            voice.append(note.Note(subject_sequence[i], quarterLength = new_rhythm[i]))


def serial_doubletime(subject_sequence):
    new_seq = []
    for i in subject_sequence:
        new_seq.append(i)
    for i in subject_sequence:
        new_seq.append(i)    
    return new_seq

def serial_doublenote(subject_sequence):
    new_seq = []
    for i in subject_sequence:
        new_seq.append(i)
        new_seq.append(i)
    return new_seq
    
def serial_rotation_pitch(subject_sequence):
    global SER_ROT_COUNTER
    new_seq = []
    SER_ROT_COUNTER += 1
    for i in range(0, len(subject_sequence)):
        index = (i + SER_ROT_COUNTER) % len(subject_sequence)
        new_seq.append(subject_sequence[index])
    return new_seq

def serial_rotation_rhythm():
    global SER_ROT_COUNTER 
    new_seq = []
    SER_ROT_COUNTER += 1
    for i in range(0, len(subject_rhythm)):
        index = (i + SER_ROT_COUNTER) % len(subject_rhythm)
        new_seq.append(subject_rhythm[index])
    return new_seq


def main(): 

    subject_sequence = generate_monte_carlo()
    
    # grammar function calls go here
    
    insert_subject(subject_sequence)
    insert_rest(answer)
    insert_rest(c_subject)

    generate_serialism(subject_sequence, answer)



    top_level = stream.Score()
    top_level.insert(0, subject)
    top_level.insert(0, answer)
    top_level.insert(0, c_subject)

    # Layout
    if top_level.metadata is None:
        top_level.metadata = metadata.Metadata()

    top_level.metadata.title = "Final"
    top_level.metadata.composer = "Matt, Sam, Kimaya and Begüm"

    # Play midi, output sheet music, or print the contents of the stream
    if ("-m" in sys.argv):
        top_level.write('midi', fp="out.midi")
    elif ("-s" in sys.argv):
        top_level.write(fp="out.xml")
    else:
        top_level.show('text') #Useful for debugging!

if __name__ == "__main__":
    main()
