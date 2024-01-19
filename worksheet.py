from modules.open_digraph import *

n0 = Node(0, 'Orsay', {}, {2: 1})
n1 = Node(1, 'Le Guichet', {}, {2: 1})
n2 = Node(2, 'Paris', {0: 1, 1: 1}, {})

g0 = OpenDigraph([0, 1], [2], [n0, n1, n2])
print(g0)
