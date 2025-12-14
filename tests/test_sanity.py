
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

if __name__ == '__main__':
    unittest.main()
