from common import (
    MIN_PHEROMONE_LEVEL,
    Point,
    RHO,
)
from ant import Ant


def clamp(min_value: float, value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


class Map:
    points: list[Point]
    distances: list[list[float]]
    ants: list[Ant]
    best_tour: list[int] | None
    absolute_best_tour: float | None
    pheromones: list[list[float]]

    def __init__(self, points: list[Point]) -> None:
        self.points = points
        self.distances = self._compute_distances()
        initial_pheromone = self._calculate_initial_pheromone()
        self.pheromones = [
            [initial_pheromone for _ in range(len(points))] for _ in range(len(points))
        ]
        self.best_tour = None
        self.absolute_best_tour = None
        self.ants = []

    def _calculate_initial_pheromone(self) -> float:
        max_distance = 0.0
        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                p1 = self.points[i]
                p2 = self.points[j]
                dist = self._distance(p1, p2)
                if dist > max_distance:
                    max_distance = dist
        return 1.0 / max_distance

    def _distance(self, p1: Point, p2: Point) -> float:
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def _compute_distances(self) -> list[list[float]]:
        n = len(self.points)
        dist_matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    dist_matrix[i][j] = self._distance(self.points[i], self.points[j])
        return dist_matrix

    def tour_length(self, tour: list[int]) -> float:
        length = 0.0
        for i in range(len(tour) - 1):
            length += self.distances[tour[i]][tour[i + 1]]
        return length

    def tick(self) -> None:
        self.ants = [Ant(self.points) for _ in range(len(self.points))]

        max_tour_length = float("inf")
        best_tour = None
        for ant in self.ants:
            ant.do_tour(self.pheromones, self.distances)
            ant.tour_length = self.tour_length(ant.tour)
            if ant.tour_length < max_tour_length:
                max_tour_length = ant.tour_length
                best_tour = ant.tour

        print(
            f"Best tour length (this iteration): {self.absolute_best_tour if self.absolute_best_tour is not None else float('inf'):.2f} ({max_tour_length:.2f})"
        )
        print(f"Best tour this iteration: {best_tour}")

        if self.best_tour is None or max_tour_length < self.tour_length(self.best_tour):
            self.best_tour = best_tour
            self.absolute_best_tour = max_tour_length
        # Update pheromones
        for i in range(len(self.points)):
            for j in range(len(self.points)):
                self.pheromones[i][j] *= 1 - RHO  # Evaporation
                self.pheromones[i][j] += sum(
                    (1.0 / ant.tour_length)
                    for ant in self.ants
                    if (
                        ant.tour[ant.tour.index(i) + 1] == j
                        or ant.tour[ant.tour.index(j) + 1] == i
                    )
                )
                # To avoid getting stuck on a local minima, clamp pheromone levels
                self.pheromones[i][j] = max(MIN_PHEROMONE_LEVEL, self.pheromones[i][j])
                self.pheromones[j][i] = self.pheromones[i][j]  # Symmetric matrix
