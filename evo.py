"""
evo.py: An evolutionary computing framework
"""

import random as rnd
import copy
from functools import reduce
import numpy as np
import time

class Evo:

    def __init__(self):
        self.pop = {}     # evaluation --> solution
        self.objectives = {} # name --> objective function
        self.agents = {} # name --> (operator function, num_solutions_input)
        self.mut_agents = []

    def add_objective(self, name, f):
        """ Register an objective with the environment """
        self.objectives[name] = f

    def add_agent(self, name, op, k=1):
        """ Register an agent with the environment
        The operator (op) defines how the agent tweaks a solution.
        k defines the number of solutions input to the agent. """
        self.agents[name] = (op, k)

    def add_mut_agent(self, op):
        """ Register the mutating agent with enviornment
        OP should take in a mutation factor parameter """
        self.mut_agents.append(op)

    def add_solution(self, sol):
        """ Add a solution to the population   """
        eval = tuple([(name, f(sol)) for name, f in self.objectives.items()])
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

    def run_mut_agents(self, num_changes):
        ''' Randomize an agent based on a number of changes'''
        for mutation in self.mut_agents:
            sol = self.get_random_solutions(k=1)[0]
            self.add_solution(mutation(sol, num_changes))

    '''
    DO WE STILL WANT TO USE THIS?
    '''
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

    def evolve(self, time_limit=300, dom=100, status=1000, mutate = 4, mut_fact = 100):
        """ Run random agents with a time limit.
        time_limit: The maximum allowed time for running this method (in seconds).
        dom: How frequently to check for and remove dominated solutions.
        status: How frequently to output the current population status.
        """
        start_time = time.time()  # Record the start time
        agent_names = list(self.agents.keys())
        i = 0

        while (time.time() - start_time) < time_limit:

            pick = rnd.choice(agent_names)
            self.run_agent(pick)

            if i % mutate:
                self.run_mut_agents(round((1 - (time.time() - start_time) / time_limit) * mut_fact))

            if i % dom == 0:
                self.remove_dominated()

            if i % status == 0:
                # Output the current status of the population
                print("Iteration: ", i)
                print("Size     : ", len(self.pop))
                print(self)

            i += 1

        self.remove_dominated()  # Final removal of dominated solutions
        print("Completed evolution process. Total iterations: ", i)


    def __str__(self):
        """ Output the solutions in the population """
        rslt = "overalloc, time_conflicts, undersupport, unwilling, unpreffered" + "\n"
        for eval, sol in self.pop.items():
            sum = 0
            for name, score in eval:
                rslt += f'{name[:2]}:{score} '
                sum =+ score
            rslt += f'\t sum: {sum} \n'

        return rslt


