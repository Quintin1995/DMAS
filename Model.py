from protocols import Protocols, NoPossibleCallersError
from phonebook import PhonebookType
import phonebook
import protocols
import random
from enum import Enum
import networkx as nx
from copy import deepcopy

class State(Enum):
    RUN         = 1
    DONE        = 2
    NO_CALLS    = 3

class Model:
    """
    GOSSIP MODEL
    Determines who can call who based on chosen protocol / phonebook initialization.
    Keeps track of who calls who.
    """
    def __init__ (self, amount_agents, amount_secrets, transfer_chance, protocol, phonebooktype):
        self.protocol           = protocol
        self.amount_agents      = amount_agents
        self.amount_secrets     = amount_secrets
        self.possible_secrets   = list(range(self.amount_secrets))
        self.transfer_chance    = transfer_chance
        self.secrets = list ()
        self.initialize_secrets()
        self.phonebook_type     = phonebooktype
        self.initialize_phonebook()
        self.call_log           = list()
        #states: RUN, DONE, NO_CALLS
        self.state              = State.RUN
        self.graph              = nx.Graph()
        self.temp_edges         = [(1,2), (3,2), (3,1)]
        self.graph.add_edges_from(self.temp_edges)

    """
    Initializes the global list of secrets.
    """
    def initialize_secrets (self):
        for agent_idx in range (self.amount_agents):
            self.secrets.append(list())
            for target_idx in range (self.amount_agents): 
                self.secrets[agent_idx].append(list())
                for secret_idx in range (self.amount_secrets):
                    self.secrets[agent_idx][target_idx].append(list())
                    self.secrets[agent_idx][target_idx][secret_idx] = 0
            
            self.secrets[agent_idx][agent_idx][random.choice(self.possible_secrets)] = 999999

    """
    Initializes a dictionary for each agent, which can be used later to store additional
    information about an agent when we decide to implement an extension in the future.
    """
    def initialize_extra_info (self):
        self.extra_info = list ([dict () for a in range (self.amount_agents)])
    
    """
    Initializes the list of agents that each agent can call.
    The agents that each agent can call are determined initially based on 
    the 'phonebook type'
    """
    def initialize_phonebook (self):
        # If we can call anyone, add everyone to the phonebook
        self.phonebook = phonebook.generate_phonebook(self.phonebook_type, self.amount_agents)

    """
    Does one more iteration of the gossip model making a call between two agents,
    according to each agents' phonebook, and the rules of the protocol.
    """        
    def next_call (self):
        try:
            caller, receiver = protocols.choose_callers(self)
        except NoPossibleCallersError:
            print ("[W] No agents are eligible to make any calls.")
            raise
        else:
            self.call(caller, receiver)
    """
    Performs the actual call when the caller and receiver have been determined.
    Transfer secrets between the agents, and log the call.
    """
    def call (self, caller, receiver):
        backup_receiver = deepcopy(receiver)
        self.transfer_secrets(caller, backup_receiver)
        self.transfer_secrets(receiver, caller)
        self.call_log.append(tuple((caller, receiver)))

    """
    Gets the current prediction that an agent has for the secret number of a target agent.
    E.g.: get_secret_value (1, 2) obtains what agent 1 thinks agent 2's secret is.
    """
    def get_secret_value (self, agent_idx, target_idx):
        if not self.agent_has_information(agent_idx, target_idx):
            return -1
        agent_knowledge = self.secrets[agent_idx][target_idx]
        highest_secrets = [idx for idx, s in enumerate(agent_knowledge) if s == max(agent_knowledge)]
        return random.choice(highest_secrets)

    """
    A simple function that determines whether an agent has received at least some 
    information about a target agent's secret.
    """
    def agent_has_information (self, agent_idx, target_idx):
        agent_knowledge = self.secrets[agent_idx][target_idx]
        if (max(agent_knowledge)) > 0:
            return True
        return False

    """
    Obtains the actual secret of an agent.
    """
    def get_agent_secret (self, agent_idx):
        return [idx for idx, s in enumerate(self.secrets[agent_idx][agent_idx]) if s == max(self.secrets[agent_idx][agent_idx])][0]

    """
    Transfers the knowledge between two agents.
    This is a one-way function, the receiver is updated with the sender's information.
    To update both, perform this function twice in opposite direction.
    """
    def transfer_secrets(self, sender, receiver):
        for target_agent in range(self.amount_agents): # Same amount of secrets as agents
            # Agents know their own secret
            if (target_agent == receiver):
                continue
            if (self.agent_has_information(sender, target_agent)):
                if (random.randint(0, 99) < self.transfer_chance):
                    self.secrets[receiver][target_agent][self.get_secret_value(sender, target_agent)] += 1

    """
    Prints to the console, the actual secrets that agents have.
    """
    def print_agent_secrets (self):
        for agent_idx in range (self.amount_agents):
            agent_secret = self.get_agent_secret(agent_idx)
            print ("{} has {}".format(agent_idx, agent_secret))
    """
    Returns true if an agent is an expert, and false if he is not.
    """
    def is_expert (self, agent_idx):
        for secret_idx in range (self.amount_agents):
            if self.get_agent_secret(secret_idx) != self.get_secret_value(agent_idx, secret_idx):
                return False
        return True

    """
    Returns a list comprehension of all the agents that are experts in the model
    """
    def get_experts (self):
        return [agent_idx for agent_idx in range (self.amount_agents) if self.is_expert(agent_idx)]

    """
    'Main' function of the model, runs given amount of iterations.
    """
    def do_iterations (self, iterations):
        for iteration in range (iterations):
            if len(self.get_experts()) == self.amount_agents:
                self.state = State.DONE
                break
            try: 
                self.next_call()
            except NoPossibleCallersError:
                print ("Ended execution after {} iterations, no more calls possible.".format(iteration))
                self.state = State.NO_CALLS
                break