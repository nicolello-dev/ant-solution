#!/bin/env python3
import random

NUM_ANTS = 200


def choose_bridge(R_m: int, L_m: int):
    k = 20
    d = 2
    return (R_m + k) ** d / ((R_m + k) ** d + (L_m + k) ** d)


def main():
    R_m = 0
    L_m = 0

    for _ in range(NUM_ANTS):
        if random.random() <= choose_bridge(R_m, L_m):
            L_m += 1
        else:
            R_m += 1

    print(f"R_m: {R_m}, L_m: {L_m}")


if __name__ == "__main__":
    main()
