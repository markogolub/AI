from prints import *
from refutation_resolution import *

def cooking_interaction(clauses, i, flag):
    inputSet = set()
    action = i[-1]
    clause = i[:-2]
    inputSet.add(clause)
    if action == "+":
        clauses.append(inputSet)
        if flag == "verbose": print(clause, "added")
    elif action == "-":
        try:
            clauses.remove(inputSet)
        except:
            pass
        if flag == "verbose": print(clause, "removed")
    elif action == "?":
        try:
            if sys.argv[3] == "verbose" or sys.argv[4] == "verbose": pass
        except:
            flag = "test"
        if flag == "verbose": print_entry_data(clauses)
        resolution = pl_resolution(clauses.copy(), inputSet, flag)
        print_resolution_data(resolution, inputSet)
