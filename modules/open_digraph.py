from typing import List, Dict, Tuple
from random import randint, sample


class Node:

    # Constructor
    def __init__(self, identity: int, label: str, parents: Dict[int, int], children: Dict[int, int]) -> None:
        """
        Constructs a new node object
        :param identity: int; its unique id in the graph
        :param label: string;
        :param parents: int->int dict; maps a parent nodes id to its multiplicity
        :param children: int->int dict; maps a child nodes id to its multiplicity
        """
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

    # Getters
    def get_id(self) -> int:
        """
        Returns node id
        """
        return self.id

    def get_label(self) -> str:
        """
        Returns node label
        """
        return self.label

    def get_parents(self) -> Dict[int, int]:
        """
        Returns node parents dict
        """
        return self.parents

    def get_children(self) -> Dict[int, int]:
        """
        Returns node children dict
        """
        return self.children

    # Setters
    def set_id(self, new_identity: int) -> None:
        """
        Changes node id
        :param new_identity: int; its unique id in the graph
        """
        self.id = new_identity

    def set_label(self, new_label: str) -> None:
        """
        Changes node label
        :param new_label: string;
        """
        self.label = new_label

    def set_children(self, new_children) -> None:
        """
        Changes node children dict
        :param new_children: int->int dict; maps a child nodes id to its multiplicity
        """
        self.children = new_children

    def add_parent_id(self, parent_id) -> None:
        """
        Adds a new parent to node parents dict
        :param parent_id: int;
        """
        if parent_id in self.get_parents():  # Already a parent
            self.parents[parent_id] += 1  # Increase the multiplicity
        else:  # Not yet a parent
            self.parents[parent_id] = 1

    def add_child_id(self, child_id):
        """
        Adds a new child to node children dict
        :param child_id: int;
        """
        if child_id in self.get_children():  # Already a child
            self.children[child_id] += 1  # Increase the multiplicity
        else:  # Not yet a child
            self.children[child_id] = 1

    # Printing methods
    def __str__(self) -> str:
        """
        Used by the __repr__ method
        """
        return f'({self.get_id()}, {self.get_label()}, {self.get_parents()}, {self.get_children()})'

    def __repr__(self) -> str:
        """
        Used to print the object
        """
        return str(self)

    # Methods
    def __eq__(self, other) -> bool:
        """
        Implementation of the "==" between two nodes
        :param other: Node;
        """
        return (self.get_id() == other.get_id() and self.get_label() == other.get_label() and
                self.get_parents() == other.get_parents() and self.get_children() == other.get_children())

    def copy(self):
        """
        Creates a copy of the node
        """
        return Node(self.get_id(), self.get_label(), self.get_parents(), self.get_children())

    def remove_parent_once(self, identity: int) -> None:
        """
        Removes an occurrence of the parent
        :param identity: int;
        """
        if identity in self.get_parents():
            if self.get_parents()[identity] <= 1:
                del self.parents[identity]
            else:
                self.parents[identity] -= 1

    def remove_child_once(self, identity: int) -> None:
        """
        Removes an occurrence of the child
        :param identity: int;
        """
        if identity in self.get_children():
            if self.get_children()[identity] <= 1:
                del self.children[identity]
            else:
                self.children[identity] -= 1

    def remove_parent_id(self, identity: int) -> None:
        """
        Removes a given parent
        :param identity: int;
        """
        if identity in self.get_parents():
            del self.parents[identity]

    def remove_child_id(self, identity: int) -> None:
        """
        Removes a given child
        :param identity: int;
        """
        if identity in self.get_children():
            del self.children[identity]


