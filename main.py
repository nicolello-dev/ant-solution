#!/usr/bin/env python3

from common import Point
from map import Map
from graph import Graph

DATA_FILE = "data/4.txt"


def load_data() -> list[Point]:
    with open(DATA_FILE, "r") as file:
        raw = file.read()
    x = ""
    y = ""
    res: list[Point] = list()
    for line in raw.splitlines():
        if line.startswith("x = ["):
            x = line[5:-2].strip()
        elif line.startswith("y = ["):
            y = line[5:-2].strip()
    x_values = [float(val) for val in x.split(" ")]
    y_values = [float(val) for val in y.split(" ")]
    for i in range(len(x_values)):
        res.append((x_values[i], y_values[i]))
    return res


map = Map(load_data())
graph = Graph(map)


def main():
    graph.render()


if __name__ == "__main__":
    main()
