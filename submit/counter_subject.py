"""
Tufts University | CS 150 Algorithmic Music Composition
Fall 2025 | Final Project
Authors: Matthew Dacey (mdacey02), Sam Lev (slev01),
         Begüm Ugurlu (bugurl01), Kimaya Vaid (kvaid01)

Generates a harmonius counter subject using a genetic algorithm
"""

from top_level import *
from rhythm_gen import *
import numpy as np

# constants
NUM_GENERATIONS = 50
NUM_CHROMOSOMES = 1000
NUM_PARENTS = 100 # must be even
SIMILARITY_COEFF = 0.17


def initialize_population(subject_rhythm):
    """
    Generates initial population for genetic algorithm
    """
    all_chromosomes = []
    for i in range(0, NUM_CHROMOSOMES):
        chromo_pitches = []
        chromo_rhythm = generate_cs_rhythm()
        # print("chromo rhythm: ", chromo_rhythm)
        for j in range(0, len(chromo_rhythm)):
            one_note = ALL_NOTES[random.randint(0, 6)]
            chromo_pitches.append(one_note)
        chromo = (chromo_pitches, chromo_rhythm)
        
        all_chromosomes.append(chromo)
    return all_chromosomes



def fitness_functon(sub_pitches, sub_rhythm, one_chromo):
    """
    function for genetic algorithm that calculates the fitness
    "cost" for all chromosomes. The higher cost implies less
    less similar to the subject sequence
    """
    score = 0
    sub_notes = []
    chromo_notes = []
    
    for i in range(0, len(sub_rhythm)):
        if sub_rhythm[i] == .5:
            sub_notes.append(sub_pitches[i])
        elif sub_rhythm[i] == 1:
            sub_notes.append(sub_pitches[i])
            sub_notes.append(sub_pitches[i])
        elif sub_rhythm[i] == 1.5:
            sub_notes.append(sub_pitches[i])
            sub_notes.append(sub_pitches[i])
            sub_notes.append(sub_pitches[i])
        else: # sub_rhythm[i] == 2
            sub_notes.append(sub_pitches[i])
            sub_notes.append(sub_pitches[i])
            sub_notes.append(sub_pitches[i])
            sub_notes.append(sub_pitches[i])
    
    chromo_pitches = one_chromo[0]
    chromo_rhythm = one_chromo[1]

    for i in range(0, len(chromo_rhythm)):
        if chromo_rhythm[i] == .5:
            chromo_notes.append(chromo_pitches[i])
        elif chromo_rhythm[i] == 1:
            chromo_notes.append(chromo_pitches[i])
            chromo_notes.append(chromo_pitches[i])
        elif chromo_rhythm[i] == 1.5:
            chromo_notes.append(chromo_pitches[i])
            chromo_notes.append(chromo_pitches[i])
            chromo_notes.append(chromo_pitches[i])
        else: # chromo_rhythm[i] == 2
            chromo_notes.append(chromo_pitches[i])
            chromo_notes.append(chromo_pitches[i])
            chromo_notes.append(chromo_pitches[i])
            chromo_notes.append(chromo_pitches[i])

    for i in range(0, len(sub_notes)):
        score += helper_fitness(sub_notes[i], chromo_notes[i])
    
    return score


def helper_fitness(sub_seq, chromo):
    """
    function for genetic algorithm that calculates the fitness
    "cost" for all chromosomes
    """
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


def genetic_algorithm(sub_pitches, sub_rhythm):
    """
    generates the pitch sequence for the counter subject
    using a genetic algorithm
    """
    chromos = initialize_population(sub_rhythm)
    
    count = 0
    while count < NUM_GENERATIONS:
        chromos.sort(key=lambda x: fitness_functon(sub_pitches, sub_rhythm, x))    

        new_generation = []
        for _ in range(NUM_CHROMOSOMES):
        #normal distribution selection
            parent1 = norm_select(chromos, SIMILARITY_COEFF)
            parent2 = norm_select(chromos, SIMILARITY_COEFF)
            child = mate(parent1, parent2)
            new_generation.append(child)
        
        chromos = new_generation

        # while loop 
        count += 1

    best_index = int(min(SIMILARITY_COEFF * NUM_CHROMOSOMES, NUM_CHROMOSOMES - 1))
    return chromos[best_index]


def mate(parent1, parent2):
    child_pitches = []
    child_rhythm = []
    
    valid_split_point = False
    par1_split_point = -1
    par2_split_point = -1
    
    while not valid_split_point:
        # randomly choose where 1st parent's genes end and 2nd parent's genes begin
        par1_split_point = random.randint(0, len(parent1[1]) -1)
        
        rhythm_sum = 0
        # find what beat split point falls on
        for i in range(0, par1_split_point):
            rhythm_sum += parent1[1][i]
        
        sum = 0
        index = 0
        # get index in parent 2 that starts on split point beat
        while sum < rhythm_sum:
            sum += parent2[1][index]
            index += 1
        
        # if they line up perfectly continue, if not repeat randomness
        if sum == rhythm_sum:
            valid_split_point = True
            par2_split_point = index


    for i in range(0, par1_split_point):
        child_pitches.append(parent1[0][i])
        child_rhythm.append(parent1[1][i])
    for i in range(par2_split_point, len(parent2[1])):
        child_pitches.append(parent2[0][i])
        child_rhythm.append(parent2[1][i])
    return (child_pitches, child_rhythm)

def norm_select(sorted_chromos, similarity_coeff):
    """
    selects an index based on a normal distribution centered around the
    similarity coefficient.

    similarity_coeff should be a real number in [0,1]
    """
    pop_size = len(sorted_chromos)
    std_dev = 0.05 * pop_size #50 for population of 1000
    target_idx = pop_size * similarity_coeff
    par_idx = -1
    while not (0 <= par_idx < pop_size):
        par_idx = round(np.random.normal(loc=target_idx, scale=std_dev))
    return sorted_chromos[par_idx]
