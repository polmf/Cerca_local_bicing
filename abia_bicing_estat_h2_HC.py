"""
FITXER ESTAT PER LA SEGONA HEURÍSTICA I HILL CLIMBING
"""

from __future__ import annotations
from bdb import set_trace

from typing import List, Generator

from abia_bicing_operators import BicingOperator, Estacio_origen, Estacio_desti, Afegir_estacio_desti, Intercanviar_destins, Eliminar_estacio, Pivotar_destins
from abia_bicing_parametres import ProblemParameters
from abia_bicing import *


class Estat(object):
    def __init__(self, params: ProblemParameters, furgonetes_util: List, estacions_origen: List):
       
        self.params = params
        self.furgonetes_util= furgonetes_util

        self.estacions_origen = estacions_origen 


    def copia(self) -> Estat:
        

        furgonetes_util_copia = []
        for furgoneta in self.furgonetes_util:
            furgoneta_copia = [furgoneta[0].copy(), [], furgoneta[2]]
            for desti in furgoneta[1]:
                furgoneta_copia[1].append(desti.copy())
            
            furgonetes_util_copia.append(furgoneta_copia)

        estacions_origen_copia = self.estacions_origen.copy()

        return Estat(self.params, furgonetes_util_copia, estacions_origen_copia)
    

    def bicis_estacions_inicials(self, llista_estacions: Estaciones) -> List[List[object]]:

        nova_llista_estacions = [[estacio.num_bicicletas_no_usadas, estacio.num_bicicletas_next, estacio.demanda] for estacio in llista_estacions]

        return nova_llista_estacions


    def calcul_cost(self, new_state: Estat):

        for id_furgoneta in range(len(new_state.furgonetes_util)):
            estacio_origen_furgo = new_state.furgonetes_util[id_furgoneta][0][0]
            num_bicicletas_no_usadas = new_state.bicis_en_estacions[estacio_origen_furgo][0]

            #2. calculem quantes bicis agafa la furgoneta
            if new_state.params.capacitat_furgo >= num_bicicletas_no_usadas:    
                new_state.furgonetes_util[id_furgoneta][0][1] = num_bicicletas_no_usadas
            else:
                new_state.furgonetes_util[id_furgoneta][0][1] = new_state.params.capacitat_furgo

            #3. calculem quantes bicis deixa en cada estació
            bicicletes_agafades = new_state.furgonetes_util[id_furgoneta][0][1]
            for desti in new_state.furgonetes_util[id_furgoneta][1]:
                diferencia_desti = (new_state.bicis_en_estacions[desti[0]][1] - new_state.bicis_en_estacions[desti[0]][2])
                
                if diferencia_desti < 0:
                    
                    if bicicletes_agafades >= abs(diferencia_desti): #si tinc suficients bicis per cobrir la demanda
                        desti[1] = abs(diferencia_desti) #bicis que deixa en el desti
                        bicicletes_agafades -= abs(diferencia_desti) #actualitzo les bicis a la furgoneta

                    else: #no tinc suficients bicis per cobrir la demanda, llavors deixo a la estacio totes les bicis que porto
                        desti[1] = bicicletes_agafades
                        bicicletes_agafades = 0 

                else:
                    desti[1] = 0

            #4. Canviem el benefici obtingut de la furgoneta
            new_state.furgonetes_util[id_furgoneta][2] = self.benefici(id_furgoneta, new_state)



    def cost_transport(self, nb: int, estacio_origen: int, estacio_final: int):
        cost = 0
        n_b = nb
        cost = ((n_b + 9) // 10)*self.distancia(estacio_origen, estacio_final)
        return cost
    


    def benefici(self, id_furgoneta: int, new_state: Estat) -> float:
        #aquesta funcio calcula per una furgoneta el benefici que ha obtingut
        benefici = 0
        
        estacio_origen_furgo = new_state.furgonetes_util[id_furgoneta][0][0]

        #la diferencia es les bicis que hi haura menys la demanda
        diferencia = (new_state.bicis_en_estacions[estacio_origen_furgo][1] - new_state.bicis_en_estacions[estacio_origen_furgo][2]) 

        if diferencia <= 0: #si hem agafat bicicletes d'un lloc que no li sobraven bicis
            benefici -= new_state.furgonetes_util[id_furgoneta][0][1] #furgoneta[0][1] és el numero de bicis que recollim
    
        #la diferencia >0 pero (la diferencia - les bicis que recollim[les bicis que no es mouran] <0) -> hi ha perdues en cost
        elif new_state.furgonetes_util[id_furgoneta][0][1] > diferencia: 
            benefici += (diferencia - new_state.furgonetes_util[id_furgoneta][0][1]) 

        new_state.bicis_en_estacions[estacio_origen_furgo][0] -= new_state.furgonetes_util[id_furgoneta][0][1]
        new_state.bicis_en_estacions[estacio_origen_furgo][1] -= new_state.furgonetes_util[id_furgoneta][0][1]

        #Ara sumarem al benefici les bicis ben mogudes
        c1 = 0
        c2 = 0
        for parada in range(len(new_state.furgonetes_util[id_furgoneta][1])):
            bicis_deixades = new_state.furgonetes_util[id_furgoneta][1][parada][1] #les bicis que hem deixat en la estacio
            desti_estacio = new_state.furgonetes_util[id_furgoneta][1][parada][0] #el id de la estacio de desti
            diferencia = (new_state.bicis_en_estacions[desti_estacio][1] - new_state.bicis_en_estacions[desti_estacio][2])
            
            if parada==0: #estem realitzant el primer transport (1r desti)
                bicis_transportades = new_state.furgonetes_util[id_furgoneta][0][1] #número de bicis que transportem desde l'origen
                estacio_origen = new_state.furgonetes_util[id_furgoneta][0][0]
                bicis_deixades_primer_desti = bicis_deixades
                c1=self.cost_transport(bicis_transportades, estacio_origen, desti_estacio)
            else:
                estacio_primer_desti = new_state.furgonetes_util[id_furgoneta][1][parada-1][0]
                c2=self.cost_transport(bicis_transportades-bicis_deixades_primer_desti,estacio_primer_desti, desti_estacio)
                
            if diferencia >= 0:
                pass
            elif bicis_deixades > abs(diferencia): #si hem deixat més bicis de la demanda, bicing no ens paga res
                pass
            else:            
                benefici += bicis_deixades
           
            new_state.bicis_en_estacions[desti_estacio][1] += bicis_deixades

        return (benefici-(c1+c2))


    def generate_actions(self) -> Generator[BicingOperator, None, None]:
       
        for id_furgoneta in range(len(self.furgonetes_util)):
            for id_est in range(len(self.params.estaciones.lista_estaciones)):
                if id_est not in self.estacions_origen and not any(id_est == desti[0] for desti in self.furgonetes_util[id_furgoneta][1]):
                    yield Estacio_origen(id_est, id_furgoneta)                  
                        
                                       
        for id_furgoneta in range(len(self.furgonetes_util)):
            for id_desti in range(len(self.params.estaciones.lista_estaciones)):                
                #si la furgoneta ja visita alguna estació
                if len(self.furgonetes_util[id_furgoneta][1]):
                       #si la furgoneta no viatja ja al desti 1 en questió:
                       if id_desti != self.furgonetes_util[id_furgoneta][1][0][0]:
                            yield Estacio_desti(id_desti, id_furgoneta)
                else:
                    yield Estacio_desti(id_desti, id_furgoneta)


        for id_furgoneta in range(len(self.furgonetes_util)):
            if len(self.furgonetes_util[id_furgoneta][1]) == 1: #si la furgoneta només té assignada una estacio, afegim estació
                for id_desti in range(len(self.params.estaciones.lista_estaciones)):
                    if id_desti != self.furgonetes_util[id_furgoneta][1][0][0]:
                        yield Afegir_estacio_desti(id_desti, id_furgoneta)
            elif len(self.furgonetes_util[id_furgoneta][1]) == 2: #si la furgoneta té assignades les dues estacions com a màxim, intercanviem els destins
                yield Intercanviar_destins(id_furgoneta)           


        for id_furgoneta in range(len(self.furgonetes_util)):
            if len(self.furgonetes_util[id_furgoneta][1]): #si te estacio desti    
                if len(self.furgonetes_util[id_furgoneta][1]) == 2: #si visita dos estacions
                    yield Eliminar_estacio(id_furgoneta) #eliminem primer només el segon desti
                    yield Eliminar_estacio(id_furgoneta, True) #eliminem els dos destins
                else: #visita una estacio
                    yield Eliminar_estacio(id_furgoneta)


        for id_furgoneta in range(len(self.furgonetes_util)):
            if len(self.furgonetes_util[id_furgoneta][1]) > 1:
                #si té assignades dos estacions desti
                for i in range(len(self.params.estaciones.lista_estaciones)):
                    yield Pivotar_destins(id_furgoneta, 0, i)


                for i in range(len(self.params.estaciones.lista_estaciones)):
                    yield Pivotar_destins(id_furgoneta, 1, i)



    def aplicar_accions(self, action: BicingOperator)-> Estat:
        new_state = self.copia()
        
        if isinstance(action, Estacio_origen):
            id_est = action.id_est
            id_furgoneta = action.id_furgoneta

            #1. canviem [origen] de la furgoneta
            new_state.furgonetes_util[id_furgoneta][0][0] = id_est #assignem la estacio origen
            new_state.estacions_origen[id_furgoneta] = id_est

            #inicialitzem les bicis en cada estacio per utilitzar-les despres:
            new_state.bicis_en_estacions = self.bicis_estacions_inicials(self.params.estaciones.lista_estaciones)

            self.calcul_cost(new_state)
            
        
        elif isinstance(action, Estacio_desti):
            id_desti = action.id_desti
            id_furgoneta = action.id_furgoneta

            #1. canviem [desti] de la furgoneta
            new_state.furgonetes_util[id_furgoneta][1] = [[id_desti, 0]] #assignem la unica estacio desti i inicialitzem a 0 les bicis que en deixa

            #inicialitzem les bicis en cada estacio per utilitzar-les despres:
            new_state.bicis_en_estacions = self.bicis_estacions_inicials(self.params.estaciones.lista_estaciones)
            
            self.calcul_cost(new_state)


        elif isinstance(action, Afegir_estacio_desti):
            id_desti = action.id_desti
            id_furgoneta = action.id_furgoneta

            #1. afegim [desti] a la furgoneta
            new_state.furgonetes_util[id_furgoneta][1].append([id_desti, 0]) #afegim la nova estacio desti i inicialitzem a 0 les bicis que en deixa

            #inicialitzem les bicis en cada estacio per utilitzar-les despres:
            new_state.bicis_en_estacions = self.bicis_estacions_inicials(self.params.estaciones.lista_estaciones)

            self.calcul_cost(new_state)

            
        elif isinstance(action, Intercanviar_destins):
            id_furgoneta = action.id_furgoneta
            
            id_desti1 = new_state.furgonetes_util[id_furgoneta][1][0][0]
            id_desti2 = new_state.furgonetes_util[id_furgoneta][1][1][0]

            new_state.furgonetes_util[id_furgoneta][1][0][0] = id_desti2
            new_state.furgonetes_util[id_furgoneta][1][1][0] = id_desti1

            #inicialitzem les bicis en cada estacio per utilitzar-les despres:
            new_state.bicis_en_estacions = self.bicis_estacions_inicials(self.params.estaciones.lista_estaciones)
            
            self.calcul_cost(new_state)

        
        elif isinstance(action, Eliminar_estacio):
            id_furgoneta = action.id_furgoneta
            destins = action.destins
            
            if destins is True:
                new_state.furgonetes_util[id_furgoneta][1].pop(1)
                new_state.furgonetes_util[id_furgoneta][1].pop(0)
            else:
                new_state.furgonetes_util[id_furgoneta][1].pop(0)

            #inicialitzem les bicis en cada estacio per utilitzar-les despres:
            new_state.bicis_en_estacions = self.bicis_estacions_inicials(self.params.estaciones.lista_estaciones)

            self.calcul_cost(new_state)


        elif isinstance(action, Pivotar_destins):
            id_furgoneta = action.id_furgoneta
            
            new_state.furgonetes_util[id_furgoneta][1][action.estacio_canvia][0] = action.id_estacio

            #inicialitzem les bicis en cada estacio per utilitzar-les despres:
            new_state.bicis_en_estacions = self.bicis_estacions_inicials(self.params.estaciones.lista_estaciones)

            self.calcul_cost(new_state)
        
        return new_state    
    
    
    def heuristic(self) -> float:

        heuristic = sum(furgoneta[2] for furgoneta in self.furgonetes_util)
        
        return heuristic


    def distancia(self, id_parada_origen: int, id_parada_desti: int) -> float:
        """
        Calcula la distància entre dos estacions, i divideix el resultat entre 1000 per passar de metres a Km.
        """
        return round((abs(self.params.estaciones.lista_estaciones[id_parada_origen].coordX - self.params.estaciones.lista_estaciones[id_parada_desti].coordX) \
        + abs(self.params.estaciones.lista_estaciones[id_parada_origen].coordY - self.params.estaciones.lista_estaciones[id_parada_desti].coordY))/1000,2)
       

    def __repr__(self):       
            distancia_total = 0
            i = 1
            repr_str = "Furgonetes Utilitzades:\n"
            for furgoneta in self.furgonetes_util:
                repr_str += f"Furgoneta {i}\n"
                repr_str += f"ID Estació Origen: {furgoneta[0][0]} - Bicicletes agafades: {furgoneta[0][1]}\n"
               
                n = 1
                d1=0
                d2=0
                for desti in furgoneta[1]:
                    if n==1:
                        d1 = self.distancia(furgoneta[0][0],desti[0])
                        repr_str += f"ID Estació Destí {n}: {desti[0]} - Bicicletes descarregades: {desti[1]} - Recorregut: {d1}km\n"
                        n += 1
                    else:
                        d2 = self.distancia(furgoneta[1][0][0],desti[0])
                        repr_str += f"ID Estació Destí {n}: {desti[0]} - Bicicletes descarregades: {desti[1]} - Recorregut: {d2}km\n"
                distancia_total += (d1+d2)
                repr_str += f"Distancia total recorreguda de la furgoneta: {round(d1+d2,2)}km \n"
                repr_str += f"Benefici furgoneta: {round(furgoneta[2], 2)} \n"

                i += 1
                repr_str += f"\n"
            repr_str += f"Benefici total: {round(self.heuristic(), 2)} € \n"
            repr_str += f"Longitud total del recorregut de les furgonetes: {round(distancia_total, 2)} km \n"

            return repr_str
   

   
def generate_initial_state(params: ProblemParameters) -> Estat:
   
    furgonetes_util = [[[i,0], [[i+1,0]], 0] for i in range(params.furgonetes_max)]
    # la clau (cada posició de la llista general) és la identificacio de la furgoneta; en la primera llista de la furgoneta ([i,0]) la 1a posició 
    # és la identificació de la estació origen de la furgoneta i la 2a posició les bicis que té la furgoneta; 
    # la segona llista de la furgoneta ([[i+1,0]]) és una llista que conté les estacions destí i les bicis que agafa per desti; 
    # la última posició de la furgoneta és el benefici 
    
    bicis_en_estacions = bicis_estacions(params.estaciones.lista_estaciones)

    #hem de calcular les bicis que agafa la furgoneta en l'estat inicial, les que deixa en les estacions i el benefici
    calcul_estat_inicial(params, furgonetes_util, bicis_en_estacions)

    estacions_origen = estacions_origen_visitades(furgonetes_util)

    return Estat(params, furgonetes_util, estacions_origen)
         


def generate_initial_state_greedy(params: ProblemParameters) -> Estat:
    """
    Genera un estat inicial en el qual assigna per cada furgoneta les estacions les quals els hi sobra més bicicletas.
    Per fer-ho ordenem en una llista les estacions amb més bicicletes sobrants i les assignem com a estacions origen a les furgonetes. 
    """

    maxims = [(id_est,excedente(params, id_est)) for id_est in range(params.furgonetes_max)] #cada tupla representa en la primera posició l'id_est i en la segona les bicis sobrants

    for id_est in range(len(params.estaciones.lista_estaciones)):        
        valor_excedent = excedente(params, id_est)
        
        #calculem el minim
        minim = min(maxims, key=lambda x: x[1])
        
        if valor_excedent > minim[1]:
            maxims.remove(minim)
            maxims.append((id_est, valor_excedent))

    estacions_origen_ordenades = sorted(maxims, key=lambda x: x[1], reverse=True)

    furgonetes_util = [[[i[0],0], [], 0] for i in estacions_origen_ordenades]

    bicis_en_estacions = bicis_estacions(params.estaciones.lista_estaciones)

    #hem de calcular les bicis que agafa la furgoneta en l'estat inicial, les que deixa en les estacions i el benefici
    calcul_estat_inicial(params, furgonetes_util, bicis_en_estacions)

    estacions_origen = estacions_origen_visitades(furgonetes_util)
    
    return Estat(params, furgonetes_util, estacions_origen)


def excedente(params: ProblemParameters, id_est) -> float:
    
    num_bicicletas_no_usadas = params.estaciones.lista_estaciones[id_est].num_bicicletas_no_usadas
    num_bicicletas_next = params.estaciones.lista_estaciones[id_est].num_bicicletas_next
    demanda = params.estaciones.lista_estaciones[id_est].demanda
    diferencia = num_bicicletas_next - demanda
    if diferencia > 0:
        if diferencia > num_bicicletas_no_usadas:
            excedente = num_bicicletas_no_usadas
        else:
            excedente = diferencia
        
    else:
        excedente = 0
              
    return excedente
   

def bicis_estacions(llista_estacions: Estaciones) -> List[List[object]]:
    """
    Retorna una llista de llistes (cada element de la llista és l'identificador de una estació que conté una llista
    amb les bicis que no es mouran i les que hi hauran en la següent hora en cada estació,
    per a poder actualitzar les modificacions fetes en cada estacio degut als trasllats de les bicis per les furgonetes
    """
    nova_llista_estacions = [[estacio.num_bicicletas_no_usadas, estacio.num_bicicletas_next, estacio.demanda] for estacio in llista_estacions]


    return nova_llista_estacions  


def calcul_estat_inicial(params: ProblemParameters, furgonetes: List[List[List]], bicis_en_estacions: List[List]):

    for id_furgoneta in range(len(furgonetes)):
        
        estacio_origen_furgo = furgonetes[id_furgoneta][0][0]
        num_bicicletas_no_usadas = bicis_en_estacions[estacio_origen_furgo][0]

        #2. calculem quantes bicis agafa la furgoneta
        if params.capacitat_furgo >= num_bicicletas_no_usadas:    
            furgonetes[id_furgoneta][0][1] = num_bicicletas_no_usadas
        else:
            furgonetes[id_furgoneta][0][1] = params.capacitat_furgo


        #3. calculem quantes bicis deixa en cada estació
        bicicletes_agafades = furgonetes[id_furgoneta][0][1]
        for desti in furgonetes[id_furgoneta][1]:
            diferencia_desti = (bicis_en_estacions[desti[0]][1] - bicis_en_estacions[desti[0]][2])
            if diferencia_desti < 0:
                if bicicletes_agafades >= abs(diferencia_desti): #si tinc suficients bicis per cobrir la demanda
                    desti[1] = abs(diferencia_desti) #bicis que deixa en el desti
                    bicicletes_agafades -= abs(diferencia_desti) #actualitzo les bicis a la furgoneta

                else: #no tinc suficients bicis per cobrir la demanda, llavors deixo a la estacio totes les bicis que porto
                    desti[1] = bicicletes_agafades
                    bicicletes_agafades = 0
 

        #4. Canviem el benefici obtingut de la furgoneta
        furgonetes[id_furgoneta][2] = benefici_furgoneta(id_furgoneta, furgonetes, bicis_en_estacions, params)


def benefici_furgoneta(id_furgoneta: int, furgonetes_util: List[List[List]], bicis_en_estacions: List[List], params: ProblemParameters) -> float:
    """
    Aquesta funcio calcula per una furgoneta el benefici que ha obtingut
    """

    benefici = 0

    estacio_origen_furgo = furgonetes_util[id_furgoneta][0][0]

    #la diferencia es les bicis que hi haura menys la demanda
    diferencia = (bicis_en_estacions[estacio_origen_furgo][1] - bicis_en_estacions[estacio_origen_furgo][2]) 
    
    if diferencia <= 0: #si hem agafat bicicletes d'un lloc que no li sobraven bicis
        benefici -= furgonetes_util[id_furgoneta][0][1] #furgoneta[0][1] és el numero de bicis que recollim

    #la diferencia >0 pero (la diferencia - les bicis que recollim[les bicis que no es mouran] <0) -> hi ha perdues en cost
    elif furgonetes_util[id_furgoneta][0][1] > diferencia: 
        benefici += (diferencia - furgonetes_util[id_furgoneta][0][1]) 

    bicis_en_estacions[estacio_origen_furgo][0] -= furgonetes_util[id_furgoneta][0][1]
    bicis_en_estacions[estacio_origen_furgo][1] -= furgonetes_util[id_furgoneta][0][1]


    #Ara sumarem al benefici les bicis ben mogudes
    c1 = 0
    c2 = 0
    for parada in range(len(furgonetes_util[id_furgoneta][1])):
        bicis_deixades = furgonetes_util[id_furgoneta][1][parada][1] #les bicis que hem deixat en la estacio
        desti_estacio = furgonetes_util[id_furgoneta][1][parada][0] #el id de la estacio de desti
        diferencia = (bicis_en_estacions[desti_estacio][1] - bicis_en_estacions[desti_estacio][2])
        
        if parada==0:
            bicis_transportades = furgonetes_util[id_furgoneta][0][1] #número de bicis que transportem desde l'origen
            estacio_origen = furgonetes_util[id_furgoneta][0][0]
            c1=abs(cost_transport(bicis_transportades, estacio_origen, desti_estacio, params))
        else:
            estacio_primer_desti = furgonetes_util[id_furgoneta][1][parada-1][0]
            c2=abs(cost_transport(bicis_transportades-bicis_deixades,estacio_primer_desti, desti_estacio, params))
            
        if diferencia >= 0:
            pass
        elif bicis_deixades > abs(diferencia): #si hem deixat més bicis de la demanda, bicing no ens paga res
            pass
        else:            
            benefici += bicis_deixades

        bicis_en_estacions[desti_estacio][1] += bicis_deixades

    return benefici-(c1+c2)


def cost_transport(nb: int, estacio_origen: int, estacio_final: int, params: ProblemParameters):
    n_b = nb
    cost = ((n_b + 9) // 10)*distancia(params, estacio_origen, estacio_final)
    return cost


def distancia(params: ProblemParameters, id_parada_origen: int, id_parada_desti: int) -> float:
    """
    Calcula la distància entre dos estacions, i divideix el resultat entre 1000 per passar de metres a Km.
    """
    return round((abs(params.estaciones.lista_estaciones[id_parada_origen].coordX - params.estaciones.lista_estaciones[id_parada_desti].coordX) \
    + abs(params.estaciones.lista_estaciones[id_parada_origen].coordY - params.estaciones.lista_estaciones[id_parada_desti].coordY))/1000,2)



def estacions_origen_visitades(furgonetes: List[List[List]]) -> List:
        origens = []
        
        for furgoneta in furgonetes:
            if len(furgoneta[0]):
                origens.append(furgoneta[0][0])
            else: 
                origens.append(None)

        return origens
