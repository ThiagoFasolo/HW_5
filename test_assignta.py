import numpy as np
import pandas as pd
from criterias import overalloc, time_conflicts, undersupport, unwilling, unpreffered, calc_objs

# Define sample array for testing
# Load the result files to examine the expected values and assist in comparisons
test1_res = np.genfromtxt('test1_res.csv', delimiter=',', skip_header=0).T
test1_res_cleaned = test1_res[~np.isnan(test1_res)]

test2_res = np.genfromtxt('test2_res.csv', delimiter=',', skip_header=0).T
test2_res_cleaned = test2_res[~np.isnan(test2_res)]

test3_res = np.genfromtxt('test3_res.csv', delimiter=',', skip_header=0).T
test3_res_cleaned = test3_res[~np.isnan(test3_res)]


# Display the results from each result file
print(test1_res_cleaned)

def test_objectives(test_files=['test1.csv', 'test2.csv', 'test3.csv'], result_files=['test1_res.csv', 'test2_res.csv', 'test3_res.csv'], *objectives):
    for test_file, result_file in zip(test_files, result_files):
        t_array = np.genfromtxt(test_file, delimiter=',', skip_header=0).T
        r_array = np.genfromtxt(result_file, delimiter=',', skip_header=0).T
        res = 0
        for obj in objectives:
            res += obj(t_array)
        print(f"Test Results for {test_file}: {res}")




# Test cases
def test_overalloc():
    result = overalloc(sample_array)
    expected_value = None  # Define expected value based on sample data
    assert result == expected_value, f"Expected {expected_value}, got {result}"

def test_time_conflicts():
    result = time_conflicts(sample_array)
    expected_value = None
    assert result == expected_value, f"Expected {expected_value}, got {result}"

def test_undersupport():
    result = undersupport(sample_array)
    expected_value = None
    assert result == expected_value, f"Expected {expected_value}, got {result}"

def test_unwilling():
    result = unwilling(sample_array)
    expected_value = None
    assert result == expected_value, f"Expected {expected_value}, got {result}"

def test_unpreferred():
    result = unpreffered(sample_array)
    expected_value = None
    assert result == expected_value, f"Expected {expected_value}, got {result}"

def test_calc_objs():
    calc_objs(sample_array)

# Run tests
if __name__ == '__main__':
    test_overalloc()
    test_time_conflicts()
    test_undersupport()
    test_unwilling()
    test_unpreferred()
    test_calc_objs()
