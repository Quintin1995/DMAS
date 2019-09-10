from enum import Enum
import random

# Define protocols
class Protocols(Enum):
    LNS = 1
    NOC = 2
    ANY = 3

AMOUNT_AGENTS  = 5
TRANSFER_CHANCE= 50
PROTOCOL       = Protocols.ANY
ITERATIONS     = 3

# Initialize agents
agents = list ([dict () for a in range (AMOUNT_AGENTS)])

for idx, a in enumerate(agents):
    a["name"] = idx
    a["secrets"] = [False] * AMOUNT_AGENTS
    a["secrets"][idx] = True

# Initialize call log
calls = list ()

def transfer_secrets(caller, receiver):
    for secret in range(AMOUNT_AGENTS): # Same amount of secrets as agents
        if (agents[receiver]["secrets"][secret]):
            continue
        
        if not (agents[caller]["secrets"][secret]):
            continue

        if random.randrange(100) < TRANSFER_CHANCE:
            agents[receiver]["secrets"][secret] = True
# Define protocol
def choose_callers_any(agents, calls):
    caller = random.choice(range(AMOUNT_AGENTS))
    receiver = random.choice(range(AMOUNT_AGENTS))
    while (receiver == caller):
        receiver = random.choice(range(AMOUNT_AGENTS))
    return (caller, receiver)

# Main loop
for iteration in range(ITERATIONS):
    if PROTOCOL == Protocols.ANY:
        caller, receiver = choose_callers_any(agents, calls)
    
    transfer_secrets(caller, receiver)
    transfer_secrets(receiver, caller)

    calls.append(tuple((caller, receiver)))

    for a in agents:
        print (a)
    print (calls)
    print ("--------------------------")
