import pandas as pd
from readfile import read_tasect
import numpy as np
from criterias import overalloc, time_conflicts, undersupport, unwilling, unpreffered, testfiles
from criterias import tas_n, sect_n
from agents import mutating_agent, min_agent, min_agent_ran, add_preferred_courses
from evo import Evo
from profiler import Profiler, profile

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
E.add_mut_agent(mutating_agent)
E.add_agent("min_agent", min_agent, k=2)
E.add_agent("min_agent_ran", min_agent_ran, k=2)
# E.add_agent("add_preferred_courses", add_preferred_courses, k=1)
# E.add_agent("", ___, k=num_sols_needed)

# Create random initial solution matrix
array = np.random.randint(0, 2, size=(len(sect_n), len(tas_n)))
array1 = np.random.randint(0, 2, size=(len(sect_n), len(tas_n)))
E.add_solution(array)
E.add_solution(array1)


E.evolve(time_limit=30, dom=100, status=100000, mutate = 4, mut_fact = 100)
print(E)

Profiler.report()

