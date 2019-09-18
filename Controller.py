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
        self.model=Model(20, 3, 100, Protocols.ANY, PhonebookType.ALL)
        self.view=View(self.root)
        # self.axis = self.view.fig.add_subplot(111)
        self.view.sidepanel.drawGraphBut.bind("<Button>",self.draw_graph)
        self.view.sidepanel.clearButton.bind("<Button>",self.clear)
  
    def run(self):
        self.root.title("DMAS - GOSSIP PROTOCOLS")
        self.root.deiconify()
        self.root.mainloop()
         
    def clear(self,event):
        self.view.fig.clear()
        self.view.fig.canvas.draw()
  
    def draw_graph(self,event):
        self.view.fig.clear()
        # self.model.calculate()
        self.axis = self.view.fig.add_subplot(111)
        
        nx.draw_networkx(self.model.graph, pos=nx.circular_layout(self.model.graph), ax=self.axis)
        # nx.draw_networkx(self.model.graph, pos=nx.circular_layout(self.model.graph), ax=self.axis)
        
        # self.view.fig = nx.draw(self.model.graph, with_labels=True, font_weight='bold', ax=self.axis)
        # self.view.ax0 = add_axes( (0.05, .05, .90, .90), facecolor=(.25,.25,.25), frameon=False)
        # nx.draw(self.model.graph, with_labels=True, font_weight='bold')
        # self.view.ax0.contourf(self.model.res["x"],self.model.res["y"],self.model.res["z"])
        self.view.fig.canvas.draw()
        # nx.draw_networkx(self.model.graph, pos=nx.circular_layout(self.model.graph), ax=self.axis)
        # plt.show()
        self.model.temp_edges = [(7,9),(3,8),(9,3)]
