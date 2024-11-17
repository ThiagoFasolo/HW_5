import numpy as np
from criterias import overalloc, time_conflicts, undersupport, unwilling, unpreffered, calc_objs

# Load expected results and sample arrays
test1_res_cleaned = np.genfromtxt('test1_res.csv', delimiter=',', skip_header=0).T[~np.isnan(np.genfromtxt('test1_res.csv', delimiter=',', skip_header=0).T)]
test2_res_cleaned = np.genfromtxt('test2_res.csv', delimiter=',', skip_header=0).T[~np.isnan(np.genfromtxt('test2_res.csv', delimiter=',', skip_header=0).T)]
test3_res_cleaned = np.genfromtxt('test3_res.csv', delimiter=',', skip_header=0).T[~np.isnan(np.genfromtxt('test3_res.csv', delimiter=',', skip_header=0).T)]

sample_array1 = np.genfromtxt('test1.csv', delimiter=',', skip_header=0).T
sample_array2 = np.genfromtxt('test2.csv', delimiter=',', skip_header=0).T
sample_array3 = np.genfromtxt('test3.csv', delimiter=',', skip_header=0).T

# Define each test as a standalone function for pytest to detect
def test_overalloc():
    assert overalloc(sample_array1) == test1_res_cleaned[0]
    assert overalloc(sample_array2) == test2_res_cleaned[0]
    assert overalloc(sample_array3) == test3_res_cleaned[0]

def test_time_conflicts():
    assert time_conflicts(sample_array1) == test1_res_cleaned[1]
    assert time_conflicts(sample_array2) == test2_res_cleaned[1]
    assert time_conflicts(sample_array3) == test3_res_cleaned[1]

def test_undersupport():
    assert undersupport(sample_array1) == test1_res_cleaned[2]
    assert undersupport(sample_array2) == test2_res_cleaned[2]
    assert undersupport(sample_array3) == test3_res_cleaned[2]

def test_unwilling():
    assert unwilling(sample_array1) == test1_res_cleaned[3]
    assert unwilling(sample_array2) == test2_res_cleaned[3]
    assert unwilling(sample_array3) == test3_res_cleaned[3]

def test_unpreferred():
    assert unpreffered(sample_array1) == test1_res_cleaned[4]
    assert unpreffered(sample_array2) == test2_res_cleaned[4]
    assert unpreffered(sample_array3) == test3_res_cleaned[4]

def test_calc_objs():
    assert calc_objs(sample_array1) == sum(test1_res_cleaned)
    assert calc_objs(sample_array2) == sum(test2_res_cleaned)
    assert calc_objs(sample_array3) == sum(test3_res_cleaned)
