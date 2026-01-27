from common import Point, ALPHA, BETA
import random


class Ant:
    tour: list[int]
    tour_length: float
    visited_set: set[int]

    def __init__(self, points: list[Point]) -> None:
        self.tour: list[int] = []
        self.tour_length = 0.0
        self.visited_set = set()

    def select_next_city(
        self,
        current_city: int,
        pheromones: list[list[float]],
        distances: list[list[float]],
    ):
        probabilities = [
            # The probability to choose a single city is proportional to pheromone^ALPHA * (1/distance)^BETA.
            # No need to divide by the sum since random.choices normalizes the weights automatically.
            (
                0.0
                if city in self.visited_set
                else (pheromones[current_city][city]) ** ALPHA
                / (distances[current_city][city]) ** BETA
            )
            for city in range(len(distances))
        ]
        if sum(probabilities) == 0.0:
            # All remaining cities have zero probability
            # Choose randomly among unvisited cities.
            unvisited_cities = [
                city for city in range(len(distances)) if city not in self.visited_set
            ]
            return random.choice(unvisited_cities)
        next_city = random.choices(
            population=list(range(len(distances))),
            weights=probabilities,
            k=1,
        )[0]
        return next_city

    def do_tour(
        self, pheromones: list[list[float]], distances: list[list[float]]
    ) -> list[int]:
        starting_city = random.randint(0, len(distances) - 1)
        self.tour.append(starting_city)
        self.visited_set.add(starting_city)

        for _ in range(len(distances) - 1):
            current_city = self.tour[-1]
            next_city = self.select_next_city(current_city, pheromones, distances)
            self.tour.append(next_city)
            self.visited_set.add(next_city)

        # Add the return to starting city
        self.tour.append(starting_city)
        return self.tour
