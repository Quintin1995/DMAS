"""
File defining protocols for caller / receiver selection.
"""

import random

# ANY
def choose_callers_any(amount_agents):
    caller = random.choice(range(amount_agents))
    receiver = random.choice(range(amount_agents))
    while (receiver == caller):
        receiver = random.choice(range(amount_agents))
    return (caller, receiver)