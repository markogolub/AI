from refutation_resolution import *
from prints import *

def cooking_tests(commands):
    for command in commands:
        inputSet = set()
        action = command[-1]
        clause = command[:-2]
        inputSet.add(clause)
        if action == "+":
            clauses.append(inputSet)
        elif action == "-":
            try: clauses.remove(inputSet)
            except: pass
        elif action == "?":
            resolution = pl_resolution(clauses.copy(), inputSet, "test")
            print_resolution_data(resolution, inputSet)