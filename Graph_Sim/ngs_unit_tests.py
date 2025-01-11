import normal_graph_sim as ngs
import numpy as np
import unittest
from scipy.sparse.csgraph import connected_components
from scipy.sparse import csr_matrix

def get_value(ver_colours):
    return np.count_nonzero(ver_colours == ngs.RED_NUMBER) - np.count_nonzero(ver_colours == ngs.BLUE_NUMBER)

class TestGetValue(unittest.TestCase):
    def test_all_red(self):
        ver_colours = np.array([ngs.RED_NUMBER, ngs.RED_NUMBER, ngs.RED_NUMBER])
        self.assertEqual(ngs.get_value(ver_colours), 3)

    def test_all_blue(self):
        ver_colours = np.array([ngs.BLUE_NUMBER, ngs.BLUE_NUMBER, ngs.BLUE_NUMBER])
        self.assertEqual(ngs.get_value(ver_colours), -3)

    def test_mixed_red_and_blue(self):
        ver_colours = np.array([ngs.RED_NUMBER, ngs.BLUE_NUMBER, ngs.RED_NUMBER, ngs.BLUE_NUMBER])
        self.assertEqual(ngs.get_value(ver_colours), 0)

    def test_no_red_or_blue(self):
        ver_colours = np.array([3, 0, 3, 0])  # Neither ngs.RED_NUMBER nor ngs.BLUE_NUMBER
        self.assertEqual(ngs.get_value(ver_colours), 0)

    def test_empty_array(self):
        ver_colours = np.array([])  # Empty array
        self.assertEqual(ngs.get_value(ver_colours), 0)

    def test_mixed_values_with_others(self):
        ver_colours = np.array([ngs.RED_NUMBER, ngs.BLUE_NUMBER, 3, 0, ngs.RED_NUMBER, ngs.BLUE_NUMBER])
        self.assertEqual(ngs.get_value(ver_colours), 0)

class TestMakeConnected(unittest.TestCase):
    def is_connected(self, matrix):
        graph = csr_matrix(matrix)
        n_components, _ = connected_components(csgraph=graph, directed=False)
        return n_components == 1

    def test_connected_graph(self):
        matrix1 = np.array([[0, 1, 1, 0],
                            [1, 0, 1, 1],
                            [1, 1, 0, 1],
                            [0, 1, 1, 0]])
        connected1 = ngs.generate_connected_graph_v2(matrix1.copy())
        self.assertTrue(self.is_connected(connected1), "Connected graph should not become disconnected.")
        self.assertTrue((matrix1 == connected1).all(), "Connected graph should not be modified.")

    def test_disconnected_graph(self):
        matrix2 = np.array([[0, 1, 0, 0],
                            [1, 0, 0, 0],
                            [0, 0, 0, 1],
                            [0, 0, 1, 0]])
        connected2 = ngs.generate_connected_graph_v2(matrix2.copy())
        self.assertTrue(self.is_connected(connected2), "Disconnected graph should not remain disconnected.")
        self.assertTrue((connected2 == connected2.T).all(), "Graph should remain symmetric.")

    def test_two_disconnected_nodes(self):
        matrix4 = np.array([[0, 0],
                            [0, 0]])
        connected4 = ngs.generate_connected_graph_v2(matrix4.copy())
        self.assertTrue(self.is_connected(connected4), "Two disconnected nodes should not remain disconnected.")
        self.assertEqual(connected4[0, 1], 1, "Edge should be added between nodes.")
        self.assertEqual(connected4[1, 0], 1, "Edge should be added between nodes.")
        self.assertEqual(connected4[0, 0], 0, "Edge should not connect to itself.")
        self.assertEqual(connected4[1, 1], 0, "Edge should not connect to itself.")

