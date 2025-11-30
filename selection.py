import numpy as np

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
