# Test script for 2d heat eq solver

# Dependencies
import numpy as np
from HeatEq_2D import *

# Configuration variables
x_max = 50			# m
dx = 0.01			# m
y_max = 50			# m
dy = 0.01			# m
t_max = 25			# s
dt = 0.001			# s
a = 0.01			# m^2/s

# Set BCs
bc_1_x_l = [[0.0 for t in range(t_max)] for y in range(y_max)]
bc_1_x_r = [[np.sin((np.pi*t)/(t_max-1)) for t in range(t_max)] for y in range(y_max)]
bc_1_y_l = [[np.sin((np.pi*t)/(t_max-1)) * (x / (x_max-1)) for t in range(t_max)] for x in range(x_max)]
bc_1_y_r = [[np.sin((np.pi*t)/(t_max-1)) * (x / (x_max-1)) for t in range(t_max)] for x in range(x_max)]
bc_1 = [bc_1_x_l, bc_1_x_r, bc_1_y_l, bc_1_y_l]
#bc_1 = [[],[]]

bc_2 = [[], [], [], []]
#bc_2 = [[],[]]

# Set IC
ic = [[0.0 for x in range(x_max)] for y in range(y_max)]

# Run the solver
result_array = heateq_2D([x_max,y_max,t_max], [dx,dy,dt], bc_1, bc_2, ic, a, True)