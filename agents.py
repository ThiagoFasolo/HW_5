import numpy as np
def mutating_agent(sol, num_changes):
    print('Sol', sol.size)
    print('num_changes', num_changes)
    indices = np.random.choice(sol.size, num_changes, replace=False)
    row_indices, col_indices = np.unravel_index(indices, sol.shape)
    sol[row_indices, col_indices] = 1 - sol[row_indices, col_indices]
    return sol

def min_agent(sols):
    ''' agent multiplies two matrixes
    finds what values are the same'''
    return sols[0] * sols[1]

def min_agent_wran(sols):
    ''' agent multiplies two matrixes
    fills the remaining 0s with random 1s'''
    sol = sols[0] * sols[1]
    # Find the indices of zeros in the matrix
    zero_indices = np.where(matrix == 0)
    zero_indices_list = list(zip(zero_indices[0], zero_indices[1]))

# def add_prefered_courses(sol):
#     ''' add all prefered courses of TAs that dont overlap'''
#     # what about
#
# def remove_time_conflicts(sol):
#     ''' make sure only 1 time black is chosen'''
#
# def add_willing_(sol):


