#other libraries
from copy import deepcopy
from enum import Enum
import networkx as nx
import numpy as np
import random

#our libraries
import protocols
from phonebook import *
from protocols import Protocols, NoPossibleCallersError

class State(Enum):
    RUN         = 1
    DONE        = 2
    NO_CALLS    = 3
    NO_INFO     = 4

class Behavior(Enum):
    LIE         = 1
    MISTAKE     = 2

class Model:
    """
    GOSSIP MODEL
    Determines who can call who based on chosen protocol / phonebook initialization.
    Keeps track of who calls who.
    """
    def __init__ (self, amount_agents, amount_secrets, transfer_chance, protocol, phonebooktype, lie_factor, behavior, phonebook_connectivity = 100, exchange_phonebooks = False):
        self.protocol           = protocol
        self.amount_agents      = amount_agents
        self.amount_secrets     = amount_secrets
        self.possible_secrets   = list(range(self.amount_secrets))
        self.transfer_chance    = transfer_chance
        self.lie_factor       = float(lie_factor)/100
        self.secrets = list ()
        self.initialize_secrets()
        self.phonebook_type     = phonebooktype
        self.phonebook_connectivity = phonebook_connectivity
        self.initialize_phonebook()
        self.phonebook_calls = list() # used for the CO protocol
        self.initialize_phonebook_calls()
        self.call_log           = list()
        self.calls_made         = 0
        self.state              = State.RUN
        self.summed_knowledge   = list()
        self.behavior           = behavior
        self.exchange_phonebooks = exchange_phonebooks # transfer phonenumbers during exchange of secrets
        self.old_secrets = np.zeros((self.amount_agents, self.amount_agents))

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
            
            self.secrets[agent_idx][agent_idx][random.choice(self.possible_secrets)] = 99999999

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
        self.phonebook = generate_phonebook(self.phonebook_type, self.amount_agents, self.phonebook_connectivity)
        self.conv_phonebook     = convert_phonebook_to_tuples(self.phonebook)
        self.graph              = nx.Graph()
        self.graph.add_edges_from(self.conv_phonebook)

    """
    Adds number to the phonebook of caller
    Also updates conv_phonebook and optionally
    updates the graph with the new edge
    """
    def add_to_phonebook(self, caller, number, update_graph = True):
        self.phonebook[caller].append(number) # add number to phonebook
        self.conv_phonebook.append((caller, number))
        if update_graph:
            new_edge = list()
            new_edge.append( (caller, number) )
        self.graph.add_edges_from(new_edge)


    """
    Initializes the calls made between agents used for the call once (CO) protocol
    if the call is made, the value is 1, no call made is 0, not in phonebook is -1
    """
    def initialize_phonebook_calls (self):
        self.phonebook_calls = np.zeros ((self.amount_agents, self.amount_agents))
        for agent_idx in range (self.amount_agents):
            current_phonebook = self.phonebook[agent_idx]
            # print("current_phonebook: ", current_phonebook) # debug
            for target_idx in range (self.amount_agents):
                if target_idx == agent_idx: # agent can't call itself
                    self.phonebook_calls[agent_idx, target_idx] = 1 # set to already called instead of impossible to call
                                                                    # this removes complications when learning 
                                                                    # new phonenumbers
                elif target_idx not in current_phonebook:
                    self.phonebook_calls[agent_idx, target_idx] = -1 # set to not possible to call (yet)
    

    """
    Reset phonebook and phonebook calls with given connectivity
    """
    def reset_phonebook(self, connectivity = 100):
        self.phonebook_connectivity = connectivity
        self.initialize_phonebook()
        self.initialize_phonebook_calls()


    """
    Does one more iteration of the gossip model making a call between two agents,
    according to each agents' phonebook, and the rules of the protocol.
    """        
    def next_call (self):
        try:
            caller, receiver = protocols.choose_callers(self)
        except NoPossibleCallersError:
            # print ("[W] No agents are eligible to make any calls.")
            raise
        else:
            self.call(caller, receiver)
    """
    Performs the actual call when the caller and receiver have been determined.
    Transfer secrets between the agents, and log the call.
    """
    def call (self, caller, receiver):
        backup_receiver = deepcopy(receiver)
        if self.exchange_phonebooks:
            self.transfer_phonenumbers(caller, receiver)
        self.transfer_secrets(caller, backup_receiver)
        self.transfer_secrets(receiver, caller)
        self.call_log.append(tuple((caller, receiver)))
        self.calls_made += 1
        self.summed_knowledge.append(self.get_sum_known_secrets())

        ## debug
        # print("\nCall: ",  self.calls_made)
        # print(caller,  " called ",  receiver, "\n")
        # print(self.phonebook_calls)
        # print()
        # print(self.phonebook)

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
            elif (self.agent_has_information(sender, target_agent)):
                secret_knowledge = self.get_secret_value(sender, target_agent)
                if (random.randint(0, 99) < self.transfer_chance):
                    self.secrets[receiver][target_agent][secret_knowledge] += float(self.secrets[sender][target_agent][secret_knowledge])/sum(self.secrets[sender][target_agent])
                else:
                    random_knowledge = random.choice(self.possible_secrets)
                    while (random_knowledge == secret_knowledge):
                        random_knowledge = random.choice(self.possible_secrets)
                    if self.behavior == Behavior.LIE:
                        self.secrets[receiver][target_agent][random_knowledge] += self.lie_factor
                    elif self.behavior == Behavior.MISTAKE:
                        if self.secrets[receiver][target_agent][random_knowledge] == 0:
                            self.secrets[receiver][target_agent][random_knowledge] += self.lie_factor
                        else:
                            self.secrets[receiver][target_agent][random_knowledge] += float(self.secrets[sender][target_agent][random_knowledge])/sum(self.secrets[sender][target_agent])

    """
    Transfer phonenumbers from sender to receiver and back
    Add new numbers to the corresponding phonebook and 
    set numbers to callable
    """
    def transfer_phonenumbers(self, sender, receiver):
        self.transfer_phonenumbers_helper(sender, receiver)
        self.transfer_phonenumbers_helper(receiver, sender)

    """
    Helper function for transfer_phonenumbers
    Transfers phonenumbers one-way
    """
    def transfer_phonenumbers_helper(self, sender, receiver):
        for number in self.phonebook[sender].copy():
            if self.phonebook_calls[receiver, number] == -1: # number not yet callable
                self.phonebook_calls[receiver, number] = 0 # set number callable and not yet called
                self.add_to_phonebook(sender, number)

    """
    Prints to the console, the actual secrets that agents have.
    """
    def print_agent_secrets (self):
        for agent_idx in range (self.amount_agents):
            agent_secret = self.get_agent_secret(agent_idx)
            # print ("{} has {}".format(agent_idx, agent_secret))

    """
    Returns true if an agent is an expert, and false if he is not.
    """
    def is_expert (self, agent_idx):
        for secret_idx in range (self.amount_agents):
            if self.get_agent_secret(secret_idx) != self.get_secret_value(agent_idx, secret_idx):
                return False
        return True


    """
    Returns the amount of secrets known to the agent.
    """ 
    def get_secret_count(self, agent_idx):
        secret_count = 0
        for secret_idx in range (self.amount_agents):
            if self.get_agent_secret(secret_idx) != self.get_secret_value(agent_idx, secret_idx):
                return secret_count
            secret_count += 1
        return secret_count


    """
    Returns the amount of secrets that an agent correctly knows
    """
    def get_amount_known_secrets (self, agent_idx):
        total = 0
        for secret_idx in range (self.amount_agents):
            if self.get_agent_secret(secret_idx) == self.get_secret_value(agent_idx, secret_idx):
                total += 1
        return total

    """
    Returns the SUMMED amount of secrets that the agents correctly know
    """
    def get_sum_known_secrets (self):
        total = 0
        for agent_idx in range (self.amount_agents):
            total += self.get_amount_known_secrets(agent_idx)
        return total

    """
    Returns a list comprehension of all the agents that are experts in the model
    """
    def get_experts (self):
        return [agent_idx for agent_idx in range (self.amount_agents) if self.is_expert(agent_idx)]

    """
    'Main' function of the model, runs given amount of iterations.
    """
    def do_iterations (self, iterations):
        new_secrets = np.zeros((self.amount_agents, self.amount_agents))
        no_new_info_count = 0
        for iteration in range (iterations):
            if self.state == State.NO_INFO:
                break
            new_info = False
            for i in range(self.amount_agents):
                for j in range(self.amount_agents):
                    new_secrets[i][j] = self.get_secret_value(i,j)
                    if new_secrets[i][j] != self.old_secrets[i][j]:
                        new_info = True
            if new_info == False:
                no_new_info_count += 1
            else:
                no_new_info_count = 0
            self.old_secrets = deepcopy(new_secrets)
            if no_new_info_count == 10:
                self.state = State.NO_INFO
                break
            if len(self.get_experts()) == self.amount_agents:
                self.state = State.DONE
                break
            try: 
                self.next_call()
            except NoPossibleCallersError:
                # print ("Ended execution after {} iterations, no more calls possible.".format(iteration))
                self.state = State.NO_CALLS
                break

    """
    Method for running multiple trials of a single model setting.
    """
    def do_experiment (self, amount, max_iterations):
        results = list()
        for _ in range (amount):
            # Reset the model
            self.reset_model()

            # Do iterations until the max amount
            self.do_iterations(max_iterations)

            # Obtain the state of the model after the iterations are done
            outcome = self.state
            amt_iterations = self.calls_made

            # Store the final state, and the amount of iterations it took to reach that state in a tuple
            observation = tuple ((outcome.name, amt_iterations))
            results.append(observation)
        return results

    def reset_model (self):
        self.call_log   = list()
        self.calls_made = 0
        self.secrets = list ()
        self.initialize_secrets()
        self.reset_phonebook(self.phonebook_connectivity) # also sets connectivity back to 100%
        self.state              = State.RUN
        self.conv_phonebook     = convert_phonebook_to_tuples(self.phonebook)
        self.graph              = nx.Graph()
        self.graph.add_edges_from(self.conv_phonebook)
        self.summed_knowledge   = list()

    """
    Returns the last call made in the call log.
    """
    def get_last_call(self):
        return (self.call_log[-1])