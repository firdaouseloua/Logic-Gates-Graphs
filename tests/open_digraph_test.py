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
        n0 = Node(0, 'i', {}, {1: 1})
        n1 = Node(1, 'j', {0: 1}, {})
        g = OpenDigraph([0], [1], [n0, n1])
        self.assertEqual(g.inputs, [0])
        self.assertEqual(g.outputs, [1])
        self.assertEqual(len(g.nodes), 2)
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
        n0 = Node(0, 'i', {}, {1: 1})
        n1 = Node(1, 'j', {0: 1}, {})
        g = OpenDigraph([0], [1], [n0, n1])
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
        n2 = Node(2, 'Paris', {0: 1}, {})
        n3 = Node(3, 'Palaiseau', {1: 1}, {})
        g = OpenDigraph([0, 1], [2, 3], [n0, n1, n2, n3])
        self.assertEqual(g.get_input_ids(), g.inputs)
        self.assertEqual(g.get_output_ids(), g.outputs)
        self.assertEqual(g.get_id_node_map(), g.nodes)
        self.assertEqual(g.get_nodes(), [n0, n1, n2, n3])
        self.assertEqual(g.get_node_ids(), [0, 1, 2, 3])
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
        n0 = Node(0, 'Orsay', {}, {})
        n1 = Node(1, 'Le Guichet', {}, {})
        n3 = Node(3, 'Palaiseau', {}, {})
        n4 = Node(4, 'Villebon', {}, {})
        n6 = Node(6, 'Bures', {}, {})
        g = OpenDigraph.empty()
        g1 = OpenDigraph([], [], [n0, n1, n3, n4, n6])

        g1.set_inputs([1])
        g1.set_outputs([6])
        g1.add_input_id(3)
        g1.add_output_id(4)
        self.assertEqual(g1.inputs, [1, 3])
        self.assertEqual(g1.outputs, [6, 4])
        with self.assertRaises(ValueError):
            g.set_inputs([1, 2])
            g.set_outputs([3, 4])
            g.add_input_id(3)
            g.add_output_id(2)

    def test_eq_Node(self):
        n0 = Node(0, 'Orsay', {}, {2: 1})
        n1 = Node(1, 'Le Guichet', {}, {2: 1})
        self.assertEqual(n0, n0)
        self.assertNotEqual(n0, n1)

    def test_eq_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {2: 1})
        n1 = Node(1, 'Le Guichet', {}, {6: 1, 2: 1})
        g1 = OpenDigraph.empty()
        g2 = OpenDigraph([3, 4], [6], [n0, n1])
        g3 = OpenDigraph([3, 4], [], [n0, n1])
        g4 = OpenDigraph([3, 4], [6], [n0])
        self.assertEqual(g1, g1)
        self.assertEqual(g2, g2)
        self.assertNotEqual(g2, g3)
        self.assertNotEqual(g2, g4)

    def test_new_id_OpenDigraph(self):
        g1 = OpenDigraph.empty()
        n0 = Node(0, 'Orsay', {}, {2: 1})
        n1 = Node(1, 'Le Guichet', {}, {2: 1})
        n2 = Node(2, 'Paris', {0: 1, 1: 1}, {})
        g2 = OpenDigraph([], [], [n0, n1, n2])
        self.assertEqual(g1.new_id(), 0)
        self.assertEqual(g2.new_id(), 3)

    def test_add_edges_OpenDigraph(self):
        # Test add_edge in the same time
        n0 = Node(0, 'Orsay', {}, {})
        n1 = Node(1, 'Le Guichet', {}, {})
        n2 = Node(2, 'Paris', {}, {})
        g = OpenDigraph([], [], [n0, n1, n2])
        g.add_edges([(0, 1), (1, 2)])
        self.assertEqual(g.get_node_by_id(0), Node(0, 'Orsay', {}, {1: 1}))
        self.assertEqual(g.get_node_by_id(1), Node(1, 'Le Guichet', {0: 1}, {2: 1}))
        self.assertEqual(g.get_node_by_id(2), Node(2, 'Paris', {1: 1}, {}))

    def test_add_node_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {}, {})
        n1 = Node(1, 'Le Guichet', {}, {})
        n2 = Node(2, 'Paris', {1: 1}, {})
        g = OpenDigraph([], [], [n0, n1])
        g.add_node('Paris', [1])
        self.assertEqual(g, OpenDigraph([], [], [n0, n1, n2]))

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

    def test_remove_edge_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {1: 1}, {})
        n1 = Node(1, 'Le Guichet', {2: 2}, {0: 1})
        n2 = Node(2, 'Paris', {}, {1: 2})
        n3 = Node(0, 'Orsay', {}, {})
        n4 = Node(1, 'Le Guichet', {2: 1}, {})
        n5 = Node(2, 'Paris', {}, {1: 1})
        g = OpenDigraph([], [], [n0, n1, n2])
        g.remove_edge(0, 1)
        g.remove_edge(1, 2)
        g.remove_edge(2, 1)
        self.assertEqual(g, OpenDigraph([], [], [n3, n4, n5]))

    def test_remove_edges_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {1: 1}, {})
        n1 = Node(1, 'Le Guichet', {2: 2}, {0: 1})
        n2 = Node(2, 'Paris', {}, {1: 2})
        n3 = Node(0, 'Orsay', {}, {})
        n4 = Node(1, 'Le Guichet', {2: 1}, {})
        n5 = Node(2, 'Paris', {}, {1: 1})
        g = OpenDigraph([], [], [n0, n1, n2])
        g.remove_edges([(0, 1), (2, 1), (1, 2)])
        self.assertEqual(g, OpenDigraph([], [], [n3, n4, n5]))

    def test_remove_parallel_edges_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {}, {1: 1})
        n1 = Node(1, 'Le Guichet', {0: 1}, {2: 2})
        n2 = Node(2, 'Paris', {1: 2}, {})
        n3 = Node(0, 'Orsay', {}, {})
        n4 = Node(1, 'Le Guichet', {}, {})
        n5 = Node(2, 'Paris', {}, {})
        g = OpenDigraph([], [], [n0, n1, n2])
        g.remove_parallel_edges(0, 1)
        g.remove_parallel_edges(1, 2)
        self.assertEqual(g, OpenDigraph([], [], [n3, n4, n5]))

    def test_remove_several_parallel_edges_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {1: 2})
        n1 = Node(1, 'Le Guichet', {0: 2}, {6: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1})
        n4 = Node(4, 'Villebon', {}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1}, {})
        n7 = Node(0, 'Orsay', {3: 1, 4: 1}, {})
        n8 = Node(1, 'Le Guichet', {}, {6: 1})
        g = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])

        g.remove_several_parallel_edges([(0, 1), (0, 1)])
        self.assertEqual(g, OpenDigraph([3, 4], [6], [n7, n8, n3, n4, n6]))
        with self.assertRaises(ValueError):
            g.remove_several_parallel_edges([(1, 2), (0, 2)])

    def test_remove_id_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {})
        n1 = Node(1, 'Le Guichet', {}, {6: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1})
        n4 = Node(4, 'Villebon', {}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        g.remove_id(2)
        g.remove_id(3)
        self.assertEqual(g, OpenDigraph([4], [6], [n0, n1, n4, n6]))

    def test_remove_nodes_by_id_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {})
        n1 = Node(1, 'Le Guichet', {}, {6: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1})
        n4 = Node(4, 'Villebon', {}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        g.remove_nodes_by_id([1, 2, 3])
        self.assertEqual(g, OpenDigraph([4], [6], [n0, n4, n6]))

    def test_add_input_node_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {})
        n1 = Node(1, 'Le Guichet', {}, {6: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1})
        n4 = Node(4, 'Villebon', {}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])

        # Test adding a new input node
        g.add_input_node(2, 1)
        self.assertEqual(g.get_input_ids(), [3, 4, 2])  # Input IDs should include the newly added node
        self.assertEqual(g.get_node_by_id(2).get_children(), {1: 1})  # The new node should have one child
        self.assertEqual(g.get_node_by_id(1).get_parents(), {2: 1})  # The child node should have one parent

        # Test adding an input node with an invalid child ID
        with self.assertRaises(ValueError):
            g.add_input_node(2, 7)  # 7 is not a valid child ID
            g.add_input_node(1, 2)  # 1 is not a valid ID

    def test_add_output_node_OpenDigraph(self):
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {})
        n1 = Node(1, 'Le Guichet', {}, {6: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1})
        n4 = Node(4, 'Villebon', {}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])

        # Test adding a new output node
        g.add_output_node(5, 1)
        self.assertEqual(g.get_output_ids(), [6, 5])  # Output IDs should include the newly added node
        self.assertEqual(g.get_node_by_id(5).get_parents(), {1: 1})  # The new node should have one parent
        self.assertEqual(g.get_node_by_id(1).get_children(), {5: 1, 6: 1})  # The parent node should have one child

        # Test adding an output node with an invalid parent ID
        with self.assertRaises(ValueError):
            g.add_output_node(2, 7)  # 7 is not a valid parent ID
            g.add_output_node(1, 2)  # 1 is not a valid ID

    def test_is_well_formed_OpenDigraph(self):
        # Test a well-formed graph
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {})
        n1 = Node(1, 'Le Guichet', {}, {6: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1})
        n4 = Node(4, 'Villebon', {}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1}, {})
        g1 = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        self.assertTrue(g1.is_well_formed())

        # Test a poorly-formed graph: A node with an invalid parent ID
        n3 = Node(3, 'Invalid Parent', {4: 1}, {})
        g2 = OpenDigraph([3], [4], [n3])
        self.assertFalse(g2.is_well_formed())

        # Test a poorly-formed graph: A node with an invalid child ID
        n4 = Node(4, 'Invalid Child', {}, {5: 1})
        g3 = OpenDigraph([3], [4], [n4])
        self.assertFalse(g3.is_well_formed())

        # Test a poorly-formed graph: A node with a parent not linked to his child
        n5 = Node(5, 'Fake Parent', {6: 1}, {})
        n5bis = Node(6, 'Fake Child', {}, {})
        g4 = OpenDigraph([3], [4], [n5, n5bis])
        self.assertFalse(g4.is_well_formed())

        # Test a poorly-formed graph: A node with a child not linked to his parent
        n6 = Node(6, 'Fake Child', {}, {7: 1})
        n6bis = Node(6, 'Fake Parent', {}, {})
        g5 = OpenDigraph([3], [4], [n6, n6bis])
        self.assertFalse(g5.is_well_formed())

        # Test a poorly-formed graph: An input node with more than one child
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {})
        n1 = Node(1, 'Le Guichet', {3: 1}, {6: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1, 1: 1})
        n4 = Node(4, 'Villebon', {}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1}, {})
        g6 = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        self.assertFalse(g6.is_well_formed())

        # Test a poorly-formed graph: An input node with a parent
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {})
        n1 = Node(1, 'Le Guichet', {}, {6: 1, 4: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1})
        n4 = Node(4, 'Villebon', {1: 1}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1}, {})
        g7 = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        self.assertFalse(g7.is_well_formed())

        # Test a poorly-formed graph: An invalid input node ID
        g8 = OpenDigraph([3], [], [])
        self.assertFalse(g8.is_well_formed())

        # Test a poorly-formed graph: An output node with more than one parent
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {6: 1})
        n1 = Node(1, 'Le Guichet', {}, {6: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1})
        n4 = Node(4, 'Villebon', {}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1, 0: 1}, {})
        g6 = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        self.assertFalse(g6.is_well_formed())

        # Test a poorly-formed graph: An output node with a child
        n0 = Node(0, 'Orsay', {3: 1, 4: 1, 6: 1}, {})
        n1 = Node(1, 'Le Guichet', {}, {6: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1})
        n4 = Node(4, 'Villebon', {}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1}, {0: 1})
        g7 = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        self.assertFalse(g7.is_well_formed())

        # Test a poorly-formed graph: An invalid output node ID
        g8 = OpenDigraph([3], [], [])
        self.assertFalse(g8.is_well_formed())

    def test_random_int_matrix(self):
        with self.assertRaises(ValueError):
            random_int_matrix(5, 4)
            random_int_matrix(5, 6, symmetric=True, oriented=True)

        m = random_int_matrix(5, 10)
        for i in range(5):
            self.assertEqual(m[i][i], 0)

        m = random_int_matrix(5, 10, symmetric=True)
        for i in range(5):
            for j in range(i+1, 5):
                self.assertEqual(m[i][j], m[j][i])

        m = random_int_matrix(5, 10, oriented=True)
        for i in range(5):
            for j in range(i+1, 5):
                if m[i][j] > 0:
                    self.assertEqual(0, m[j][i])

        m = random_int_matrix(5, 10, dag=True)
        for i in range(5):
            for j in range(i+1, 5):
                self.assertEqual(0, m[j][i])

    def test_graph_from_adjacency_matrix(self):
        m = [[0, 1, 1, 0, 0],
             [0, 0, 0, 1, 2],
             [0, 0, 0, 2, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 0]]
        n1 = Node(0, '0', {3: 1}, {1: 1, 2: 1})
        n2 = Node(1, '1', {0: 1}, {3: 1, 4: 2})
        n3 = Node(2, '2', {0: 1}, {3: 2})
        n4 = Node(3, '3', {1: 1, 2: 2}, {0: 1, 4: 1})
        n5 = Node(4, '4', {1: 2, 3: 1}, {})
        self.assertEqual(OpenDigraph([], [], [n1, n2, n3, n4, n5]), graph_from_adjacency_matrix(m))
        with self.assertRaises(ValueError):
            graph_from_adjacency_matrix([[1, 1, 1], [1, 1, 1]])

    # For these tests, we need to test if the code either is a well_formed_graph or raises an error
    # See next class how to do it correctly with no try/except
    def test_random_OpenDigraph(self):
        # Free Form
        graph = OpenDigraph.random(n=10, bound=9, form='free')
        self.assertTrue(graph.is_well_formed())

        # DAG Form
        graph = OpenDigraph.random(n=10, bound=9, form='DAG')
        self.assertTrue(graph.is_well_formed())

        # Oriented Form
        graph = OpenDigraph.random(n=10, bound=9, form='oriented')
        self.assertTrue(graph.is_well_formed())

        # Loop-Free Form
        graph = OpenDigraph.random(n=10, bound=9, form='loop-free')
        self.assertTrue(graph.is_well_formed())

        # Undirected Form
        graph = OpenDigraph.random(n=10, bound=9, form='undirected')
        self.assertTrue(graph.is_well_formed())

        # Loop-Free Undirected Form
        graph = OpenDigraph.random(n=10, bound=9, form='loop-free_undirected')
        self.assertTrue(graph.is_well_formed())

        # Inputs/Outputs Consistency
        with self.assertRaises(ValueError):
            OpenDigraph.random(n=10, bound=9, inputs=5, outputs=5)
        # self.assertEqual(len(graph.get_input_ids()), 5)
        # self.assertEqual(len(graph.get_output_ids()), 5)

        # Invalid Form
        with self.assertRaises(ValueError):
            OpenDigraph.random(n=10, bound=9, form='invalid_form')

        # Invalid Inputs/Outputs Values
        with self.assertRaises(ValueError):
            OpenDigraph.random(n=10, bound=9, inputs=5, outputs=6, form='oriented')
            OpenDigraph.random(n=10, bound=9, inputs=11, outputs=0, form='oriented')
            OpenDigraph.random(n=10, bound=9, inputs=0, outputs=11, form='oriented')

    def test_adjency_matrix_OpenDigraph(self):
        m = [[0, 1, 1, 0, 0],
             [0, 0, 0, 1, 2],
             [0, 0, 0, 2, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 0]]
        n1 = Node(0, '0', {3: 1}, {1: 1, 2: 1})
        n2 = Node(1, '1', {0: 1}, {3: 1, 4: 2})
        n3 = Node(2, '2', {0: 1}, {3: 2})
        n4 = Node(3, '3', {1: 1, 2: 2}, {0: 1, 4: 1})
        n5 = Node(4, '4', {1: 2, 3: 1}, {})
        g = OpenDigraph([], [], [n1, n2, n3, n4, n5])
        self.assertEqual(m, g.adjacency_matrix())


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
