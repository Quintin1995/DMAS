
from itertools import permutations
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.style as style
import networkx as nx
import numpy as np
import re
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

model=Model(AMOUNT_AGENTS, MAX_SECRET, TRANSFER_CHANCE, Protocols.ANY, PhonebookType.ALL, LIE_FACTOR, BEHAVIOR)

results = model.do_experiment(10, 9999)

for iteration, result in enumerate(results):
    print("Trial {}: {}".format(iteration, result))