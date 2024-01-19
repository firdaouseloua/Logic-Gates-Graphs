import unittest
import sys
import os
root = os.path.normpath(os.path.join(os.path.dirname(__file__)))
sys.path.append(root)  # allows us to fetch files from the project root
from modules.open_digraph import *


class InitTest(unittest.TestCase):

    def test_init_Node(self):
        n = Node(0, 'i', {}, {1: 1})
        self.assertEqual(n.id, 0)
        self.assertEqual(n.label, 'i')
        self.assertEqual(n.parents, {})
        self.assertEqual(n.children, {1: 1})
        self.assertIsInstance(n, Node)

    def test_init_OpenDigraph(self):
        g = OpenDigraph([0], [0], [Node(0, 'i', {}, {1: 1})])
        self.assertEqual(g.inputs, [0])
        self.assertEqual(g.outputs, [0])
        self.assertEqual(len(g.nodes), 1)
        self.assertEqual(g.nodes[0].label, 'i')

    def test_empty_OpenDigraph(self):
        g = OpenDigraph.empty()
        self.assertEqual(g.inputs, [])
        self.assertEqual(g.outputs, [])
        self.assertEqual(len(g.nodes), 0)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