class OpenDigraph:  # for open directed graph

    # Constructors
    def __init__(self, inputs: List[int], outputs: List[int], nodes: List[Node]) -> None:
        """
        Constructs a new OpenDigraph object
        :param inputs: int list; the ids of the input nodes
        :param outputs: int list; the ids of the output nodes
        :param nodes: node iter;
        """
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id: node for node in nodes}  # self.nodes: <int,node> dict

    @classmethod
    def empty(cls):
        """
        Creates an instance of the class with empty inputs, outputs, and nodes
        """
        return cls(inputs=[], outputs=[], nodes=[])

    # Getters
    def get_input_ids(self) -> List[int]:
        """
        Returns digraph input list
        """
        return self.inputs

    def get_output_ids(self) -> List[int]:
        """
        Returns digraph output list
        """
        return self.outputs

    def get_id_node_map(self) -> Dict[int, Node]:
        """
        Returns digraph nodes dictionnary
        """
        return self.nodes

    def get_nodes(self) -> List[Node]:
        """
        Returns a list of all the nodes
        """
        return list(self.nodes.values())

    def get_node_ids(self) -> List[int]:
        """
        Returns a list of all the ids
        """
        return list(self.nodes.keys())

    def get_node_by_id(self, node_id: int) -> Node:
        """
        Returns a node given its id
        """
        return self.nodes[node_id]

    def get_nodes_by_ids(self, ids: List[int]) -> List[Node]:
        """
        Returns a list of nodes given a list of ids
        """
        return [self.nodes[node_id] for node_id in ids if node_id in self.nodes]

    # Setters
    def set_inputs(self, new_inputs: List[int]) -> None:
        """
        Changes digraph input list
        :param new_inputs: List[int];
        """
        nodes = self.get_node_ids()
        for i in new_inputs:
            if i not in nodes:  # An ID doesn't exist
                raise ValueError("A given ID doesn't exist")
                # We will also have to check that the graph is still well-formed later
        self.inputs = new_inputs

    def set_outputs(self, new_outputs: List[int]) -> None:
        """
        Changes digraph output list
        :param new_outputs: List[int];
        """
        nodes = self.get_node_ids()
        for i in new_outputs:
            if i not in nodes:  # An ID doesn't exist
                raise ValueError("A given ID doesn't exist")
                # We will also have to check that the graph is still well-formed later
        self.outputs = new_outputs

    def add_input_id(self, input_id: int) -> None:
        """
        Adds a new input to the input list
        :param input_id: int;
        """
        if input_id not in self.get_input_ids():  # Useless to add it twice
            if input_id in self.get_node_ids():  # Check that the ID exists
                self.inputs.append(input_id)
            else:
                ValueError("ID doesn't exist")  # We will also have to check that the graph is still well-formed later

    def add_output_id(self, output_id: int) -> None:
        """
        Adds a new input to the input list
        :param output_id: int;
        """
        if output_id not in self.get_output_ids():  # Useless to add it twice
            if output_id in self.get_node_ids():  # Check that the ID exists
                self.outputs.append(output_id)
            else:
                ValueError("ID doesn't exist")  # We will also have to check that the graph is still well-formed later

    # Printing methods
    def __str__(self) -> str:
        """
        Used by the __repr__ method
        """
        return f'({self.get_input_ids()}, {self.get_output_ids()}, {self.get_nodes()})'

    def __repr__(self) -> str:
        """
        Used to print the object
        """
        return str(self)

    # Methods
    def __eq__(self, other) -> bool:
        """
        Implementation of the "==" between two digraphs
        :param other: OpenDigraph;
        """
        return (self.get_input_ids() == other.get_input_ids() and self.get_output_ids() == other.get_output_ids()
                and self.get_nodes() == other.get_nodes())

    def copy(self):
        """
        Creates a copy of the graph
        """
        return OpenDigraph(list(self.get_input_ids()), list(self.get_output_ids()),
                           list(self.get_nodes_by_ids(self.get_node_ids())))

    def new_id(self):
        """
        Finds and return an unused ID in the graph
        """
        used_ids = set(self.get_input_ids() + self.get_output_ids() + list(self.get_node_ids()))
        return max(used_ids) + 1 if used_ids else 0  # If there's no existing id, return 0, else the max + 1
        # We suppose that if we have n ids, they all go from 0 to n-1
        # Still doesn't cause any problem if we don't have that condition
        # We'll just have ids not numerotated from 0 to n-1
        # But this function is faster (O(n)) than checking for the first unused id from 0 to n (O(n^2))

    def add_edge(self, src: int, tgt: int) -> None:
        """
        Adds an edge from the source node to the target node
        :param src: int; id of the source node
        :param tgt: int; id of the target node
        """
        nodes = self.get_node_ids()
        if src in nodes and tgt in nodes:
            self.get_node_by_id(src).add_child_id(tgt)  # Add a child to the source node
            self.get_node_by_id(tgt).add_parent_id(src)  # Add a parent to the target node
        else:
            raise ValueError("src or tgt doesn't exist")

    def add_edges(self, edges: List[Tuple[int, int]]) -> None:
        """
        Adds edges between each pair of node IDs in the list of edges
        :param edges: list(tuple(int, int)); list of edges to add (int; source node, int; target node)
        """
        for src, tgt in edges:
            self.add_edge(src, tgt)

    def remove_edge(self, src: int, tgt: int) -> None:
        """
        Removes an edge from the graph between the source node and the target node
        :param src: int; id of the source node
        :param tgt: int; id of the target node
        """
        nodes = self.get_node_ids()
        if src in nodes and tgt in nodes:
            self.get_node_by_id(tgt).remove_child_once(src)  # Remove a child of the source node
            self.get_node_by_id(src).remove_parent_once(tgt)  # Remove a parent of the target node
        else:
            raise ValueError("src or tgt doesn't exist")

    def remove_edges(self, edges: List[Tuple[int, int]]) -> None:
        """
        Removes an edge between each pair of node IDs in the list of edges
        :param edges: list(tuple(int, int)); list of edges to add (int; source node, int; target node)
        """
        for src, tgt in edges:
            self.remove_edge(src, tgt)

    def remove_parallel_edges(self, src: int, tgt: int) -> None:
        """
        Removes all edges from the graph between the source node and the target node
        :param src: int; id of the source node
        :param tgt: int; id of the target node
        """
        nodes = self.get_node_ids()
        if src in nodes and tgt in nodes:
            self.get_node_by_id(tgt).remove_parent_id(src)  # Remove all parents of the source node
            self.get_node_by_id(src).remove_child_id(tgt)  # Remove all children of the target node
        else:
            raise ValueError("src or tgt doesn't exist")

    def remove_several_parallel_edges(self, edges: List[Tuple[int, int]]) -> None:
        """
        Removes all edges between each pair of node IDs in the list of edges
        :param edges: list(tuple(int, int)); list of edges to add (int; source node, int; target node)
        """
        for src, tgt in edges:
            self.remove_parallel_edges(src, tgt)

    def add_node(self, label="", parents=None, children=None) -> int:
        """
        Adds a node with a label to the graph, assigning it a new id.
        Links it with the parent and child id nodes with their respective multiplicities.
        If the default values for parents and/or children are None, assign them an empty dictionary.
        Returns the id of the new node.
        :param label: string;
        :param parents: List[int]; ids of the parents
        :param children: List[int]; ids of the childrens
        """
        nodes = self.get_node_ids()
        # Create a new object Node
        new_node = Node(self.new_id(), label, {}, {})
        if parents is not None:
            for parent in parents:
                if parent in nodes:  # Check that the parent exists
                    new_node.add_parent_id(parent)
                else:
                    raise ValueError("One parent doesn't exist")
        if children is not None:
            for child in children:
                if child in nodes:  # Check that the child exists
                    new_node.add_child_id(child)
                else:
                    raise ValueError("One child doesn't exist")

        # Add the new node to the graph
        self.nodes[new_node.get_id()] = new_node

        return new_node.get_id()

    def add_input_node(self, node_id: int, child_id: int) -> None:
        """
        Adds a new input node to the graph and links it to the specified child node.
        :param node_id: int; id of the new input node
        :param child_id: int; id of the child node
        """
        # Asserts to keep the graph well-formed
        if node_id in self.get_node_ids():
            raise ValueError("Node already exists")
        if child_id not in self.get_node_ids():
            raise ValueError("Child doesn't exist")

        # Create a new input node with no parents and one child
        node = Node(node_id, "", {}, {})
        self.nodes[node_id] = node
        self.add_input_id(node_id)
        self.add_edge(node_id, child_id)

    def add_output_node(self, node_id: int, parent_id: int) -> None:
        """
        Adds a new output node to the graph and links it to the specified parent node.
        :param node_id: int; id of the new output node
        :param parent_id: int; id of the parent node
        """
        # Asserts to keep the graph well-formed
        if node_id in self.get_node_ids():
            raise ValueError("Node already exists")
        if parent_id not in self.get_node_ids():
            raise ValueError("Parent doesn't exist")

        # Create a new output node with one parent and no children
        node = Node(node_id, "", {}, {})
        self.nodes[node_id] = node
        self.add_output_id(node_id)
        self.add_edge(parent_id, node_id)

    def remove_id(self, identity: int) -> None:
        """
        Removes a node from its id
        :param identity: int; id of the node to remove
        """
        if identity in self.get_node_ids():

            parents = list(self.get_node_by_id(identity).get_parents().keys())
            children = list(self.get_node_by_id(identity).get_children().keys())
            for parent in parents:  # Remove all links with parents
                self.remove_parallel_edges(parent, identity)
            for child in children:  # Remove all links with children
                self.remove_parallel_edges(identity, child)
            self.nodes.pop(identity)

            inputs = self.get_input_ids()
            outputs = self.get_output_ids()
            if identity in inputs:  # Check if the node was an input
                self.set_inputs([node for node in inputs if node != identity])
            elif identity in outputs:  # Check if the node was an output
                self.set_inputs([node for node in outputs if node != identity])

    def remove_nodes_by_id(self, ids: List[int]) -> None:
        """
        Removes all nodes with IDs in the list of edges
        :param ids: list(int); list of nodes to remove
        """
        for identity in ids:
            self.remove_id(identity)

    def is_well_formed(self) -> bool:
        """
        Returns True if the graph is well-formed, else False
        """
        # Getters
        node_ids = self.get_node_ids()
        input_ids = self.get_input_ids()
        output_ids = self.get_output_ids()

        # Property 1: Check if each input and output node is in the graph
        for input_id in input_ids:  # inputs
            if input_id not in node_ids:
                return False
        for output_id in output_ids:  # outputs
            if output_id not in node_ids:
                return False

        # Property 2: Check if each input node has a single child and no parent
        for input_id in input_ids:
            input_node = self.get_node_by_id(input_id)
            children = input_node.get_children()
            parents = input_node.get_parents()
            if len(children) != 1 or len(parents) > 0:  # Wrong number of children or have parent(s)
                return False
            for child_multiplicity in children.values():  # At this step, it's exactly one value
                if child_multiplicity != 1:  # Wrong multiplicity
                    return False

        # Property 3: Check if each output node has a single parent and no children
        for output_id in output_ids:
            output_node = self.get_node_by_id(output_id)
            children = output_node.get_children()
            parents = output_node.get_parents()
            if len(children) > 0 or len(parents) != 1:  # Wrong number of parents or have child(ren)
                return False
            for parent_multiplicity in parents.values():  # At this step, it's exactly one value
                if parent_multiplicity != 1:    # Wrong multiplicity
                    return False

        # Property 4: Check if each key in nodes corresponds to a node which has the key as id
        for node_id, node in self.get_id_node_map().items():
            if node.get_id() != node_id:
                return False

        # Property 5: Check the relationship between parents and children
        for node_id, node in self.get_id_node_map().items():
            for child_id, multiplicity in node.get_children().items():  # child->parent
                child = self.get_node_by_id(child_id)
                parents = child.get_parents()
                if node_id not in parents or parents[node_id] != multiplicity:
                    return False
            for parent_id, multiplicity in node.get_parents().items():  # parent->child
                parent = self.get_node_by_id(parent_id)
                children = parent.get_children()
                if node_id not in children or children[node_id] != multiplicity:
                    return False

        return True

    def assert_is_well_formed(self) -> None:
        """
        Asserts if the graph is well-formed, raises an error if it's not
        """
        if not self.is_well_formed():
            raise ValueError("Graph not well-formed")
        
    @classmethod
    def random(cls, n, bound, inputs=0, outputs=0, form="free"):
        """
        Generates a random graph according to the constraints given by the user.
        :param n: int; number of nodes in the graph
        :param bound: int; maximum value for edge weights
        :param inputs: int; number of input nodes (if 0, randomly chosen)
        :param outputs: int; number of output nodes (if 0, randomly chosen)
        :param form: str; form of the graph
        :return: OpenDigraph; randomly generated graph
        """
        if inputs < 0 or outputs < 0 or n < inputs + outputs:
            raise ValueError("Invalid input/output values")

        # Generate adjacency matrix according to the specified form
        if form == "free":
            matrix = random_int_matrix(n, bound)
        elif form == "DAG":
            matrix = random_int_matrix(n, bound, dag=True)
        elif form == "oriented":
            matrix = random_int_matrix(n, bound, oriented=True)
        elif form == "loop-free":
            matrix = random_int_matrix(n, bound, null_diag=True)
        elif form == "undirected":
            matrix = random_int_matrix(n, bound, symmetric=True)
        elif form == "loop-free_undirected":
            matrix = random_int_matrix(n, bound, symmetric=True, null_diag=True)
        else:
            raise ValueError("Invalid graph form")

        # Create OpenDigraph instance from adjacency matrix
        graph = graph_from_adjacency_matrix(matrix)

        # Select inputs and outputs randomly (by checking for every node if it's a possible input/output node)
        node_ids = graph.get_node_ids()

        inputs_list = [i for i in node_ids if len(graph.get_node_by_id(i).get_parents()) == 0 and
                       len(graph.get_node_by_id(i).get_children()) == 1]
        if len(inputs_list) < inputs:
            raise ValueError("This graph has too few possibilities for inputs nodes")
        inputs_list = sample(node_ids, inputs)

        outputs_list = [i for i in node_ids if len(graph.get_node_by_id(i).get_children()) == 0 and
                        len(graph.get_node_by_id(i).get_parents()) == 1 and i not in inputs_list]
        if len(outputs_list) < outputs:
            raise ValueError("This graph has too few possibilities for outputs nodes")
        outputs_list = sample(node_ids, outputs)
        
        for node_id in inputs_list:
            graph.add_input_id(node_id)
        for node_id in outputs_list:
            graph.add_output_id(node_id)

        return graph
    
    def node_id_to_index_map(self) -> Dict[int, int]:
        """
        Returns a dictionary mapping each node ID to a unique integer index.
        The indices are in the range 0 ≤ i < n, where n is the number of nodes in the graph.
        :return: Dict[int, int];
        """
        node_ids = sorted(self.get_node_ids())  # Sort the node IDs
        node_index_map = {node_id: index for index, node_id in enumerate(node_ids)}  # Map each node ID to its index
        return node_index_map

    def adjacency_matrix(self) -> List[List[int]]:
        """
        Generates an adjacency matrix for the graph, ignoring inputs and outputs.
        Considers all nodes in the graph.
        :return: List[List[int]]; The adjacency matrix representing the connections between nodes.
        """
        # Get all nodes and their IDs
        nodes = self.get_nodes()
        node_ids = self.get_node_ids()
        
        # Initialize the adjacency matrix
        n = len(node_ids)
        adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        # Populate the adjacency matrix based on connections between nodes
        for node in nodes:
            node_id = node.get_id()
            children = node.get_children()
            for child_id, child_value in children.items():
                adj_matrix[node_id][child_id] = child_value  # Set the corresponding cell to 1
                
        return adj_matrix


