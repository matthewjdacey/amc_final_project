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


# have varying similarity to the melody over time (or over a sample space)
# smth in algorithm can try to make population properly varied w respect to 
# the subject sequence- bell curve  

# monte carlo method for subject rhythm

import sys
import random
from music21 import *

# overall global variables
C_MIDI = 60  # middle C in midi notation
ALL_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
NOTES_PER_SECTION = 0
SER_ROT_COUNTER = 0

# ga global variables
NUM_GENERATIONS = 50
NUM_CHROMOSOMES = 1000
NUM_PARENTS = 100 # must be even
SIMILARITY_COEFF = .25

# chord global variables
measure_num = 0
# a_min = chord.Chord([45, 48, 52], quarterLength = 2) # A minor
# b_dim = chord.Chord([47, 50, 53], quarterLength = 2) # B diminished
# c_maj = chord.Chord([48, 52, 55], quarterLength = 2) # C major
# d_min = chord.Chord([50, 53, 57], quarterLength = 2) # D minor
# e_min = chord.Chord([52, 55, 59], quarterLength = 2) # E minor
# f_maj = chord.Chord([53, 57, 60], quarterLength = 2) # F major
# g_maj = chord.Chord([55, 59, 62], quarterLength = 2) # G major

a_min = [45, 48, 52] # A minor
b_dim = [47, 50, 53] # B diminished
c_maj = [48, 52, 55] # C major
d_min = [50, 53, 57] # D minor
e_min = [52, 55, 59] # E minor
f_maj = [53, 57, 60] # F major
g_maj = [55, 59, 62] # G major

chord_list = [a_min, b_dim, c_maj, d_min, e_min, f_maj, g_maj]

# all voices
voice1 = stream.Part()    
voice2 = stream.Part()    
voice3 = stream.Part()
voice4 = stream.Part()
voice1.append(tempo.MetronomeMark(number=120))

subject_rhythm = []

# grammar phrases
exp_grammar = ["KLKL", "KLLL", "KKLL"]
dev_grammar = ["KMLL", "MLML", "MMML", "LMKL"]
final_grammar = ["KNKK", "KNNK", "NNKN"]
k = [("S__", 0.3), ("SC_", 0.7)]
l = [("A__", 0.2), ("AC_", 0.6), ("C__", 0.2)]
m = [("AAC", 0.25), ("CCA", 0.25), ("CCC", 0.25), ("AAA", 0.25)]
n = [("SC_", 0.4), ("SS_", 0.4), ("C__", 0.2)]

#random.seed(1087)

#
# notes_to_scale_deg: converts a note (letter) to an integer
#
def notes_to_scale_deg(note):
    if note == 'C':
        return 0
    elif note == 'D':
        return 1
    elif note == 'E':
        return 2
    elif note == 'F':
        return 3   
    elif note == 'G':
        return 4
    elif note == 'A':
        return 5
    elif note == 'B':
        return 6
    
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
    
