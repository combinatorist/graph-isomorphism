import unittest
import graph_isomorphism as gi
from graph_isomorphism import Graph

######## Simplest Example ########
edge_set_graph = Graph([
    (0, 1),
    (1, 2),
])

edge_set_graph_relabeled = Graph([
    ('a', 'b'),
    ('b', 'c'),
])

nodes = set(range(3))

permutations = [
    {0: 0, 1: 1, 2: 2},
    {0: 0, 1: 2, 2: 1},
    {0: 1, 1: 0, 2: 2},
    {0: 1, 1: 2, 2: 0},
    {0: 2, 1: 0, 2: 1},
    {0: 2, 1: 1, 2: 0},
]

homomorphisms = [permutations[0], permutations[-1]]

redundant_graph = Graph([a for a in reversed(edge_set_graph)] + list(edge_set_graph))

node_degree = {1: [0, 2], 2: [1]}

######## Second Example ########
edge_set_graph2 = Graph([
    (0, 1),
    (1, 2),
    (2, 3),
])

node_degree2 = {1: [0, 3], 2: [1, 2]}

node_degree_permutations2 = [
    {0: 0, 1: 1, 2: 2, 3: 3},
    {0: 0, 1: 2, 2: 1, 3: 3},
    {0: 3, 1: 1, 2: 2, 3: 0},
    {0: 3, 1: 2, 2: 1, 3: 0},
]

from pprint import pprint
pprint(gi.find_all_graphs_up_to_order(4))

class bq_tests(unittest.TestCase):
    def test001_collect_nodes(self):
        self.assertEqual(
            nodes,
            edge_set_graph.nodes()
        )

    def test002_create_permutations(self):
        self.assertEqual(
            permutations,
            gi.create_permutations(nodes)
        )

    def test003_permute_graph(self):
        self.assertEqual(
            ((0, 1), (1, 2)),
            edge_set_graph.permute(permutations[-1])
        )

    def test004_cannonize_graph(self):
        self.assertEqual(
            edge_set_graph,
            Graph(redundant_graph)
        )

    def test005_is_same_graph(self):
        # redundant on test004_cannonize_graph
        self.assertTrue(
            edge_set_graph == redundant_graph
        )
        self.assertFalse(
            edge_set_graph == edge_set_graph[:-1]
        )

    def test006_find_homomorphisms(self):
        self.assertEqual(
            homomorphisms,
            gi.find_homomorphisms(edge_set_graph, permutations)
        )
        self.assertEqual(
            [node_degree_permutations2[0], node_degree_permutations2[-1]],
            gi.find_homomorphisms(edge_set_graph2, node_degree_permutations2)
        )

    def test007_degree_nodes(self):
        self.assertEqual(
            node_degree,
            edge_set_graph.degree_nodes()
        )
        self.assertEqual(
            node_degree2,
            edge_set_graph2.degree_nodes()
        )

    def test008_node_degree_permutations(self):
        self.assertEqual(
            homomorphisms,
            edge_set_graph.node_degree_permutations()
        )

        self.assertEqual(
            node_degree_permutations2,
            edge_set_graph2.node_degree_permutations()
        )

    def test009_powerset(self):
        self.assertEqual(
            frozenset([
                frozenset({}),
                frozenset({1}),
                frozenset({0}),
                frozenset({0, 1}),
            ]),
            frozenset(gi.powerset(range(2)))
        )
        self.assertEqual(
            frozenset([
                frozenset({}),
                frozenset({(0, 1)}),
                frozenset({(1, 2)}),
                frozenset({(0, 1), (1, 2)}),
            ]),
            frozenset(gi.powerset(edge_set_graph))
        )

if __name__ == '__main__':
        unittest.main()