def random_int_list(n: int, bound: int, unique=False) -> List[int]:
    """
    Returns a list of n random integers between 0 and n
    :param n: int; numbers of integers wanted
    :param bound: int; maximum value of the integers
    :param unique: bool; set True if you want only unique integers
    """
    if unique and n > bound + 1:
        raise ValueError("Bound too small compared to n")
    res = []
    for _ in range(n):
        tmp = randint(0, bound)
        if unique:
            while tmp in res:  # All numbers must be different to be IDs
                tmp = randint(0, bound)
        res.append(tmp)
    return res


def random_int_matrix(n: int, bound: int, unique=False, null_diag=True, symmetric=False,
                      oriented=False, dag=False) -> List[List[int]]:
    """
    Returns a matrix of nxn random integers between 0 and n
    :param n: int; numbers of rows and columns wanted
    :param bound: int; maximum value of the integers
    :param unique: bool; set True if you want only unique integers
    :param null_diag: bool; set True if you want the diagonal to be zeros
    :param symmetric: bool; set True if you want the matrix to be symmetric
    :param oriented: bool; set True if you want the matrix to define an oriented graph
    :param dag: bool; set True if you want the matrix to define an acyclic graph
    """
    if symmetric and (oriented or dag):
        raise ValueError("Matrix cannot be symmetric and oriented/acyclic")

    res = []
    for _ in range(n):
        res.append(random_int_list(n, bound, unique))

    if null_diag:
        for i in range(n):
            res[i][i] = 0

    if symmetric:
        for i in range(n):
            for j in range(i+1, n):
                res[j][i] = res[i][j]

    if oriented:
        for i in range(n):
            for j in range(i+1, n):
                if res[i][j] > 0:
                    res[j][i] = 0

    if dag:
        for i in range(n):
            for j in range(i+1, n):
                res[j][i] = 0

    return res


def graph_from_adjacency_matrix(matrix: List[List[int]]) -> OpenDigraph:
    """
    Returns an OpenDigraph from an adjency matrix
    :param matrix: List[List[int]]; the ajdency matrix
    """
    n = len(matrix)
    nodes = []
    for identity in range(n):
        children = {}
        parents = {}
        for i in range(n):
            if len(matrix[i]) != n or len(matrix[identity]) != n:
                raise ValueError("The matrix is not a squared matrix")

            if matrix[identity][i]:
                children[i] = matrix[identity][i]

            if matrix[i][identity]:
                parents[i] = matrix[i][identity]

        node = Node(identity, str(identity), parents, children)
        nodes.append(node)

    return OpenDigraph([], [], nodes)
