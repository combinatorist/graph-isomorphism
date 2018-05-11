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
    """ Generates all edge_sets and groups them into isomorphism classes
    """

    def degree_counts(degree_nodes):
        return {k: len(list(v)) for k, v in degree_nodes.items()}

    nodes = range(order)
    possible_edges = frozenset(combinations(nodes, 2))
    edge_sets = powerset(possible_edges)

    # group edge_sets by identifying topological characteristics
    analyzed = {edge_set: degree_nodes(edge_set) for edge_set in edge_sets}
    node_degree_counts = {k: degree_counts(v) for k, v in analyzed.items()}

    grouped_by_degree_counts = defaultdict(list)
    for k, v in node_degree_counts.items():
        grouped_by_degree_counts[frozenset(v.items())].append((k, analyzed[k]))

    # subgroup edge_sets into isomorphic equivalence classes
    subgrouped_by_isomorphism = dict()
    for k, analyzed_edge_sets in grouped_by_degree_counts.items():
        new_edge_sets = [[analyzed_edge_sets[0][0]]]
        for edge_set, node_degrees in analyzed_edge_sets[1:]:
            is_isomorphic = False

            #:warning: Finding homomorphic permutations, but need isomorphisms
            # we need to map from graph A to B based on node degree.
            # so, A's degree 1 nodes to B's degree 1 nodes, etc
            for permutation in create_node_degree_permutations(node_degrees):
                for edge_set_class in new_edge_sets:
                    if is_isomorphism(permutation, edge_set, edge_set_class[0]):
                        is_isomorphic = True
                        edge_set_class.append(edge_set)
                        break
                if is_isomorphic:
                    break
            if not is_isomorphic:
                new_edge_sets.append([edge_set])
        subgrouped_by_isomorphism[k] = new_edge_sets

    return subgrouped_by_isomorphism
