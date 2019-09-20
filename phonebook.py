"""
Phonebook initialization type, determines who can call who.

TYPES:
- ALL (Everyone is accessible to everyone initially.)
"""
class PhonebookType:
    ALL     = 1     # Everyone is in the phonebook

"""
Generate a phonebook based on the given phonebook type.
"""
def generate_phonebook (phonebook_type, amount_agents):
    phonebook = list()

    if phonebook_type == PhonebookType.ALL:
        for agent_idx in range (amount_agents):
            phonebook.append(list())
            phonebook[agent_idx] = list(range(amount_agents))
        
            # Remove ourselves from the list
            if agent_idx in phonebook[agent_idx]:
                phonebook[agent_idx].remove(agent_idx)
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
        