
import sys
import os
import unittest

# Add root to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data import V_CARROS, V_PECAS
from src import graph_ops

class TestProjectStructure(unittest.TestCase):
    def test_data_loading(self):
        self.assertGreater(len(V_CARROS), 0)
        self.assertGreater(len(V_PECAS), 0)

    def test_graph_ops(self):
        B = graph_ops.build_bipartite_graph()
        self.assertEqual(len(B.nodes), len(V_CARROS) + len(V_PECAS))
        
        # Test Criticality format (should have 5 elements now)
        crit = graph_ops.get_part_criticality(B)
        self.assertEqual(len(crit[0]), 5, "Criticality should return tuple of 5 elements")
        
        # Test Clustering
        P = graph_ops.build_projected_graph(B)
        avg_c, trans, _ = graph_ops.get_clustering_analysis(P)
        self.assertGreaterEqual(avg_c, 0.0)
        self.assertLessEqual(avg_c, 1.0)

    def test_jaccard(self):
        B = graph_ops.build_bipartite_graph()
        P = graph_ops.build_projected_graph(B)
        P = graph_ops.calculate_jaccard_weights(B, P)
        
        has_jaccard = any('jaccard' in d for u, v, d in P.edges(data=True))
        self.assertTrue(has_jaccard, "Edges should have jaccard attribute")

if __name__ == '__main__':
    unittest.main()
