# Makes printing more transparent.
def print_separators(flag):
    if flag == "verbose": print("=============")
    else: pass

def print_entry_data(clauses):
    for i, clause in enumerate(clauses):
        print(str(i + 1) + ".", ' v '.join(clause))

def print_resolution_data(resolution, goal):
    if resolution is not False:
        print((' v '.join(goal)), "is true")
    else:
        print((' v '.join(goal)), "is unkown")

# Indexes and prints an input clauses and a negated goal.
# Returns the last index.
def formatted_print(F, G, sosLength, flag):
    print_separators(flag)
    index = sosLength + 1
    for goal in G:
        gSet = set()
        if goal.startswith("~"):
            gSet.add(goal[1:])
        else:
            gSet.add("~" + str(goal))
        F.append(gSet)
        if flag == "verbose": print(str(index) + ".", ' v '.join(gSet))
        index += 1
    print_separators(flag)
    return index
