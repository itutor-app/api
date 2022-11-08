from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
scale = 3.
size = 10000

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return stats.truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

def matrix_to_array(matrix):
    x_1d = []
    for x in matrix:
        for y in x:
            x_1d.append(y)
    return x_1d

def is_normal_distribution(teste):
    if teste[1] > 0.05:
        return "É uma distribuição normal? Sim"
    return "É uma distribuição normal? Não"

matrix_normal = get_truncated_normal(mean=0, sd=1, low=-5, upp=5).rvs(size=(11,11))
matrix_normal_inteiro = matrix_normal.round().astype(int)

matrix_normal_2 = get_truncated_normal(mean=0, sd=1, low=-5, upp=5).rvs(size=(11,11))
matrix_normal_2_inteiro = matrix_normal_2.round().astype(int)

matrix_random = np.random.randint(low=-5, high=5, size=(11, 11))

vetor_normal = get_truncated_normal(mean=0, sd=1, low=-5, upp=5).rvs(size=200)
vetor_normal_inteiro = vetor_normal.round().astype(int)

vetor_random = [np.random.randint(-5, 5) for z in range(200)]

bins = 2 * 100 + 1
print("X: ", matrix_normal)
print("\nBins: ", bins)



vetor_from_matrix_normal = matrix_to_array(matrix_normal)
vetor_from_matrix_normal_inteiro = matrix_to_array(matrix_normal_inteiro)
vetor_from_matrix_normal_2 = matrix_to_array(matrix_normal_2)
vetor_from_matrix_normal_2_inteiro = matrix_to_array(matrix_normal_2_inteiro)
vetor_from_matrix_random = matrix_to_array(matrix_random)



kstest_vetor_normal = stats.kstest(vetor_normal, cdf="norm", args=(0, 1), N=len(vetor_normal))
kstest_vetor_normal_inteiro = stats.kstest(vetor_normal_inteiro, cdf="norm", args=(0, 1), N=len(vetor_normal_inteiro))
kstest_vetor_nao_normal = stats.kstest(vetor_random, cdf="norm", args=(0, 1), N=len(vetor_random))
ks_2samp_vetor_nao_normal_e_vetor_normal = stats.ks_2samp( vetor_random, vetor_normal)

print("Vetor NORMAL: ", kstest_vetor_normal, is_normal_distribution(kstest_vetor_normal))
print("Vetor NORMAL INTEIRO: ", kstest_vetor_normal_inteiro, is_normal_distribution(kstest_vetor_normal_inteiro))
print("Vetor Não-Normal: ", kstest_vetor_nao_normal, is_normal_distribution(kstest_vetor_nao_normal))
print("Teste entre vetor não-normal e normal: ", ks_2samp_vetor_nao_normal_e_vetor_normal, is_normal_distribution(ks_2samp_vetor_nao_normal_e_vetor_normal))


kstest_matriz_normal = stats.kstest(matrix_normal, cdf="norm", args=(0, 1))
kstest_matriz_normal_inteiro = stats.kstest(matrix_normal_inteiro, cdf="norm", args=(0, 1))
kstest_matriz_normal_2 = stats.kstest(matrix_normal_2, cdf="norm", args=(0, 1))
kstest_matriz_normal_2_inteiro = stats.kstest(matrix_normal_2_inteiro, cdf="norm", args=(0, 1))
kstest_matriz_nao_normal = stats.kstest(matrix_random, cdf="norm", args=(0, 1))

print("\nMatriz NORMAL: ", kstest_matriz_normal, is_normal_distribution(kstest_matriz_normal))
print("Matriz NORMAL INTEIRO: ", kstest_matriz_normal_inteiro, is_normal_distribution(kstest_matriz_normal_inteiro))
print("Matriz NORMAL 2: ", kstest_matriz_normal_2, is_normal_distribution(kstest_matriz_normal_2))
print("Matriz NORMAL 2 INTEIRO: ", kstest_matriz_normal_2_inteiro, is_normal_distribution(kstest_matriz_normal_2_inteiro))
print("Matriz Não-Normal: ", kstest_matriz_nao_normal, is_normal_distribution(kstest_matriz_nao_normal))


kstest_vetor_de_matriz_normal = stats.kstest(vetor_from_matrix_normal, cdf="norm", args=(0, 1))
kstest_vetor_de_matriz_normal_inteiro = stats.kstest(vetor_from_matrix_normal_inteiro, cdf="norm", args=(0, 1))
kstest_vetor_de_matriz_normal_2 = stats.kstest(vetor_from_matrix_normal_2, cdf="norm", args=(0, 1))
kstest_vetor_de_matriz_normal_2_inteiro = stats.kstest(vetor_from_matrix_normal_2_inteiro, cdf="norm", args=(0, 1))
kstest_vetor_de_matriz_nao_normal = stats.kstest(vetor_from_matrix_random, cdf="norm", args=(0, 1))

print("\nVetor de Matriz NORMAL: ", kstest_vetor_de_matriz_normal, is_normal_distribution(kstest_vetor_de_matriz_normal))
print("Vetor de Matriz NORMAL INTEIRO: ", kstest_vetor_de_matriz_normal_inteiro, is_normal_distribution(kstest_vetor_de_matriz_normal_inteiro))
print("Vetor de Matriz NORMAL_2: ", kstest_vetor_de_matriz_normal_2, is_normal_distribution(kstest_vetor_de_matriz_normal_2))
print("Vetor de Matriz NORMAL_2 INTEIRO: ", kstest_vetor_de_matriz_normal_2_inteiro, is_normal_distribution(kstest_vetor_de_matriz_normal_2_inteiro))
print("Vetor de Matriz Não-Normal: ", kstest_vetor_de_matriz_nao_normal, is_normal_distribution(kstest_vetor_de_matriz_nao_normal))

ks2samp_vetores_nao_normal_e_normal = stats.ks_2samp(vetor_from_matrix_random, vetor_from_matrix_normal)
ks2samp_vetores_normais = stats.ks_2samp(vetor_from_matrix_normal, vetor_from_matrix_normal_2)
ks2samp_vetores_normais_inteiros = stats.ks_2samp(vetor_from_matrix_normal_inteiro, vetor_from_matrix_normal_2_inteiro)

print("Vetores de Matrizes não-normal teste se é normal: ", ks2samp_vetores_nao_normal_e_normal, is_normal_distribution(ks2samp_vetores_nao_normal_e_normal))
print("Vetores de Matrizes normais ks_2samp: ", ks2samp_vetores_normais, is_normal_distribution(ks2samp_vetores_normais))
print("Vetores de Matrizes normais INTEIROS ks_2samp: ", ks2samp_vetores_normais_inteiros, is_normal_distribution(ks2samp_vetores_normais_inteiros))
#plt.hist(vetor_normal, 12)
#plt.show()