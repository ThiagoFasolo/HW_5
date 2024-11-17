import numpy as np
import pandas as pd
from readfile import read_tasect
from criterias import overalloc, time_conflicts, undersupport, unwilling, unpreffered, testfiles, tas_n, sect_n
from ivan_evo import Evo

# read and test the test files
testfiles('test1.csv', 'test2.csv', 'test3.csv')

# create the environment
E = Evo()

# Add the objective functions
E.add_objective("overalloc", overalloc)
E.add_objective("time_conflicts", time_conflicts)
E.add_objective("undersupport", undersupport)
E.add_objective("unwilling", unwilling)
E.add_objective("unpreffered", unpreffered)

# Register agents with Evo
E.add_agent("swapper", swapper, k=1)

# Create random initial solution matrix
array = np.random.randint(0, 2, size=(len(sect_n), len(tas_n)))
E.add_solution(array)

print(E)
E.evolve(n=5000000, dom=100, status=100000)
print(E)
