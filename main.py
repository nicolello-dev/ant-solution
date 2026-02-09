#!/bin/env python3
import random

NUM_ANTS = 200
k = 20
d = 2
R_m = 0
L_m = 0
len_right = 1
len_left = 1

for _ in range(NUM_ANTS):
    p_r = (R_m + k) ** d / ((R_m + k) ** d + (L_m + k) ** d)
    p_l = 1 - p_r
    p_r /= len_right
    p_l /= len_left
    p_r, p_l = p_r / (p_r + p_l), p_l / (p_r + p_l)
    if random.random() < p_r:
        R_m += 1
    else:
        L_m += 1

print(f"R_m: {R_m}, L_m: {L_m}")
