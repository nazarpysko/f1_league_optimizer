from bt_scheme import PartialSolutionWithOptimization, BacktrackingOptSolver, State, Solution
from typing import *

#presupuesto, puntos

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
            return self.decisions, self.current_spending, -self.f(), self.team

        def successors(self) -> Iterable["f1pointsPS"]:
            if self.team is None:
                # print(len(team_salaries))
                for team in range(len(team_points)):
                    print(team)
                    yield f1pointsPS(self.decisions, self.n, self.taken, self.current_spending + team_salaries[team],
                                     self.current_score + team_points[team], team)
            elif self.n < len(drivers_salaries):
                yield f1pointsPS(self.decisions + (-1,), self.n + 1, self.taken, self.current_spending,
                                 self.current_score, self.team)
                new_spending = self.current_spending + drivers_salaries[self.n]
                if new_spending <= budget:
                    if drivers_salaries[self.n] <= 18.0 and 69 not in self.decisions:
                        yield f1pointsPS(self.decisions + (69,), self.n + 1, self.taken + 1, new_spending,
                                     self.current_score + 2*drivers_points[self.n], self.team)
                    yield f1pointsPS(self.decisions + (self.team,), self.n + 1, self.taken + 1, new_spending,
                                     self.current_score + drivers_points[self.n], self.team)
        def state(self) -> State:
            return self.n, self.current_score, self.current_spending

        def f(self) -> Union[int, float]:
            return -self.current_score

    initialPS = f1pointsPS((), 0, 0, 0, 0, None)
    return BacktrackingOptSolver.solve(initialPS)


def delta(a, b):
    if a == 69:
        return 2
    elif a == b:
        return 1
    return 0


def predict(sol, team, carrera_actual):
    drivers_salaries, drivers_points, team_salaries, team_points = carrera_actual
    total_score = 0
    total_spending = 0
    total_score += team_points[team]
    total_spending += team_salaries[team]

    for indice, i in enumerate(sol):
        total_score += drivers_points[indice] * delta(i, team)
        total_spending += drivers_salaries[indice] * (1 if i == team or i == 69 else 0)

    return sol, total_spending, total_score, team


def calcula(drivers, teams, budget, etiqueta):
    print("-----------------------------------------------")
    print(f"Calculando resultado {etiqueta}")
    print("-----------------------------------------------")

    drivers_salaries, drivers_points = drivers
    team_salaries, team_points = teams
    sols = []

    for sol in f1league_points_solver((drivers_salaries, drivers_points), (team_salaries, team_points), budget):
        print(sol)
        sols.append(sol)
    print("\n<TERMINADO>")

    return sols[-1]


def print_resultado(sol, etiqueta):
    print(f"Resultados: {etiqueta}")
    drivers, total_spending, total_score, team = sol
    print(f'{total_score}p {total_spending}$. Participa: {teams_labels[team]}, {[drivers_labels[indice] for indice, i in enumerate(drivers) if i != -1]}')
    drivers, predict_spending, predict_score, team = predict(drivers, team, datos_carrera_actual)
    print(f'Predicción: {predict_score}p {predict_spending}$. Participa: {teams_labels[team]}, {[drivers_labels[indice] for indice, i in enumerate(drivers) if i != -1]}\n')


if __name__ == '__main__':
    presupuesto = 100

    drivers_labels = ["Verstappen", "Hamilton", "Bottas", "Norris", "Perez", "Leclerc", "Ricciardo", "Alonso", "Sainz",
                      "Ocon", "Stroll", "Gasly", "Vettel", "Tsunoda", "Giovinazzi", "Raikkonen", "Russell",
                      "Schumacher", "Latifi", "Mazepin"]

    drivers_points_average = [174.33, 168.33, 137.00, 161.67, 141.67, 151.00, 133.33, 114.33, 136.67, 126.00, 122.0, 125.67, 100.33, 119.67, 109.33, 97.00, 94.33, 94.00, 73.33, 72.00]
    drivers_points_rolling_average = [154, 165, 140, 140, 149, 147, 143, 114, 136, 123, 117, 122, 114, 119, 106, 109, 96, 94, 85, 72]
    drivers_points_italia = [184, 171, 88, 170, 130, 158, 137, 122, 157, 128, 140, 147, 96, 119, 100, 107, 79, 95, 67, 88]
    drivers_points_portugal = [169, 167, 165, 151, 147, 148, 129, 132, 124, 140, 100, 124, 110, 94, 119, 65, 99, 88, 77, 73]

    drivers_salaries_italia = [30.5, 30.5, 25.5, 25.4, 24.5, 23.3, 23.2, 20.2, 20.4, 15.2, 18.5, 16.5, 15.6, 13.9, 11.0, 13.5,
                        7.5, 6.9, 5.2, 4.6]
    drivers_salaries_portugal = [31.1, 30.7, 26.5, 26.0, 24.5, 24.0, 22.3, 20.4, 19.8, 17.1, 16.6, 16.4, 14.9, 12.3, 11.8, 11.5, 7.9, 6.7, 5.0, 4.1]


    teams_labels = ["Mercedes", "Red Bull", "McLaren", "Ferrari", "Alpine", "Aston Martin", "Alpha Tauri",
                    "Alpha Romeo", "Hash", "Williams"]

    team_points_average = [161.67, 161.33, 147.00, 146.00, 120.00, 110.00, 117.33, 102.67, 77.67, 86.33]
    team_points_rolling_average = [161, 151, 143, 130, 130, 121, 122, 100, 80, 88]
    team_points_portugal = [175, 167, 135, 139, 137, 105, 113, 95, 75, 89]
    team_points_italia = [137, 157, 155, 153, 124, 117, 123, 99, 83, 82]

    team_salaries_italia = [27.0, 26.5, 25.1, 20.4, 17.9, 18.5, 14.6, 12.0, 7.0, 5.4]
    team_salaries_portugal = [27.7, 26.6, 25.0, 20.0, 18.8, 17.2, 14.9, 11.6, 6.5, 5.9]

    drivers_salaries_actual = drivers_salaries_portugal
    team_salaries_actual = team_salaries_portugal
    datos_carrera_actual = (drivers_salaries_actual, drivers_points_portugal, team_salaries_actual, team_points_portugal)

    sol_average = calcula((drivers_salaries_actual, drivers_points_average), (team_salaries_actual, team_points_average), presupuesto, "Average")
    sol_rolling_average = calcula((drivers_salaries_actual, drivers_points_rolling_average), (team_salaries_actual, team_points_rolling_average), presupuesto, "Rolling Average")
    sol_carrera_pasada = calcula((drivers_salaries_actual, drivers_points_italia), (team_salaries_actual, team_points_italia), presupuesto, "Carrera pasada")
    # sol_maximo_app = predict((-1, -1, -1, -1, 4, 4, -1, 4, -1, 69, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1), 4, datos_carrera_actual)
    # sol_futuro_optimo = calcula((drivers_salaries_italia, drivers_points_portugal), (team_salaries_italia, team_points_portugal), 100, "Carrera conociendo el futuro")

    print("\n\n")
    print("++++++++++")
    print("RESULTADOS")
    print("++++++++++")
    print("\n\n")


    print_resultado(sol_average, "Average")
    print_resultado(sol_rolling_average, "Rolling Average")
    print_resultado(sol_carrera_pasada, "Carrera pasada")
    # print_resultado(sol_maximo_app, "Maxima App")
    # print_resultado(sol_futuro_optimo, "Futuro Optimo")
