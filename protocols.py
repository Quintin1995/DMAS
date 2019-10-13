from enum import Enum
import random
import numpy as np

"""
Protocol types for caller / receiver selection.

TYPES:
- ANY   (Call anyone)
- CO    (Call someone new)
"""
class Protocols(Enum):
    ANY         = 1
    CO          = 2
    TOK         = 3
    SPI         = 4
    LNS         = 5

"""
Exception type that is raised when there are no more callers left.
Gives a signal to the model that no more calls can be made, so the model knows to skip.
"""
class NoPossibleCallersError (Exception):
    pass

"""
Function that can choose the callers for a new call based on the type of protocol given.
"""
def choose_callers(model):
    amount_agents = model.amount_agents
    phonebook = model.phonebook
    call_log  = model.call_log
    protocol  = model.protocol
    secrets   = model.secrets
    
    # Find all agents that have other agents in their phonebook
    possible_callers = [agent for agent in range (amount_agents) if len(phonebook[agent]) > 0]

    # Call anyone
    if protocol == Protocols.ANY:
        # The list of possible callers is anyone in the phonebook 
        pass

    # Call once
    elif protocol == Protocols.CO:
        # Pick someone that still has someone in their phonebook that they have not called yet
        phonebook_calls = model.phonebook_calls
        possible_callers =  [agent for agent in possible_callers if list(phonebook_calls[agent]).count(0) > 0]
        
    # Token: Each agent starts with a token, when you call someone you give your token away. Agents can only call if they have a token
    elif protocol == Protocols.TOK:
        # From all agents that have someone in their phonebook, remove all the 
        # agents for which their last call was FROM them
        possible_callers = [agent for agent in possible_callers if last_call_direction(agent, call_log) != CallDirection.FROM]

    # SPIder in the web: Each agent starts with a token, when you call someone you take their token. Agents can only call if they have a token
    elif protocol == Protocols.SPI:
        # From all agents that have someone in their phonebook, remove all the 
        # agents for which their last call was TO them
        possible_callers = [agent for agent in possible_callers if last_call_direction(agent, call_log) != CallDirection.TO]

    # Learn New Secrets: Only call those agents of whom you have not learned their secret
    elif protocol == Protocols.LNS:
        eligible_receivers_lns = list()
        for potential_caller in range(amount_agents):
            eligible_receivers_lns.append(phonebook[potential_caller].copy())
            if potential_caller not in possible_callers:
                continue
            for potential_receiver in phonebook[potential_caller]:
                if model.get_secret_value(potential_caller, potential_receiver) == model.get_agent_secret(potential_receiver):
                    eligible_receivers_lns[potential_caller].remove(potential_receiver)

        possible_callers = [agent for agent in possible_callers if len(eligible_receivers_lns[agent]) > 0]


    if len(possible_callers) < 1:
        raise NoPossibleCallersError

    # Pick a random agent from the eligible agents
    caller = random.choice(possible_callers)

    # Determine who this agent can call
    if protocol == Protocols.CO:
        eligible_receivers = np.where(phonebook_calls[caller, :] == 0.0)[0]
    else:
        eligible_receivers = phonebook[caller]

    if protocol == Protocols.LNS:
        eligible_receivers = eligible_receivers_lns[caller]

    # Self is already not in phonebook, so can safely call first choice
    receiver = random.choice(eligible_receivers)

    # Update the phonebook according to protocol specifications
    update_phonebook(model, caller, receiver, phonebook, protocol)

    return (caller, receiver)
"""
Update the phonebook after caller and receiver of a new call are known.
E.g. if caller cannot call same agent again, remove the receiver from the caller's phonebook.
"""
def update_phonebook(model, caller, receiver, phonebook, protocol):
    # In call any protocol, we remove no one from the phonebooks
    if protocol == Protocols.ANY:
        pass
    
    # In call once, we set the corresponding call to 1 (call made)
    elif protocol == Protocols.CO:
        model.phonebook_calls[caller, receiver] = 1 
        pass

    # No changes need to be made to the phonebook based on an agents call
    # The callable agents are determined based on the models call log.
    elif protocol == Protocols.TOK:
        pass

    # No changes need to be made to the phonebook based on an agents call
    # The callable agents are determined based on the models call log.
    elif protocol == Protocols.SPI:
        pass

"""
An enum that signifies the direction of a call.
NO_CALLS means no calls were found in the call log.
FROM     means that the retrieved call was FROM the agent.
TO       means that the retrieved call was TO the agent.
"""
class CallDirection (Enum):
    NO_CALLS    = 1
    FROM        = 2
    TO          = 3

"""
Returns the direction of the last call involving given agent.
"""
def last_call_direction (agent_idx, call_log):
    # Iterate the call log in reverse order
    for caller, receiver in reversed(call_log):
        # Find first occurence of agent
        if caller == agent_idx:
            return CallDirection.FROM
        
        if receiver == agent_idx:
            return CallDirection.TO
    
    # If we traversed the whole list and did not find the agent, return no calls
    return CallDirection.NO_CALLS