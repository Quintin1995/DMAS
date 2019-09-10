from enum import Enum
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

AMOUNT_AGENTS   = 22
MAX_SECRET      = 22
TRANSFER_CHANCE = 100
PROTOCOL        = Protocols.ANY
ITERATIONS      = 60
possible_secrets = list(range(MAX_SECRET))

def get_secret_value (agent_idx, target_idx):
    agent_knowledge = secrets[agent_idx][target_idx]
    highest_secrets = [idx for idx, s in enumerate(agent_knowledge) if s == max(agent_knowledge)]
    return random.choice(highest_secrets)

def agent_has_information (agent_idx, target_idx):
    agent_knowledge = secrets[agent_idx][target_idx]
    if (max(agent_knowledge)) > 0:
        return True
    return False

def get_agent_codename (agent_idx): 
    return "Agent {}".format(agent_idx + 1)

def get_secret_codename (secret_idx):
    return "secret {}".format(secret_idx + 1)

def get_agent_secret (agent_idx):
    return [idx for idx, s in enumerate(secrets[agent_idx][agent_idx]) if s == max(secrets[agent_idx][agent_idx])][0]

# Initialize agents
agents  = list ([dict () for a in range (AMOUNT_AGENTS)])
secrets = list ()

for agent_idx in range (AMOUNT_AGENTS):
    secrets.append(list())
    for target_idx in range (AMOUNT_AGENTS): 
        secrets[agent_idx].append(list())
        for secret_idx in range (MAX_SECRET):
            secrets[agent_idx][target_idx].append(list())
            secrets[agent_idx][target_idx][secret_idx] = 0
    
    secrets[agent_idx][agent_idx][random.choice(possible_secrets)] = 999999


# Initialize call log
calls = list ()
avg_knowledge = list ()

def transfer_secrets(sender, receiver):
    for target_agent in range(AMOUNT_AGENTS): # Same amount of secrets as agents
        # Agents know their own secret
        if (target_agent == receiver):
            continue
        if (agent_has_information(sender, target_agent)):
            secrets[receiver][target_agent][get_secret_value(sender, target_agent)] += 1

# Define protocol
def choose_callers_any(agents, calls):
    caller = random.choice(range(AMOUNT_AGENTS))
    receiver = random.choice(range(AMOUNT_AGENTS))
    while (receiver == caller):
        receiver = random.choice(range(AMOUNT_AGENTS))
    return (caller, receiver)

for agent_idx in range (AMOUNT_AGENTS):
    agent_secret = get_agent_secret(agent_idx)
    print ("{} has {}".format(get_agent_codename(agent_idx), get_secret_codename(agent_secret)))

# Main loop
for iteration in range(ITERATIONS):
    # print (secrets)
    if PROTOCOL == Protocols.ANY:
        caller, receiver = choose_callers_any(agents, calls)
    
    transfer_secrets(caller, receiver)
    transfer_secrets(receiver, caller)

    calls.append(tuple((caller, receiver)))
    # avg_knowledge.append (sum ([len([True for s in agents[a]["secrets"] if s == True]) for a in range (AMOUNT_AGENTS)]) / AMOUNT_AGENTS)


for target_idx in range (AMOUNT_AGENTS):
    for agent_idx in range (AMOUNT_AGENTS):
        print ("{} thinks {} has {}".format(get_agent_codename(agent_idx), get_agent_codename(target_idx), get_secret_codename(get_secret_value(agent_idx, target_idx))))

    agent_secret = get_agent_secret(target_idx)
    print ("{} has {}".format(get_agent_codename(target_idx), get_secret_codename(agent_secret)))
    print ()

# for i in ITERATIONS: 
#     print (""l)
# print (calls)
# print (avg_knowledge)
# print ("--------------------------")

print ()