#
# generate_subject_rhythm: generates an 8-bar rhythm that is standard for all
#                          subject voices in the piece using the Monte Carlo 
#                          method
#
def generate_subject_rhythm():
    global subject_rhythm
    global NOTES_PER_SECTION

    note_options = [0.5, 1, 1.5, 2]
    default_weights = [20, 50, 5, 40]
    note_weights = default_weights.copy()
    sum = 0
    curr = 0
    prev1 = 0
    prev2 = 0
    rhythm = []
    while sum < 32:
        while True:
            # change note weights based on previous/sum
            
            # make it likely to get back on the downbeat if we are off of it
            if sum % 1 != 0:
                note_weights = [80, 10, 20, 0]
                
            # make sycopated half notes unlikely
            if sum % 2 != 0:
                note_weights[3] = max(note_weights[3] - 20, 0)
                
            # want strings of eighth notes
            if prev1 == .5 and prev2 == .5:
                note_weights[0] += 40
                
            # make it likely to end w half note
            if sum == 30:
                note_weights[3] = 80
                
            # get back to downbeat if we get dotted quarter
            if prev1 == 1.5:
                note_weights = [80, 0, 20, 0]
                
            # no three half notes in a row
            if prev1 == 2 and prev2 == 2:
                note_weights[3] = 0
                
            curr = random.choices(note_options, weights=note_weights)[0]

            # no ties over bar lines
            if (sum % 4 ) > (sum + curr) % 4 and (sum + curr) % 4 != 0:
                continue
            
            # don't start half notes off of downbeat
            if curr == 2 and sum % 1 != 0:
                continue

            # must to sum to exactly 32
            if sum + curr > 32:
                continue
            break
        
        rhythm.append(curr)
        sum += curr
        prev1 = curr
        prev2 = prev1
        note_weights = default_weights.copy()
    print(rhythm)
    subject_rhythm = rhythm
    NOTES_PER_SECTION = len(rhythm)
        
#
# generate_monte_carlo: generates the pitch sequence for the subject
#
def generate_monte_carlo():
    curr = 0
    prev = -1
    sequence = []

    while curr < NOTES_PER_SECTION:
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

        if curr == NOTES_PER_SECTION-1 or curr == 0:
            next = 0

        sequence.append(ALL_NOTES[next])
        prev = next
        curr += 1
    
    return sequence


#
# insert_subject: inserts the subject picthes and rhythms into the
#                 respective voice
#
def insert_subject(subject_sequence, voice):
    for i in range(0, len(subject_sequence)):
        voice.append(note.Note(subject_sequence[i], quarterLength = \
                               subject_rhythm[i]))

#
# insert_rest: inserts 8 whole rests into the respective voice
#     
def insert_rest(voice):
    for i in range(0, 8):
        voice.append(note.Rest(quarterLength = 4))


#
# generate_serialism: generates and inserts the answer rhythm and pitches
#                     into its respective voice after using serialism
#                     transformations
#
def generate_serialism(subject_sequence, voice):
    transformation = random.randint(0,3)
    
    if transformation == 0:
        new_seq = serial_doublenote(subject_sequence)
        for i in range(0, len(new_seq)):
            voice.append(note.Note(new_seq[i], quarterLength = \
                                   (subject_rhythm[i % NOTES_PER_SECTION])/2))
    elif transformation == 1:
        new_seq = serial_doubletime(subject_sequence)
        for i in range(0, len(new_seq)):
            voice.append(note.Note(new_seq[i], quarterLength = \
                                   (subject_rhythm[i % NOTES_PER_SECTION])/2))
    elif transformation == 2:
        new_seq = serial_rotation_pitch(subject_sequence)
        for i in range(0, len(new_seq)):
            voice.append(note.Note(new_seq[i], quarterLength = \
                                   subject_rhythm[i]))
    else:
        new_rhythm = serial_rotation_rhythm()
        for i in range(0, len(new_rhythm)):
            voice.append(note.Note(subject_sequence[i], quarterLength = \
                                   new_rhythm[i]))


#
# serial_doubletime: transformation for serialism where the pitches are
#                    repeated twice (ABCD -> ABCDABCD)
#
def serial_doubletime(subject_sequence):   
    return subject_sequence * 2


#
# serial_doublenote: transformation for serialism where each pitch is 
#                    repeated twice (ABCD -> AABBCCDD)
#
def serial_doublenote(subject_sequence):
    new_seq = []
    for i in subject_sequence:
        new_seq.append(i)
        new_seq.append(i)
    return new_seq
    

#
# serial_rotation_pitch: transformation for serialism where the pitch sequence
#                        is rotated by a certain value (SER_ROT_COUNTER)
#
def serial_rotation_pitch(subject_sequence):
    global SER_ROT_COUNTER
    new_seq = []
    SER_ROT_COUNTER += 1
    for i in range(0, len(subject_sequence)):
        index = (i + SER_ROT_COUNTER) % len(subject_sequence)
        new_seq.append(subject_sequence[index])
    return new_seq


