"""
evo.py: An evolutionary computing framework
"""
import random as rnd
import copy
from functools import reduce
import numpy as np


    class Evo:
        def __init__(self, tas_n, sect_n):
            self.tas_n = tas_n  # TA information, including max assignments and willingness
            self.sect_n = sect_n  # Section information, including meeting times and min TAs required
            # Initialize other components like pop, fitness, agents

        def overallocation(self, array):
            ta_alloc = array.sum(axis=1)  # Sum assignments for each TA across sections
            ta_req = self.tas_n[:, 1]  # Max assigned column from tas_n

            difference = ta_alloc - ta_req
            print("Overallocation Differences:", difference)
            difference[difference < 0] = 0  # Ignore under-allocation

            return np.sum(difference)

        def time_conflicts(self, array):
            conflicts = 0
            section_times = self.sect_n[:, 1]  # Assuming 2nd column in sect_n represents meeting time
            print(self.sect_n)

            # Iterate over each TA
            for ta_idx in range(array.shape[0]):
                assigned_sections = np.where(array[ta_idx, :] == 1)[0]  # Sections assigned to TA
                assigned_times = section_times[assigned_sections]  # Times for assigned sections

                # Count as a conflict if duplicate times exist
                if len(assigned_times) != len(set(assigned_times)):
                    conflicts += 1  # Only one conflict per TA, regardless of multiple conflicts

            return conflicts

        def undersupport(self, array):
            required_tas = self.sect_n[:, -2]  # Assuming last column in sect_n is 'min_tas_required'
            actual_tas = array.sum(axis=0)  # Count of TAs assigned per section

            under_support = required_tas - actual_tas
            under_support[under_support < 0] = 0  # No penalty if actual meets/exceeds required

            return np.sum(under_support)

        def unwilling(self, array):
            penalty = 0
            for ta_idx in range(array.shape[0]):
                for sec_idx in range(array.shape[1]):
                    # Check if TA is assigned but unwilling (0 means unwilling in tas_n)
                    if array[ta_idx, sec_idx] == 1 and self.tas_n[ta_idx, sec_idx + 2] == 0:
                        penalty += 1
            return penalty

    def unpreferred(self, sol):
        return sum(1 for entry in sol if entry['preference'] == 'W')

    def add_fitness_criteria(self, name, f):
        """ Register an objective with the environment """
        self.fitness[name] = f


    def add_agent(self, name, op, k=1):
        """ Register an agent with the environment
        The operator (op) defines how the agent tweaks a solution.
        k defines the number of solutions input to the agent. """
        self.agents[name] = (op, k)

    def add_solution(self, sol):
        """ Add a solution to the population   """
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])
        self.pop[eval] = sol   # ((name1, objval1), (name2, objval2)....)  ===> solution

    def get_random_solutions(self, k=1):
        """ Pick k random solutions from the population """
        if len(self.pop) == 0: # no solutions in the population (This should never happen!)
            return []
        else:
            solutions = tuple(self.pop.values())
            # Doing a deep copy of a randomly chosen solution (k times)
            return [copy.deepcopy(rnd.choice(solutions)) for _ in range(k)]


    def run_agent(self, name):
        """ Invoke a named agent on the population """
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)


    def dominates(self, p, q):
        """
        p = evaluation of one solution: ((obj1, score1), (obj2, score2), ... )
        q = evaluation of another solution: ((obj1, score1), (obj2, score2), ... )
        """
        pscores = np.array([score for name, score in p])
        qscores = np.array([score for name, score in q])
        score_diffs = qscores - pscores
        return min(score_diffs) >= 0 and max(score_diffs) > 0.0


    def reduce_nds(self, S, p):
        return S - {q for q in S if self.dominates(p, q)}

    def remove_dominated(self):
        nds = reduce(self.reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k: self.pop[k] for k in nds}

    def evolve(self, n=1, dom=100, status=1000):
        """ Run random agents n times
        n:  Number of agent invocations
        status: How frequently to output the current population
        """
        agent_names = list(self.agents.keys())
        for i in range(n):
            pick = rnd.choice(agent_names)
            self.run_agent(pick)

            if i % dom == 0:
                self.remove_dominated()

            if i % status == 0:
                self.remove_dominated()
                print("Iteration: ", i)
                print("Size     : ", len(self.pop))
                print(self)

        self.remove_dominated()

    def __str__(self):
        """ Output the solutions in the population """
        header = "groupname,overallocation,conflicts,undersupport,unwilling,unpreferred\n"
        groupname = "Group1"
        for eval, sol in self.pop.items():
            eval_dict = {name: score for name, score in eval}
            header += f"{groupname},{eval_dict['overallocation']},{eval_dict['conflicts']},{eval_dict['undersupport']},{eval_dict['unwilling']},{eval_dict['unpreferred']}\n"
        return header



