import tkinter as Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from itertools import permutations
import sys
import matplotlib.pyplot as plt
import networkx as nx


class View(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        # self.frame = Tk.Frame(master)
        self.fig = Figure( figsize=(7.5, 4), dpi=80 )
        # self.ax0 = self.fig.add_axes( (0.05, .05, .90, .90), facecolor=(.25,.25,.25), frameon=False)
        # self.ax0 = self.fig
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)
        self.sidepanel=SidePanel(self)

        self.exppanel = ExpPanel(self.sidepanel)
        self.parampanel = ParamPanel(self.sidepanel)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        # self.canvas.draw()

class SidePanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)

        self.drawGraphBut = Tk.Button(self, text="Draw Graph")
        self.drawGraphBut.pack(side="top",fill=Tk.BOTH)
        
        self.clearButton = Tk.Button(self, text="Clear")
        self.clearButton.pack(side="top",fill=Tk.BOTH)

        self.iterBut = Tk.Button(self, text="1 iteration")
        self.iterBut.pack(side="bottom",fill=Tk.BOTH)

        self.resetButton = Tk.Button(self, text="Reset model")
        self.resetButton.pack(side="top",fill=Tk.BOTH)

class ExpPanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=1)

        self.testBut = Tk.Button(self, text="Test")
        self.testBut.pack(side="top",fill=Tk.BOTH)

class ParamPanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=1)

        self.testBut = Tk.Button(self, text="Test")
        self.testBut.pack(side="top",fill=Tk.BOTH)
