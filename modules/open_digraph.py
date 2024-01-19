class Node:

    def __init__(self, identity, label, parents, children):
        """
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent nodes id to its multiplicity
        children: int->int dict; maps a child nodes id to its multiplicity
        """
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

    def __str__(self):
        return f'({self.id}, {self.label}, {self.parents}, {self.children})'

    def __repr__(self):
        return str(self)


class OpenDigraph:  # for open directed graph

    def __init__(self, inputs, outputs, nodes):
        """
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id: node for node in nodes}  # self.nodes: <int,node> dict

    def __str__(self):
        return f'({self.inputs}, {self.outputs}, {self.nodes})'

    def __repr__(self):
        return str(self)

    @classmethod
    def empty(cls):
        # Create an instance of the class with empty inputs, outputs, and nodes
        return cls(inputs=[], outputs=[], nodes=[])
