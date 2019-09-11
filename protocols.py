from enum import Enum
import random

"""
Protocol types for caller / receiver selection.

TYPES:
- LNS (Call someone new)
- ANY (Call anyone)
"""
class Protocols(Enum):
    LNS         = 1
    NOC         = 2
    ANY         = 3

"""
Function that can choose the callers for a new call based on the type of protocol given.
"""
def choose_callers(amount_agents, phonebook, protocol):

    if protocol == Protocols.ANY:
        caller = random.choice(range(amount_agents))
        
        # Determine who this agent can call
        eligible_receivers = phonebook[caller]

        # Self is already not in phonebook, so can safely call first choice
        receiver = random.choice(eligible_receivers)

    return (caller, receiver)