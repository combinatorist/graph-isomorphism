from itertools import combinations, permutations, product
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

def is_isomorphism(permutation, left, right=None):
    """ Does the permutation on the right graph equal the left one?
    """
    if not right:
        right = left
    return is_same_graph(permute_graph(left, permutation), right)

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

def powerset(raw_set):
    """ Generates all possible subsets of a set
    """
    order = len(list(raw_set))
    power_generator = (
        frozenset(c)
        for r in range(order + 1)
        for c in combinations(raw_set, r)
    )
    return frozenset(power_generator)

def find_all_graphs_up_to_order(order):
    """ Generates all edge_sets and groups into isomorphism classes
    """

    def degree_counts(edge_set):
        return {k: len(list(v)) for k, v in degree_nodes(edge_set).items()}

    nodes = range(order)
    possible_edges = frozenset(combinations(nodes, 2))
    edge_sets = powerset(possible_edges)

    # group edge_sets by identifying topological characteristics
    analyzed = {edge_set: degree_counts(edge_set) for edge_set in edge_sets}

    grouped_by_degree_counts = defaultdict(set)
    for k, v in analyzed.items():
        grouped_by_degree_counts[frozenset(v.items())].add(k)

    # subgroup edge_sets into isomorphic equivalence classes
    subgrouped_by_isomorphism = dict()
    for k, edge_sets in grouped_by_degree_counts.items():
        new_edge_sets = list(list(edge_sets[0]))
        for edge_set in edge_sets[1:]:
            if edge_set

    return grouped_by_degree_counts ## WIP: intermediate result
