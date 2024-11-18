import numpy as np
from criterias import tas_n, sect_n
from profiler import profile, Profiler

global tas_n
global sect_n

@profile
def mutating_agent(sol, num_changes):
    '''' Randomly mutates a given solution matriz by flipping values at specific positions
    Takes in 2D array and number of mutations applied'''
    indices = np.random.choice(sol.size, num_changes, replace=False)
    row_indices, col_indices = np.unravel_index(indices, sol.shape)
    sol[row_indices, col_indices] = 1 - sol[row_indices, col_indices]
    #
    return sol

@profile
def min_agent(sols):
    ''' agent multiplies two matrixes
    finds what values are the same'''
    return sols[0] * sols[1]


@profile
def min_agent_ran(sols):
    '''
    Agent multiplies two matrices element-wise.
    Fills some of the remaining 0s with random 1s.

    Parameters:
    sols (list of np.array): List containing two 2D numpy arrays to be multiplied element-wise.

    Returns:
    np.array: The resulting matrix after filling some zero values with random 1s.
    '''
    # Element-wise multiplication of the two matrices
    sol = sols[0] * sols[1]
    # Find the indices of zeros in the matrix
    zero_indices = np.where(sol == 0)
    zero_indices_list = list(zip(zero_indices[0], zero_indices[1]))
    # Determine the number of
    # zero positions to turn into 1s (randomly select a subset)
    num_random_ones = int(len(zero_indices_list) * 0.25)  # e.g., 25% of zeros are converted to 1s
    random_indices = np.random.choice(len(zero_indices_list), num_random_ones, replace=False)
    # Set randomly selected zero positions to 1
    for idx in random_indices:
        row, col = zero_indices_list[idx]
        sol[row, col] = 1

    return sol


@profile
def add_preferred_courses(sol):
    # MAY NOT WORK BECAUSE OF IT NEEDS A DICT FOR PREFFERED CLASS. MAYBE YOU CAN MAKE IT WORK
    """
    Add preferred courses to the solution matrix for each TA without conflicts.

    Parameters:
    sol (np.array): A 2D array where rows represent TAs and columns represent courses (1 if assigned, 0 if not).
    preferred_courses (dict): A dictionary mapping each TA (row index) to a list of preferred course indices (column indices).

    Returns:
    np.array: Updated solution matrix with preferred courses added where possible.
    """
    # Iterate over each TA and their preferred courses
    for ta_index, courses in tas_n[:, 2:]:
        # Check if the TA already has an assigned course
        if not np.any(sol[ta_index, :]):  # Ensure no other courses are assigned to this TA
            for course_index in courses:
                # Assign the first available preferred course without conflict
                sol[ta_index, course_index] = 1
                break  # Stop after assigning the first preferred course

    return sol

@ profile
def remove_time_conflicts(sol, time_blocks):
    # SAME ISSUE AS ABOVE
    """
    Ensure each TA is assigned to only one time block, removing any conflicts.

    Parameters:
    sol (np.array): A 2D array where rows represent TAs and columns represent courses (1 if assigned, 0 if not).
    time_blocks (list): A list where each entry represents the time block of the corresponding column in `sol`.

    Returns:
    np.array: Updated solution matrix with time conflicts removed.
    """
    # Iterate over each TA
    for ta_index in range(sol.shape[0]):
        # Dictionary to keep track of the first assignment in each time block
        assigned_in_block = {}

        # Iterate over each course assignment for the current TA
        for course_index in range(sol.shape[1]):
            if sol[ta_index, course_index] == 1:  # TA is assigned to this course
                time_block = time_blocks[course_index]

                # Check if the TA is already assigned to another course in this time block
                if time_block in assigned_in_block:
                    # Conflict: reset this course assignment to 0
                    sol[ta_index, course_index] = 0
                else:
                    # No conflict: store the course as assigned in this time block
                    assigned_in_block[time_block] = course_index

    return sol


