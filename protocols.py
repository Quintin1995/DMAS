"""
File defining protocols for caller / receiver selection.
"""

from enum import Enum
import random

# Define protocols
class Protocols(Enum):
    LNS         = 1
    NOC         = 2
    ANY         = 3

# ANY
def choose_callers_any(amount_agents, phonebook):
    caller = random.choice(range(amount_agents))
    receiver = random.choice(range(amount_agents))
    while (receiver == caller):
        receiver = random.choice(range(amount_agents))
    return (caller, receiver)