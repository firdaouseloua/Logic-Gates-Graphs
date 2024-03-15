import unittest
import sys
import os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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
        g = OpenDigraph.random(n=10, bound=9, form='free')
        self.assertTrue(g.is_well_formed())

        # DAG Form
        g = OpenDigraph.random(n=10, bound=9, form='DAG')
        self.assertTrue(g.is_well_formed())

        # Oriented Form
        g = OpenDigraph.random(n=10, bound=9, form='oriented')
        self.assertTrue(g.is_well_formed())

        # Loop-Free Form
        g = OpenDigraph.random(n=10, bound=9, form='loop-free')
        self.assertTrue(g.is_well_formed())

        # Undirected Form
        g = OpenDigraph.random(n=10, bound=9, form='undirected')
        self.assertTrue(g.is_well_formed())

        # Loop-Free Undirected Form
        g = OpenDigraph.random(n=10, bound=9, form='loop-free_undirected')
        self.assertTrue(g.is_well_formed())

        # Inputs/Outputs Consistency
        with self.assertRaises(ValueError):
            OpenDigraph.random(n=10, bound=9, inputs=5, outputs=5)
            self.assertEqual(len(graph.get_input_ids()), 5)
            self.assertEqual(len(graph.get_output_ids()), 5)

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

    '''
    def test_save_as_dot_file_OpenDigraph(self):
        # Create a graph
        g = OpenDigraph.empty()
        g.add_node(label="A")
        g.add_node(label="B")
        g.add_edge(0, 1)

        # Save the graph
        file_path = "test_graph.dot"
        graph.save_as_dot_file(file_path)

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path))

        # Check the content of the file
        with open(file_path, 'r') as file:
            content = file.read()
            expected_content = "digraph G {\n" \
                               "v0 [label=\"A\"];\n" \
                               "v1 [label=\"B\"];\n" \
                               "v0 -> v1 [label=\"1\"];\n" \
                               "}\n"
            self.assertEqual(content, expected_content)

        # Remove the file after the test
        os.remove(file_path)
        
    def test_from_dot_file_OpenDigraph(self):
        # Create a sample .dot file content
        dot_content = """
        digraph G {
            v0 [label="Node 0"];
            v1 [label="Node 1"];
            v2 [label="Node 2"];
            v3 [label="Node 3"];
            v0 -> v1;
            v1 -> v2;
            v1 -> v3;
        }
        """
        # Save the sample .dot content to a file
        with open("sample_graph.dot", "w") as file:
            file.write(dot_content)
        
        # Load the graph from the .dot file
        loaded_graph = OpenDigraph.from_dot_file("sample_graph.dot")
        
        # Verify the loaded graph structure
        self.assertListEqual(loaded_graph.get_input_ids(), [0])
        self.assertListEqual(loaded_graph.get_output_ids(), [2, 3])
        self.assertEqual(len(loaded_graph.get_nodes()), 4)
        self.assertEqual(loaded_graph.get_nodes()[0].get_label(), "Node 0")
        self.assertEqual(loaded_graph.get_nodes()[1].get_label(), "Node 1")
        self.assertEqual(loaded_graph.get_nodes()[2].get_label(), "Node 2")
        self.assertEqual(loaded_graph.get_nodes()[3].get_label(), "Node 3")
        self.assertDictEqual(loaded_graph.get_nodes()[0].get_children(), {1: 1})
        self.assertDictEqual(loaded_graph.get_nodes()[1].get_children(), {2: 1, 3: 1})

        # Clean up: Delete the sample .dot file
        import os
        os.remove("sample_graph.dot")
    '''

    def test_degree_Node(self):
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {})
        n1 = Node(1, 'Le Guichet', {}, {6: 1, 4: 1})
        n3 = Node(3, 'Palaiseau', {}, {})
        n4 = Node(4, 'Villebon', {1: 1}, {0: 1})
        self.assertEqual(n0.degree(), 2)
        self.assertEqual(n0.indegree(), 2)
        self.assertEqual(n0.outdegree(), 0)
        self.assertEqual(n1.degree(), 2)
        self.assertEqual(n1.indegree(), 0)
        self.assertEqual(n1.outdegree(), 2)
        self.assertEqual(n3.degree(), 0)
        self.assertEqual(n3.indegree(), 0)
        self.assertEqual(n3.outdegree(), 0)
        self.assertEqual(n4.degree(), 2)
        self.assertEqual(n4.indegree(), 1)
        self.assertEqual(n4.outdegree(), 1)

    def test_is_cyclic_OpenDigraph(self):
        # Acyclic graph
        n0 = Node(0, 'Orsay', {3: 1, 4: 1}, {})
        n1 = Node(1, 'Le Guichet', {}, {6: 1})
        n3 = Node(3, 'Palaiseau', {}, {0: 1})
        n4 = Node(4, 'Villebon', {}, {0: 1})
        n6 = Node(6, 'Bures', {1: 1}, {})
        g1 = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        self.assertFalse(g1.is_cyclic())

        # Cyclic graph
        n0 = Node(0, 'A', {2: 1}, {1: 1})
        n1 = Node(1, 'B', {0: 1}, {2: 1})
        n2 = Node(2, 'C', {1: 1}, {0: 1})
        g2 = OpenDigraph([], [], [n0, n1, n2])
        self.assertTrue(g2.is_cyclic())

    def test_is_well_formed_BoolCirc(self):
        # Well-formed BoolCirc
        n0 = Node(0, '&', {3: 1, 4: 1}, {})
        n1 = Node(1, '&', {}, {6: 1})
        n3 = Node(3, '|', {}, {0: 1})
        n4 = Node(4, '|', {}, {0: 1})
        n6 = Node(6, '|', {1: 1}, {})
        b = BoolCirc(OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6]), True)
        self.assertTrue(b.is_well_formed())

        # Cyclic graph
        n0 = Node(0, '&', {2: 1}, {1: 1})
        n1 = Node(1, '|', {0: 1}, {2: 1})
        n2 = Node(2, '&', {1: 1}, {0: 1})
        b = BoolCirc(OpenDigraph([], [], [n0, n1, n2]), True)
        self.assertFalse(b.is_well_formed())

        # Unknown label
        n0 = Node(0, '&', {}, {})
        n1 = Node(1, '|', {}, {})
        n2 = Node(2, '1', {}, {})
        b = BoolCirc(OpenDigraph([], [], [n0, n1, n2]), True)
        self.assertFalse(b.is_well_formed())

        # Copy node without exactly 1 input
        n0 = Node(0, '&', {}, {})
        n1 = Node(1, '|', {}, {})
        n2 = Node(2, '', {}, {})
        b = BoolCirc(OpenDigraph([], [], [n0, n1, n2]), True)
        self.assertFalse(b.is_well_formed())

        # Poorly-formed graph
        n0 = Node(0, '&', {3: 1, 4: 1}, {})
        n1 = Node(1, '&', {3: 1}, {6: 1})
        n3 = Node(3, '&', {}, {0: 1, 1: 1})
        n4 = Node(4, '&', {}, {0: 1})
        n6 = Node(6, '&', {1: 1}, {})
        b = BoolCirc(OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6]), True)
        self.assertFalse(b.is_well_formed())

    def test_minmax_id_OpenDigraph(self):
        n0 = Node(0, '&', {3: 1, 4: 1}, {})
        n1 = Node(1, '&', {}, {6: 1})
        n3 = Node(3, '|', {}, {0: 1})
        n4 = Node(4, '|', {}, {0: 1})
        n6 = Node(6, '|', {1: 1}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        self.assertEqual(g.max_id(), 6)
        self.assertEqual(g.min_id(), 0)

    def test_shift_indices_OpenDigraph(self):
        n0 = Node(0, '&', {3: 1, 4: 1}, {})
        n1 = Node(1, '&', {}, {6: 1})
        n3 = Node(3, '|', {}, {0: 1})
        n4 = Node(4, '|', {}, {0: 1})
        n6 = Node(6, '|', {1: 1}, {})
        n7 = Node(1, '&', {4: 1, 5: 1}, {})
        n8 = Node(2, '&', {}, {7: 1})
        n9 = Node(4, '|', {}, {1: 1})
        n10 = Node(5, '|', {}, {1: 1})
        n11 = Node(7, '|', {2: 1}, {})
        g = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        g1 = OpenDigraph([3, 4], [6], [n0, n1, n3, n4, n6])
        g2 = OpenDigraph([4, 5], [7], [n7, n8, n9, n10, n11])

        g1.shift_indices(1)
        self.assertEqual(g1, g2)
        g1.shift_indices(-1)
        self.assertEqual(g1, g)

    def test_iparallel_OpenDigraph(self):
        n0 = Node(0, '&', {}, {})
        n1 = Node(1, '&', {}, {})
        n2 = Node(2, '|', {}, {})
        n3 = Node(3, '|', {}, {})
        g = OpenDigraph([0], [1], [n0, n1])
        g1 = OpenDigraph([2], [3], [n2, n3])
        g1_bis = OpenDigraph([2], [3], [n2, n3])
        g2 = OpenDigraph([0, 2], [1, 3], [n0, n1, n2, n3])

        g.iparallel(g1)
        self.assertEqual(g1, g1_bis)
        self.assertEqual(g, g2)

    def test_parallel_OpenDigraph(self):
        n0 = Node(0, '&', {}, {})
        n1 = Node(1, '&', {}, {})
        n2 = Node(2, '|', {}, {})
        n3 = Node(3, '|', {}, {})
        g = OpenDigraph([0], [1], [n0, n1])
        g_bis = OpenDigraph([0], [1], [n0, n1])
        g1 = OpenDigraph([2], [3], [n2, n3])
        g1_bis = OpenDigraph([2], [3], [n2, n3])
        g2 = OpenDigraph([0, 2], [1, 3], [n0, n1, n2, n3])

        g3 = OpenDigraph()
        g3.parallel(g, g1)
        self.assertEqual(g, g_bis)
        self.assertEqual(g1, g1_bis)
        self.assertEqual(g2, g3)

    def test_icompose_OpenDigraph(self):
        n0 = Node(0, '&', {}, {})
        n1 = Node(1, '&', {}, {})
        n2 = Node(2, '|', {}, {})
        n3 = Node(3, '|', {}, {})
        n0_bis = Node(0, '&', {3: 1}, {})
        n3_bis = Node(3, '|', {}, {0: 1})
        f = OpenDigraph([0], [1], [n0, n1])
        f1 = OpenDigraph([2], [3], [n2, n3])
        f1_bis = OpenDigraph([2], [3], [n2, n3])
        f2 = OpenDigraph([2], [1], [n0_bis, n1, n2, n3_bis])
        f3 = OpenDigraph([0], [], [n0, n2, n3])

        f.icompose(f1)
        self.assertEqual(f1, f1_bis)
        self.assertEqual(f, f2)
        with self.assertRaises(ValueError):
            f1.icompose(f3)

    def test_compose_OpenDigraph(self):
        n0 = Node(0, '&', {}, {})
        n1 = Node(1, '&', {}, {})
        n2 = Node(2, '|', {}, {})
        n3 = Node(3, '|', {}, {})
        n0_bis = Node(0, '&', {3: 1}, {})
        n3_bis = Node(3, '|', {}, {0: 1})
        f = OpenDigraph([0], [1], [n0, n1])
        f_bis = OpenDigraph([0], [1], [n0, n1])
        f1 = OpenDigraph([2], [3], [n2, n3])
        f1_bis = OpenDigraph([2], [3], [n2, n3])
        f2 = OpenDigraph([2], [1], [n0_bis, n1, n2, n3_bis])
        f5 = OpenDigraph([0], [], [n0, n2, n3])

        f3 = OpenDigraph()
        f4 = OpenDigraph()
        f3.compose(f, f1)
        self.assertEqual(f, f_bis)
        self.assertEqual(f1, f1_bis)
        self.assertEqual(f2, f3)
        graph.save_as_dot_file("example_graph.dot", verbose=True)
        with self.assertRaises(ValueError):
            f4.compose(f1, f5)

    def test_identity_OpenDigraph(self):
        g = OpenDigraph.identity(3)

        self.assertEqual(g.get_input_ids(), [0, 1, 2])
        self.assertEqual(g.get_output_ids(), [0, 1, 2])

        # Vérification des nœuds
        self.assertEqual(len(g.get_nodes()), 3)

        # Vérification des connexions
        for node_id in range(3):
            node = g.get_node_by_id(node_id)
            self.assertEqual(node.get_parents(), {node_id: 1})
            self.assertEqual(node.get_children(), {node_id: 1})

    '''
    def test_connected_components_OpenDigraph(self):
        n0 = Node(0, '&', {}, {})
        n1 = Node(1, '&', {}, {})
        n2 = Node(2, '|', {}, {})
        n3 = Node(3, '|', {}, {})
        f = OpenDigraph([0], [1], [n0, n1])
        f1 = OpenDigraph([2], [3], [n2, n3])

        f3 = OpenDigraph()
        f3.compose(f, f1)
        f4 = OpenDigraph()
        f4.parallel(f, f1)
        self.assertEqual(f3.connected_components(), (3, {0: 0, 1: 1, 2: 2, 3: 0}))
        self.assertEqual(f4.connected_components(), (3, {0: 0, 1: 1, 2: 2, 3: 0}))
    '''


# Creating a simple example graph
node1 = Node(identity=1, label="A", parents={}, children={2: 1, 3: 1})
node2 = Node(identity=2, label="B", parents={1: 1}, children={4: 1})
node3 = Node(identity=3, label="C", parents={1: 1}, children={4: 1})
node4 = Node(identity=4, label="D", parents={2: 1, 3: 1}, children={})

graph = OpenDigraph(inputs=[1], outputs=[4], nodes=[node1, node2, node3, node4])


# Save the graph as a .dot file
graph.save_as_dot_file("example_graph.dot", verbose=True)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run
