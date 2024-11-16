import numpy as np
import pandas as pd


# Read and preprocess TA and section data
def read_tasect(tasfile='tas.csv', sectfile='sections.csv'):
    '''Reads and cleans section and TA information'''
    # Read files
    tas = pd.read_csv(tasfile)
    sect = pd.read_csv(sectfile)

    # Clean and prepare section data
    clean_sect = sect.drop(columns=['instructor', 'location', 'students', 'topic'])
    clean_sect['daytime'], time_index = pd.factorize(clean_sect['daytime'])

    # Clean and prepare TA data
    mapping = {'U': 0, 'W': 1, 'P': 2}
    clean_tas = tas.drop(columns=['name'])
    for col in clean_tas.columns[2:]:
        clean_tas[col] = clean_tas[col].map(mapping)

    return clean_tas, clean_sect


# Overallocation penalty calculation
def overalloc(array, tas_n):
    ta_alloc = array.sum(axis=0)
    ta_req = tas_n[:, 1]  # Max assigned column

    difference = ta_alloc - ta_req
    difference[difference < 0] = 0  # Ignore under-allocation

    return np.sum(difference)





# Time conflict penalty calculation
def time_conflicts(array, sect_n):
    conflicts = 0
    for ta_idx in range(array.shape[1]):
        assigned_sections = np.where(array[:, ta_idx] == 1)[0]
        assigned_times = sect_n[assigned_sections, 1]  # Assuming 2nd column in sect_n is time

        if len(assigned_times) != len(set(assigned_times)):
            conflicts += 1  # Count TA with time conflicts
    return conflicts


# Under-support penalty calculation
def undersupport(array, sect_n):
    required_tas = sect_n[:, -1]  # Assuming last column in sect_n is required TA count
    actual_tas = array.sum(axis=1)

    under_support = required_tas - actual_tas
    under_support[under_support < 0] = 0  # Ignore over-support

    return np.sum(under_support)


# Unwilling penalty calculation
def unwilling(array, tas_n):
    penalty = 0
    for sec_idx in range(array.shape[0]):
        for ta_idx in range(array.shape[1]):
            if array[sec_idx, ta_idx] == 1 and tas_n[ta_idx, 2 + sec_idx] == 0:  # Assuming 0 means unwilling
                penalty += 1
    return penalty


# Unpreferred penalty calculation
def unpreferred(array, tas_n):
    penalty = 0
    for sec_idx in range(array.shape[0]):
        for ta_idx in range(array.shape[1]):
            if array[sec_idx, ta_idx] == 1 and tas_n[
                ta_idx, 2 + sec_idx] == 1:  # Assuming 1 means willing, not preferred
                penalty += 1
    return penalty


# Read in data
tas, sect = read_tasect()
tas_n = tas.to_numpy()
sect_n = sect.to_numpy()

# Create random assignment matrix
array = np.random.randint(0, 2, size=(len(sect), len(tas)))

# Calculate objectives
overallocation_penalty = overalloc(array, tas_n)
time_conflict_penalty = time_conflicts(array, sect_n)
undersupport_penalty = undersupport(array, sect_n)
unwilling_penalty = unwilling(array, tas_n)
unpreferred_penalty = unpreferred(array, tas_n)

# Display results
print("Overallocation Penalty:", overallocation_penalty)
print("Time Conflict Penalty:", time_conflict_penalty)
print("Under-Support Penalty:", undersupport_penalty)
print("Unwilling Penalty:", unwilling_penalty)
print("Unpreferred Penalty:", unpreferred_penalty)
