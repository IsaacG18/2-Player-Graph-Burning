import normal_graph_sim as ngs
import numpy as np

def test_make_connected():
    def is_connected(matrix):
        from scipy.sparse import csr_matrix
        from scipy.sparse.csgraph import connected_components

        graph = csr_matrix(matrix)
        n_components, _ = connected_components(csgraph=graph, directed=False)
        return n_components == 1

    # Test 1: Connected graph
    matrix1 = np.array([[0, 1, 1, 0],
                        [1, 0, 1, 1],
                        [1, 1, 0, 1],
                        [0, 1, 1, 0]])
    connected1 = ngs.generate_connected_graph_v2(matrix1.copy())
    assert is_connected(connected1), "Test 1 Failed: Connected graph should not become disconnect."
    assert (matrix1 == connected1).all(), "Test 1 Failed: Connected graph should not be modified."

    # Test 2: Disconnected graph
    matrix2 = np.array([[0, 1, 0, 0],
                        [1, 0, 0, 0],
                        [0, 0, 0, 1],
                        [0, 0, 1, 0]])
    connected2 = ngs.generate_connected_graph_v2(matrix2.copy())
    assert is_connected(connected2), "Test 2 Failed: Disonnected graph should not remain disconnect."
    assert (connected2 == connected2.T).all(), "Test 2 Failed: Graph should remain symmetric."

    # Test 3: Two disconnected nodes
    matrix4 = np.array([[0, 0],
                        [0, 0]])
    connected4 = ngs.generate_connected_graph_v2(matrix4.copy())
    assert is_connected(connected4), "Test 3 Failed: Two disconnected nodes should not remain disconnect"
    assert connected4[0, 1] == 1 and connected4[1, 0] == 1, "Test 3 Failed: Edge should be added between nodes."
    assert connected4[1, 1] == 0 and connected4[1, 1] == 0, "Test 3 Failed: Edge should not connect to themselves."

    print("All tests passed!")

test_make_connected()