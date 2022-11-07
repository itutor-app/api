from scipy import stats
from igraph import Graph
from igraph import plot, save, color_name_to_rgba
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import random
from tabulate import tabulate

class ITutorClassificator():

    def __init__(self, static_path):
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

        self.lista_inter_adj = np.matrix(g.get_adjacency().data)
        matrix = g.get_adjacency().data
        matrix.insert(0, self.list_names)
        for index, row in enumerate(matrix[1:]):
            row.insert(0, self.list_names[index])
        print(tabulate(matrix, headers='firstrow', tablefmt='fancy_grid'))
        """
            PLOT IGRAPH
        """
        plot(
            g,
            target=self.PATH_GRAPH_IMAGE.format(name=self.random_name),
            #layout=g.layout("kk"),
            vertex_label=g.vs['name'] if self.list_names != [] else None,
            vertex_color="rgba(5%, 100%, 100%, 0%)",
            vertex_frame_color="rgba(5%, 100%, 100%, 0%)",
            #vertex_shape="circle", # circle | rectangle
            #vertex_size=35,
            #edge_width=2,
            #edge_arrow_size=1,
            bbox=(400, 400),
            margin=60
        )

        """
            MATPLOTLIB PLOT
        """
        # fig, ax = plt.subplots()
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
        inter_mean = np.mean(self.lista_inter_adj)

        # -------------------
        # scale = 3.
        # range = 10
        # size = 10000
        #
        # X = stats.truncnorm(a=0, b=5, scale=scale).rvs(size=self.lista_inter_adj.shape)
        # X = X.round().astype(int)
        #
        # bins = 2 * range + 1
        # print("X: ", X)
        # print("\nBins: ", bins)
        # x_1d = []
        # for x in X:
        #     for y in x:
        #         x_1d.append(y)
        # plt.hist(x_1d, bins)
        # plt.show()
        # - --------------------------------

        inter_std = np.std(self.lista_inter_adj)
        interacion_norm_cdf = stats.norm.cdf(self.lista_inter_adj, loc=inter_mean, scale=inter_std)
        self.teoric_sample = np.random.randint(self.lista_inter_adj.max()+1, size=self.lista_inter_adj.shape)
        teoric_norm_cdf = stats.norm.cdf(self.teoric_sample, loc=inter_mean, scale=inter_std)
        teoric_mean = np.mean(self.teoric_sample)
        teoric_std = np.std(self.teoric_sample)

        critico = lambda x: 1.35810/np.sqrt(x)

        print("Tamanho dados interação: ", len(self.lista_inter_adj), "Tamanho dados teoric: ", len(self.teoric_sample))
        print("Crítico : ", critico(len(self.lista_inter_adj)))

        inter_kstest = stats.stats.kstest(self.lista_inter_adj, cdf="norm")
        teoric_kstest = stats.stats.kstest(self.teoric_sample, cdf="norm")
        print("\n# SEM MEDIA E DESVIO PADRÃO\nINTERAÇÃO: ", inter_kstest,
              "\nTEORICA", teoric_kstest)

        inter_kstest_cdf = stats.stats.kstest(interacion_norm_cdf, cdf="norm")
        teoric_kstest_cdf = stats.stats.kstest(teoric_norm_cdf, cdf="norm")
        print("\n# CDF - SEM MEDIA E DESVIO PADRÃO\nINTERAÇÃO: ", inter_kstest_cdf,
              "\nTEORICA", teoric_kstest_cdf)

        inter_kstest_mean_std = stats.stats.kstest(self.lista_inter_adj, cdf="norm", args=(inter_mean, inter_std), N=len(self.lista_inter_adj))
        teoric_kstest_mean_std = stats.stats.kstest(self.teoric_sample, cdf="norm", args=(teoric_mean, teoric_std), N=len(self.teoric_sample))
        print("\n# COM MEDIA E DESVIO PADRÃO", "\nINTERAÇÃO: ", inter_kstest_mean_std,"\nTEORIC: ", teoric_kstest_mean_std)

        #inter_teoric_kstest = stats.stats.ks_2samp(self.lista_inter_adj, self.teoric_sample)
        self.random_percent = inter_kstest[0]
        #print("\n# COMPARAÇÃO ENTRE AMBOS OS DADOS SEM MEDIA E SEM DESVIO\n", inter_teoric_kstest)



        print("\nINTERAÇAO NORMAL CDF\n", interacion_norm_cdf)
        print("\nTEORIC NORMAL CDF\n", teoric_norm_cdf)
        print("INTERACAO SAMPLE:\n", self.lista_inter_adj)
        print("\nTEORIC SAMPLE\n", self.teoric_sample)

        plt.title("Interaction Curve")
        plt.plot(interacion_norm_cdf, self.lista_inter_adj, '-b')
        #plt.plot(self.teoric_sample, teoric_norm_cdf, '-g')
        #plt.tight_layout()
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