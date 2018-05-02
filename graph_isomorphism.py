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

def is_same_graph(left, right):
    # assumes both graphs have same node names
    return cannonize_graph(left) == cannonize_graph(right)

def is_isomorphism(permutation, edge_set):
    return is_same_graph(edge_set, permute_graph(edge_set, permutation))

def find_homomorphisms(edge_set, node_permutations):
    return [p for p in node_permutations if is_isomorphism(p, edge_set)]

def degree_nodes(edge_set):
    incidents = [node for pair in edge_set for node in pair]
    counts = defaultdict(int)
    for node in incidents:
        counts[node] += 1
    by_count = defaultdict(list)
    for node, count in counts.items():
        by_count[count].append(node)
    return by_count

def add_dicts(left, right):
    return dict(list(left.items()) + list(right.items()))

def create_node_degree_permutations(node_degree):
    """ Finds permutations preserving node_degree (no trivial heteromorphisms)
    """
    by_degree = [create_permutations(v) for v in node_degree.values()]
    consolidated = [reduce(add_dicts, combo) for combo in product(*by_degree)]
    return consolidated
