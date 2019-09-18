import tkinter as Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from itertools import permutations
import sys
import matplotlib.pyplot as plt
import networkx as nx


class View():
    def __init__(self, master):
        self.frame = Tk.Frame(master)
        self.fig = Figure( figsize=(7.5, 4), dpi=80 )
        # self.ax0 = self.fig.add_axes( (0.05, .05, .90, .90), facecolor=(.25,.25,.25), frameon=False)
        # self.ax0 = self.fig
        self.frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.sidepanel=SidePanel(master)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas.draw()
 

class SidePanel():
    def __init__(self, root):
        self.sidePanel = Tk.Frame( root )
        self.sidePanel.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.drawGraphBut = Tk.Button(self.sidePanel, text="Draw Graph")
        self.drawGraphBut.pack(side="top",fill=Tk.BOTH)
        self.clearButton = Tk.Button(self.sidePanel, text="Clear")
        self.clearButton.pack(side="top",fill=Tk.BOTH)
  