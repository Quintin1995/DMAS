from enum import Enum
import random

"""
Protocol types for caller / receiver selection.

TYPES:
- ANY   (Call anyone)
- CO    (Call someone new)
"""
class Protocols(Enum):
    ANY         = 1
    CO          = 2

"""
Exception type that is raised when there are no more callers left.
Gives a signal to the model that no more calls can be made, so the model knows to skip.
"""
class NoPossibleCallersError (Exception):
    pass

"""
Function that can choose the callers for a new call based on the type of protocol given.
"""
def choose_callers(amount_agents, phonebook, protocol):
    # Call anyone
    if protocol == Protocols.ANY:
        # Pick anyone from the range of agents
        possible_callers = range (amount_agents)

    # Call once
    if protocol == Protocols.CO:
        # Pick someone that still has someone in their phonebook
        possible_callers = [agent for agent in range(amount_agents) if len(phonebook[agent]) > 0]
    
    if len(possible_callers) < 1:
        raise NoPossibleCallersError

    # Pick a random agent from the eligible agents
    caller = random.choice(possible_callers)

    # Determine who this agent can call
    eligible_receivers = phonebook[caller]

    # Self is already not in phonebook, so can safely call first choice
    receiver = random.choice(eligible_receivers)

    # Update the phonebook according to protocol specifications
    update_phonebook(caller, receiver, phonebook, protocol)

    return (caller, receiver)

"""
Update the phonebook after caller and receiver of a new call are known.
E.g. if caller cannot call same agent again, remove the receiver from the caller's phonebook.
"""
def update_phonebook(caller, receiver, phonebook, protocol):
    # In call any protocol, we remove no one from the phonebooks
    if protocol == Protocols.ANY:
        pass
    
    # In call once, we remove the receiver from the caller's phonebook
    elif protocol == Protocols.CO:
        phonebook[caller].remove(receiver)