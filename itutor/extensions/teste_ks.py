from rpy2 import robjects
import sys
import json

def main(command):
    lista = json.loads(command[1])
    max_value = max(lista)
    lista = robjects.IntVector(lista)
    a = robjects.r(f"""
                    KSgeneral::disc_ks_test({lista.r_repr()}, ecdf(0:{max_value}), exact = TRUE)
                    """)
    print("Statistics:", a[0][0])

if __name__ == "__main__":
    t1 = [1] * 3 + [2] * 5 + [3] * 8 + [4] * 10 + \
         [5] * 15 + \
         [6] * 10 + [7] * 8 + [8] * 5 + [9] * 3
    main(sys.argv)

