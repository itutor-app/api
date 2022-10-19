from scipy import stats
import igraph as ig
from igraph import Graph
from igraph import plot, save
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import random
import threading

class ITutorClassificator(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.list_inter = []
        self.list_names = []
        self.lista_inter_adj = []
        self.teoric_sample = []

    def GenerateGraph(self):

        interactions = [(random.randint(1, 50), random.randint(1, 50)) for x in
                        range(50)] if self.list_inter == [] else self.list_inter

        g = Graph(interactions, directed=True)

        if self.list_names:
            g.vs["name"] = self.list_names
            g.vs["label"] = self.list_names

        self.lista_inter_adj = []

        for x in g.get_adjacency():
            for y in x:
                self.lista_inter_adj.append(y)

        fig, ax = plt.subplots()

        plot(
            g,
            target=ax,
            layout=g.layout("circular"),
            vertex_label=g.vs['name'] if self.list_names != [] else None,
            vertex_color="lightblue",
            vertex_shape="rectangle",
            vertex_size=0.3
        )
        plt.savefig("static/grafos/Graph.png")


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

    def FormatData(self, data):
        list_tuple = {}
        for d in data:
            if d["starter"]["registration"] not in list_tuple:
                list_tuple[d["starter"]["registration"]] = {"name": d["starter"]["name"], "interactions": []}
            list_tuple[d["starter"]["registration"]]["interactions"].append((d["finisher"]["registration"], d["finisher"]["name"]))
        keys = list(list_tuple.keys())
        for i in list_tuple:
            for interaction in list_tuple[i]["interactions"]:
                self.list_inter.append((keys.index(i), keys.index(interaction[0])))
        self.list_names = [list_tuple[x]["name"] for x in list_tuple]

    def Reset(self):
        self.list_inter = []
        self.list_names = []
        self.lista_inter_adj = []
        self.teoric_sample = []

    def run(self):
        self.GenerateGraph()
        self.CreatePlotComparison()

def init_app(app):
  app.itutor = ITutorClassificator()