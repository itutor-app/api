from igraph import Graph
import networkx as nx
from igraph import plot
import matplotlib.pyplot as plt
import re
import random
from tabulate import tabulate
import subprocess
import sys
import os

class ITutorClassificator():

    def __init__(self, static_path):
        self.list_inter = []
        self.list_inter_names = []
        self.list_names = []
        self.lista_inter_adj = []
        self.teoric_sample = []
        self.random_percent = 0.9345
        self.random_name = ""
        self.STATIC_PATH = static_path
        self.PATH_GRAPH_IMAGE = static_path + "/{name}-graph.png"
        self.PATH_HIST_IMAGE = static_path + "/{name}-histogram"
        self.match_percent = r"(Statistics:\s)(.*)"

    def GenerateGraph(self):

        interactions = [(random.randint(1, 50), random.randint(1, 50)) for x in
                        range(50)] if self.list_inter == [] else self.list_inter

        g = Graph(interactions, directed=True)
        print("NAMES: ", self.list_inter_names)
        #self.CreateGraphNetworkx()
        if self.list_names:
            g.vs["name"] = self.list_names
            g.vs["label"] = self.list_names

        self.lista_inter_adj = []

        for x in g.get_adjacency().data:
            for y in x:
                self.lista_inter_adj.append(y)

        matrix = g.get_adjacency().data
        matrix.insert(0, self.list_names)
        for index, row in enumerate(matrix[1:]):
            row.insert(0, self.list_names[index])
        print(tabulate(matrix, headers='firstrow', tablefmt='fancy_grid'))
        self.CreateGraphCairuIgraph(g)

    def CreateGraphNetworkx(self):
        nxg = nx.DiGraph(self.list_inter_names)
        layout_planar = nx.planar_layout(nxg)
        node_sizes = [300 * len(x) if len(x) > 4 else 100 * len(x) for x in self.list_names]
        # fig, ax = plt.subplots()
        # nx.draw(nxg, layout_planar, with_labels=True, node_size=node_sizes, node_color=(0, 0, 0, 0), ax=ax, margins=0.01)
        nx.draw(nxg, pos=layout_planar, node_size=node_sizes, arrows=True, with_labels=True, node_shape="s",
                node_color="none", bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))
        plt.show()
        plt.savefig(self.PATH_GRAPH_IMAGE.format(name=self.random_name + "-matplotlib"))

    def CreateGraphCairuIgraph(self, g):
        """
                    PLOT IGRAPH
        """
        plot(
            g,
            target=self.PATH_GRAPH_IMAGE.format(name=self.random_name),
            #layout=g.layout("kk"),
            vertex_label=g.vs['name'] if self.list_names != [] else None,
            #vertex_color="rgba(5%, 100%, 100%, 0%)",
            #vertex_frame_color="rgba(5%, 100%, 100%, 0%)",
            # vertex_shape="circle", # circle | rectangle
            #vertex_size=45,
            # edge_width=2,
            #edge_arrow_size=1,
            bbox=(350, 600),
            margin=60
        )


    def CreateGraphMatplotLib(self, g):
        """
                    MATPLOTLIB PLOT
                """
        fig, ax = plt.subplots()
        plot(
            g,
            target=ax,
            #layout="kk",  # print nodes in a circular layout
            #vertex_size=0.3,
            vertex_frame_color="white",
            vertex_color="white",
            #vertex_label_color=["blue"]*len(g.vs["name"]),
            vertex_label=g.vs['name'] if self.list_names != [] else None,
            #vertex_label_size=10.0
        )
        plt.savefig(self.PATH_GRAPH_IMAGE.format(name=self.random_name+"-matplotlib"))#"./itutor/static/grafos/Graph.png"

    def CreatePlotComparison(self):
        file = os.path.abspath("./extensions/teste_ks.py").replace("\\", "/")
        print(file)
        p = subprocess.run([sys.executable, file, str(self.lista_inter_adj)], capture_output=True, text=True)
        print("LOG EXECUCAO SUBPROCESS:", p.stdout)
        statistics = re.match(self.match_percent, str(p.stdout)).groups()[1]
        print("-------------\nStatistics Recebida:", statistics)
        self.random_percent = float(statistics)
        plt.hist(self.lista_inter_adj)
        plt.savefig(self.PATH_HIST_IMAGE.format(name=self.random_name))
        plt.clf()

    def FormatData(self, data):
        list_tuple = {}

        for d in data:
            if d["starter"]["registration"] not in list_tuple:
                list_tuple[d["starter"]["registration"]] = {"name": d["starter"]["name"], "interactions": []}

            if "finisher" in d and d["finisher"]:
                if d["finisher"]["registration"] not in list_tuple:
                    list_tuple[d["finisher"]["registration"]] = {"name": d["finisher"]["name"], "interactions": []}
                list_tuple[d["starter"]["registration"]]["interactions"].append(
                    (d["finisher"]["registration"], d["finisher"]["name"]))
            else:
                print("Entrou no Else e adicionou o valor: ", d["starter"]["name"])
                list_tuple[d["starter"]["registration"]]["interactions"].append(
                    (d["starter"]["registration"], d["starter"]["name"]))

        keys = list(list_tuple.keys())
        print(list_tuple)
        for i in list_tuple:
            for interaction in list_tuple[i]["interactions"]:
                self.list_inter.append((keys.index(i), keys.index(interaction[0])))
                self.list_inter_names.append((list_tuple[i]["name"], interaction[1]))
        self.list_names = [list_tuple[x]["name"] for x in list_tuple]

    def Reset(self):
        self.list_inter = []
        self.list_names = []
        self.lista_inter_adj = []
        self.teoric_sample = []
        self.random_name = ""

    def SetName(self, name):
        self.random_name = name

    def run(self):
        self.GenerateGraph()
        self.CreatePlotComparison()

def init_app(app):
  app.itutor = ITutorClassificator(app.static_folder)