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

 

class Controller():
    def __init__(self):
        self.root = Tk.Tk()
        self.model=Model(6, 3, 100, Protocols.ANY, PhonebookType.TWO_WORLDS)
        self.view=View(self.root)
        self.axis = self.view.fig.add_subplot(111)
        self.view.sidepanel.drawGraphBut.bind("<Button>",self.draw_graph)
        self.view.sidepanel.clearButton.bind("<Button>",self.clear)
        self.view.sidepanel.iterBut.bind("<Button>", self.Btn_Do_iterations)
        self.view.sidepanel.resetButton.bind("<Button>", self.reset_model)

    def run(self):
        self.root.title("DMAS - GOSSIP PROTOCOLS")
        self.root.deiconify()
        self.root.mainloop()
         
    def clear(self,event):
        self.view.fig.clear()
        self.view.fig.canvas.draw()
  
    def reset_model(self, event):
        self.model.reset_model()
  
    def draw_graph(self,event):
        self.view.fig.clear()
        self.axis = self.view.fig.add_subplot(111)
        nx.draw_networkx(self.model.graph, pos=nx.circular_layout(self.model.graph), ax=self.axis)
        self.view.fig.canvas.draw()


    def Btn_Do_iterations(self, event):
        self.axis.clear()
        self.model.do_iterations(1)
        self.model.graph.add_edges_from(self.model.call_log)
        
        nx.draw_networkx(self.model.graph, pos=nx.circular_layout(self.model.graph), edge_color='#000000', arrows=True, ax=self.axis)

        # Redraw selected nodes
        if(len(self.model.call_log) > 0):

            nx.draw_networkx_nodes(self.model.graph, nodelist=self.model.get_experts(), node_color='#00FF00', pos=nx.circular_layout(self.model.graph), ax=self.axis)
            nx.draw_networkx_nodes(self.model.graph, nodelist=list(self.model.get_last_call()), node_color='#F0F0F0', pos=nx.circular_layout(self.model.graph), ax=self.axis)
            nx.draw_networkx_edges(self.model.graph, edgelist=list().append(self.model.get_last_call()), edge_color='#0000FF', pos=nx.circular_layout(self.model.graph), ax=self.axis)

        print("doing iteration")
        nx.draw_networkx(self.model.graph, pos=nx.circular_layout(self.model.graph), ax=self.axis)
        self.view.canvas.draw()
        print("iets")
        
