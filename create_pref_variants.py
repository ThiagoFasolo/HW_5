from itertools import product
import numpy as np
import random
from criterias import tas_n, sect_n
from profiler import Profiler, profile
global tas_n
global sect_n
@profile
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


def generate_variants(base_matrix, conflicts):
    # Initialize the list of all variant matrices
    variants = []

    # Create a list of lists, where each sublist contains all possible configurations for each conflict group
    all_combinations = []

    for conflict_group in conflicts:
        group_combinations = []
        for coord in conflict_group:
            # Create a new copy of the base matrix for each possibility
            temp_matrix = base_matrix.copy()
            # Set all conflicted coordinates to 0
            for c in conflict_group:
                temp_matrix[c[0], c[1]] = 0
            # Set the current coordinate to 1
            temp_matrix[coord[0], coord[1]] = 1
            group_combinations.append(temp_matrix)
        all_combinations.append(group_combinations)

    # Shuffle the list in place
    random.shuffle(all_combinations)

    # Calculate the 1/5  size of the list
    part = len(all_combinations) // 5
    # Select the first
    all_combinations = all_combinations[:part]

    # Generate the product of all combinations across all conflict groups
    for combination in product(*all_combinations):
        # Combine matrices from each group into a single matrix
        combined_matrix = sum(combination)
        # Using 'minimum' to avoid overlapping 1's going beyond 1, if any
        combined_matrix = np.minimum(combined_matrix, 1)
        variants.append(combined_matrix)

    return variants


@profile
def create_prefs():
    '''
    create all possible combinations of preferene matrixes where everyone is willing
    '''

    # Create solution where everyone has their preferences
    pref_sol = tas_n[:, 2:]
    # Replace all 1s and 2s with 0s; Replace all 3s with 1s
    pref_sol[(pref_sol == 1) | (pref_sol == 2)] = 0
    pref_sol[pref_sol == 3] = 1

    # Find the Labs with time conflicts:
    conflicting_labs = {}
    for lab_id, time_id in sect_n[:, [0, 1]]:
        if time_id in conflicting_labs:
            conflicting_labs[time_id].append(lab_id)
        else:
            conflicting_labs[time_id] = [lab_id]
    conflicting_labs_list = list(conflicting_labs.values())
    # Find list of lists of conflicts
    conflicts = find_conflicts(pref_sol, conflicting_labs_list)

    # Create all solutions where no one has a time conflict:
    return generate_variants(pref_sol, conflicts)