from prints import *
from refutation_resolution import *

def resolution_interactive_verbose(clauses, goal):
    print_entry_data(clauses)
    resolution = pl_resolution(clauses, goal, "verbose")
    print_resolution_data(resolution, goal)

def resolution_interactive(clauses, goal):
    resolution = pl_resolution(clauses, goal, "test")
    if resolution is not False:
        print((' v '.join(goal)), "is true")
    else:
        print((' v '.join(goal)), "is unkown")
