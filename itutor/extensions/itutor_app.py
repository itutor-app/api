from scipy import stats
from igraph import Graph
from igraph import plot, save
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import random
import threading
import os

class ITutorClassificator(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.list_inter = []
        self.lista_inter_adj = []
        self.teoric_sample = []

    def GenerateGraph(self, random_inter=False):
        interactions = [(random.randint(1, 50), random.randint(1, 50)) for x in
                        range(200)] if random_inter else self.list_inter
        g = Graph(interactions, directed=True)
        self.lista_inter_adj = []
        for x in g.get_adjacency():
            for y in x:
                self.lista_inter_adj.append(y)
        g.layout("kk")

        plot(g, "./itutor/static/grafos/Graph.png")

    def CreatePlotComparison(self):
        self.lista_inter_adj.sort()
        interacion_norm = stats.norm.cdf(self.lista_inter_adj, loc=0, scale=1)

        self.teoric_sample = np.linspace(min(self.lista_inter_adj), max(self.lista_inter_adj))
        teoric_norm = stats.norm.cdf(self.teoric_sample, loc=0, scale=1)
        gs = gridspec.GridSpec(4, 4)
        plt.subplot(gs[:2, :2])
        plt.title("Interaction Curve")
        plt.plot(self.lista_inter_adj, interacion_norm, '-b')
        plt.subplot(gs[:2, 2:])
        plt.title("Teoric Curve")
        plt.plot(self.teoric_sample, teoric_norm, '-g')
        plt.subplot(gs[2:4, 1:3])
        plt.plot(self.lista_inter_adj, interacion_norm, '-b')
        plt.plot(self.teoric_sample, teoric_norm, '-g')
        plt.tight_layout()
        plt.savefig("static/curvas/Curves-Comparison")

    def run(self):
        self.GenerateGraph(True)
        self.CreatePlotComparison()

def init_app(app):
  app.itutor = ITutorClassificator()