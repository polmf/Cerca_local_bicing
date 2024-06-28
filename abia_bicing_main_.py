from aima.search import hill_climbing
from abia_bicing_parametres import ProblemParameters
from abia_bicing_problem import BicingProblem
from abia_bicing import *
from abia_bicing_estat import generate_initial_state, generate_initial_state_greedy


import matplotlib
matplotlib.use('agg')


import matplotlib.pyplot as plt
from timeit import timeit


estaciones = Estaciones(25, 1250, 42)
parametres = ProblemParameters(estaciones, 5)
estat_inicial = generate_initial_state(parametres)
estat_inicial_greedy = generate_initial_state_greedy(parametres)


#n = hill_climbing(BicingProblem(estat_inicial))
#n = hill_climbing(BicingProblem(estat_inicial_greedy))
#print(n)                # Estat final
#print(n.heuristic())    # Valor de l'estat final


#temps_en_milisegons = (timeit(lambda: hill_climbing(BicingProblem(estat_inicial)), number=1) * 1000)
#print('\n', round(temps_en_milisegons, 2), 'milisegons')


## Solucio no greedy:


# Realiza la medición del tiempo y multiplica por 1000 para obtener milisegundos
times_bicing = [timeit(lambda: hill_climbing(BicingProblem(estat_inicial)), number=1) for _ in range(10)]


data_to_plot = [times_bicing]
labels = ['hill_climbing']


# Crear una figura con un tamaño específico
plt.figure(figsize=(8, 8))


#Dibuixar el boxplot:
plt.boxplot(data_to_plot, labels=labels)
plt.ylabel('Temps d\'Execucio (segons)')
plt.title('Temps d\'Execucio amb solucio no greedy')
plt.savefig('temps_6_operadors.png')


"""
Experiment Especial:


#####################
#1. Calcul del temps


## Solucio greedy:


# Realiza la medición del tiempo y multiplica por 1000 para obtener milisegundos
times_bicing = [timeit(lambda: hill_climbing(BicingProblem(estat_inicial_greedy)), number=1) * 1000]


data_to_plot = [times_bicing]
labels = ['hill_climbing']


# Crear una figura con un tamaño específico
plt.figure(figsize=(8, 8))


#Dibuixar el boxplot:
plt.boxplot(data_to_plot, labels=labels)
plt.ylabel('Temps d\'Execucio (milisegons)')
plt.title('Temps d\'Execucio amb solucio greedy')
plt.savefig('temps_experiment_especial_greedy.png')


################################


## Solucio no greedy:


# Realiza la medición del tiempo y multiplica por 1000 para obtener milisegundos
times_bicing = [timeit(lambda: hill_climbing(BicingProblem(estat_inicial)), number=1) * 1000]


data_to_plot = [times_bicing]
labels = ['hill_climbing']


# Crear una figura con un tamaño específico
plt.figure(figsize=(8, 8))


#Dibuixar el boxplot:
plt.boxplot(data_to_plot, labels=labels)
plt.ylabel('Temps d\'Execucio (milisegons)')
plt.title('Temps d\'Execucio amb solucio no greedy')
plt.savefig('temps_experiment_especial.png')




################################################
"""


#Calcul del benefici:
#n = hill_climbing(BicingProblem(estat_inicial_greedy))


#benefici = n.heuristic()
#data_to_plot = [benefici]
#labels = ['experiment especial']


# Crear una figura con un tamaño específico
#plt.figure(figsize=(8, 8))


#Dibuixar el boxplot:
#plt.boxplot(data_to_plot, labels=labels)
#plt.ylabel('Benefici en euros')
#plt.title('Execucio amb solucio no greedy')
#plt.savefig('benefici_experiment_especial.png')










"""
Experiment 1:


# Realiza la medición del tiempo y multiplica por 1000 para obtener milisegundos
times_bicing = [timeit(lambda: hill_climbing(BicingProblem(estat_inicial)), number=1) * 1000]


data_to_plot = [times_bicing]
labels = ['hill_climbing']


# Crear una figura con un tamaño específico
plt.figure(figsize=(8, 8))


#Dibuixar el boxplot:
plt.boxplot(data_to_plot, labels=labels)
plt.ylabel('Temps d\'Execucio (segons)')
plt.title('Comparativa d\'Algoritmes amb Boxplots')
plt.savefig('experiment1_4_operadors.png')


"""


"""
#Calcul del benefici:
n = hill_climbing(BicingProblem(estat_inicial_greedy))


benefici = n.heuristic()


# Supongamos que tienes etiquetas para las barras.
etiquetas = ['Benefici màxim']


# Crear una figura con un tamaño específico
plt.figure(figsize=(8, 8))


# Crear el gráfico de barras
plt.bar(etiquetas, [benefici], width=0.2)


# Puedes personalizar aún más el gráfico, como añadir etiquetas a los ejes y un título.
#plt.xlabel('Etiquetas de Eje X')
plt.ylabel('Euros')
plt.title('Experiment Especial')


# Mostrar el gráfico
plt.savefig('prova_experiment_especial.png')
"""

