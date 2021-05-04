from bt_scheme import PartialSolutionWithOptimization, BacktrackingOptSolver, State, Solution
from typing import *

class F1_Driver:
    def __init__(self, name, points, salary):
        self.name = name
        self.points = points
        self.salary = salary
        self.ratio = points/salary

    def set_points(self, points):
        self.points = points

    def set_salary(self, salary):
        self.salary = salary
        self.set_ratio()

    def set_ratio(self):
        self.ratio = self.points/self.salary

    def pretty_print(self):
        return self.name + ": " + str(self.points) + "p, " + str(self.salary) + "$, " + str(self.ratio) + "p/$"


def f1league_points_solver(salaries, points, budget):
    class f1pointsPS(PartialSolutionWithOptimization):
        def __init__(self, decisions: Tuple[int], n: int, taken: int, current_spending: int, current_score: int):
            self.decisions = decisions
            self.n = n
            self.taken = taken
            self.current_spending = current_spending
            self.current_score = current_score

        def is_solution(self) -> bool:
            return self.current_spending <= budget and self.n == len(salaries) and self.taken == 5

        def get_solution(self) -> Solution:
            return self.decisions, -self.f()

        def successors(self) -> Iterable["f1pointsPS"]:
            if self.n < len(salaries):
                yield f1pointsPS(self.decisions + (0,), self.n + 1, self.taken, self.current_spending, self.current_score)
                new_spending = self.current_spending + salaries[self.n]
                if new_spending <= budget:
                    yield f1pointsPS(self.decisions + (1,), self.n + 1, self.taken + 1, new_spending, self.current_score + points[self.n])

        def state(self) -> State:
            return self.n, self.current_score, self.current_spending

        def f(self) -> Union[int, float]:
            return -self.current_score

    initialPS = f1pointsPS((), 0, 0, 0, 0)
    return BacktrackingOptSolver.solve(initialPS)

if __name__ == '__main__':
    presupuesto = 80.0

    labels = ["Verstappen", "Hamilton", "Bottas", "Norris", "Perez", "Leclerc", "Ricciardo", "Alonso", "Sainz", "Ocon",
              "Stroll", "Gasly", "Vettel", "Tsunoda", "Giovinazzi", "Raikkonen", "Russell", "Schumacher", "Latifi",
              "Mazepin"]

    points = [154, 165, 140, 140, 149, 147, 143, 114, 136, 123, 117, 122, 114, 119, 106, 109, 96, 94, 85, 72]
    salaries = [31.1, 30.7, 26.5, 26.0, 24.5, 24.0, 22.3, 20.4, 19.8, 17.1, 16.6, 16.4, 14.9, 12.3, 11.8, 11.5, 7.9,
                6.7, 5.0, 4.1]

    # drivers = {}

    # for i in range(len(labels)):
    #     drivers[labels[i]] = F1_Driver(labels[i], points[i], salaries[i])

    for sol in f1league_points_solver(salaries, points, presupuesto):
        print(sol)
    print("\n<TERMINADO>")

    total = 0
    sol_optima = [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    for indice, i in enumerate(sol_optima):
        total += points[indice] * i

    print(total)


