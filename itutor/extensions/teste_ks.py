from rpy2 import robjects
from rpy2.robjects.packages import importr
import sys
import json

def main(command):
    try:
        data = json.loads(command[1])
        lista = data["interactions"]
        nomes = data["interactions_r"]
        image_name = data["image_name"]
        max_value = max(lista)
        lista = robjects.IntVector(lista)
        nomes = robjects.StrVector(nomes)
        image_name = [image_name]
        image_name = robjects.StrVector(image_name)

        robjects.r(f'''
                        library("igraph")
                        g4 <- graph({nomes.r_repr()})
                        l <- layout.kamada.kawai(g4)
                        l <- norm_coords(l, ymin=-1, ymax=1, xmin=-1.30, xmax=1.30)
                        png({image_name.r_repr()}[1], width = 350, height = 600)
                        par(new=TRUE, mar = c(0, 0, 0, 0))
                        plot(g4, layout=l*0.7, edge.arrow.size=.5, vertex.color="gold", vertex.size=10,
                        vertex.frame.color="gray", vertex.label.color="black", vertex.label.cex=1.1, vertex.label.dist=1.8,
                        edge.curved=0, rescale=T, vertex.label.degree=-pi/2)
                        dev.off()
                    ''')
        kstest = robjects.r(f"""
                                library("KSgeneral")
                                KSgeneral::disc_ks_test({lista.r_repr()}, ecdf(0:{max_value}), exact = TRUE)
                            """)
        print("Statistics:", kstest[0][0])
    except Exception as e:
        print("Erro ao executar script R:", e)



if __name__ == "__main__":
    #teste = "{'interactions': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 'interactions_r': ('Renway', 'Renway', 'Ana', 'Josi', 'Ana', 'Amanda', 'Ana', 'Amanda', 'Josi', 'Ellys', 'Josi', 'Ellys', 'Josi', 'Amanda', 'Amanda', 'Amanda', 'Leo', 'Renway', 'Leo', 'Ana', 'Leo', 'Josi', 'Ellys', 'Josi', 'Mayra', 'Mayra', 'Rafa', 'Ellys', 'Rafa', 'Josi', 'Rafa', 'Amanda', 'Blenda', 'Renway'), 'image_name': 'C:\\Users\\eliel\\PycharmProjects\\API-ITutor\\itutor\\static/123456-graph.png'}"
    main(sys.argv) #sys.argv

