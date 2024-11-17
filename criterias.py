import numpy as np
from readfile import read_tasect

global tas_n
global sect_n

tas, sect = read_tasect(tasfile='tas.csv', sectfile='sections.csv')
tas_n = tas.to_numpy()
sect_n = sect.to_numpy()

# Overallocation penalty calculation
def overalloc(array):
    ta_alloc = array.sum(axis=0)
    ta_req = tas_n[:, 1]  # Max assigned column
    difference = ta_alloc - ta_req
    difference[difference < 0] = 0  # Ignore under-allocation

    return np.sum(difference)


# Time conflict penalty calculation
def time_conflicts(array):
    conflicts = 0
    for ta_idx in range(array.shape[1]):
        assigned_sections = np.where(array[:, ta_idx] == 1)[0]
        assigned_times = sect_n[assigned_sections, 1]  # Assuming 2nd column in sect_n is time

        if len(assigned_times) != len(set(assigned_times)):
            conflicts += 1  # Count TA with time conflicts
    return conflicts


# Under-support penalty calculation
def undersupport(array):
    required_tas = sect_n[:, 2]  # min ta
    actual_tas = array.sum(axis=1)

    under_support = required_tas - actual_tas
    under_support[under_support < 0] = 0  # Ignore over-support

    return np.sum(under_support)


# Unwilling penalty calculations
def unwilling(array):
    matrix = array * (tas_n[:, 2:]).T
    unwilling = np.count_nonzero(matrix == 1)
    return unwilling


# Unpreffered penalty calculations
def unpreffered(array):
    matrix = array * (tas_n[:, 2:]).T
    unprefered = np.count_nonzero(matrix == 2)
    return unprefered


def calc_objs(array):
    # Calculate objectives
    overallocation_penalty = overalloc(array)
    time_conflict_penalty = time_conflicts(array)
    undersupport_penalty = undersupport(array)
    unwilling_penalty = unwilling(array)
    unpreferred_penalty = unpreffered(array)

    # Display results
    print("Overallocation Penalty:", overallocation_penalty)
    print("Time Conflict Penalty:", time_conflict_penalty)
    print("Under-Support Penalty:", undersupport_penalty)
    print("Unwilling Penalty:", unwilling_penalty)
    print("Unpreferred Penalty:", unpreferred_penalty)


def testfiles(*files):
    for file in files:
        # read in test arrays
        print(file)
        t_array = np.genfromtxt(file, delimiter=',', skip_header=0).T
        calc_objs(t_array)