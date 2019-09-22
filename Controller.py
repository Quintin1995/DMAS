from Model import *
import tkinter as Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from itertools import permutations
import sys
import matplotlib.pyplot as plt
from protocols import *
from phonebook import *
import networkx as nx
from View import View, SidePanel
import matplotlib.style as style
style.use('seaborn-bright')

## temp experiment parameters
AMOUNT_AGENTS   = 10
MAX_SECRET      = 3
TRANSFER_CHANCE = 100

## colors for the graph
EXPERT_COLOR = '#00FF00'
CALLER_COLOR = '#F0F0F0'
EDGE_COLOR   = '#00FFFF'

# PLOT TITLES
LINE_PLOT_TITLE = "Sum of agent knowledge progression"
LINE_PLOT_YLAB  = "Sum of known agent secrets"
LINE_PLOT_XLAB  = "Amount of calls made"

class Controller():
    def __init__(self):
        self.root = Tk.Tk()
        self.model=Model(AMOUNT_AGENTS, MAX_SECRET, TRANSFER_CHANCE, Protocols.ANY, PhonebookType.TWO_WORLDS)
        self.view=View(self.root)
        self.axis = self.view.fig.add_subplot(111)
        self.line_axis = self.view.line_fig.add_subplot(111)
        self.view.sidepanel.drawGraphBut.bind("<Button>",self.draw_graph)
        self.view.sidepanel.clearButton.bind("<Button>",self.clear)
        self.view.sidepanel.iterBut.bind("<Button>", self.Btn_Do_iterations)
        self.view.parampanel.resetButton.bind("<Button>", self.reset_model)
        self.selected_model = self.view.parampanel.selected_model
        self.selected_phonebook = self.view.parampanel.selected_phonebook
        self.selected_amount_agents = self.view.parampanel.amount_agents

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

        amount_agents = int(self.selected_amount_agents.get())

        self.model=Model(amount_agents, MAX_SECRET, TRANSFER_CHANCE, protocol, phonebook)
        self.draw_graph(event)
  
    def draw_graph(self,event):
        self.view.fig.clear()
        self.axis = self.view.fig.add_subplot(111)
        nx.draw_networkx(self.model.graph, pos=nx.circular_layout(self.model.graph), ax=self.axis)
        self.view.fig.canvas.draw()
        self.draw_line(event)

    def draw_line(self,event):
        self.view.line_fig.clear()
        self.line_axis = self.view.line_fig.add_subplot(111)
        print (self.model.summed_knowledge)
        self.set_line_style()
        
        self.view.line_fig.canvas.draw()

    def set_line_style(self):
        self.line_axis.set_title(LINE_PLOT_TITLE)
        self.line_axis.set_ylabel(LINE_PLOT_YLAB)
        self.line_axis.set_xlabel(LINE_PLOT_XLAB)

    def Btn_Do_iterations(self, event):
        self.axis.clear()
        self.model.do_iterations(1)
        self.model.graph.add_edges_from(self.model.call_log)
        
        nx.draw_networkx(self.model.graph, pos=nx.circular_layout(self.model.graph), edge_color='#000000', arrows=True, ax=self.axis)

        print(self.model.call_log)

        # Redraw selected nodes
        last_call = list()
        last_call.append(self.model.get_last_call())
        #list().append(self.model.get_last_call())
        nx.draw_networkx_nodes(self.model.graph, nodelist=self.model.get_experts(), node_color=EXPERT_COLOR, pos=nx.circular_layout(self.model.graph), ax=self.axis)
        nx.draw_networkx_nodes(self.model.graph, nodelist=list(self.model.get_last_call()), node_color=CALLER_COLOR, pos=nx.circular_layout(self.model.graph), ax=self.axis)
        nx.draw_networkx_edges(self.model.graph, edgelist=last_call, edge_color=EDGE_COLOR, pos=nx.circular_layout(self.model.graph), ax=self.axis)

        self.view.canvas.draw()
        
        self.line_axis.clear()
        self.set_line_style ()
        self.line_axis.plot(list(range(self.model.calls_made)),self.model.summed_knowledge)
        self.view.line_canvas.draw()