#
# serial_rotation_rhythm: transformation for serialism where the rhythm sequence
#                         is rotated by a certain value (SER_ROT_COUNTER)
#
def serial_rotation_rhythm():
    global SER_ROT_COUNTER 
    new_seq = []
    SER_ROT_COUNTER += 1
    for i in range(0, len(subject_rhythm)):
        index = (i + SER_ROT_COUNTER) % len(subject_rhythm)
        new_seq.append(subject_rhythm[index])
    return new_seq
    

#
# initialize_population: function for genetic algorithm that generates
#                        all initial chromosomes
#
def initialize_population():
    all_chromosomes = []
    for i in range(0, NUM_CHROMOSOMES):
        one_chromo = []
        for j in range(0, NOTES_PER_SECTION):
            one_note = ALL_NOTES[random.randint(0, 6)]
            one_chromo.append(one_note)
        all_chromosomes.append(one_chromo)
    return all_chromosomes


#
# fitness_function: function for genetic algorithm that calculates the fitness
#                   "cost" for all chromosomes. The higher cost implies less
#                   less similar to the subject sequence
#
def fitness_functon(sub_seq, one_chromo):
    score = 0
    for i in range(0, len(one_chromo)):
        score += helper_fitness(sub_seq[i], one_chromo[i])
    return score


#
# helper_fitness: function for genetic algorithm that calculates the fitness
#                  "cost" for all chromosomes
#
def helper_fitness(sub_seq, chromo):
    interval = abs(notes_to_midi(sub_seq) - notes_to_midi(chromo))
    if interval == 0 or interval == 12:
        interval_grade = 1
    elif interval == 4 or interval == 7:
        interval_grade = .5
    elif interval == 2 or interval == 5 or interval == 10 or interval == 11:
        interval_grade = 2
    elif interval == 1 or interval == 3 or interval == 6 or interval == 8 or interval == 9:
        interval_grade = 4
    else:
        interval_grade = 5

    #return diff * interval_grade
    return interval_grade


#
# genetic_algorithm: main genetic algorithm function that generates the
#                    pitch sequence for the counter subject
#
def genetic_algorithm(sub_seq):
    chromos = initialize_population()
    
    count = 0
    while count < NUM_GENERATIONS:
        
        chromos.sort(key=lambda x: fitness_functon(sub_seq, x))
        
        desired_index = int(SIMILARITY_COEFF * NUM_CHROMOSOMES)
        if desired_index - NUM_PARENTS < 0:
            low_i = 0
            high_i = NUM_PARENTS
        elif desired_index + NUM_PARENTS > NUM_CHROMOSOMES:
            low_i = NUM_CHROMOSOMES - NUM_PARENTS - 1
            high_i = NUM_CHROMOSOMES - 1
        else:
            low_i = int(desired_index - NUM_PARENTS / 2 )
            high_i = int(desired_index + NUM_PARENTS /2)
                


        # select + mate parents
        parents = chromos[low_i:high_i]
        new_generation = []
        for i in range(0, NUM_CHROMOSOMES):
            # cant mate w itself
            par1_i = random.randint(0, len(parents)-1)
            par2_i = random.randint(0, len(parents)-1)
            while par1_i == par2_i:
                par2_i = random.randint(0, len(parents)-1)
            
            parent1 = parents[par1_i]
            parent2 = parents[par2_i]
            child = mate(parent1, parent2)
            new_generation.append(child)
        
        chromos = new_generation

        # while loop 
        count += 1

    best_index = int(min(SIMILARITY_COEFF * NUM_CHROMOSOMES, NUM_CHROMOSOMES - 1))
    return chromos[best_index]

