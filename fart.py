import numpy as np
import pandas as pd

from assignta import undersupport_penalty, unwilling_penalty


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
    ta_alloc = array.sum(axis=1)  # Sum assignments for each TA across sections
    ta_req = tas_n[:, 1]  # Max assigned column from tas_n

    difference = ta_alloc - ta_req
    print("Overallocation Differences:", difference)
    difference[difference < 0] = 0  # Ignore under-allocation

    return np.sum(difference)


# Time conflict penalty calculation
def time_conflicts(array, sect_n):
    conflicts = 0
    # Extract the `daytime` information for each section
    section_times = sect_n[:, 1]  # Assuming 2nd column in sect_n represents meeting time
    print(sect_n)
    # Iterate over each TA (row in array)
    for ta_idx in range(array.shape[0]):
        # Find all sections assigned to this TA
        assigned_sections = np.where(array[ta_idx, :] == 1)[0]

        # Check for time conflicts by looking at the `daytime` values
        assigned_times = section_times[assigned_sections]

        # Count as a conflict if there are duplicate times
        if len(assigned_times) != len(set(assigned_times)):
            conflicts += 1  # Only count one conflict per TA, regardless of number of conflicts

    return conflicts
def undersupport(array, sect_n):
    # Extract the required TA count for each section
    required_tas = sect_n[:, -2]  # Assuming the last column in sect_n is 'min_tas_required'

    # Calculate the number of TAs assigned to each section
    actual_tas = array.sum(axis=0)  # Sum each column to get the count of TAs assigned per section

    # Calculate penalties for under-support
    under_support = required_tas - actual_tas
    under_support[under_support < 0] = 0  # No penalty if actual TAs meet or exceed required

    # Sum up the total under-support penalties
    return np.sum(under_support)

# Unwilling penalty calculation
def unwilling(array, tas_n):
    penalty = 0
    # Iterate over each TA and section
    for ta_idx in range(array.shape[0]):
        for sec_idx in range(array.shape[1]):
            # Check if TA is assigned to this section and unwilling to support it
            if array[ta_idx, sec_idx] == 1 and tas_n[ta_idx, sec_idx + 2] == 0:  # Assuming 0 means unwilling
                penalty += 1
    return penalty



# Load Test1.csv to use as the assignment array
def load_test_array(filename='Test1.csv'):
    '''Loads Test1.csv as an assignment matrix'''
    return pd.read_csv(filename, header=None).to_numpy()


# Main execution
tas, sect = read_tasect()
tas_n = tas.to_numpy()
sect_n = sect.to_numpy()

# Load the test assignment array from Test1.csv
array = load_test_array('Test1.csv')
print("Assignment Array from Test1.csv:\n", array)

# Calculate overallocation and time conflict penalties
overallocation_penalty = overalloc(array, tas_n)
time_conflict_penalty = time_conflicts(array, sect_n)
undersupport_penalty = undersupport(array, sect_n)
unwilling_penalty = unwilling(array, sect_n)

# Display results
print("Overallocation Penalty:", overallocation_penalty)
print("Time Conflict Penalty:", time_conflict_penalty)
print("Undersupport Penalty:", undersupport_penalty)
print("Unwilling Penalty:", unwilling_penalty)