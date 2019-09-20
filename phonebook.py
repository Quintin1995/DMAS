import random

"""
Phonebook initialization type, determines who can call who.

TYPES:
- ALL (Everyone is accessible to everyone initially.)
"""
class PhonebookType:
    ALL         = 1     # Everyone is in the phonebook
    TWO_WORLDS  = 2     
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

        
    return phonebook


def convert_phonebook_to_tuples(phonebook):
    amount_agents = len(phonebook)
    conv_phonebook = list()
    for agent_idx in range (amount_agents):
        # conv_phonebook.append(list())
        # conv_phonebook[agent_idx] = list(range(amount_agents))
        for agent2_idx in phonebook[agent_idx]:
            conv_phonebook.append((agent_idx, agent2_idx))

    return conv_phonebook
        