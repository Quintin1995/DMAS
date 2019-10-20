#other libraries
from itertools import permutations
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.style as style
import networkx as nx
import numpy as np
import os
from os.path import join
import re
import sys
import time
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
MAX_SECRET      = 2
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

# plot generation
PLOT_FN = "test" # start of the plot filename, will be extended with plot types and image type
IMAGE_TYPE = ".png"

# csv file generation
CSV_FN = "test_output.csv" # file name, will be stored in experiment folder

DEBUG = False


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

        #set button functions
        self.view.exppanel.run_experi_butn.bind("<Button>", self.Btn_perform_experiments)
        self.view.sidepanel.iterBut.bind("<Button>", self.Btn_Do_iterations)
        self.view.sidepanel.iterXBut.bind("<Button>", self.Btn_DoN_iterations)
        self.view.parampanel.resetButton.bind("<Button>", self.reset_model)

        #get values from parampanel
        self.selected_model = self.view.parampanel.selected_model
        self.selected_phonebook = self.view.parampanel.selected_phonebook
        self.selected_behavior = self.view.parampanel.selected_behavior
        self.selected_amount_agents = self.view.parampanel.amount_agents
        self.selected_transfer_chance = self.view.parampanel.transfer_chance
        self.selected_lie_factor = self.view.parampanel.lie_factor
        self.selected_amount_connectivity = self.view.parampanel.amount_connectivity
        self.transfer_pb = self.view.parampanel.pb_mode_var     #pb = probability

        #get values from sidepanel
        self.selected_amount_iterations = self.view.sidepanel.amount_iterations

        #get values from experiment panel
        self.amount_experiments = self.view.exppanel.experi_count
        self.max_amount_iters_experiments = self.view.exppanel.max_allowed_iters


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
            edges_tuples, amount_agents = self.parse_gossip_state(raw_graph_string)

        #in case of a custom graph we do not want to set the amount of agents
        # because the amount of agents is already set in the graph creator, 
        # when the parse_gossip_state has been called.
        if choice != "CUSTOM GRAPH" :
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


    def parse_gossip_state(self, raw_graph_string):
        graph = list()
        try:
            intermediate_string = raw_graph_string.replace(')', ']')
            intermediate_string = intermediate_string.replace('(', '[')
            edges_list, nodes_list = json.loads(intermediate_string)
            for current_node, edge_list in enumerate(edges_list):
                for node in edge_list:
                    graph.append((current_node,node))
        except:
            messagebox.showerror("Parsing Error", "Be sure to give correct syntax.")
            return list((0,0)), 0

        return graph, len(nodes_list)

  
    def draw_graph(self,event):
        #axis is the first plot with the graph in it.
        self.view.fig.clear()
        self.axis = self.view.fig.add_subplot(111)

        #draw the graph itself
        pos_current = nx.circular_layout(self.model.graph)
        
        #we do not need axis for this matplotlib plot, because it is a graph
        self.axis.axis('off')

        #add algend
        self.axis.legend(self.legend_styling, ['Little knowledge', 'More knowledge', 'Expert'], loc='upper left', framealpha=0.33)

        #draw the graph
        nx.draw_networkx(self.model.graph, node_color=self.get_agent_colors(), pos=pos_current, ax=self.axis)

        #redraw
        self.view.fig.canvas.draw()
        self.draw_line(event)


    #create a list of agent names to be shown in the graph
    def get_graph_labels(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        agent_dict = {}
        modules_op = 0
        addition = ""

        for i in range(self.model.amount_agents):
            if i % 26 == 0 and i != 0:
                addition = alphabet[modules_op]
                modules_op += 1
            letter = alphabet[i%26]
            agent_dict[i] = str(addition + letter)
        for elem in agent_dict:
            print(elem)
        return agent_dict


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

    def get_node_size(self, agent_idx):
        return (175 * self.model.get_amount_known_secrets(agent_idx)) + 100

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


    #performs the experiments
    def Btn_perform_experiments (self, event):
        experiment_folder = self.view.exppanel.data_folder_name_textarea.get(1.0, 'end-1c')

        #create folder name based on params
        pr = self.model.protocol.name
        amt_agents = str(self.model.amount_agents)
        amt_exp = str(int(self.amount_experiments.get()))
        tr_ch = str(self.model.transfer_chance)
        lie_fac = str(int(self.model.lie_factor*100))
        param_string = "pr={}_a={}_amt_exp={}_lie_tr={}_lie_fac={}".format(pr, amt_agents, amt_exp, tr_ch, lie_fac )
        
        experiment_folder = experiment_folder + "_" + param_string

        self.create_experiment_folder(experiment_folder)

        amount_experiments = int(self.amount_experiments.get())
        max_iters = int(self.max_amount_iters_experiments.get())
        
        # Start the model, obtain the results
        results = self.do_experiment(amount_experiments, max_iters)

        # Write progress to console NOTE: Maybe remove this later?
        for iteration, result in enumerate(results):
            if DEBUG:
                print("Trial {}: {}".format(iteration, result))

        # Create the graphs
        self.create_plots(results, experiment_folder)

        # Write the results to CSV
        self.write_results_to_csv(results, experiment_folder, CSV_FN)

    def do_experiment (self, amount, max_iterations):
        start_time = time.time()

        progress_bar = self.view.exppanel.progress_bar
        iterations_per_percent = amount / 100.0
        
        results = list()
        for _ in range (amount):
            # Reset the model
            self.model.reset_model()

            # Do iterations until the max amount
            self.model.do_iterations(max_iterations)
            
            # Obtain the state of the model after the iterations are done
            outcome = self.model.state
            amt_iterations = self.model.calls_made

            # Store the final state, and the amount of iterations it took to reach that state in a tuple
            observation = tuple ((outcome.name, amt_iterations))
            results.append(observation)

            # Update progress
            if _ % iterations_per_percent == 0 and _!=0:# your code
                elapsed_time = time.time() - start_time
                progress_bar.config(text="Progress: {}%, {:0.2f}s / 1000 trials".format(_ // iterations_per_percent, elapsed_time * 1000 / _ ))
                progress_bar.update()
            
            progress_bar.config(text="Finished.")
        return results

    """
    Creates and stores the all the figures that is created upon running an experiment.
    """
    def create_plots(self, results, path):        
        self.create_barplot(results, path, PLOT_FN + "_barplot" + IMAGE_TYPE)
        self.create_boxplot(results, path, PLOT_FN + "_boxplot" + IMAGE_TYPE)
        self.create_hist_plot(results, path, PLOT_FN + "_hist" + IMAGE_TYPE)

    """
    Creates the barplot figure that is created upon running an experiment.
    """
    def create_barplot(self, results, path, filename):
        tot_path = os.path.join("data", path, filename)

        categories = ['Success', 'Failed', 'Did not finish']
        values = list()
        values.append(len(list([v for s, v in results if s == 'DONE'])))
        values.append(len(list([v for s, v in results if s == 'NO_CALLS'])))
        values.append(len(list([v for s, v in results if s == 'RUN'])))
        fig, ax = plt.subplots()
        bar = ax.bar(categories, values, alpha=0.4)
        for rect in bar:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width()/2.0, height, '%10.2f%%' % ((int(height)/float(len(results))) * 100.0), ha='center', va='bottom')
        # plt.show()

        plt.title("Experiment results")

        fig.savefig(tot_path)

    """
    Creates the boxplot figure that is created upon running an experiment.
    """
    def create_boxplot(self, results, path, filename):
        tot_path = os.path.join("data", path, filename) 

        plot_data = [numturns for (exit_status, numturns) in results if exit_status == 'DONE'] # only plot succesful runs
        fig, ax = plt.subplots()
        ax.boxplot(plot_data)

        ax.axes.get_xaxis().set_visible(False) # disable x-axis (it would only show a 1)

        ax.set_ylabel("Calls made")
        plt.title("Boxplot of calls made")

        fig.savefig(tot_path)

    def create_hist_plot(self, results, path, filename):
        tot_path = os.path.join("data", path, filename)
        
        plt.figure() # init new figure
        plot_data = [numturns for (exit_status, numturns) in results if exit_status == 'DONE'] # only plot succesful runs

        if DEBUG:
            print (plot_data)
        plot_data_std  = np.std(plot_data)
        # plt.hist(plot_data, bins=25, edgecolor='k', alpha=0.65)
        # plt.ylabel('Occurences')
        # plt.show()

        
        # the histogram of the data
        if len(plot_data) > 0:
            fig, ax = plt.subplots()
            n, bins, patches = ax.hist(plot_data, bins = 15, density=1, edgecolor='k', alpha=0.65)
            plot_data_mean = sum(plot_data) / float(len(plot_data))

            # add median line
            plt.axvline(sum(plot_data)/float(len(plot_data)), color='k', linestyle='dashed', linewidth=1)

            # add a 'best fit' line
            y = ((1 / (np.sqrt(2 * np.pi) * plot_data_std)) *
                np.exp(-0.5 * (1 / plot_data_std * (bins - plot_data_mean))**2))
            ax.plot(bins, y, '--r')

            ax.set_xlabel('# of calls')
            ax.set_ylabel('Probability')

            #format title of historgram
            title_str = "{} agents - Protocol {} - Truth Prob. {}%".format(str(self.model.amount_agents), self.model.protocol.name, str(self.model.transfer_chance) )
            plt.title(title_str)

            ax.legend(["Mean", "Fitted curve"])
            # Tweak spacing to prevent clipping of ylabel
            fig.tight_layout()
            # plt.show()

            fig.savefig(tot_path) # save plot

        

    #creates a new experiment folder in the data directory
    def create_experiment_folder(self, path):
        tot_path = os.path.join("data", path) 

        if not os.path.exists(tot_path):
            os.makedirs(tot_path)


    def write_results_to_csv (self, results, csv_path, filename):
        tot_path = os.path.join("data", csv_path, filename)

        # Collect information
        amount_agents = self.model.amount_agents
        model_type    = self.model.protocol.name
        phonebook     = PhonebookType(self.model.phonebook_type).name
        current_time  = time.strftime("%X_%x")
        # Open the file for writing
        file = open(tot_path, 'w+')

        # Write file header
        file.write("trial;model_type;phonebook;amount_agents;iterations;state;time\n")

        # Process the results
        for iteration, result in enumerate(results):
            state, calls_made = result
            file.write("{};".format(iteration))
            file.write("{};".format(model_type))
            file.write("{};".format(phonebook))
            file.write("{};".format(amount_agents))
            file.write("{};".format(calls_made))
            file.write("{};".format(state))
            file.write("{}\n".format(current_time))
        
        # Close file
        file.close()



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

        # Redraw caller and callee nodes
        last_call = list()
        last_call.append(self.model.get_last_call())
        
        #set expert color
        experts = list(self.model.get_experts())

        #set caller colors
        callers = list(self.model.get_last_call())

        #determine which nodes need resizing and need to be redrawed
        to_update_nodes = []
        for agent in range(self.model.amount_agents):
            if agent not in callers:
                to_update_nodes.append(agent)
            if agent not in experts:
                to_update_nodes.append(agent)

        #draw all other nodes first
        for agent in to_update_nodes:
            nx.draw_networkx_nodes(self.model.graph, nodelist=[agent], node_color=self.get_agent_color(agent), pos=nx.circular_layout(self.model.graph), ax=self.axis, node_size=self.get_node_size(agent))
        
        #draw all expert nodes
        for agent in experts:
            nx.draw_networkx_nodes(self.model.graph, nodelist=[agent], node_color=EXPERT_COLOR, pos=nx.circular_layout(self.model.graph), ax=self.axis, node_size=self.get_node_size(agent))
        
        #draw caller and callee nodes.
        for agent in callers:
            nx.draw_networkx_nodes(self.model.graph, nodelist=[agent], node_color=CALLER_COLOR, pos=nx.circular_layout(self.model.graph), ax=self.axis, node_size=self.get_node_size(agent))
        
        #set Call color, the edge between callers
        nx.draw_networkx_edges(self.model.graph, edgelist=last_call, edge_color=EDGE_COLOR, pos=nx.circular_layout(self.model.graph), ax=self.axis)

        self.view.canvas.draw()
        
        self.line_axis.clear()
        self.set_line_style ()

        #update the axis of the lower plot
        self.line_axis.set_ylim([0, (self.model.amount_agents * self.model.amount_agents)])
        self.line_axis.plot(list(range(self.model.calls_made)),self.model.summed_knowledge)
        self.view.line_canvas.draw()
        self.update_info()