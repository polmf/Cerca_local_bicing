from typing import Generator


from aima.search import Problem


from abia_bicing_operators import BicingOperator
from abia_bicing_estat import Estat




class BicingProblem(Problem):
    def __init__(self, initial_state: Estat):
        super().__init__(initial_state)


    def actions(self, state: Estat) -> Generator[BicingOperator, None, None]:
        return state.generate_actions()


    def result(self, state: Estat, action: BicingOperator) -> Estat:
        return state.aplicar_accions(action)


    def value(self, state: Estat) -> float:
        return state.heuristic()


    def goal_test(self, state: Estat) -> bool:
        return False

