# Test script for 1d heat eq csolver

# Dependencies
import numpy as np
from HeatEq_1D import *

# Configuration variables
x_max = 100			# m
dx = 0.01			# m
t_max = 10000		# s
dt = 0.001			# s
a = 0.01			# m^2/s

# Set BCs
bc_1_l = gen_bc_sin(t_max, dt, 2.0, 1.0, 0.0)
bc_1_r = gen_bc_sin(t_max, dt, 2.0, 1.0, 0.0)
bc_1 = [bc_1_l, []]
#bc_1 = [[],[]]

bc_2_l = gen_bc_zero(t_max)
bc_2_r = gen_bc_const(t_max, 1000.0)
bc_2 = [[], bc_2_r]
#bc_2 = [[],[]]

# Set IC
ic = [0.0 for i in range(x_max)]

# Run the solver
result_array = heateq_1D([x_max,t_max], [dx,dt], bc_1, bc_2, ic, a, True)