#
# fitness_function: function for genetic algorithm that mates the chromosomes
#
def mate(parent1, parent2):
    child = []
    for i in range(0, len(parent1)):
        if i < len(parent1) /2:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child


#
# generate_grammar: generates the grammar sequence for the piece
#
def generate_grammar():
    exp = exp_grammar[random.randint(0, 2)]
    dev = dev_grammar[random.randint(0, 3)]
    final = final_grammar[random.randint(0, 2)]

    grammar_seq = []
    # making grammar
    for i in exp:
        grammar_seq.append(random_grammar(i))

    for i in dev:
        grammar_seq.append(random_grammar(i))

    for i in final:
        grammar_seq.append(random_grammar(i))
    
    return mix_grammar(grammar_seq)

#
# random_grammar: randomly chooses values for grammar
#
def random_grammar(letter):
    if letter == 'K':
        return random.choices([tup[0] for tup in k], weights=[tup[1] for tup in k], k=1)
    elif letter == 'L':
        return random.choices([tup[0] for tup in l], weights=[tup[1] for tup in l], k=1)
    elif letter == 'M':
        return random.choices([tup[0] for tup in m], weights=[tup[1] for tup in m], k=1)
    else: # letter == 'N'
        return random.choices([tup[0] for tup in n], weights=[tup[1] for tup in n], k=1)


#
# mix_grammar: mixes roles to be assigned to different voices
#
def mix_grammar(sequence):
    new_seq = []
    for i in sequence:
        shuffled = ''.join(random.sample(i, len(i)))  #random permutation
        new_seq.append(shuffled)
    return new_seq


#
# each_part: calls respective functions to append pitch and rhythm sequence
#            to respective voices
#
def each_part(i, voice, sub_seq):
    if i == 'S':
        insert_subject(sub_seq, voice)
    elif i == 'A':
        generate_serialism(sub_seq, voice)
    elif i == 'C':
        new_cs = genetic_algorithm(sub_seq)
        for j in range(0, len(new_cs)):
            voice.append(note.Note(new_cs[j], quarterLength = subject_rhythm[j % NOTES_PER_SECTION]))
    else: # i == '_'
            insert_rest(voice)


#
# make_voice: calls each_part to append values into voices
#
def make_voice(v1, v2, v3, subject_sequence):
    sub_seq = subject_sequence
    for i in range(0, len(v1)):
        if v1[i] == 'S' or v2[i] == 'S' or v3[i] == 'S':
            sub_seq = generate_monte_carlo()
        each_part(v1[i], voice1, sub_seq)
        each_part(v2[i], voice2, sub_seq)
        each_part(v3[i], voice3, sub_seq)

#
# make_chord_voice4: adds chords to voice4
#
def make_chord_voice4():
    global chord_list
    
    for i in range(0, 96):
        prev = None
        
        
        # insert rules here... 
        while True:
            curr = random.choice(chord_list)
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

        voice4.append(chord.Chord(curr, quarterLength = 4))
        prev = curr

def main(): 

    generate_subject_rhythm()
    grammar_seq = generate_grammar()
    v1 = []
    v2 = []
    v3 = []
    for i in grammar_seq:
        v1.append(i[0])
        v2.append(i[1])
        v3.append(i[2])

    print(grammar_seq)

    subject_sequence = generate_monte_carlo()
    make_voice(v1, v2, v3, subject_sequence)

    top_level = stream.Score()
    
    # transpose voice1 1 octave up
    for i in range(0, len(voice1)):
        if isinstance(voice1[i], note.Note):
            voice1[i].pitch.midi += 12
        
    # transpose voice3 1 octave down
    for i in range(0, len(voice3)):
        if isinstance(voice3[i], note.Note):
            voice3[i].pitch.midi -= 12

    make_chord_voice4()

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
    elif ("-s" in sys.argv):
        top_level.write(fp="proj.xml")
    else:
        top_level.show('text') #Useful for debugging!

if __name__ == "__main__":
    main()
