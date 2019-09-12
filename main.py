from enum import Enum
import math
import random
import protocols
from protocols import Protocols
from phonebook import PhonebookType
from model import Model

"""
Experiment properties
"""
AMOUNT_AGENTS   = 10
MAX_SECRET      = 3
TRANSFER_CHANCE = 100
PROTOCOL        = Protocols.CO
ITERATIONS      = 600
PHONEBOOKTYPE   = PhonebookType.ALL

# Create a new instance of the model
gossip_model = Model(AMOUNT_AGENTS, MAX_SECRET, TRANSFER_CHANCE, PROTOCOL, PHONEBOOKTYPE)

# [!] Main loop start
gossip_model.do_iterations(ITERATIONS)
# [!] Main loop end

# Everything below here just prints the outcome.
for target_idx in range (AMOUNT_AGENTS):
    for agent_idx in range (AMOUNT_AGENTS):
        print ("Agent {} thinks agent {} has secret #{}".format(agent_idx, target_idx, gossip_model.get_secret_value(agent_idx, target_idx)))

    agent_secret = gossip_model.get_agent_secret(target_idx)
    print ("Agent {} has secret #{}".format(target_idx, agent_secret))
    print ()
print (gossip_model.call_log)