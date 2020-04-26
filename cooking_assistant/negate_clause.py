# Returns a negative list of clauses.
def negate(clause):
    negativeClause = set()
    for match in clause:
        if match.startswith("~"): negativeClause.add(match[1:])
        else: negativeClause.add("~" + str(match))
    return negativeClause
