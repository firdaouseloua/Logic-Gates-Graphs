from typing import List, Dict, Tuple


class Node:

    # Constructor
    def __init__(self, identity: int, label: str, parents: Dict[int, int], children: Dict[int, int]) -> None:
        """
        Construct a new node object
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent nodes id to its multiplicity
        children: int->int dict; maps a child nodes id to its multiplicity
        (Not sure what the multiplicity is)
        """
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

    # Getters
    def get_id(self) -> int:
        """
        Return node id
        """
        return self.id

    def get_label(self) -> str:
        """
        Return node label
        """
        return self.label

    def get_parents(self) -> Dict[int, int]:
        """
        Return node parents dict
        """
        return self.parents

    def get_children(self) -> Dict[int, int]:
        """
        Return node children dict
        """
        return self.children

    # Setters
    def set_id(self, new_identity: int) -> None:
        """
        Change node id
        new_identity: int; its unique id in the graph
        """
        self.id = new_identity

    def set_label(self, new_label: str) -> None:
        """
        Change node label
        new_label: string;
        """
        self.label = new_label

    def set_children(self, new_children) -> None:
        """
        Change node children dict
        new_children: int->int dict; maps a child nodes id to its multiplicity
        """
        self.children = new_children

    def add_parent_id(self, parent_id) -> None:
        """
        Add a new parent to node parents dict
        parent_id: int;
        """
        if parent_id in self.parents:  # Already a parent
            self.parents[parent_id] += 1  # Increase the multiplicity
        else:  # Not yet a parent
            self.parents[parent_id] = 1

    def add_child_id(self, child_id):
        """
        Add a new child to node children dict
        child_id: int;
        """
        if child_id in self.children:  # Already a child
            self.children[child_id] += 1  # Increase the multiplicity
        else:  # Not yet a child
            self.children[child_id] = 1

    # Printing methods
    def __str__(self) -> str:
        """
        Used by the __repr__ method
        """
        return f'({self.id}, {self.label}, {self.parents}, {self.children})'

    def __repr__(self) -> str:
        """
        Used to print the object
        """
        return str(self)

    # Methods
    def __eq__(self, other) -> bool:
        """
        Implementation of the "==" between two nodes
        other: Node;
        """
        return (self.id == other.id and self.label == other.label and
                self.parents == other.parents and self.children == other.children)

    def copy(self):
        """
        Create a copy of the node
        """
        return Node(self.id, self.label, dict(self.parents), dict(self.children))


class OpenDigraph:  # for open directed graph

    # Constructors
    def __init__(self, inputs: List[int], outputs: List[int], nodes: List[Node]) -> None:
        """
        Construct a new OpenDigraph object
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id: node for node in nodes}  # self.nodes: <int,node> dict

    @classmethod
    def empty(cls):
        """
        Create an instance of the class with empty inputs, outputs, and nodes
        """
        return cls(inputs=[], outputs=[], nodes=[])

    # Getters
    def get_input_ids(self) -> List[int]:
        """
        Return diagraph input list
        """
        return self.inputs

    def get_output_ids(self) -> List[int]:
        """
        Return diagraph output list
        """
        return self.outputs

    def get_id_node_map(self) -> Dict[int, Node]:
        """
        Return diagraph nodes dictionnary
        """
        return self.nodes

    def get_nodes(self) -> List[Node]:
        """
        Return a list of all the nodes
        """
        return list(self.nodes.values())

    def get_node_ids(self) -> List[int]:
        """
        Return a list of all the ids
        """
        return list(self.nodes.keys())

    def get_node_by_id(self, node_id: int) -> Node:
        """
        Return a node given its id
        """
        return self.nodes[node_id]

    def get_nodes_by_ids(self, ids: List[int]) -> List[Node]:
        """
        Return a list of nodes given a list of ids
        """
        return [self.nodes[node_id] for node_id in ids if node_id in self.nodes]

    # Setters
    def set_inputs(self, new_inputs: List[int]) -> None:
        """
        Change diagraph input list
        new_inputs: List[int];
        """
        self.inputs = new_inputs

    def set_outputs(self, new_outputs: List[int]) -> None:
        """
        Change diagraph output list
        new_outputs: List[int];
        """
        self.outputs = new_outputs

    def add_input_id(self, input_id: int) -> None:
        """
        Add a new input to the input list
        input_id: int;
        """
        if input_id not in self.inputs:  # useless to add it twice
            self.inputs.append(input_id)

    def add_output_id(self, output_id: int) -> None:
        """
        Add a new input to the input list
        input_id: int;
        """
        if output_id not in self.outputs:  # useless to add it twice
            self.outputs.append(output_id)

    # Printing methods
    def __str__(self) -> str:
        """
        Used by the __repr__ method
        """
        return f'({self.inputs}, {self.outputs}, {self.nodes})'

    def __repr__(self) -> str:
        """
        Used to print the object
        """
        return str(self)

    # Methods
    def __eq__(self, other) -> bool:
        """
        Implementation of the "==" between two diagraphs
        other: OpenDiagraph;
        """
        return (self.inputs == other.inputs and self.outputs == other.outputs
                and self.nodes == other.nodes)

    def copy(self):
        """
        Create a copy of the graph
        """
        return OpenDigraph(list(self.inputs), list(self.outputs), list(self.nodes.values()))

    def new_id(self):
        """
        Find and return an unused ID in the graph
        """
        used_ids = set(self.inputs + self.outputs + list(self.nodes.keys()))
        return max(used_ids) + 1 if used_ids else 0  # If there's no existing id, return 0, else the max + 1
        # We suppose that if we have n ids, they all go from 0 to n-1
        # Still doesn't cause any problem if we don't have that condition
        # We'll just have ids not numerotated from 0 to n-1
        # But this function is faster (O(n)) than checking for the first unused id from 0 to n (O(n^2))

    def add_edge(self, src: int, tgt: int) -> None:
        """
        Add an edge from the source node to the target node
        src: int; source node
        tgt: int; target node
        """
        if src in self.nodes and tgt in self.nodes:
            self.get_node_by_id(src).add_child_id(tgt)  # Add a child to the source node
            self.get_node_by_id(tgt).add_parent_id(src)  # Add a parent to the target node

    def add_edges(self, edges: List[Tuple[int, int]]) -> None:
        """
        Add edges between each pair of node IDs in the list of edges
        edges: list(tuple(int, int)); list of edges to add (int; source node, int; target node)
        """
        for src, tgt in edges:
            self.add_edge(src, tgt)

    def add_node(self, label="", parents=None, children=None) -> int:
        """
        Adds a node with a label to the graph, assigning it a new id.
        Links it with the parent and child id nodes with their respective multiplicities.
        If the default values for parents and/or children are None, assign them an empty dictionary.
        Returns the id of the new node.
        label: string;
        parents: List[int]; ids of the parents
        children: List[int]; ids of the childrens
        """
        # Create an new object Node
        new_node = Node(self.new_id(), label, {}, {})
        if parents is not None:
            for parent in parents:
                new_node.add_parent_id(parent)
        if children is not None:
            for child in children:
                new_node.add_child_id(child)

        # Add the new node to the graph
        self.nodes[new_node.get_id()] = new_node

        return new_node.get_id()
