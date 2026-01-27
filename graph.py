import pygame
from map import Map
from common import MAX_FPS, Point, MAX_ITERATIONS

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Graph:
    def __init__(self, map: Map):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.map = map
        self.running = True

    def _map_points_to_screen(self, point: Point):
        min_x = min(p[0] for p in self.map.points)
        max_x = max(p[0] for p in self.map.points)
        min_y = min(p[1] for p in self.map.points)
        max_y = max(p[1] for p in self.map.points)
        x = int(
            (point[0] - min_x) / (max_x - min_x) * (self.screen.get_width() - 40) + 20
        )
        y = int(
            (point[1] - min_y) / (max_y - min_y) * (self.screen.get_height() - 40) + 20
        )
        return (x, y)

    def tick(self, iteration: int):
        self.screen.fill(WHITE)
        # Draw points
        if iteration < MAX_ITERATIONS:
            self.map.tick()

        # Draw pheromones
        # for i in range(len(self.map.points)):
        #     for j in range(i + 1, len(self.map.points)):
        #         pheromone_level = self.map.pheromones[i][j]
        #         if pheromone_level > 0.05:
        #             p1 = self.map.points[i]
        #             p2 = self.map.points[j]
        #             intensity = min(255, int(pheromone_level * 500))
        #             color = (intensity, intensity, intensity)
        #             pygame.draw.line(
        #                 self.screen,
        #                 color,
        #                 self._map_points_to_screen(p1),
        #                 self._map_points_to_screen(p2),
        #                 1,
        #             )

        # Draw best tour
        if self.map.best_tour is not None:
            for i in range(len(self.map.best_tour) - 1):
                p1 = self.map.points[self.map.best_tour[i]]
                p2 = self.map.points[self.map.best_tour[i + 1]]
                pygame.draw.line(
                    self.screen,
                    BLUE,
                    self._map_points_to_screen(p1),
                    self._map_points_to_screen(p2),
                    2,
                )

        for point in self.map.points:
            pygame.draw.circle(self.screen, RED, self._map_points_to_screen(point), 5)

        font = pygame.font.SysFont(None, 24)
        if self.map.best_tour is not None:
            length_text = font.render(
                f"Best tour length: {self.map.tour_length(self.map.best_tour):.2f}",
                True,
                GREEN,
            )
            self.screen.blit(length_text, (10, 10))

        pygame.display.flip()
        if MAX_FPS > 0:
            self.clock.tick(MAX_FPS)
        else:
            self.clock.tick()

    def render(self):
        iteration = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.tick(iteration)
            iteration += 1
