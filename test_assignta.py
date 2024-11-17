import numpy as np
from criterias import overalloc, time_conflicts, undersupport, unwilling, unpreffered, calc_objs, testfiles

test_arrays = testfiles('test1.csv', 'test2.csv', 'test3.csv')
print(test_arrays)

# Test cases
def test_overalloc():
    result = overalloc(sample_array)
    assert result == expected_value  # Replace with expected value based on sample data

def test_time_conflicts():
    result = time_conflicts(sample_array)
    assert result == expected_value  # Replace with expected value based on sample data

def test_undersupport():
    result = undersupport(sample_array)
    assert result == expected_value  # Replace with expected value based on sample data

def test_unwilling():
    result = unwilling(sample_array)
    assert result == expected_value  # Replace with expected value based on sample data

def test_unpreferred():
    result = unpreffered(sample_array)
    assert result == expected_value  # Replace with expected value based on sample data

def test_calc_objs(capsys):
    calc_objs(sample_array)
    captured = capsys.readouterr()
    # Define assertions based on expected printed output

# To test the testfiles function
def test_testfiles():
    # Test file paths
    testfile_paths = ["testfile1.csv", "testfile2.csv"]
    testfiles(*testfile_paths)
    # Add assertions or validations for expected behavior if possible

# Replace expected_value with correct values based on your logic for each function.
