import sys
from refutation_resolution import *
from prints import *
from resolution_interaction import *
from cooking_interaction import *

clauses = []
with open(sys.argv[2]) as file:
    for line in file:
        if line.startswith("#"): continue
        clauses.append(set(line.strip().lower().split(" v ")))

goal = clauses.pop()

if sys.argv[1] == "resolution":
    try:
        if sys.argv[3] == "verbose" or sys.argv[4] == "verbose":
            resolution_interactive_verbose(clauses, goal)
    except:
        resolution_interactive(clauses, goal)

elif sys.argv[1] == "cooking_interactive":
    while True:
        print("Please enter your query")
        i = input().strip().lower()
        if i == "exit": break
        flag = "verbose"
        try:
            if sys.argv[3] == "verbose" or sys.argv[4] == "verbose": pass
        except:
            flag = "test"

        cooking_interaction(clauses, i, flag)

elif sys.argv[1] == "cooking_test":
    commands = []
    with open(sys.argv[3]) as file:
        for line in file:
            if line.startswith("#"): continue
            commands.append(line.strip().lower())

    cooking_tests(commands)