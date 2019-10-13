# DMAS
Design of Multi Agent Systems Repository.
Date: Friday 06-09-2019


# Required Packages (Python3)
- numpy (1.17.2)
- tkinter (3.6.8-1)
- matplotlib (3.1.1)
- networkx (2.3)


# How to run (23 Sep 2019)
- Most up to date Branch --> master
- Run command: python3 main.py

# Gaining knowledge
The amount of knowledge that agents have is depicted in the top graph, which shows the network.
The progression of combined knowledge of the agents in the simulation is shown in the bottom graph.

The amount of agents in the simulation can be set using the AMOUNT AGENTS setting in the side panel on the right.
Agents gain knowledge by calling each other, which is when they transfer their knowledge between them.
To make the next call, click the '1 iteration' button.
To make more than one call at a time, use the 'Do N iterations' button, it will only render the graph of the last iteration.
The agents that last called are shown in the top graph as a cyan highlighted edge, between the two highlighted nodes.

At the beginning of the simulation, agents only know their own secrets, and their color in the graph is red, corresponding to 'little knowledge'.
As the agents learn more of the secrets of the other agents, their knowledge increases until they know all the secrets. As they learn more secrets, their node in the graph will start to change from red to green.
When an agent knows each other agent's secrets, they are 'experts', and their node in the graph will become blue.

# Protocols
Protocols determine which agents can be randomly selected to call each other at a given point in time.
To select a protocol to experiment with, choose the desired protocols from the dropdown menu in the sidebar on the right.
Protocols can only select possibilities for calls that are allowed by the agents' phonebook.

The protocols implemented in the simulation are:
- ANY (Agents can call any other agent in their phonebook)
- CO (Agents can only call other agents once)
- LNS (Agents can only call agents that have a secret that they don't have yet)
- SPI (Spider in the web)
- TOK (Token based protocols)

To update the model with a new protocol setting, or to reset the current model, click the "Set model" button.

# Transferring knowledge
When two agents call each other, they will transfer their secrets.
When no lying is used, the sender will tell the receiver for each agent which secret the sender believes they have.
To balance the weight of lies and truth in the system, each agent transfers a value based on how sure they are the other agent has that secret.
If an agent has heard that agent A has secret 1 twice and secret 2 three times, it will transfer secret 2 for agent A with strength 0.6.
A truth percentage can be set, which is universal for all agents, which determines the chance an agent tells the truth.
If an agent is not telling the truth about an agent, a secret is chosen at random to be transferred, according to two different implementations: LIE and MISTAKE.
- LIE: The secret randomly chosen to be transfered is send to the receiver with a fixed strenght caled lie_factor.
- MISTAKE: The secret randomly chosen to be transfere is send to the receiver with a fixed strenght called lie_factor if the sender has never heard the secret (count is 0). If the sender has heard the secret, the strenght is calculated as with a truthful transfer.
This means that with the LIE implementation, an agent always tells the lie, whereas with the MISTAKE implementation, the agent shares the value of how much it is convinced that this wrong secret might be the truth.

# Phonebook
The phonebook determines the edges of the network.
Agents that do not have each other's 'phone numbers' cannot call each other.
The currently implemented graph structures that can be generated are: 
- ALL (Fully connected bi-directional graph)
- TWO WORLDS (Two worlds, with a single connection between two random agents from each world)
- RANDOM (Generates a random graph in which each agent is at least connected to one other agent)

Note: The connectivity setting influences the ratio of connected agents for the RANDOM graphs.
Setting the connectivity to 1 percent generates a graph with the minimum required edges to connect all agents. Setting the connectivity to 100 percent generates a fully connected graph.

To update the model with a new phonebook setting, or to reset the current model, click the "Set model" button.

# Session statistics
In the left-hand sidepanel, information about the current session is shown.

*Model status*: Shows the status of the current simulation
- Running: The model is not terminated, and there are calls left to make.
- Success: The model has terminated, because every agent has reached expert knowledge.
- Failed: The model has terminated, because there are no more calls left to make, not all agents have become experts.

*Call log*: Shows a log of all the calls made in the current simulation.