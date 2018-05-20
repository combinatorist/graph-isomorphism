from itertools import combinations, permutations, product
from functools import reduce
from operator import add
from collections import defaultdict

class Graph(tuple):
    def __init__(self, edge_set):
        self.__original_edge__set = edge_set
        self.__id = tuple(sorted(set(tuple(sorted(pair)) for pair in edge_set)))
        self.__store = dict()

    def __repr__(self):
        return self.__id.__repr__()

    def __hash__(self):
        return self.__id.__hash__()

    def __eq__(self, right):
        return self.__hash__() == right.__hash__()

    def __len__(self):
        return self.__id.__len__()

    def nodes(self):
        if not self.__store.get('nodes', None):
            nodes = set(reduce(add, self.__id))
            self.__store['nodes'] = nodes
        return self.__store['nodes']

    def permutations(self):
        if not self.__store.get('permutations', None):
            permutations = create_permutations(self.nodes)
            self.__store['permutations'] = permutations
        return self.__store['permutations']

    def degree_nodes(self):
        if not self.__store.get('degree_nodes', None):
            incidents = [node for pair in self.__id for node in pair]
            counts = defaultdict(int)
            for node in incidents:
                counts[node] += 1
            by_count = defaultdict(list)
            for node, count in counts.items():
                by_count[count].append(node)
            self.__store['degree_nodes'] = by_count
        return self.__store['degree_nodes']

    def degree_counts(self):
        if not self.__store.get('degree_counts', None):
            self.__store['degree_counts'] = {k: len(list(v)) for k, v in self.degree_nodes().items()}
        return self.__store['degree_counts']

    def node_degree_permutations(self):
        """ Finds permutations preserving node_degree (no trivial heteromorphisms)
        """
        if not self.__store.get('node_degree_permutations', None):
            by_degree = [create_permutations(v) for v in self.degree_nodes().values()]
            consolidated = [reduce(add_dicts, combo) for combo in product(*by_degree)]
            self.__store['node_degree_permutations'] = consolidated
        return self.__store['node_degree_permutations']

    def permute(self, permutation):
        return Graph(tuple(tuple(permutation[node] for node in pair) for pair in self.__id))

    def map_by_node_degree(self, other):
        """ Creates default of nodes in left to right based on node degree.
        """
        left = self.degree_nodes()
        right = other.degree_nodes()
        by_degree = [(left[k], right[k]) for k in left.keys()]
        return {k : v for pair in by_degree for k, v in zip(*pair)}

def create_permutations(nodes):
    return [dict(zip(nodes, reorder)) for reorder in permutations(nodes)]

def compose_dicts(left, right):
    return {k: left[right[k]] for k in left.keys()}

def is_isomorphism(permutation, left, right=None):
    """ Does the permutation on the right graph equal the left one?
    """
    if not right:
        right = left
    return right == left.permute(permutation)

def find_homomorphisms(edge_set, node_permutations):
    return [p for p in node_permutations if is_isomorphism(p, edge_set)]

def add_dicts(left, right):
    return dict(list(left.items()) + list(right.items()))

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

    nodes = range(order)
    possible_edges = frozenset(combinations(nodes, 2))
    edge_sets = [Graph(edge_set) for edge_set in powerset(possible_edges)]

    grouped_by_degree_counts = defaultdict(list)
    for graph in edge_sets:
        grouped_by_degree_counts[frozenset(graph.degree_counts().items())].append(graph)

    def subgroup_by_isomorphism(graphs):
        """ Takes a list of graphs and returns list of equivalence classes
        """
        equivalence_classes = [[graphs[0]]]
        for graph in graphs[1:]:
            is_isomorphic = False
            for equivalence_class in equivalence_classes:
                base = equivalence_class[0]
                for intra in base.node_degree_permutations():
                    inter = base.map_by_node_degree(graph)
                    mapped = base.permute(compose_dicts(inter, intra))
                    if graph == mapped:
                        is_isomorphic = True
                        equivalence_class.append(graph)
                        break
                if is_isomorphic:
                    break
            if not is_isomorphic:
                equivalence_classes.append([graph])
        return equivalence_classes

    return {k: subgroup_by_isomorphism(v) for k, v in grouped_by_degree_counts.items()}

