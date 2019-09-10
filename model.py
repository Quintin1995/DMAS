from protocols import Protocols
from phonebook import PhonebookType
import phonebook
import protocols
import random
from enum import Enum


class Model:
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

    def initialize_secrets (self):
        for agent_idx in range (self.amount_agents):
            self.secrets.append(list())
            for target_idx in range (self.amount_agents): 
                self.secrets[agent_idx].append(list())
                for secret_idx in range (self.amount_secrets):
                    self.secrets[agent_idx][target_idx].append(list())
                    self.secrets[agent_idx][target_idx][secret_idx] = 0
            
            self.secrets[agent_idx][agent_idx][random.choice(self.possible_secrets)] = 999999

    def initialize_extra_info (self):
        self.extra_info = list ([dict () for a in range (self.amount_agents)])
    
    def initialize_phonebook (self):
        # If we can call anyone, add everyone to the phonebook
        self.phonebook = phonebook.generate_phonebook(self.phonebook_type, self.amount_agents)
            
    def next_call (self):
        if self.protocol == Protocols.ANY:
            caller, receiver = protocols.choose_callers_any(self.amount_agents, self.phonebook)
            self.call(caller, receiver)

    def call (self, caller, receiver):
        self.transfer_secrets(caller, receiver)
        self.transfer_secrets(receiver, caller)
        self.call_log.append(tuple((caller, receiver)))

    def get_secret_value (self, agent_idx, target_idx):
        agent_knowledge = self.secrets[agent_idx][target_idx]
        highest_secrets = [idx for idx, s in enumerate(agent_knowledge) if s == max(agent_knowledge)]
        return random.choice(highest_secrets)

    def agent_has_information (self, agent_idx, target_idx):
        agent_knowledge = self.secrets[agent_idx][target_idx]
        if (max(agent_knowledge)) > 0:
            return True
        return False

    def get_agent_secret (self, agent_idx):
        return [idx for idx, s in enumerate(self.secrets[agent_idx][agent_idx]) if s == max(self.secrets[agent_idx][agent_idx])][0]

    def transfer_secrets(self, sender, receiver):
        for target_agent in range(self.amount_agents): # Same amount of secrets as agents
            # Agents know their own secret
            if (target_agent == receiver):
                continue
            if (self.agent_has_information(sender, target_agent)):
                if (random.randint(0, 99) < self.transfer_chance):
                    self.secrets[receiver][target_agent][self.get_secret_value(sender, target_agent)] += 1

    def print_agent_secrets (self):
        for agent_idx in range (self.amount_agents):
            agent_secret = self.get_agent_secret(agent_idx)
            print ("{} has {}".format(agent_idx, agent_secret))

    