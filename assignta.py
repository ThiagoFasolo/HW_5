import pandas as pd
from readfile import read_tasect
import numpy as np
from criterias import overalloc, time_conflicts, undersupport, unwilling, unpreffered, testfiles
from criterias import tas_n, sect_n
from agents import mutating_agent, min_agent, min_agent_ran, add_preferred_courses
from evo import Evo
from profiler import Profiler, profile


# Function to find and display the best solution
def find_best_solution(pop):
    """
    This function identifies the best solution based on the lowest penalty sum,
    and prints the assigned sections for each TA and the assigned TAs for each section.

    Parameters:
    pop (dict): A dictionary with evaluations as keys and solutions as values.

    Returns:
    dict: The best solution found with details on assignments and penalty scores.
    """

    # Convert the population dictionary to a list of solutions with penalties
    solutions = [
        {
            'assignments': sol,
            'overallocation': evals[0][1],  # Accessing scores by index assuming a specific order
            'time_conflicts': evals[1][1],
            'undersupport': evals[2][1],
            'unwilling': evals[3][1],
            'unpreferred': evals[4][1]
        }
        for evals, sol in pop.items()
    ]

    # Find the solution with the lowest total penalty sum
    best_solution = min(solutions,
                        key=lambda sol: sol['overallocation'] + sol['time_conflicts'] + sol['undersupport'] + sol[
                            'unwilling'] + sol['unpreferred'])

    # Extract information from the best solution
    assignments = best_solution['assignments']
    overallocation = best_solution['overallocation']
    time_conflicts = best_solution['time_conflicts']
    undersupport = best_solution['undersupport']
    unwilling = best_solution['unwilling']
    unpreferred = best_solution['unpreferred']
    total_sum = overallocation + time_conflicts + undersupport + unwilling + unpreferred

    print(f"Best Solution Penalties:")
    print(f"  - Overallocation Penalty: {overallocation}")
    print(f"  - Time Conflict Penalty: {time_conflicts}")
    print(f"  - Under-Support Penalty: {undersupport}")
    print(f"  - Unwilling Penalty: {unwilling}")
    print(f"  - Unpreferred Penalty: {unpreferred}")
    print(f"  - Total Sum: {total_sum}\n")

    print("Assigned Sections for Each TA:")
    for ta_index in range(assignments.shape[1]):
        assigned_sections = [f"Section {sec_index + 1}" for sec_index, assigned in enumerate(assignments[:, ta_index])
                             if assigned == 1]
        print(f"  - TA{ta_index + 1}: {', '.join(assigned_sections)}")

    print("\nAssigned TAs for Each Section:")
    for sec_index in range(assignments.shape[0]):
        assigned_tas = [f"TA{ta_index + 1}" for ta_index, assigned in enumerate(assignments[sec_index, :]) if
                        assigned == 1]
        print(f"  - Section {sec_index + 1}: {', '.join(assigned_tas)}")

    return best_solution


# Read and test the test files
testfiles('test1.csv', 'test2.csv', 'test3.csv')

# Create the environment
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


# Create random initial solution matrices
array = np.random.randint(0, 2, size=(len(sect_n), len(tas_n)))
array1 = np.random.randint(0, 2, size=(len(sect_n), len(tas_n)))
E.add_solution(array)
E.add_solution(array1)

# Evolve solutions
E.evolve(time_limit=30, dom=25, status=100000, mutate=4, mut_fact=100)

# Find and display the best solution based on the evolved population
best_solution = find_best_solution(E.pop)

# Report profiling
Profiler.report()
