from enum import Enum
import matplotlib.pyplot as plt
import networkx as nx
import random
"""
Phonebook initialization type, determines who can call who.

TYPES:
- ALL (Everyone is accessible to everyone initially.)
"""
class PhonebookType(Enum):
    ALL         = 1     # Everyone is in the phonebook
    TWO_WORLDS  = 2 
    PARTIAL_GRAPH  = 3
    CUSTOM_GRAPH = 4
"""
Generate a phonebook based on the given phonebook type.
"""
def generate_phonebook (phonebook_type, amount_agents, connectivity):
    phonebook = list()

    if phonebook_type == PhonebookType.ALL:
        for agent_idx in range (amount_agents):
            phonebook.append(list())
            phonebook[agent_idx] = list(range(amount_agents))
        
            # Remove ourselves from the list
            if agent_idx in phonebook[agent_idx]:
                phonebook[agent_idx].remove(agent_idx)
    
    if phonebook_type == PhonebookType.TWO_WORLDS:
        all_agents = list(range(amount_agents))
        world_one  = all_agents[:len(all_agents) // 2]
        world_two  = all_agents[len(all_agents) // 2:]

        for agent_idx in world_one:
            phonebook.append(list())
            phonebook[agent_idx] = list(world_one)

            # Remove ourselves from the list
            if agent_idx in phonebook[agent_idx]:
                phonebook[agent_idx].remove(agent_idx)

        for agent_idx in world_two:
            phonebook.append(list())
            phonebook[agent_idx] = list(world_two)

            # Remove ourselves from the list
            if agent_idx in phonebook[agent_idx]:
                phonebook[agent_idx].remove(agent_idx)
        
        # Create a single connection between the two worlds
        connected_agent_one = random.choice(world_one)
        connected_agent_two = random.choice(world_two)
        phonebook[connected_agent_one].append(connected_agent_two)
        phonebook[connected_agent_two].append(connected_agent_one)        

    if phonebook_type == PhonebookType.PARTIAL_GRAPH:
        #generate a partial graph first
        G = generate_partial_graph(amount_agents, connectivity/100.0)
        #make a phonebook out of the graph as we know a phonebook, a list with lists
        nodes = list(G.nodes)
        for agnt_idx in range(amount_agents):
            phonebook.append(list())
        for idx, node in enumerate(nodes):
            for edge in list(G.edges(node)):
                a,b = edge
                if a != idx:
                    phonebook[idx].append(a)
                if b != idx:
                    phonebook[idx].append(b)
    if phonebook_type == PhonebookType.CUSTOM_GRAPH:
        #passing because we already have a graph to make a phonebook from
        for agent_idx in range (amount_agents):
            phonebook.append(list())

    # print(phonebook)
    return phonebook


"""
Returns a Graph object based on the amount of agents(nodes) and connectivity fraction in percents.
"""
def generate_partial_graph(amount_agents=10, connectivity=1.0):
    #calculate theoretical connectivity, when fully connected.
    theory_connections = amount_agents * (amount_agents - 1) / 2
    #how many connections still need to be added to reach the desired connectivity.
    connections2do = theory_connections * connectivity
    connections_made = 0
    
    #create the graph and add the first node.
    G = nx.Graph()
    first_node = int(0)
    G.add_node(first_node)

    #create minimal spanning tree, to ensure that each node is connected to the rest of the graph.
    for i in range(1,amount_agents):
        node = random.choice(list(G.nodes))
        G.add_edge(i, node)
        G.add_node(int(i))
        connections_made += 1

    #calc amount of available connections
    available_connections = get_available_connections(G, amount_agents)

    #add edges, until desired amount of connectivity is reached.
    if len (available_connections) > 0 and int(connections2do - connections_made) > 0:
        picks = random.sample(available_connections, int(connections2do - connections_made))
        for agent1, agent2 in picks:
            G.add_edge(agent1, agent2)

    print ("Created random graph that is {} connected".format(get_connectivity(amount_agents, G)))
    return G


"""
Returns list of edges that are not present in the graph yet. These edges can still be added.
"""
def get_available_connections(G, amount_agents):
    from itertools import combinations
    all_connections = list(combinations(range(amount_agents), 2))
    available_connections = list()
    for connection in all_connections:
        if connection not in G.edges:
            available_connections.append(connection)
    return available_connections


"""
Returns emperical connectivity of the graph.
"""
def get_connectivity(amount_agents, graph):
    theory_connec = amount_agents * (amount_agents - 1) / 2
    real_connec = len(graph.edges)

    emperical_connec = real_connec / float(theory_connec)
    return emperical_connec



def convert_phonebook_to_tuples(phonebook):
    amount_agents = len(phonebook)
    conv_phonebook = list()
    for agent_idx in range (amount_agents):
        for agent2_idx in phonebook[agent_idx]:
            conv_phonebook.append((agent_idx, agent2_idx))

    return conv_phonebook
        