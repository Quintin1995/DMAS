from enum import Enum
from tqdm import tqdm
import math
import random


# Define protocols
class Protocols(Enum):
    LNS         = 1
    NOC         = 2
    ANY         = 3

class LiarType (Enum):
    BLUFFER     = 1
    SABOTEUR    = 2

AMOUNT_AGENTS   = 3
MAX_SECRET      = 2
TRANSFER_CHANCE = 100
PROTOCOL        = Protocols.ANY
ITERATIONS      = 5
possible_secrets = list(range(MAX_SECRET))

def get_secret_value (agent_idx, secret_idx):
    agent_knowledge = agents[agent_idx]["secrets"][secret_idx]
    highest_secrets = [idx for idx, s in enumerate(agent_knowledge) if s == max(agent_knowledge)]
    return random.choice(highest_secrets)

def agent_knows_secret (agent_idx, secret_idx):
    agent_knowledge = agents[agent_idx]["secrets"][secret_idx]
    if (max(agent_knowledge)) > 0:
        return True
    return False

# Initialize agents
agents = list ([dict () for a in range (AMOUNT_AGENTS)])

for idx, a in enumerate(agents):
    a["name"]           = idx
    a["secrets"]        = list ()
    for o in range(AMOUNT_AGENTS): 
        a["secrets"].append(list())
        for s in possible_secrets:
            a["secrets"][o].append(0)

    a["secrets"][idx][random.choice(possible_secrets)] = 999999
    a["addressbook"]    = list()

# Initialize call log
calls = list ()
avg_knowledge = list ()

def transfer_secrets(caller, receiver):
    for secret in range(AMOUNT_AGENTS): # Same amount of secrets as agents
        if (agent_knows_secret(caller, secret)):
            agents[receiver]["secrets"][secret][get_secret_value(caller, receiver)] += 1

# Define protocol
def choose_callers_any(agents, calls):
    caller = random.choice(range(AMOUNT_AGENTS))
    receiver = random.choice(range(AMOUNT_AGENTS))
    while (receiver == caller):
        receiver = random.choice(range(AMOUNT_AGENTS))
    return (caller, receiver)

# Main loop
for iteration in tqdm(range(ITERATIONS)):
    if PROTOCOL == Protocols.ANY:
        caller, receiver = choose_callers_any(agents, calls)
    
    transfer_secrets(caller, receiver)
    transfer_secrets(receiver, caller)

    calls.append(tuple((caller, receiver)))
    # avg_knowledge.append (sum ([len([True for s in agents[a]["secrets"] if s == True]) for a in range (AMOUNT_AGENTS)]) / AMOUNT_AGENTS)

    for a in agents:
        print (a)

# for i in ITERATIONS: 
#     print (""l)
print (calls)
print (avg_knowledge)
print ("--------------------------")
