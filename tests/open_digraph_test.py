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

    def test_copy_Node(self):
        n = Node(0, 'i', {}, {1: 1})
        self.assertIsNot(n.copy(), n)
        self.assertEqual(n.copy(), n)

    def test_copy_OpenDigraph(self):
        g = OpenDigraph([0], [0], [Node(0, 'i', {}, {1: 1})])
        self.assertIsNot(g.copy(), g)
        self.assertEqual(g.copy(), g)

    def test_getters_Node(self):
        n = Node(0, 'i', {}, {1: 1})
        self.assertEqual(n.get_id(), n.id)
        self.assertEqual(n.get_label(), n.label)
        self.assertEqual(n.get_parents(), n.parents)
        self.assertEqual(n.get_children(), n.children)

    def test_getters_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {}, {2: 1})
        n1 = Node(1, 'Le Guichet', {}, {2: 1})
        n2 = Node(2, 'Paris', {0: 1, 1: 1}, {})
        g = OpenDigraph([0, 1], [2], [n0, n1, n2])
        self.assertEqual(g.get_input_ids(), g.inputs)
        self.assertEqual(g.get_output_ids(), g.outputs)
        self.assertEqual(g.get_id_node_map(), g.nodes)
        self.assertEqual(g.get_nodes(), [n0, n1, n2])
        self.assertEqual(g.get_node_ids(), [0, 1, 2])
        self.assertEqual(g.get_node_by_id(1), n1)
        self.assertEqual(g.get_nodes_by_ids([0, 2]), [n0, n2])

    def test_setters_Node(self):
        n = Node(0, 'i', {}, {1: 1})
        n.set_id(1)
        n.set_label('j')
        n.set_children({2: 1, 0: 1})
        n.add_parent_id(2)
        n.add_parent_id(2)
        n.add_child_id(1)
        n.add_child_id(0)
        self.assertEqual(n.id, 1)
        self.assertEqual(n.label, 'j')
        self.assertEqual(n.parents, {2: 2})
        self.assertEqual(n.children, {2: 1, 0: 2, 1: 1})

    def test_setters_OpenDigraph(self):
        g = OpenDigraph.empty()
        g.set_inputs([1, 2])
        g.set_outputs([3, 4])
        g.add_input_id(3)
        g.add_input_id(3)
        g.add_output_id(2)
        g.add_output_id(2)
        self.assertEqual(g.inputs, [1, 2, 3])
        self.assertEqual(g.outputs, [3, 4, 2])

    def test_eq_Node(self):
        n0 = Node(0, 'Orsay', {}, {2: 1})
        n1 = Node(1, 'Le Guichet', {}, {2: 1})
        self.assertEqual(n0, n0)
        self.assertNotEqual(n0, n1)

    def test_eq_OpenDiagraph(self):
        n0 = Node(0, 'Orsay', {}, {2: 1})
        n1 = Node(1, 'Le Guichet', {}, {2: 1})
        n2 = Node(0, 'Orsay', {}, {2: 1})
        g1 = OpenDigraph.empty()
        g2 = OpenDigraph([3, 4], [6], [n0, n1, n2])
        g3 = OpenDigraph([3, 4], [], [n0, n1, n2])
        g4 = OpenDigraph([3, 4], [6], [n2])
        self.assertEqual(g1, g1)
        self.assertEqual(g2, g2)
        self.assertNotEqual(g2, g3)
        self.assertNotEqual(g2, g4)

    def test_new_id_OpenDigraph(self):
        g1 = OpenDigraph.empty()
        n0 = Node(0, 'Orsay', {}, {2: 1})
        n1 = Node(1, 'Le Guichet', {}, {2: 1})
        n2 = Node(2, 'Paris', {0: 1, 1: 1}, {})
        g2 = OpenDigraph([3, 4], [6], [n0, n1, n2])
        self.assertEqual(g1.new_id(), 0)
        self.assertEqual(g2.new_id(), 7)

    def test_add_edges_OpenDigraph(self):
        # Test add_edge in the same time
        n0 = Node(0, 'Orsay', {}, {})
        n1 = Node(1, 'Le Guichet', {}, {})
        n2 = Node(2, 'Paris', {}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n2])
        g.add_edges([(0, 1), (1, 2)])
        self.assertEqual(g.get_node_by_id(0), Node(0, 'Orsay', {}, {1: 1}))
        self.assertEqual(g.get_node_by_id(1), Node(1, 'Le Guichet', {0: 1}, {2: 1}))
        self.assertEqual(g.get_node_by_id(2), Node(2, 'Paris', {1: 1}, {}))

    def test_add_node_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {}, {})
        n1 = Node(1, 'Le Guichet', {}, {})
        n2 = Node(7, 'Paris', {1: 1}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1])
        g.add_node('Paris', [1])
        self.assertEqual(g, OpenDigraph([3, 4], [6], [n0, n1, n2]))

    def test_remove_child_once_Node(self):
        n = Node(0, 'i', {}, {1: 1, 2: 2})
        n.remove_child_once(1)
        n.remove_child_once(2)
        n.remove_child_once(3)
        self.assertEqual(n, Node(0, 'i', {}, {2: 1}))

    def test_remove_parent_once_Node(self):
        n = Node(0, 'i', {1: 1, 2: 2}, {})
        n.remove_parent_once(1)
        n.remove_parent_once(2)
        n.remove_parent_once(3)
        self.assertEqual(n, Node(0, 'i', {2: 1}, {}))

    def test_remove_child_id_Node(self):
        n = Node(0, 'i', {}, {1: 2})
        n.remove_child_id(1)
        n.remove_child_id(2)
        self.assertEqual(n, Node(0, 'i', {}, {}))

    def test_remove_parent_id_Node(self):
        n = Node(0, 'i', {1: 2}, {})
        n.remove_parent_id(1)
        n.remove_parent_id(2)
        self.assertEqual(n, Node(0, 'i', {}, {}))

    def test_remove_edge_OpenDiagraph(self):
        n0 = Node(0, 'Orsay', {1: 1}, {})
        n1 = Node(1, 'Le Guichet', {2: 2}, {0: 1})
        n2 = Node(2, 'Paris', {}, {1: 2})
        n3 = Node(0, 'Orsay', {}, {})
        n4 = Node(1, 'Le Guichet', {2: 1}, {})
        n5 = Node(2, 'Paris', {}, {1: 1})
        g = OpenDigraph([3, 4], [6], [n0, n1, n2])
        g.remove_edge(0, 1)
        g.remove_edge(1, 2)
        g.remove_edge(2, 1)
        self.assertEqual(g, OpenDigraph([3, 4], [6], [n3, n4, n5]))

    def test_remove_edges_OpenDiagraph(self):
        n0 = Node(0, 'Orsay', {1: 1}, {})
        n1 = Node(1, 'Le Guichet', {2: 2}, {0: 1})
        n2 = Node(2, 'Paris', {}, {1: 2})
        n3 = Node(0, 'Orsay', {}, {})
        n4 = Node(1, 'Le Guichet', {2: 1}, {})
        n5 = Node(2, 'Paris', {}, {1: 1})
        g = OpenDigraph([3, 4], [6], [n0, n1, n2])
        g.remove_edges([(0, 1), (2, 1), (1, 2)])
        self.assertEqual(g, OpenDigraph([3, 4], [6], [n3, n4, n5]))

    def test_remove_parallel_edges_OpenDiagraph(self):
        n0 = Node(0, 'Orsay', {1: 1}, {})
        n1 = Node(1, 'Le Guichet', {2: 2}, {0: 1})
        n2 = Node(2, 'Paris', {}, {1: 2})
        n3 = Node(0, 'Orsay', {}, {})
        n4 = Node(1, 'Le Guichet', {}, {})
        n5 = Node(2, 'Paris', {}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n2])
        g.remove_parallel_edges(0, 1)
        g.remove_parallel_edges(1, 2)
        self.assertEqual(g, OpenDigraph([3, 4], [6], [n3, n4, n5]))

    def test_remove_several_parallel_edges_OpenDiagraph(self):
        n0 = Node(0, 'Orsay', {1: 1}, {})
        n1 = Node(1, 'Le Guichet', {2: 2}, {0: 1})
        n2 = Node(2, 'Paris', {}, {1: 2})
        n3 = Node(0, 'Orsay', {}, {})
        n4 = Node(1, 'Le Guichet', {}, {})
        n5 = Node(2, 'Paris', {}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n2])
        g.remove_several_parallel_edges([(0, 1), (1, 2)])
        self.assertEqual(g, OpenDigraph([3, 4], [6], [n3, n4, n5]))

    def test_remove_id_OpenDiagraph(self):
        n0 = Node(0, 'Orsay', {}, {})
        n1 = Node(1, 'Le Guichet', {}, {})
        n2 = Node(2, 'Paris', {}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n2])
        g.remove_id(2)
        g.remove_id(3)
        self.assertEqual(g, OpenDigraph([3, 4], [6], [n0, n1]))

    def test_remove_nodes_by_id_OpenDiagraph(self):
        n0 = Node(0, 'Orsay', {}, {})
        n1 = Node(1, 'Le Guichet', {}, {})
        n2 = Node(2, 'Paris', {}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n2])
        g.remove_nodes_by_id([1, 2, 3])
        self.assertEqual(g, OpenDigraph([3, 4], [6], [n0]))


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
