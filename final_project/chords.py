from music21 import *
import numpy as np
import sys

harmony = stream.Part()

# np 8x8 matrix of zeros 


# things that could be interesting: 
# different matrices for major/minor
# 7th chords? 
# different matrices for different composers' styles
# would probably need to have customizable lengths==> make functions modular

chord_matrix = np.array([
    [0, .1, .1, .1, .3, .3, .1], #I
    [.2, 0, 0, 0, .6, 0, .2], #ii
    [0, 0, 0, .3, 0, .6, .1], #iii
    [.1, 0, .2, .3, .4, 0, 0], #IV
    [.5, .1, 0, 0, .2, 0, .2], #V
    [.2, 0, 0, .5, .3, 0, 0], #vi
    [.8, 0, 0, 0, 0, .2, 0] #viidim
])



def gen_progression(length):
    progression = np.zeros(length)
    progression[0] = 0 # start w tonic
    
    for i in range(1, length):
        print("working on " + str(i))
        current = int(progression[i - 1])
        probabilites = chord_matrix[current]
        progression[i] = np.random.choice(len(probabilites), p=probabilites)

    return progression

progression = gen_progression(8)
C_MIDI = 60
for c in progression:
    newChord = chord.Chord([int(C_MIDI + c), int(C_MIDI + c+4), int(C_MIDI + c+7)])
    harmony.append(newChord)
    print("Chord: " + str(c) + " " + str(newChord.pitchNames))

top_level = stream.Stream()
top_level.insert(0, harmony)
if ("-m" in sys.argv):
    top_level.write('midi', fp="out.midi")
elif ("-s" in sys.argv):
    top_level.write(fp="out.xml")
else:
    top_level.show('text') #Useful for debugging!
    
# for chord in progression:
#     if chord == 0:
#         print("I")
#     elif chord == 1:
#         print("ii")
#     elif chord == 2:
#         print("iii")
#     elif chord == 3:
#         print("IV")
#     elif chord == 4:
#         print("V")
#     elif chord == 5:
#         print("vi")
#     elif chord == 6:
#         print("viidim")