
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

model=Model(AMOUNT_AGENTS, MAX_SECRET, TRANSFER_CHANCE, Protocols.CO, PhonebookType.TWO_WORLDS, LIE_FACTOR, BEHAVIOR)

results = model.do_experiment(100, 9999)

for iteration, result in enumerate(results):
    print("Trial {}: {}".format(iteration, result))

print (results)

plot_data = [v for (s, v) in results if s == 'DONE']

print (plot_data)
plot_data_std  = np.std(plot_data)
# plt.hist(plot_data, bins=25, edgecolor='k', alpha=0.65)
# plt.ylabel('Occurences')
# plt.axvline(sum(plot_data)/float(len(plot_data)), color='k', linestyle='dashed', linewidth=1)
# plt.show()

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(plot_data, 25, density=1, edgecolor='k', alpha=0.65)

# add a 'best fit' line
if (len(plot_data) > 0):
    plot_data_mean = sum(plot_data) / float(len(plot_data))
    y = ((1 / (np.sqrt(2 * np.pi) * plot_data_std)) *
        np.exp(-0.5 * (1 / plot_data_std * (bins - plot_data_mean))**2))
    ax.plot(bins, y, '--r')
ax.set_xlabel('Smarts')
# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()

categories = ['Success', 'Failed', 'Did not finish']
values = list()
values.append(len(list([v for s, v in results if s == 'DONE'])))
values.append(len(list([v for s, v in results if s == 'NO_CALLS'])))
values.append(len(list([v for s, v in results if s == 'RUN'])))
fig, ax = plt.subplots()
bar = ax.bar(categories, values, alpha=0.4)
for rect in bar:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height, '%10.2f%%' % (int(height)/float(len(results))), ha='center', va='bottom')
plt.show()

fig, ax = plt.subplots()
ax.boxplot(plot_data)
plt.show()