class TestBurnGraph(unittest.TestCase):
    def test_no_red_or_blue(self):
        adj_mat = np.array([[0, 1, 0],
                            [1, 0, 1],
                            [0, 1, 0]])
        ver_colours = np.array([0, 0, 0])
        ngs.burn_graph(adj_mat, ver_colours)
        expected = np.array([0, 0, 0])
        np.testing.assert_array_equal(ver_colours, expected, "Graph should not change with no RED or BLUE vertices.")

    def test_all_red(self):
        adj_mat = np.array([[0, 1, 1],
                            [1, 0, 1],
                            [1, 1, 0]])
        ver_colours = np.array([ngs.RED_NUMBER, ngs.RED_NUMBER, ngs.RED_NUMBER])
        ngs.burn_graph(adj_mat, ver_colours)
        expected = np.array([ngs.RED_NUMBER, ngs.RED_NUMBER, ngs.RED_NUMBER])
        np.testing.assert_array_equal(ver_colours, expected, "All vertices are RED; they should remain unchanged.")

    def test_red_and_blue(self):
        adj_mat = np.array([[0, 1, 0],
                            [1, 0, 1],
                            [0, 1, 0]])
        ver_colours = np.array([ngs.RED_NUMBER, 0, ngs.BLUE_NUMBER])
        ngs.burn_graph(adj_mat, ver_colours)
        expected = np.array([ngs.RED_NUMBER, ngs.PURPLE_NUMBER, ngs.BLUE_NUMBER])
        np.testing.assert_array_equal(ver_colours, expected, "Graph should spread RED and BLUE correctly.")

    def test_with_purple(self):
        adj_mat = np.array([[0, 1, 1],
                            [1, 0, 0],
                            [1, 0, 0]])
        ver_colours = np.array([ngs.PURPLE_NUMBER, 0, 0])
        ngs.burn_graph(adj_mat, ver_colours)
        expected = np.array([ngs.PURPLE_NUMBER, ngs.PURPLE_NUMBER, ngs.PURPLE_NUMBER])
        np.testing.assert_array_equal(ver_colours, expected, "Graph should spread PURPLE correctly.")

    def test_mixed_colors(self):
        adj_mat = np.array([[0, 1, 1, 0],
                            [1, 0, 0, 1],
                            [1, 0, 0, 1],
                            [0, 1, 1, 0]])
        ver_colours = np.array([ngs.RED_NUMBER, ngs.BLUE_NUMBER, ngs.PURPLE_NUMBER, 0])
        ngs.burn_graph(adj_mat, ver_colours)
        expected = np.array([ngs.RED_NUMBER, ngs.BLUE_NUMBER, ngs.PURPLE_NUMBER, ngs.PURPLE_NUMBER])
        np.testing.assert_array_equal(ver_colours, expected, "Graph should handle mixed colors correctly.")

    def test_single_spread(self):
        adj_mat = np.array([[0, 1, 1, 0],
                            [1, 0, 0, 1],
                            [1, 0, 0, 1],
                            [0, 1, 1, 0]])
        ver_colours = np.array([ngs.RED_NUMBER, 0, 0, 0])
        ngs.burn_graph(adj_mat, ver_colours)
        expected = np.array([ngs.RED_NUMBER, ngs.RED_NUMBER, ngs.RED_NUMBER, 0])
        np.testing.assert_array_equal(ver_colours, expected, "Graph should spread to only 2 vertexs.")

    def test_double_single_spread(self):
        adj_mat = np.array([[0, 1, 1, 0],
                            [1, 0, 0, 0],
                            [1, 0, 0, 1],
                            [0, 0, 1, 0]])
        ver_colours = np.array([ngs.RED_NUMBER, 0, 0, ngs.BLUE_NUMBER])
        ngs.burn_graph(adj_mat, ver_colours)
        expected = np.array([ngs.RED_NUMBER, ngs.RED_NUMBER, ngs.PURPLE_NUMBER, ngs.BLUE_NUMBER])
        np.testing.assert_array_equal(ver_colours, expected, "Graph should spread read to 2 and the blue should spread to only 1")

class TestGenerateConnectedGraph(unittest.TestCase):
    def is_connected(self, matrix):
        graph = csr_matrix(matrix)
        n_components, _ = connected_components(csgraph=graph, directed=False)
        return n_components == 1

    def test_edge_count(self):
        n = 10
        con_mat = ngs.generate_connected_graph(n)
        edge_count = np.sum(con_mat) / 2  # Each edge is counted twice in the adjacency matrix
        self.assertEqual(edge_count, n - 1, "Graph should have exactly n-1 edges.")

    def test_graph_connected(self):
        n = 10
        con_mat = ngs.generate_connected_graph(n)
        self.assertTrue(self.is_connected(con_mat), "Graph should be connected.")

