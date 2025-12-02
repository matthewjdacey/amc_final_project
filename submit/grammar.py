"""
grammar.py
Tufts University | CS 150 Algorithmic Music Composition
Fall 2025 | Final Project
Authors: Matthew Dacey (mdacey02), Sam Lev (slev01),
         Begüm Ugurlu (bugurl01), Kimaya Vaid (kvaid01)

Derives high-level structure of composition from grammar
"""
import random

# grammar encoding
EXP_GRAMMAR = ["KLKL", "KLLL", "KKLL"]
DEV_GRAMMAR = ["KMLL", "MLML", "MMML", "LMKL"]
FINAL_GRAMMAR = ["KNKK", "KNNK", "NNKN"]
K = [("S__", 0.3), ("SC_", 0.7)]
L = [("A__", 0.2), ("AC_", 0.6), ("C__", 0.2)]
M = [("AAC", 0.25), ("CCA", 0.25), ("CCC", 0.25), ("AAA", 0.25)]
N = [("SC_", 0.4), ("SS_", 0.4), ("C__", 0.2)]

def generate_grammar():
    """
    Randomly derives a structure from the encoded grammar
    """
    exp = random.choice(EXP_GRAMMAR)
    dev = random.choice(DEV_GRAMMAR)
    final = random.choice(FINAL_GRAMMAR)

    grammar_seq = []
    # making grammar
    for i in exp:
        grammar_seq.append(random_grammar(i))

    for i in dev:
        grammar_seq.append(random_grammar(i))

    for i in final:
        grammar_seq.append(random_grammar(i))
    
    return mix_grammar(grammar_seq)


def random_grammar(letter):
    """
    Randomly selects symbols from the grammar
    """
    if letter == 'K':
        return random.choices([tup[0] for tup in K], weights=[tup[1] for tup in K], k=1)
    elif letter == 'L':
        return random.choices([tup[0] for tup in L], weights=[tup[1] for tup in L], k=1)
    elif letter == 'M':
        return random.choices([tup[0] for tup in M], weights=[tup[1] for tup in M], k=1)
    else: # letter == 'N'
        return random.choices([tup[0] for tup in N], weights=[tup[1] for tup in N], k=1)


def mix_grammar(sequence):
    """
    Shuffles which role is assigned to which voice in the score,
    given a derivation from the grammar
    """
    new_seq = []
    for i in sequence:
        shuffled = list(i[0])
        random.shuffle(shuffled)
        shuffled = str(''.join(shuffled))
        
        new_seq.append(shuffled)
    return new_seq