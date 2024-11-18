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

def find_conflicts(assignment, conflicting_labs):
    conflicts = []

    # Iterate over each group of conflicting labs
    for conflict_group in conflicting_labs:
        # Sum the assignments in the conflicting labs
        sub_matrix = assignment[:, conflict_group]  # Selecting columns for the labs
        conflicts_sum = np.sum(sub_matrix, axis=1)  # Sum along the columns now to get sum per TA

        # Identify TAs with conflicts
        # Conflict occurs if a TA is assigned to more than one lab in the group
        conflict_indices = np.where(conflicts_sum > 1)[0]  # TAs indices with conflicts

        # Append conflicts for each TA
        for ta_index in conflict_indices:
            # Find specific labs where the TA is assigned within this conflict group
            assigned_labs = [lab for lab in conflict_group if assignment[ta_index, lab] == 1]
            conflicts.append([(ta_index, lab) for lab in assigned_labs])

    return conflicts


@profile
def resolve_time_conflicts(assignment):
    # Create mapping of lab IDs to their corresponding time slots
    conflicting_labs = {}
    for lab_id, time_id in sect_n[:, [0, 1]]:
        if time_id not in conflicting_labs:
            conflicting_labs[time_id] = []
        conflicting_labs[time_id].append(lab_id)

    # Convert conflicting lab IDs into lists of conflicts
    conflicting_labs_list = list(conflicting_labs.values())
    # Find conflicts based on current assignment
    conflicts = find_conflicts(assignment[0], conflicting_labs_list)
    resolved_assignment = assignment[0].copy()

    # Resolve each conflict
    for conflict_group in conflicts:
        for ta_index in set(ta for ta, _ in conflict_group):
            # Extract just the lab indices for the current TA's conflicts
            ta_conflicts = [lab for ta, lab in conflict_group if ta == ta_index]

            if len(ta_conflicts) > 1:
                keep_lab = np.random.choice(ta_conflicts)  # Randomly choose one lab to keep
                for lab in ta_conflicts:
                    if lab != keep_lab:
                        resolved_assignment[ta_index, lab] = 0

    return resolved_assignment





