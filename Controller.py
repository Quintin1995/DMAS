#other libraries
from itertools import permutations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.style as style
import networkx as nx
import numpy as np
import sys
import tkinter as Tk
from tkinter import messagebox

#our libraries
from Model import *
from protocols import *
from phonebook import *
from View import View, SidePanel

style.use('seaborn-bright')

## temp experiment parameters
AMOUNT_AGENTS   = 10
MAX_SECRET      = 3
TRANSFER_CHANCE = 100
LIE_FACTOR      = 25
BEHAVIOR        = Behavior.LIE

## colors for the graph
EXPERT_COLOR = '#0000FF'
CALLER_COLOR = "cyan" #'#F0F0F0'
EDGE_COLOR   = '#00FFFF'

# PLOT TITLES
LINE_PLOT_TITLE = "Sum of agent knowledge progression"
LINE_PLOT_YLAB  = "Sum of known agent secrets"
LINE_PLOT_XLAB  = "Amount of calls made"

class Controller():
    def __init__(self):
        self.root = Tk.Tk()
        self.model=Model(AMOUNT_AGENTS, MAX_SECRET, TRANSFER_CHANCE, Protocols.ANY, PhonebookType.ALL, LIE_FACTOR, BEHAVIOR)
        self.view=View(self.root)
        self.axis = self.view.fig.add_subplot(111)
        self.axis.legend(loc='center')
        self.axis.axis('off')
        #set second plot axis in the main plot
        self.line_axis = self.view.line_fig.add_subplot(111)

        #legend styling of the graph plot
        self.legend_styling = [Line2D([0], [0], color='w', markerfacecolor='#FF0000', marker='o', markersize=10, lw=4),
                        Line2D([0], [0], color='w', markerfacecolor='#00FF00', marker='o', markersize=10, lw=4),
                        Line2D([0], [0], color='w', markerfacecolor='#0000FF', marker='o', markersize=10, lw=4)]

        self.draw_graph(0)
        self.draw_line(0)

        self.view.sidepanel.iterBut.bind("<Button>", self.Btn_Do_iterations)
        self.view.sidepanel.iterXBut.bind("<Button>", self.Btn_DoN_iterations)
        self.view.parampanel.resetButton.bind("<Button>", self.reset_model)
        self.selected_model = self.view.parampanel.selected_model
        self.selected_phonebook = self.view.parampanel.selected_phonebook
        self.selected_behavior = self.view.parampanel.selected_behavior
        self.selected_amount_agents = self.view.parampanel.amount_agents
        self.selected_transfer_chance = self.view.parampanel.transfer_chance
        self.selected_lie_factor = self.view.parampanel.lie_factor
        self.selected_amount_iterations = self.view.sidepanel.amount_iterations
        self.selected_amount_connectivity = self.view.parampanel.amount_connectivity
        self.transfer_pb = self.view.parampanel.pb_mode_var

    def run(self):
        self.root.title("DMAS - GOSSIP PROTOCOLS")
        self.root.deiconify()
        self.root.mainloop()
         
    def clear(self,event):
        self.view.fig.clear()
        self.view.fig.canvas.draw()
        self.view.line_fig.clear()
        self.view.line_fig.canvas.draw()
  
    def reset_model(self, event):
        self.view.leftpanel.model_call_log_textarea.delete('1.0', Tk.END)
        choice = self.selected_model.get()
        protocol = Protocols.ANY
        if choice == 'ANY':
            protocol = Protocols.ANY
        elif choice == "LNS":
            protocol = Protocols.LNS
        elif choice == "SPI":
            protocol = Protocols.SPI
        elif choice == "TOK":
            protocol = Protocols.TOK
        elif choice == "CO":
            protocol = Protocols.CO
            
        choice = self.selected_phonebook.get()
        phonebook = PhonebookType.ALL
        if choice == 'ALL':
            phonebook = PhonebookType.ALL
        elif choice == "TWO WORLDS":
            phonebook = PhonebookType.TWO_WORLDS
        elif choice == "RANDOM GRAPH":
            phonebook = PhonebookType.RAND_GRAPH
        elif choice == "CUSTOM GRAPH":
            phonebook = PhonebookType.CUSTOM_GRAPH
            raw_graph_string = self.view.parampanel.retrieve_input_graph()
            edges_tuples = self.get_edges_from_raw_graph_string(raw_graph_string)

        amount_agents = int(self.selected_amount_agents.get())
        transfer_chance = int(self.selected_transfer_chance.get())
        lie_factor = float(self.selected_lie_factor.get())

        choice = self.selected_behavior.get()
        behavior = Behavior.LIE
        if choice == 'LIE':
            behavior = Behavior.LIE
        elif choice == 'MISTAKE':
            behavior = Behavior.MISTAKE

        transfer_pb = False
        if self.transfer_pb.get():
            transfer_pb = True

        connectivity = int(self.selected_amount_connectivity.get())
        self.model=Model(amount_agents, MAX_SECRET, transfer_chance, protocol, phonebook, lie_factor, behavior, connectivity, transfer_pb)

        #must happen after model is initialized
        if(phonebook == PhonebookType.CUSTOM_GRAPH):
            for a,b in edges_tuples:
                self.model.phonebook[a].append(b)
                self.model.phonebook[b].append(a)
            #also update the graph in the model with the newly created graph
            self.model.graph.clear()
            #add all defined nodes to the graph
            self.model.graph.add_nodes_from(list(range(self.model.amount_agents)))
            self.model.graph.add_edges_from(edges_tuples)

        #reset the call idx
        self.callIdx = 0
        
        #update the actual graph, when the reset button is pressed.
        self.draw_graph(event)
        self.update_info()

    
    #takes in a raw unformated string from the GUI, and will make a list of tuples,
    #these tuples are edges for the graph to be created
    def get_edges_from_raw_graph_string(self, raw_graph_string):
        tuple_list = list()
        lazy_tuples = raw_graph_string.split('\n')      #lazy, as in there are no parenthesis required for this tuple.
        for lazy_tuple in lazy_tuples:
            lazy_tuple = lazy_tuple.replace('(', '')
            lazy_tuple = lazy_tuple.replace(')', '')
            nodes_of_edge = lazy_tuple.split(',')
            a = int(nodes_of_edge[0])
            b = int(nodes_of_edge[1])
            if( (a > self.model.amount_agents-1) or (b > self.model.amount_agents-1) ):
                messagebox.showerror("Index Error", "Trying to reference an Agent that does not exist")
                return list()
            tuple_list.append((a, b))
        return tuple_list
  
    def draw_graph(self,event):
        #axis is the first plot with the graph in it.
        self.view.fig.clear()
        self.axis = self.view.fig.add_subplot(111)
        nx.draw_networkx(self.model.graph, node_color=self.get_agent_colors(), pos=nx.circular_layout(self.model.graph), ax=self.axis)
        self.axis.axis('off')
        self.axis.legend(self.legend_styling, ['Little knowledge', 'More knowledge', 'Expert'], loc='upper left', framealpha=0.33)

        self.view.fig.canvas.draw()
        self.draw_line(event)

    def draw_line(self,event):
        self.view.line_fig.clear()
        self.line_axis = self.view.line_fig.add_subplot(111)
        self.line_axis.set_ylim([0, (self.model.amount_agents * self.model.amount_agents)])
        # print (self.model.summed_knowledge)
        self.set_line_style()
        
        self.view.line_fig.canvas.draw()

    def set_line_style(self):
        self.line_axis.set_title(LINE_PLOT_TITLE)
        self.line_axis.set_ylabel(LINE_PLOT_YLAB)
        self.line_axis.set_xlabel(LINE_PLOT_XLAB)

    def Btn_Do_iterations(self, event):
        self.do_iterations(1)

    def update_model_state (self):
        lbl = self.view.leftpanel.model_state_lbl
        if self.model.state == State.RUN:
            val = "State: running"
            col = "blue"
        elif self.model.state == State.NO_CALLS:
            val = "State: failed"
            col = "red"
        else:
            val = "State: success"
            col = "green"
        lbl.config(fg=col, text=val)
        self.view.leftpanel.update()

    def update_iterations (self):
        lbl = self.view.leftpanel.model_iter_lbl
        val = self.model.calls_made
        lbl.config(text="Calls made: " + str(val))
        self.view.leftpanel.update()

    def update_info (self):
        self.update_model_state()
        self.update_iterations()

    def Btn_DoN_iterations(self, event):
        amount = int(self.selected_amount_iterations.get())
        self.do_iterations(amount)
        
    def do_iterations (self, amount):
        #clear the axes, turn them of and add a legend
        self.axis.clear()
        self.axis.axis('off')
        self.axis.legend(self.legend_styling, ['Little knowledge', 'More knowledge', 'Expert'], loc='upper left', framealpha=0.33)

        #perform main loop
        self.model.do_iterations(amount)

        #update textare of left panel with last element of call log
        self.view.leftpanel.model_call_log_textarea.insert(Tk.END, self.get_formated_call(amount) )

        #update the visualization of the graph with calls
        self.model.graph.add_edges_from(self.model.call_log)
        
        #set colors of the agents according to their fraction of total possible knowlegde/secrets
        agent_colors = self.get_agent_colors()
        nx.draw_networkx(self.model.graph, pos=nx.circular_layout(self.model.graph), edge_color='#000000', node_color=agent_colors, arrows=True, ax=self.axis)

        # Redraw selected nodes
        last_call = list()
        last_call.append(self.model.get_last_call())
        
        #set expert color
        nx.draw_networkx_nodes(self.model.graph, nodelist=self.model.get_experts(), node_color=EXPERT_COLOR, pos=nx.circular_layout(self.model.graph), ax=self.axis)
        
        #set caller colors
        nx.draw_networkx_nodes(self.model.graph, nodelist=list(self.model.get_last_call()), node_color=CALLER_COLOR, pos=nx.circular_layout(self.model.graph), ax=self.axis)
        
        #set Call color, the edge between callers
        nx.draw_networkx_edges(self.model.graph, edgelist=last_call, edge_color=EDGE_COLOR, pos=nx.circular_layout(self.model.graph), ax=self.axis)

        self.view.canvas.draw()
        
        self.line_axis.clear()
        self.set_line_style ()

        #update the axis
        self.line_axis.set_ylim([0, (self.model.amount_agents * self.model.amount_agents)])
        self.line_axis.plot(list(range(self.model.calls_made)),self.model.summed_knowledge)
        self.view.line_canvas.draw()
        self.update_info()


    def get_formated_call(self, amount):
        self.view.leftpanel.model_call_log_textarea.delete('1.0', Tk.END)
        formated_call = ""
        call_log_list = list(enumerate(self.model.call_log))
        for idx, call in reversed(call_log_list):
            a,b = call
            formated_call += "Call " + str(idx+1) + ": Agent " + str(a) + " calls Agent " + str(b) + "\n"

        return formated_call            


    def get_agent_color (self, agent_idx):
        known_secrets  = self.model.get_amount_known_secrets(agent_idx)
        fraction_known = known_secrets / float(self.model.amount_agents)

        return [1.0 - fraction_known, fraction_known, 0.0]
        
    def get_agent_colors (self):
        return [self.get_agent_color(agent_idx) for agent_idx in range(self.model.amount_agents)]