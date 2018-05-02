from itertools import permutations, product
from functools import reduce
from operator import add
from collections import defaultdict

def collect_nodes(edge_set):
  return set(reduce(add, edge_set))

def create_permutations(nodes):
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

def find_homomorphisms(edge_set, permutations):
    return [perm for perm in permutations if is_isomorphism(perm, edge_set)]

def degree_nodes(edge_set):
    incidents = [node for pair in edge_set for node in pair]
    counts = defaultdict(int)
    for node in incidents:
        counts[node] += 1
    by_count = defaultdict(list)
    for node, count in counts.items():
        by_count[count].append(node)
    return by_count

def add_dicts(a, b):
    return dict(list(a.items()) + list(b.items()))

def create_node_degree_permutations(node_degree):
    """ Finds permutations preserving node_degree (no trivial heteromorphisms)
    """
    by_degree = [create_permutations(v) for v in node_degree.values()]
    combined_permutations = product(*by_degree)
    consolidated = [reduce(add_dicts, combo) for combo in combined_permutations]
    return consolidated
