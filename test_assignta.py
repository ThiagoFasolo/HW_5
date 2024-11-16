# Adjusting the `overallocation` method to handle TAs dynamically
# Updating Evo class's overallocation method to handle missing TA entries in `ta_max_assigned`
import random as rnd
import copy
from functools import reduce
import numpy as np



class Evo:

    def __init__(self):
        self.pop = {}     # evaluation --> solution
        self.fitness = {} # name --> objective function
        self.agents = {} # name --> (operator function, num_solutions_input)

    def overallocation(self, sol):
        ta_counts = {}
        for entry in sol:
            ta = entry['ta']
            ta_counts[ta] = ta_counts.get(ta, 0) + 1

        # Extend max assignments to handle unknown TAs with a default max of 1
        ta_max_assigned = {"TA1": 1, "TA2": 1, "TA3": 3}  # Known TAs
        return sum(max(0, ta_counts[ta] - ta_max_assigned.get(ta, 1)) for ta in ta_counts)

    def conflicts(self, sol):
        section_ta_counts = {}
        for entry in sol:
            section = entry['section']
            if section not in section_ta_counts:
                section_ta_counts[section] = set()
            section_ta_counts[section].add(entry['ta'])
        return sum(1 for tas in section_ta_counts.values() if len(tas) > 1)

    def undersupport(self, sol):
        section_min_ta = {0: 2, 1: 2, 2: 2}  # Replace with actual data or parameters
        section_counts = {}
        for entry in sol:
            section = entry['section']
            section_counts[section] = section_counts.get(section, 0) + 1
        return sum(max(0, section_min_ta[section] - section_counts.get(section, 0)) for section in section_min_ta)

    def unwilling(self, sol):
        return sum(1 for entry in sol if entry['preference'] == 'U')

    def unpreferred(self, sol):
        return sum(1 for entry in sol if entry['preference'] == 'W')

    def add_fitness_criteria(self, name, f):
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        self.agents[name] = (op, k)

    def add_solution(self, sol):
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])
        self.pop[eval] = sol

    def get_random_solutions(self, k=1):
        if len(self.pop) == 0:
            return []
        else:
            solutions = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(solutions)) for _ in range(k)]

    def run_agent(self, name):
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)

    def dominates(self, p, q):
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
        header = "groupname,overallocation,conflicts,undersupport,unwilling,unpreferred\n"
        groupname = "Group1"
        for eval, sol in self.pop.items():
            eval_dict = {name: score for name, score in eval}
            header += f"{groupname},{eval_dict['overallocation']},{eval_dict['conflicts']},{eval_dict['undersupport']},{eval_dict['unwilling']},{eval_dict['unpreferred']}\n"
        return header

# Reinitializing Evo and running the setup again
evo = Evo()

evo.add_fitness_criteria("overallocation", evo.overallocation)
evo.add_fitness_criteria("conflicts", evo.conflicts)
evo.add_fitness_criteria("undersupport", evo.undersupport)
evo.add_fitness_criteria("unwilling", evo.unwilling)
evo.add_fitness_criteria("unpreferred", evo.unpreferred)

for sol in solutions_test1 + solutions_test2 + solutions_test3:
    evo.add_solution(sol)

# Registering mutation agent
def mutate(sol_list):
    sol = sol_list[0]
    sol = copy.deepcopy(sol)
    idx = rnd.randint(0, len(sol) - 1)
    sol[idx]['section'] = (sol[idx]['section'] + 1) % len(test1_df.columns)
    return sol

evo.add_agent("mutate", mutate)

evo.evolve(n=10, dom=5, status=5)

# Displaying the final non-dominated solutions table
str(evo)
