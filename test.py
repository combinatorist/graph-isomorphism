import unittest
import graph_isomorphism as gi

######## Simplest Example ########
edge_set_graph = (
    (0, 1),
    (1, 2),
)

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

redundant_graph = [a for a in reversed(edge_set_graph)] + list(edge_set_graph)

node_degree = {1: [0, 2], 2: [1]}

######## Second Example ########
edge_set_graph2 = (
    (0, 1),
    (1, 2),
    (2, 3),
)

node_degree2 = {1: [0, 3], 2: [1, 2]}

node_degree_permutations2 = [
    {0: 0, 1: 1, 2: 2, 3: 3},
    {0: 0, 1: 2, 2: 1, 3: 3},
    {0: 3, 1: 1, 2: 2, 3: 0},
    {0: 3, 1: 2, 2: 1, 3: 0},
]

print(gi.find_all_graphs_up_to_order(2))

class bq_tests(unittest.TestCase):
    def test001_collect_nodes(self):
        self.assertEqual(
            nodes,
            gi.collect_nodes(edge_set_graph)
        )

    def test002_create_permutations(self):
        self.assertEqual(
            permutations,
            gi.create_permutations(nodes)
        )

    def test003_permute_graph(self):
        self.assertEqual(
            [(2, 1), (1, 0)],
            gi.permute_graph(edge_set_graph, permutations[-1])
        )

    def test004_cannonize_graph(self):
        self.assertEqual(
            edge_set_graph,
            gi.cannonize_graph(redundant_graph)
        )

    def test005_is_same_graph(self):
        # redundant on test004_cannonize_graph
        self.assertTrue(
            gi.is_same_graph(edge_set_graph, redundant_graph)
        )
        self.assertFalse(
            gi.is_same_graph(edge_set_graph, edge_set_graph[:-1])
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
            gi.degree_nodes(edge_set_graph)
        )
        self.assertEqual(
            node_degree2,
            gi.degree_nodes(edge_set_graph2)
        )

    def test008_create_node_degree_permutations(self):
        self.assertEqual(
            homomorphisms,
            gi.create_node_degree_permutations(node_degree)
        )

        self.assertEqual(
            node_degree_permutations2,
            gi.create_node_degree_permutations(node_degree2)
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
