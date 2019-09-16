from tkinter import *
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class UserInterface:

    def __init__ (self, model):
        self.model = model
        self.network = GossipGraph(self.model)

        # Main window
        self.window = Tk()
        self.initialize_window()
        
        self.stat_amount_calls = Label(self.window, text="0")
        self.stat_amount_calls.grid(column=0, row=0)
        
        self.sb_iterations = Spinbox(self.window, from_=1, to=100, width=5)
        self.sb_iterations.grid(column=2,row=2)

        self.lb_last_calls = Listbox(self.window)
        self.lb_last_calls.grid(column=3,row=3)

        self.initialize_network_canvas()

        btn = Button(self.window, text="Go!", command=self.btn_do_iterations)
        btn.grid(column=1, row=0)

    def initialize_window (self):
        self.window.title("Gossip Protocol Dashboard") 
        self.window.geometry('840x420')

    def initialize_network_canvas(self):
        figure = self.network.get_figure()
        self.canvas = FigureCanvasTkAgg(figure, master=self.window)
        self.canvas.get_tk_widget().grid(column=4,row=4)
        
    def btn_do_iterations (self):
        iterations = int(self.sb_iterations.get())
        self.model.do_iterations(iterations)
        self.update_view()

    def update_view (self):
        self.update_stats ()
        self.update_last_calls ()
        self.update_network ()
        self.canvas.draw ()

    def update_network (self):
        self.network.update_graph()

    def update_stats (self):
        self.stat_amount_calls.configure(text=str(len(self.model.call_log)))

    def update_last_calls (self):
        # empty list
        self.lb_last_calls.delete(0, END)
        last_calls = self.model.call_log[-100:]
        for call in last_calls:
            formatted_call = "Agent {} => Agent {}".format(*call)
            self.lb_last_calls.insert(0, formatted_call)

    def show (self):
        self.window.mainloop()



class GossipGraph:
    def __init__(self, model):
        self.model = model
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(self.model.amount_agents))

    def update_graph(self):
        self.axis.clear()
        self.graph.add_edges_from(self.model.call_log)
        nx.draw_networkx(self.graph, pos=nx.circular_layout(self.graph), arrows=True, ax=self.axis)

    def get_figure (self):
        figure = plt.figure(figsize=(5,4))
        self.axis = figure.add_subplot(111)
        nx.draw_networkx(self.graph, pos=nx.circular_layout(self.graph), ax=self.axis)
        plt.axis('off')
        return figure