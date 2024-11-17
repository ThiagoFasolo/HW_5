import numpy as np
import pandas as pd
from criterias import overalloc, time_conflicts, undersupport, unwilling, unpreffered, calc_objs

# Load data from 'test1.csv' as sample_array
file = 'test1.csv'
# sample_array = pd.read_csv('test1.csv').values
# t_array = np.genfromtxt(file, delimiter=',', skip_header=0).T
sample_array = np.genfromtxt(file, delimiter=',', skip_header=0).T

def test_objectives(test_file, result_file, *objectives)
    result = overalloc(sample_array)
    expected_value = None  # Define expected value for overallocation based on sample data
# Test cases
def test_overalloc():
    result = overalloc(sample_array)
    expected_value = None  # Define expected value for overallocation based on sample data
    assert result == expected_value, f"Expected {expected_value}, got {result}"

def test_time_conflicts():
    result = time_conflicts(sample_array)
    expected_value = None  # Define expected value for time conflicts based on sample data
    assert result == expected_value, f"Expected {expected_value}, got {result}"

def test_undersupport():
    result = undersupport(sample_array)
    expected_value = None  # Define expected value for undersupport based on sample data
    assert result == expected_value, f"Expected {expected_value}, got {result}"

def test_unwilling():
    result = unwilling(sample_array)
    expected_value = None  # Define expected value for unwilling penalty based on sample data
    assert result == expected_value, f"Expected {expected_value}, got {result}"

def test_unpreferred():
    result = unpreffered(sample_array)
    expected_value = None  # Define expected value for unpreferred penalty based on sample data
    assert result == expected_value, f"Expected {expected_value}, got {result}"

def test_calc_objs():
    # Use calc_objs directly for combined penalty outputs
    calc_objs(sample_array)

# Run tests
if __name__ == '__main__':
    test_overalloc()
    test_time_conflicts()
    test_undersupport()
    test_unwilling()
    test_unpreferred()
    test_calc_objs()