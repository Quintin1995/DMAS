import networkx as nx
from itertools import permutations
import matplotlib.pyplot as plt

#init graphk
G = nx.Graph()

amount_nodes = 4

nodes = range(1,amount_nodes)
edges = [x for x in permutations(nodes, 2 )]



for node in nodes:
    G.add_node(node)
for edge in edges:
    print(edge)



nx.draw(G)
plt.show()