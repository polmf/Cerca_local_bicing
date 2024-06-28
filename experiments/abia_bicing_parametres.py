from typing import List
from abia_bicing import *




class ProblemParameters(object):
    capacitat_furgo = 30
   
    def __init__(self, estacions: Estaciones, furgonetes_max: int):
        self.estaciones = estacions
        self.furgonetes_max = furgonetes_max
       




    def __repr__(self):
        return f"Parametres(EStacions={self.estaciones}, Màxim de furgonetes={self.furgonetes_max})"



