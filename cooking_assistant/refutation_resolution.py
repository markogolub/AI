from prints import *
from negate_clause import *

# Resolves two clauses and returns a set of resolvents
def pl_resolve(c1, c2):
    negativeC1 = negate(c1)
    intersection = negativeC1.intersection(c2)
    return intersection


# Refutation resolution algorithm:
def pl_resolution(F, G, flag):
    sosLength = len(F)
    index = formatted_print(F, G, sosLength, flag)

    while True:
        new = []
        visited = set()

        # Generates pairs of clauses that it attempts to resolve.
        # Builds on the assumption that the set of input premises is consistent.
        # Set of support (SoS): the clauses obtained from the negated goal as well as all subsequently derived clauses
        for index1, c1 in enumerate(F[0:sosLength]):
            for index2, c2 in enumerate(F[sosLength:]):

                # Removal of redundant clauses based on subsumption F∧(F∨G)≡F.
                if c1.issubset(c2): continue
                if c2.issubset(c1): continue

                # Removal of tautologies.
                if pl_resolve(c1, c1): continue
                if pl_resolve(c2, c2): continue

                resolvents = pl_resolve(c1, c2)

                # If nothing was resolved.
                if len(resolvents) == 0: continue
                # If clauses had complementary literals and resolution did result with NIL.
                if len(resolvents) == len(negate(c1)) and len(resolvents) == len(c2):
                    if flag == "verbose" :
                        print(str(index) + ". NIL (" + str(index1 + 1) + ", " + str(sosLength + index2 + 1) + ")")
                    print_separators(flag)
                    return True

                # If clauses had complementary literals and resolution did not result with NIL.
                # Builds a union of clauses with no literals resolved.
                resolvedClause = (c1 - negate(resolvents)).union(c2 - resolvents)
                if resolvedClause in visited: continue
                else:
                    if flag == "verbose":
                        print(str(index) + ".", ' v '.join(resolvedClause) + "(" + str(index1 + 1) + ", " + str(sosLength + index2 + 1) + ")")
                    index += 1
                    new.append(resolvedClause)
                    visited.add(frozenset(resolvedClause))

        if len(new) == 0:
            print_separators(flag)
            return False
        else:
            sosLength = len(F)
            F.extend(new)
