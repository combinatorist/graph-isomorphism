from itertools import permutations
from functools import reduce
from operator import add

def collect_nodes(edge_set):
  return set(reduce(add, edge_set))

def create_permutations(edge_set, nodes=None):
    # memoization
    if not nodes:
        nodes = collect_nodes(edge_set)
    return [dict(zip(nodes, reorder)) for reorder in permutations(nodes)]

def permute_graph(edge_set, permutation):
    return [tuple(permutation[node] for node in pair) for pair in edge_set]

def cannonize_graph(edge_set):
    return tuple(sorted(set(tuple(sorted(pair)) for pair in edge_set)))

def is_same_graph(g, h):
    # assumes both graphs have same node names
    return cannonize_graph(g) == cannonize_graph(h)

def is_isomorphism(permutation, edge_set):
    return is_same_graph(edge_set, permute_graph(edge_set, permutation))

def find_homomorphisms(edge_set, permutations=None):
    # memoization
    if not permutations:
        permutations = create_permutations(edge_set)
    return [perm for perm in permutations if is_isomorphism(perm, edge_set)]
