import random


BARS_PER_PHRASE = 8
NOTES_PER_SECTION = 0

note_options = [0.5, 1, 1.5, 2]
default_weights = [20, 50, 5, 40]
activity = []


#
# generate_subject_rhythm: generates an 8-bar rhythm that is standard for all
#                          subject voices in the piece using the Monte Carlo 
#                          method
#
def generate_subject_rhythm():
    global NOTES_PER_SECTION, activity

    # make no modifiers for subject rhythm
    default_activity = [1] * BARS_PER_PHRASE
    sub_rhythm = generate_rhythm(default_activity)
    NOTES_PER_SECTION = len(sub_rhythm)
    
    activity = measure_activity(sub_rhythm)
    return NOTES_PER_SECTION, sub_rhythm

def measure_activity(sub_rhythm):
    activity_factors = []
    subj_index = 0
    for i in range(0, BARS_PER_PHRASE): 
        sum = 0
        activity = 0
        while sum < 4:
            sum += sub_rhythm[subj_index]
            subj_index += 1
            activity += 1
        activity_factors.append(activity)
    
    for i in range(0, len(activity_factors)):
        activity_factors[i] = activity_factors[i] / 4.0
    
    print("activity factors: ", activity_factors)
    return activity_factors


def generate_cs_rhythm(sub_rhythm):
    global activity 
    return generate_rhythm(activity)
    


def generate_rhythm(activity):
    global NOTES_PER_SECTION, note_options, default_weights


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
                note_weights[3] = max(note_weights[3] - 40, 0)
                
            # want strings of eighth notes
            if prev1 == .5 and prev2 == .5:
                note_weights[0] += 40
                
            # make it very likely to end w half note
            if sum == 30:
                note_weights[3] = 100
                
            # get back to downbeat if we get dotted quarter
            if prev1 == 1.5:
                note_weights = [80, 0, 20, 0]
                
            # no three half notes in a row
            if prev1 == 2 and prev2 == 2:
                note_weights[3] = 0
                
            # modify weights based on activity
            # activity_index = int( (sum+curr) / 4 ) if (sum + curr) < 32 else BARS_PER_PHRASE -1
           
            curr_activity = activity[int(sum/4)]
            # print("curr activity: ", curr_activity)
            # curr_activity = 1.5 # testing
            # if subject is more active, want current iteration to be less active and vice versa
            # lower current activity factor ==> modify note weights to favor shorter notes
            # higher current activity factor ==> modify note weights to favor longer notes
            note_weights[0] *= (2 - curr_activity)
            note_weights[1] *= 1 # unchanged
            note_weights[2] *= curr_activity
            note_weights[3] *= curr_activity

            # print("note weight sum: ", str(note_weights[0] + note_weights[1] + note_weights[2] + note_weights[3]))

            curr = random.choices(note_options, weights=note_weights)[0]

            # no ties over bar lines
            if (sum % 4 ) > (sum + curr) % 4 and (sum + curr) % 4 != 0:
                note_weights = default_weights.copy()
                continue
            
            # don't start half notes off of downbeat
            if curr == 2 and sum % 1 != 0:
                note_weights = default_weights.copy()
                continue

            # must to sum to exactly 32
            if sum + curr > 32:
                note_weights = default_weights.copy()
                continue
            break
        
        rhythm.append(curr)
        sum += curr
        prev1 = curr
        prev2 = prev1
        note_weights = default_weights.copy()
    
    return rhythm
