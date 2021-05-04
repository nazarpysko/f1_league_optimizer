from bt_scheme import PartialSolutionWithOptimization, BacktrackingOptSolver, State, Solution
from typing import *


def f1league_points_solver(drivers, teams, budget):
    drivers_salaries, drivers_points = drivers
    team_salaries, team_points = teams
    print(drivers_salaries)

    class f1pointsPS(PartialSolutionWithOptimization):
        def __init__(self, decisions: Tuple[int], n: int, taken: int, current_spending: int, current_score: int,
                     team: int):
            self.decisions = decisions
            self.n = n
            self.taken = taken
            self.current_spending = current_spending
            self.current_score = current_score
            self.team = team

        def is_solution(self) -> bool:
            return self.current_spending <= budget and self.n == len(drivers_salaries) and self.taken == 5

        def get_solution(self) -> Solution:
            return self.decisions, -self.f(), self.current_spending, self.team

        def successors(self) -> Iterable["f1pointsPS"]:
            if self.team is None:
                for team in range(len(team_points)):
                    yield f1pointsPS(self.decisions, self.n, self.taken, self.current_spending + team_salaries[team],
                                     self.current_score + team_points[team], team)
            elif self.n < len(drivers_salaries):
                yield f1pointsPS(self.decisions + (-1,), self.n + 1, self.taken, self.current_spending,
                                 self.current_score, self.team)
                new_spending = self.current_spending + drivers_salaries[self.n]
                if new_spending <= budget:
                    yield f1pointsPS(self.decisions + (self.team,), self.n + 1, self.taken + 1, new_spending,
                                     self.current_score + drivers_points[self.n], self.team)

        def state(self) -> State:
            return self.n, self.current_score, self.current_spending

        def f(self) -> Union[int, float]:
            return -self.current_score

    initialPS = f1pointsPS((), 0, 0, 0, 0, None)
    return BacktrackingOptSolver.solve(initialPS)


def delta(a, b):
    return 1 if a == b else 0


def tester(team, sol):
    total_score = 0
    total_spending = 0
    total_score += team_points_portugal[team]
    total_spending += team_salaries_portugal[team]

    for indice, i in enumerate(sol):
        total_score += drivers_points_portugal[indice] * delta(i, team)
        total_spending += drivers_salaries_portugal[indice] * delta(i, team)

    return total_score, total_spending


if __name__ == '__main__':
    presupuesto = 100

    drivers_labels = ["Verstappen", "Hamilton", "Bottas", "Norris", "Perez", "Leclerc", "Ricciardo", "Alonso", "Sainz",
                      "Ocon", "Stroll", "Gasly", "Vettel", "Tsunoda", "Giovinazzi", "Raikkonen", "Russell",
                      "Schumacher", "Latifi", "Mazepin"]

    drivers_points_portugal = [167, 169, 165, 151, 147, 148, 129, 132, 124, 140, 100, 124, 110, 94, 119, 65, 99, 88, 77, 73]
    drivers_points_italia = [184, 171, 88, 170, 130, 158, 137, 122, 157, 128, 140, 147, 96, 119, 100, 107, 79, 95, 67, 88]
    drivers_salaries_portugal = [30.5, 30.5, 25.5, 25.4, 24.5, 23.3, 23.2, 20.2, 20.4, 15.2, 18.5, 16.5, 15.6, 13.9, 11.0, 13.5,
                        7.5, 6.9, 5.2, 4.6]


    teams_labels = ["Mercedes", "Red Bull", "McLaren", "Ferrari", "Alpine", "Aston Martin", "Alpha Tauri",
                    "Alpha Romeo", "Hash", "Williams"]
    team_points_portugal = [175, 167, 135, 139, 137, 105, 113, 95, 75, 89]
    team_points_italia = [137, 157, 155, 153, 124, 117, 123, 99, 83, 82]
    team_salaries_portugal = [27.0, 26.5, 25.1, 20.4, 17.9, 18.5, 14.6, 12.0, 7.0, 5.4]


    print("-----------------------------------------------")
    print("Calculando resultado Ideal conociendo el futuro")
    print("-----------------------------------------------")

    drivers_salaries = drivers_salaries_portugal
    drivers_points = drivers_points_portugal
    team_salaries = team_salaries_portugal
    team_points = team_points_portugal

    sols_optimo = []
    for sol in f1league_points_solver((drivers_salaries, drivers_points), (team_salaries, team_points), presupuesto):
        print(sol)
        sols_optimo.append(sol)
    print("\n<TERMINADO>")

    sols_predict = []
    print("\n\n")
    print("------------------------------------")
    print("Calculando resultado Ideal conociendo el pasado inmediato")
    print("------------------------------------")

    drivers_salaries = drivers_salaries_portugal
    drivers_points = drivers_points_italia
    team_salaries = team_salaries_portugal
    team_points = team_points_italia

    for sol in f1league_points_solver((drivers_salaries, drivers_points), (team_salaries, team_points), presupuesto):
        print(sol)
        sols_predict.append(sol)
    print("\n<TERMINADO>")


    print("\n\n")
    print("++++++++++")
    print("RESULTADOS")
    print("++++++++++")
    print("\n\n")


    # max de la app
    team_optimo = 4
    sol_optima = [-1, -1, -1, -1, 4, 4, -1, 4, -1, 4, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1]
    total_score, total_spending = tester(team_optimo, sol_optima)
    print("Resultados optimos de la app")
    print(f'{total_score}p {total_spending}$. Apostado en: {teams_labels[team_optimo]} {[drivers_labels[indice] for indice, i in enumerate(sol_optima) if i != -1]}')

    print("\nResultados optimos conociendo el futuro")
    sol_optima, total_score, total_spending, team_optimo = sols_optimo[-1]
    print(f'{total_score}p {total_spending}$. Apostado en: {teams_labels[team_optimo]} {[drivers_labels[indice] for indice, i in enumerate(sol_optima) if i != -1]}')

    print("\nResultados optimos conociendo el pasado inmediato")
    sol_optima, total_score, total_spending, team_optimo = sols_predict[-1]
    print(f'{total_score}p {total_spending}$. Apostado en: {teams_labels[team_optimo]} {[drivers_labels[indice] for indice, i in enumerate(sol_optima) if i != -1]}')