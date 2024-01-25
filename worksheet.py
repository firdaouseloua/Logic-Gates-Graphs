import inspect
from modules.open_digraph import *

# Use of the inspect module
# Get the list of methods for Node class
node_methods = [method for method, _ in inspect.getmembers(Node)]
print("Node methods:", node_methods)

# Get the source code, doc, and file for the `copy` method in Node class
copy_method = getattr(Node, 'copy', None)
if copy_method:
    copy_source = inspect.getsource(copy_method)
    copy_doc = inspect.getdoc(copy_method)
    copy_file = inspect.getfile(copy_method)
    print("\nNode copy method source code:\n", copy_source)
    print("Node copy method docstring:", copy_doc)
    print("\nNode copy method file:", copy_file)

# Get the list of methods for OpenDigraph class
open_digraph_methods = [method for method, _ in inspect.getmembers(OpenDigraph)]
print("\nOpenDigraph methods:", open_digraph_methods)

# Get the source code, doc, and file for the `copy` method in OpenDigraph class
copy_method_open_digraph = getattr(OpenDigraph, 'copy', None)
if copy_method_open_digraph:
    copy_source_open_digraph = inspect.getsource(copy_method_open_digraph)
    copy_doc_open_digraph = inspect.getdoc(copy_method_open_digraph)
    copy_file_open_digraph = inspect.getfile(copy_method_open_digraph)
    print("\nOpenDigraph copy method source code:\n", copy_source_open_digraph)
    print("OpenDigraph copy method docstring:", copy_doc_open_digraph)
    print("\nOpenDigraph copy method file:", copy_file_open_digraph)


# Priting OpenDiagraph
n0 = Node(0, 'Orsay', {}, {2: 1})
n1 = Node(1, 'Le Guichet', {}, {2: 1})
n2 = Node(2, 'Paris', {0: 1, 1: 1}, {})
print("\nOpenDiagraph printing method:")
g = OpenDigraph([0, 1], [2], [n0, n1, n2])
print(g)
