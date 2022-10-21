from scipy import stats
from igraph import Graph
from igraph import plot, save
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import random
import threading
import os
PATH_GRAPH_IMAGE = "static/grafos/{name}-graph.png"
PATH_CURVE_IMAGE = "static/curvas/{name}-curve"

class ITutorClassificator(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.list_inter = []
        self.list_names = []
        self.lista_inter_adj = []
        self.teoric_sample = []
        self.random_percent = 0.0
        self.random_name = ""

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
            layout=g.layout("kk"),
            vertex_label=g.vs['name'] if self.list_names != [] else None,
            vertex_color="lightblue",
            vertex_shape="rectangle",
            vertex_size=0.3
        )
        print("meu path: ", os.path.abspath("itutor/static"))
        print("Existe a pasta grafos? ", "Sim" if os.path.exists("static/grafos") else "Não")
        if os.path.exists("static/grafos") is False:
            os.mkdir(f"{os.path.abspath('itutor/static')}/grafos")
        plt.savefig(PATH_GRAPH_IMAGE.format(name=self.random_name))#"./itutor/static/grafos/Graph.png"


    def CreatePlotComparison(self):
        #self.lista_inter_adj.sort()
        interacion_norm = stats.norm.cdf(self.lista_inter_adj, loc=0, scale=1)
        inter_mean = np.mean(self.lista_inter_adj)
        inter_std = np.std(self.lista_inter_adj)


        self.teoric_sample = np.linspace(min(self.lista_inter_adj), max(self.lista_inter_adj))
        teoric_sample_test = [random.randint(min(self.lista_inter_adj), max(self.lista_inter_adj)+1) for x in range(len(self.lista_inter_adj))]
        teoric_norm = stats.norm.cdf(self.teoric_sample, loc=0, scale=1)
        teoric_mean = np.mean(self.teoric_sample)
        teoric_std = np.std(self.teoric_sample)

        critico = lambda x: 1.35810/np.sqrt(x)

        print("Tamanho dados interação: ", len(self.lista_inter_adj), "Tamanho dados teoric: ", len(teoric_sample_test))
        print("Crítico : ", critico(len(self.lista_inter_adj)))
        print("# SEM MEDIA E DESVIO PADRÃO")

        print(stats.stats.kstest(self.lista_inter_adj, cdf="norm"))
        print(stats.stats.kstest(self.teoric_sample, cdf="norm"))
        print("# COM MEDIA E DESVIO PADRÃO")
        print(stats.stats.kstest(self.lista_inter_adj, cdf="norm", args=(inter_mean, inter_std), N=len(self.lista_inter_adj)))
        print(stats.stats.kstest(self.teoric_sample, cdf="norm", args=(teoric_mean, teoric_std), N=len(self.teoric_sample)))
        print("# COMPARAÇÃO ENTRE AMBOS OS DADOS")
        print(stats.stats.ks_2samp(self.lista_inter_adj, self.teoric_sample))

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
        print("Existe a pasta curvas? ", "Sim" if os.path.exists("static/curvas") else "Não")
        if os.path.exists("static/curvas") is False:
            os.mkdir(f"{os.path.abspath('itutor/static')}/curvas")
        plt.savefig(PATH_CURVE_IMAGE.format(name=self.random_name))#"./itutor/static/curvas/Curves-Comparison"

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
        self.random_name = ""

    def GenerateRandomName(self):
        for x in range(10):
            self.random_name += random.choice("qwertyuiopasdfghjklçzxcvbnm123456789")

    def run(self):
        self.GenerateGraph()
        self.CreatePlotComparison()

def init_app(app):
  app.itutor = ITutorClassificator()