import unittest
import graph_isomorphism as gi

edge_set_graph = (
  (0, 1),
  (1, 2),
)

permutations = [
    {0: 0, 1: 1, 2: 2},
    {0: 0, 1: 2, 2: 1},
    {0: 1, 1: 0, 2: 2},
    {0: 1, 1: 2, 2: 0},
    {0: 2, 1: 0, 2: 1},
    {0: 2, 1: 1, 2: 0},
]

redundant_graph = [a for a in reversed(edge_set_graph)] + list(edge_set_graph)

node_degree = {1: [0, 2], 2: [1]}

class bq_tests(unittest.TestCase):
    def test001_collect_nodes(self):
        self.assertEqual(
            set(range(3)),
            gi.collect_nodes(edge_set_graph)
        )

    def test002_create_permutations(self):
        self.assertEqual(
            permutations,
            gi.create_permutations(edge_set_graph)
        )

    def test_003_permute_graph(self):
        self.assertEqual(
            [(2, 1), (1, 0)],
            gi.permute_graph(edge_set_graph, permutations[-1])
        )

    def test_004_cannonize_graph(self):
        self.assertEqual(
            edge_set_graph,
            gi.cannonize_graph(redundant_graph)
        )

    def test_005_is_same_graph(self):
        # redundant on test_004_cannonize_graph
        self.assertTrue(
            gi.is_same_graph(edge_set_graph, redundant_graph)
        )
        self.assertFalse(
            gi.is_same_graph(edge_set_graph, edge_set_graph[:-1])
        )

    def test_006_find_homomorphisms(self):
        self.assertEqual(
            [permutations[0], permutations[-1]],
            gi.find_homomorphisms(edge_set_graph)
        )

    def test_007_degree_nodes(self):
        self.assertEqual(
            node_degree,
            gi.degree_nodes(edge_set_graph)
        )

    def test_008_create_node_degree_permutations(self):
        self.assertEqual(
            permutations[:1] + permutations[-1:],
            gi.create_node_degree_permutations(node_degree)
        )

if __name__ == '__main__':
        unittest.main()