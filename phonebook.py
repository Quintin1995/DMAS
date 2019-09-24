import random
from enum import Enum
import matplotlib.pyplot as plt
import networkx as nx
"""
Phonebook initialization type, determines who can call who.

TYPES:
- ALL (Everyone is accessible to everyone initially.)
"""
class PhonebookType:
    ALL         = 1     # Everyone is in the phonebook
    TWO_WORLDS  = 2 
    RAND_GRAPH  = 3
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

    if phonebook_type == PhonebookType.RAND_GRAPH:
        G = generate_random_graph(amount_agents, connectivity/100.0)

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

    return phonebook


def generate_random_graph(amount_agents=10, connectivity=1.0):
    print("starting generating random graph")
    G = nx.Graph()
    first_node = int(0)
    G.add_node(first_node)

    for i in range(1,amount_agents):
        node = random.choice(list(G.nodes))
        G.add_edge(i, node)
        G.add_node(int(i))
   
    for i in range(amount_agents):
        picks = random.sample(list(range(amount_agents)), int(amount_agents*connectivity))
        print(picks)
        for sample in picks:
            G.add_edge(i, sample)

    print("end generating random graph")
    return G


def convert_phonebook_to_tuples(phonebook):
    amount_agents = len(phonebook)
    conv_phonebook = list()
    for agent_idx in range (amount_agents):
        # conv_phonebook.append(list())
        # conv_phonebook[agent_idx] = list(range(amount_agents))
        for agent2_idx in phonebook[agent_idx]:
            conv_phonebook.append((agent_idx, agent2_idx))

    return conv_phonebook
        