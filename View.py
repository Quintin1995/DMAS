import tkinter as Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from itertools import permutations
import sys
import matplotlib.pyplot as plt
from tkinter import scrolledtext
import networkx as nx


class View(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        
        self.fig = Figure( figsize=(15, 6), dpi=80 )
        self.line_fig = Figure( figsize=(15, 6), dpi=80 )

        self.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)
        self.sidepanel=SidePanel(self)

        self.leftpanel=LeftPanel(self)

        self.exppanel = ExpPanel(self.sidepanel)
        self.parampanel = ParamPanel(self.sidepanel)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        self.line_canvas = FigureCanvasTkAgg(self.line_fig, master=self)
        self.line_canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


class LeftPanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)

        #Frame for fields
        self.group_info = Tk.LabelFrame(self, text="Session information", padx=5, pady=5)
        self.group_info.pack(side="top", fill=Tk.BOTH)
        
        #Protocol status text
        self.model_state_lbl = Tk.Label(self.group_info, text="Protocol running", fg="blue")
        self.model_state_lbl.pack(side="top", fill=Tk.BOTH)

        #amount calls made txt
        self.model_iter_lbl = Tk.Label(self.group_info, text="Calls made: 0")
        self.model_iter_lbl.pack(side="top", fill=Tk.BOTH)

        #call log
        self.model_call_log_lbl = Tk.Label(self.group_info, text="Call Log", fg="green")
        self.model_call_log_lbl.pack(side="top", fill=Tk.BOTH)
        self.model_call_log_textarea = Tk.Text(self.group_info, height=20, width=35)
        self.model_call_log_textarea.pack(side="top", fill=Tk.BOTH)



class SidePanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)

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
        self.amount_agents.delete(0,"end")
        self.amount_agents.insert(0,"10")
        self.amount_agents.pack(side="top", fill=Tk.BOTH)

        AVAILABLE_PHONEBOOKS = ["LIE", "MISTAKE"]
        self.selected_behavior = Tk.StringVar(self)
        self.selected_behavior.set("LIE") # default value

        Tk.Label(self.group_model, text="Behavior").pack(side="top", fill=Tk.BOTH)
        self.behavior_selector = Tk.OptionMenu(self.group_model, self.selected_behavior, *AVAILABLE_PHONEBOOKS)
        self.behavior_selector.pack(side="top", fill=Tk.BOTH)

        Tk.Label(self.group_model, text="Chance of telling the truth in percentage").pack(side="top", fill=Tk.BOTH)
        self.transfer_chance = Tk.Spinbox(self.group_model, from_=1, to=100)
        self.transfer_chance.delete(0,"end")
        self.transfer_chance.insert(0,"100")
        self.transfer_chance.pack(side="top", fill=Tk.BOTH)

        Tk.Label(self.group_model, text="Strength of a lie in percentage").pack(side="top", fill=Tk.BOTH)
        self.lie_factor = Tk.Spinbox(self.group_model, from_=0, to=1)
        self.lie_factor.delete(0,"end")
        self.lie_factor.insert(0,"25")
        self.lie_factor.pack(side="top", fill=Tk.BOTH)

        AVAILABLE_PHONEBOOKS = ["ALL", "TWO WORLDS", "RANDOM GRAPH", "CUSTOM GRAPH"]
        self.selected_phonebook = Tk.StringVar(self)
        self.selected_phonebook.set("ALL") # default value

        Tk.Label(self.group_model, text="Phonebook").pack(side="top", fill=Tk.BOTH)
        self.phonebook_selector = Tk.OptionMenu(self.group_model, self.selected_phonebook, *AVAILABLE_PHONEBOOKS)
        self.phonebook_selector.pack(side="top", fill=Tk.BOTH)

        Tk.Label(self.group_model, text="Connectivity of the Random Graph in percentage").pack(side="top", fill=Tk.BOTH)
        self.amount_connectivity = Tk.Spinbox(self.group_model, from_=1, to=100)
        self.amount_connectivity.delete(0,"end")
        self.amount_connectivity.insert(0,"100")
        self.amount_connectivity.pack(side="top", fill=Tk.BOTH)

        #graph creator panel
        info_string = "Graph creator, on tuples (without paranthesis)\n Example:\n 0,1\n1,0\n2,0" + "\nSet phonebook to CUSTOM GRAPH" + "\nClick on set model"
        self.model_param_pnl_graph_creator_lbl = Tk.Label(self.group_model, text=info_string, fg="red")
        self.model_param_pnl_graph_creator_lbl.pack(side="top", fill=Tk.BOTH)
        self.model_param_pnl_graph_creator_textarea = Tk.Text(self.group_model, height=10, width=20)
        self.model_param_pnl_graph_creator_textarea.pack(side="top", fill=Tk.BOTH)

        self.resetButton = Tk.Button(self.group_model, text="Set model")
        self.resetButton.pack(side="top",fill=Tk.BOTH)
        

    def retrieve_input_graph(self):
        return self.model_param_pnl_graph_creator_textarea.get("1.0",'end-1c')