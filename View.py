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
        self.line_fig = Figure( figsize=(7.5, 4), dpi=80 )
        # self.ax0 = self.fig.add_axes( (0.05, .05, .90, .90), facecolor=(.25,.25,.25), frameon=False)
        # self.ax0 = self.fig
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)
        self.sidepanel=SidePanel(self)

        self.leftpanel=LeftPanel(self)

        self.exppanel = ExpPanel(self.sidepanel)
        self.parampanel = ParamPanel(self.sidepanel)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        self.line_canvas = FigureCanvasTkAgg(self.line_fig, master=self)
        self.line_canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        # self.canvas.draw()

class LeftPanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)

        self.group_info = Tk.LabelFrame(self, text="Session information", padx=5, pady=5)
        self.group_info.pack(side="top", fill=Tk.BOTH)
        
        self.model_state_lbl = Tk.Label(self.group_info, text="Protocol running", fg="blue")
        self.model_state_lbl.pack(side="top", fill=Tk.BOTH)

        self.model_iter_lbl = Tk.Label(self.group_info, text="Calls made: 0")
        self.model_iter_lbl.pack(side="top", fill=Tk.BOTH)


class SidePanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)
        
        # self.drawGraphBut = Tk.Button(self, text="Draw Graph")
        # self.drawGraphBut.pack(side="top",fill=Tk.BOTH)
        
        # self.clearButton = Tk.Button(self, text="Clear")
        # self.clearButton.pack(side="top",fill=Tk.BOTH)

        self.group_run = Tk.LabelFrame(self, text="Run model", padx=5, pady=5)
        self.group_run.pack(side="bottom", fill=Tk.BOTH)

        self.iterBut = Tk.Button(self.group_run, text="1 iteration")
        self.iterBut.pack(side="top",fill=Tk.BOTH)
        
        Tk.Label(self.group_run, text="Amount iterations").pack(side="top", fill=Tk.BOTH)
        self.amount_iterations = Tk.Spinbox(self.group_run, from_=1, to=10000)
        self.amount_iterations.pack(side="top", fill=Tk.BOTH)

        self.iterXBut = Tk.Button(self.group_run, text="Do N iterations")
        self.iterXBut.pack(side="top",fill=Tk.BOTH)


class ExpPanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=1)

        # self.testBut = Tk.Button(self, text="Test")
        # self.testBut.pack(side="top",fill=Tk.BOTH)

class ParamPanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=1)

        self.group_model = Tk.LabelFrame(self, text="Model parameters", padx=5, pady=5)
        self.group_model.pack(side="top", fill=Tk.BOTH)

        AVAILABLE_MODELS = ["ANY", "CO", "LNS", "SPI", "TOK"]
        self.selected_model = Tk.StringVar(self)
        self.selected_model.set("ANY") # default value

        Tk.Label(self.group_model, text="Protocol").pack(side="top", fill=Tk.BOTH)
        self.model_selector = Tk.OptionMenu(self.group_model, self.selected_model, *AVAILABLE_MODELS)
        self.model_selector.pack(side="top", fill=Tk.BOTH)


        Tk.Label(self.group_model, text="Amount agents").pack(side="top", fill=Tk.BOTH)
        self.amount_agents = Tk.Spinbox(self.group_model, from_=3, to=100)
        self.amount_agents.pack(side="top", fill=Tk.BOTH)

        AVAILABLE_PHONEBOOKS = ["ALL", "TWO WORLDS"]
        self.selected_phonebook = Tk.StringVar(self)
        self.selected_phonebook.set("ALL") # default value

        Tk.Label(self.group_model, text="Phonebook").pack(side="top", fill=Tk.BOTH)
        self.phonebook_selector = Tk.OptionMenu(self.group_model, self.selected_phonebook, *AVAILABLE_PHONEBOOKS)
        self.phonebook_selector.pack(side="top", fill=Tk.BOTH)

        self.resetButton = Tk.Button(self.group_model, text="Set model")
        self.resetButton.pack(side="top",fill=Tk.BOTH)
