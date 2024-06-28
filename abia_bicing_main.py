from aima.search import hill_climbing, simulated_annealing, exp_schedule
from abia_bicing_parametres import ProblemParameters
from abia_bicing_problem import BicingProblem
from abia_bicing import *
from abia_bicing_estat_h1_SA import generate_initial_state, generate_initial_state_greedy


import matplotlib
matplotlib.use('agg')


import matplotlib.pyplot as plt
from timeit import timeit

"[1 esatcio 50 bicicletes],[1 furgoneta 5 estacions]"
estaciones = Estaciones(25, 1250, 9)
parametres = ProblemParameters(estaciones, 5)
#estat_inicial = generate_initial_state(parametres)
estat_inicial_greedy = generate_initial_state_greedy(parametres)

#k=5, lam=0.01, limit=2000
#n = simulated_annealing(BicingProblem(estat_inicial),schedule= exp_schedule(k=1,lam=0.0005, limit=2000))
n = simulated_annealing(BicingProblem(estat_inicial_greedy),schedule= exp_schedule(k=5, lam=0.01, limit=2000))

#n = hill_climbing(BicingProblem(estat_inicial))
#n = hill_climbing(BicingProblem(estat_inicial_greedy))
print(n)                # Estat final
#print(n.heuristic())    # Valor de l'estat final


temps_en_milisegons = (timeit(lambda: simulated_annealing(BicingProblem(estat_inicial_greedy)), number=1) * 1000)
print('\n', round(temps_en_milisegons, 2), 'milisegons')



