# Test script

# Dependencies
import numpy as np
from HeatEq_1D import *

# Configuration variables
x_max = 100			# m
dx = 0.01			# m
t_max = 10000		# s
dt = 0.001			# s
a = 1.0				# m^2/s

# Set BCs
bc_0 = gen_bc_sin(t_max, dt, 2.0, 1.0, 0.0)
bc_max = gen_bc_sin(t_max, dt, 2.0, 1.0, 0.0)

# Set IC
ic = [0.0 for i in range(x_max)]

# Run the solver
result_array = heateq_1D([x_max,t_max], [dx,dt], [bc_0,bc_max], [], ic, a, True)