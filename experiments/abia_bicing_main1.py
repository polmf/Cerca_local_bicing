import matplotlib.pyplot as plt
import numpy as np
from timeit import timeit
from aima.search import hill_climbing, simulated_annealing, exp_schedule
from abia_bicing_parametres import ProblemParameters
from abia_bicing_problem import BicingProblem
from abia_bicing import Estaciones
from abia_bicing_estat_h2_HC import generate_initial_state_greedy as gisg2
from abia_bicing_estat_h1 import generate_initial_state_greedy as gisg1
from abia_bicing_estat_h2_SA import generate_initial_state_greedy as sa2
from abia_bicing_estat_h1_SA import generate_initial_state_greedy as sa1


# Define tus estaciones y parámetros como lo has hecho en tu código
param_configs = []
for j in range(10):
    estaciones = Estaciones(25, 1250, j)
    parametres = ProblemParameters(estaciones, 5)
    param_configs.append(parametres)


tiempos_greedy = []  # Lista para almacenar los tiempos medios (estado inicial greedy)
beneficios_greedy = []  # Lista para almacenar los beneficios medios (estado inicial greedy)
tiempos_normal = []  # Lista para almacenar los tiempos medios (estado inicial normal)
beneficios_normal = []  # Lista para almacenar los beneficios medios (estado inicial normal)


for config in param_configs:
    tiempos_config_greedy = []
    tiempos_config_normal = []
    beneficios_config_greedy = []
    beneficios_config_normal = []
   
    for _ in range(5):
        # Crea un problema con la configuración actual y estado inicial greedy
        problem_greedy = BicingProblem(gisg2(config))
        tiempo_ms_greedy = [timeit(lambda: hill_climbing(problem_greedy), number=1) * 1000 for _ in range(5)]
        tiempos_config_greedy.append(np.mean(tiempo_ms_greedy))
        resultado_heuristica_greedy = hill_climbing(problem_greedy).heuristic()
        beneficios_config_greedy.append(resultado_heuristica_greedy)


        # Crea un problema con la configuración actual y estado inicial normal
        problem_sa2 = BicingProblem(sa2(config))
        tiempo_ms_sa2 = [timeit(lambda: simulated_annealing(problem_sa2, schedule=exp_schedule(k=1,lam=0.0005, limit=2000)), number=1) * 1000 for _ in range(5)]
        tiempos_config_normal.append(np.mean(tiempo_ms_sa2))
        resultado_heuristica_sa2 = simulated_annealing(problem_sa2, schedule=exp_schedule(k=5, lam=0.1, limit=3500)).heuristic()
        beneficios_config_normal.append(resultado_heuristica_sa2)


    tiempos_greedy.append(np.mean(tiempos_config_greedy))
    beneficios_greedy.append(np.mean(beneficios_config_greedy))
    tiempos_normal.append(np.mean(tiempos_config_normal))
    beneficios_normal.append(np.mean(beneficios_config_normal))


# Graficar el tiempo
plt.figure()
plt.plot(range(10), tiempos_greedy, marker='o', label='hill_climbing')
plt.plot(range(10), tiempos_normal, marker='x', label='simulated_annealing')
plt.title('Tiempo Promedio')
plt.xlabel('Configuración de Parámetros')
plt.ylabel('Tiempo (ms)')
plt.xticks(range(10))
plt.legend()
plt.show()


# Graficar el beneficio
plt.figure()
plt.plot(range(10), beneficios_greedy, marker='o', color='red', label='hill_climbing')
plt.plot(range(10), beneficios_normal, marker='x', color='blue', label='simulated_annealing')
plt.title('Beneficio Promedio')
plt.xlabel('Configuración de Parámetros')
plt.ylabel('Beneficio')
plt.xticks(range(10))
plt.legend()
plt.show()



