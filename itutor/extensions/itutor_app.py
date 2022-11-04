from scipy import stats
from igraph import Graph
from igraph import plot, save, color_name_to_rgba
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import random
import threading


class ITutorClassificator(threading.Thread):

    def __init__(self, static_path):
        threading.Thread.__init__(self)
        self.list_inter = []
        self.list_names = []
        self.lista_inter_adj = []
        self.teoric_sample = []
        self.random_percent = 0.9345
        self.random_name = ""
        self.STATIC_PATH = static_path
        self.PATH_GRAPH_IMAGE = static_path + "/{name}-graph.png"
        self.PATH_CURVE_IMAGE = static_path + "/{name}-curve"

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

        # fig, ax = plt.subplots()
        """
            PLOT IGRAPH
        """
        plot(
            g,
            target=self.PATH_GRAPH_IMAGE.format(name=self.random_name),
            layout=g.layout("kk"),
            vertex_label=g.vs['name'] if self.list_names != [] else None,
            vertex_color="rgba(5%, 100%, 100%, 0%)",
            vertex_frame_color="rgba(5%, 100%, 100%, 0%)",
            vertex_shape="circle", # circle | rectangle
            vertex_size=50,
            edge_width=0.3,
            edge_arrow_size=1
            #vertex_label_dist=5
        )

        """
            MATPLOTLIB PLOT
        """
        # plot(
        #     g,
        #     target=ax,
        #     layout="kk",  # print nodes in a circular layout
        #     vertex_size=0.3,
        #     vertex_frame_color="white",
        #     vertex_color="white",
        #     vertex_label_color=["blue"]*len(g.vs["name"]),
        #     vertex_label=g.vs['name'] if self.list_names != [] else None,
        #     vertex_label_size=10.0
        # )
        # plt.savefig(self.PATH_GRAPH_IMAGE.format(name=self.random_name+"-matplotlib"))#"./itutor/static/grafos/Graph.png"


    def CreatePlotComparison(self):
        #self.lista_inter_adj.sort()
        print("LISTA DE ADJACENTE GRAFO\n", self.lista_inter_adj)
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

        self.random_percent = stats.stats.ks_2samp(self.lista_inter_adj, self.teoric_sample)[0]

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
        plt.savefig(self.PATH_CURVE_IMAGE.format(name=self.random_name))#"./itutor/static/curvas/Curves-Comparison"


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
  app.itutor = ITutorClassificator(app.static_folder)