class TestColourPoint(unittest.TestCase):
    def test_no_points(self):
        ver_colours = np.array([0, 0, 0])
        count = 0
        points = []
        colour = 1
        new_count = ngs.colour_point(ver_colours, count, points, colour)
        self.assertEqual(new_count, 0, "Count should remain 0 when points is empty.")
        np.testing.assert_array_equal(ver_colours, [0, 0, 0], "Vertex colours should remain unchanged when points is empty.")

    def test_point_already_coloured(self):
        ver_colours = np.array([0, 1, 0])
        count = 0
        points = [1]
        colour = 2
        new_count = ngs.colour_point(ver_colours, count, points, colour)
        self.assertEqual(new_count, 1, "Count should increment if the point is already coloured.")
        np.testing.assert_array_equal(ver_colours, [0, 1, 0], "Vertex colours should remain unchanged if point is already coloured.")

    def test_point_not_coloured(self):
        ver_colours = np.array([0, 0, 0])
        count = 0
        points = [1]
        colour = 1
        new_count = ngs.colour_point(ver_colours, count, points, colour)
        self.assertEqual(new_count, 0, "Count should not increment if the point is coloured successfully.")
        np.testing.assert_array_equal(ver_colours, [0, 1, 0], "Vertex colours should be updated when a point is coloured.")

    def test_multiple_points(self):
        ver_colours = np.array([0, 1, 0, 0])
        count = 0
        points = [1, 2, 3]
        colour = 2
        new_count = ngs.colour_point(ver_colours, count, points, colour)
        self.assertEqual(new_count, 1, "Count should skip already coloured points and stop at the first uncoloured point.")
        np.testing.assert_array_equal(ver_colours, [0, 1, 2, 0], "Vertex colours should update the first uncoloured point.")

    def test_out_of_bounds(self):
        ver_colours = np.array([0, 0, 0])
        count = 3
        points = [0, 1, 2]
        colour = 1
        new_count = ngs.colour_point(ver_colours, count, points, colour)
        self.assertEqual(new_count, 3, "Count should remain the same if it is out of bounds.")
        np.testing.assert_array_equal(ver_colours, [0, 0, 0], "Vertex colours should remain unchanged if count is out of bounds.")


class TestSimGraph(unittest.TestCase):
    def test_all_vertices_coloured(self):
        adj_mat = np.array([[0, 1, 0],
                            [1, 0, 1],
                            [0, 1, 0]])
        red_points = [0]
        blue_points = [2]
        result = ngs.sim_graph(adj_mat, red_points, blue_points)
        expected = np.array([ngs.RED_NUMBER, ngs.PURPLE_NUMBER, ngs.BLUE_NUMBER]) 
        np.testing.assert_array_equal(result, expected, "Vertices should be coloured correctly.")

    def test_no_colours(self):
        adj_mat = np.array([[0, 1, 0],
                            [1, 0, 1],
                            [0, 1, 0]])
        red_points = []
        blue_points = []
        result = ngs.sim_graph(adj_mat, red_points, blue_points)
        expected = np.zeros(adj_mat.shape[0]) 
        np.testing.assert_array_equal(result, expected, "No vertices should be coloured if no points are given.")

    def test_single_colour_spread(self):
        adj_mat = np.array([[0, 1, 1],
                            [1, 0, 0],
                            [1, 0, 0]])
        red_points = [0]
        blue_points = []
        result = ngs.sim_graph(adj_mat, red_points, blue_points)
        expected = np.array([ngs.RED_NUMBER, ngs.RED_NUMBER, ngs.RED_NUMBER]) 
        np.testing.assert_array_equal(result, expected, "Red should spread to all connected vertices.")

    def test_blue_colour_spread(self):
        adj_mat = np.array([[0, 1, 0, 0],
                            [1, 0, 1, 0],
                            [0, 1, 0, 1],
                            [0, 0, 1, 0]])
        red_points = []
        blue_points = [3]
        result = ngs.sim_graph(adj_mat, red_points, blue_points)
        expected = np.array([ngs.BLUE_NUMBER, ngs.BLUE_NUMBER, ngs.BLUE_NUMBER, ngs.BLUE_NUMBER]) 
        np.testing.assert_array_equal(result, expected, "Blue should spread within its connected component.")

class TestFindWinner(unittest.TestCase):
    def test_red_wins(self):
        adj_mat = np.array([[0, 1, 0],
                            [1, 0, 1],
                            [0, 1, 0]])
        red_points = [0]
        blue_points = []
        result = ngs.find_winner(adj_mat, red_points, blue_points)
        self.assertEqual(result, 1, "Red should win when it dominates the graph.")

    def test_blue_wins(self):
        adj_mat = np.array([[0, 1, 0, 0],
                            [1, 0, 1, 0],
                            [0, 1, 0, 1],
                            [0, 0, 1, 0]])
        red_points = []
        blue_points = [3]
        result = ngs.find_winner(adj_mat, red_points, blue_points)
        self.assertEqual(result, 2, "Blue should win when it dominates the graph.")

    def test_tie(self):
        adj_mat = np.array([[0, 1, 0, 0],
                            [1, 0, 0, 0],
                            [0, 0, 0, 1],
                            [0, 0, 1, 0]])
        red_points = [0]
        blue_points = [3]
        result = ngs.find_winner(adj_mat, red_points, blue_points)
        self.assertEqual(result, 0, "The game should be a tie when red and blue have equal areas.")

if __name__ == "__main__":
    unittest.main()
